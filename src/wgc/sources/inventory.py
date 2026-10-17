"""Persisted page/region identities, exact revisions and coverage accounting."""
from __future__ import annotations
import copy
import hashlib
import uuid
from pathlib import Path
from wgc.contracts.source import canonical_bytes, load_json, _check_schema, _shape
from .geometry import SCALE, check_box, effective_crop, overlaps, area

SCHEMA = Path(__file__).resolve().parents[3] / 'contracts/ig/regions.schema.json'
LEVELS = ('transcription', 'descriptive_semantics', 'formal_semantics')
STATUSES = ('represented', 'partial', 'unprocessed', 'excluded')


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def seal(record):
    record = copy.deepcopy(record)
    record['revision'] = digest({k:v for k,v in record.items() if k != 'revision'})
    return record


def check_revision(record):
    if record['revision'] != seal(record)['revision']:
        raise ValueError('revision hash mismatch')


def new_registry(source_id, source_revision):
    return {'format':'wgc-source-identities-1', 'source_id':source_id,
            'source_revision':source_revision, 'entries':[]}


def validate_registry(registry):
    if set(registry) != {'format','source_id','source_revision','entries'} or registry['format'] != 'wgc-source-identities-1':
        raise ValueError('invalid persisted registry')
    keys, ids = set(), set()
    for entry in registry['entries']:
        if set(entry) != {'kind','key','id'} or entry['kind'] not in ('page','region') or not isinstance(entry['key'],str) or not entry['key']:
            raise ValueError('invalid registry entry')
        key = (entry['kind'],entry['key'])
        if key in keys or entry['id'] in ids:
            raise ValueError('duplicate registry identity/key')
        if not entry['id'].startswith(entry['kind']+':'):
            raise ValueError('identity kind mismatch')
        try: uuid.UUID(entry['id'].split(':',1)[1])
        except (ValueError, AttributeError): raise ValueError('invalid registry UUID') from None
        keys.add(key); ids.add(entry['id'])


def assign(registry, kind, key):
    validate_registry(registry)
    if kind not in ('page','region') or not isinstance(key,str) or not key:
        raise ValueError('explicit nonempty identity key required')
    for entry in registry['entries']:
        if entry['kind'] == kind and entry['key'] == key: return entry['id']
    identity = kind+':'+str(uuid.uuid4())
    registry['entries'].append({'kind':kind,'key':key,'id':identity})
    registry['entries'].sort(key=lambda e:(e['kind'],e['key']))
    return identity


def make_region(registry, key, page, box, *, kind='unclassified', role='inventory', reason='Not yet inventoried'):
    check_box(box)
    return seal({'id':assign(registry,'region',key), 'key':key, 'page_id':page['id'],
                 'source_revision':registry['source_revision'], 'box':list(box),
                 'kind':kind, 'denominator_role':role, 'uncertainty':[reason] if reason else [],
                 'coverage':{level:{'status':'unprocessed','reason':reason,'gap':True,'boundary':None}
                             for level in LEVELS}})


def assemble(source, pages, regions, registry, *, reading_order=None, links=None, evidence=None, toolchain=None):
    result = seal({'format':'wgc-inventory-1','source':source,'pages':pages,'regions':regions,
                   'registry':copy.deepcopy(registry),
                   'reading_order':reading_order if reading_order is not None else [r['id'] for r in regions],
                   'links':links or [],'evidence':evidence or [],'toolchain':toolchain or []})
    validate(result)
    return result


def safe_artifact(root, relative):
    """Repo-relative POSIX paths; reject links and Win32 aliases before access."""
    if (not isinstance(relative,str) or not relative or '\\' in relative or ':' in relative
            or relative.startswith('/') or any(p in ('','.','..') or p.endswith((' ','.'))
            or p.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}
            for p in relative.split('/'))):
        raise ValueError('unsafe artifact path')
    root = Path(root).resolve(); path = root/relative
    current = path
    while current != root:
        if current.is_symlink() or (hasattr(current,'is_junction') and current.is_junction()):
            raise ValueError('linked artifact path')
        current = current.parent
    if not path.resolve().is_relative_to(root): raise ValueError('artifact escapes root')
    return path


def file_pin(root, relative):
    path = safe_artifact(root,relative)
    raw = path.read_bytes()
    return {'path':relative,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def page_basis(page):
    """Physical address and coordinate basis, independent of labels/evidence."""
    return {k:page[k] for k in ('id','key','source_revision','pdf_page','media_box',
                               'crop_box','effective_crop_box','rotation','user_unit')}


def page_basis_hash(page):
    return digest(page_basis(page))


def partition_hash(document):
    """Exact author scope before coverage decisions, avoiding circular hashes.

    This sidecar basis is not the frozen IG-1A whole-record review basis. That
    separate reconciliation and human decision must still be established.
    """
    return digest({'source':document['source'], 'registry':document['registry'],
                   'pages':sorted([page_basis(p) for p in document['pages']],key=lambda p:p['id']),
                   'regions':sorted([{k:v for k,v in r.items() if k not in ('coverage','revision')}
                                     for r in document['regions']],key=lambda r:r['id']),
                   'reading_order':document['reading_order'], 'links':document['links']})


def validate(document, root=None):
    canonical_bytes(document)
    schema = load_json(SCHEMA); _check_schema(schema,schema)
    errors = _shape(document,schema,schema,'$')
    if errors: raise ValueError('inventory schema: '+'; '.join(errors[:8]))
    check_revision(document); validate_registry(document['registry'])
    source = document['source']; registry = document['registry']
    if (source['id'],source['sha256']) != (registry['source_id'],registry['source_revision']):
        raise ValueError('registry/source revision mismatch; explicit revision mapping required')
    for pin in (source['pdf'],source['provenance']):
        safe_artifact(root or Path.cwd(),pin['path'])
        if root is not None and file_pin(root,pin['path']) != pin:
            raise ValueError('source/provenance artifact hash mismatch')
    if source['pdf']['sha256'] != source['sha256']:
        raise ValueError('source SHA differs from PDF pin')
    if len(source['independent_counts']) < 2 or len({c['tool'] for c in source['independent_counts']}) < 2 or any(c['count'] != source['page_count'] for c in source['independent_counts']):
        raise ValueError('independent PDF page count disagreement')
    actual_geometry = None
    if root is not None:
        from .pdf import source_structure
        actual_geometry, _ = source_structure(safe_artifact(root,source['pdf']['path']))
        if len(actual_geometry) != source['page_count']:
            raise ValueError('missing PDF page/source structure count mismatch')
    entries = {(e['kind'],e['key']):e['id'] for e in registry['entries']}
    pages = {}; nums = set()
    for page in document['pages']:
        check_revision(page)
        if page['id'] in pages or page['pdf_page'] in nums: raise ValueError('duplicate page')
        if page['id'] != entries.get(('page',page['key'])) or page['source_revision'] != source['sha256']:
            raise ValueError('page registry/source mismatch')
        if page['key'] != f'physical-page:{page["pdf_page"]}':
            raise ValueError('physical page identity remapping is forbidden')
        for box in [page['media_box'],page['crop_box']]:
            if len(box)!=4 or box[0]>=box[2] or box[1]>=box[3]: raise ValueError('invalid PDF page box')
        if effective_crop(page['media_box'],page['crop_box']) != page['effective_crop_box']:
            raise ValueError('effective CropBox/MediaBox mismatch')
        if actual_geometry is not None:
            actual = actual_geometry.get(page['pdf_page'])
            if actual is None or any(page[k] != v for k,v in actual.items()):
                raise ValueError('stale page geometry/source structure basis')
        if page['label']['status'] == 'unknown' and (page['label']['value'] is not None or not page['label']['reason']):
            raise ValueError('unknown printed label requires null and reason')
        if page['label']['status'] != 'unknown' and not page['label']['value']:
            raise ValueError('known label needs a value')
        if page['label']['status'] == 'verified' and page['label']['evidence'] is None:
            raise ValueError('verified printed label needs exact evidence pin')
        pages[page['id']] = page; nums.add(page['pdf_page'])
    if nums != set(range(1,source['page_count']+1)): raise ValueError('missing PDF page accounting')
    regions = {}; keys = set(); partition = {}
    for region in document['regions']:
        check_revision(region); check_box(region['box'])
        if region['id'] in regions or region['key'] in keys: raise ValueError('duplicate region identity/key')
        if region['page_id'] not in pages or region['source_revision'] != source['sha256'] or entries.get(('region',region['key'])) != region['id']:
            raise ValueError('region registry/page/source mismatch')
        if region['denominator_role'] == 'inventory':
            for previous in partition.get(region['page_id'],[]):
                if overlaps(previous,region['box']): raise ValueError('overlapping inventory denominator')
            partition.setdefault(region['page_id'],[]).append(region['box'])
        for level, cov in region['coverage'].items():
            if cov['status'] == 'represented' and (cov['gap'] or cov['reason']):
                raise ValueError('represented region cannot have a gap/reason')
            if cov['status'] != 'represented' and not cov['reason']:
                raise ValueError('partial/unprocessed/excluded needs a reason')
            if cov['status'] in ('partial','unprocessed') and not cov['gap']:
                raise ValueError('partial/unprocessed must retain a gap')
            boundary = cov['boundary']
            if cov['status'] == 'excluded':
                if boundary is None or boundary['source_revision'] != source['sha256'] or boundary['region_id'] != region['id'] or boundary['box'] != region['box'] or boundary['level'] != level or boundary['partition_hash'] != partition_hash(document):
                    raise ValueError('exclusion boundary is not exact/current')
                if root is not None and file_pin(root,boundary['decision']['path']) != boundary['decision']:
                    raise ValueError('exclusion decision artifact mismatch')
            elif boundary is not None: raise ValueError('boundary only permitted for excluded coverage')
        regions[region['id']] = region; keys.add(region['key'])
    order = document['reading_order']
    if len(order)!=len(set(order)) or set(order)!=set(regions): raise ValueError('reading order must name each region exactly once')
    links = set()
    for link in document['links']:
        key = (link['kind'],link['from'],link['to'])
        if key in links or link['from'] not in regions or link['to'] not in regions or link['from']==link['to']:
            raise ValueError('duplicate/dangling/self region link')
        links.add(key)
    evidence_ids = {}
    for ev in document['evidence']:
        region = regions.get(ev['region_id'])
        if ev['id'] in evidence_ids or region is None or ev['region_revision'] != region['revision'] or ev['box'] != region['box'] or ev['source_sha256'] != source['sha256']:
            raise ValueError('duplicate/stale evidence locator')
        if ev['page_id']!=region['page_id'] or ev['pdf_page']!=pages[region['page_id']]['pdf_page']:
            raise ValueError('evidence page locator mismatch')
        page = pages[region['page_id']]
        if ev['page_basis_hash'] != page_basis_hash(page):
            raise ValueError('stale evidence page geometry/physical address basis')
        from .geometry import render_size_pixels
        if (ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels']) != render_size_pixels(region['box'],page,ev['render_parameters']['dpi']):
            raise ValueError('render DPI/geometry pixel dimensions mismatch')
        for name in ('text','image','crop_pdf'):
            artifact = ev[name]; safe_artifact(root or Path.cwd(),artifact['path'])
            if root is not None and file_pin(root,artifact['path']) != artifact:
                raise ValueError('evidence artifact hash mismatch')
        if ev['text_offsets']['start']!=0 or ev['text_offsets']['end']!=ev['text_codepoints']:
            raise ValueError('text locator requires half-open Unicode codepoint offsets')
        if root is not None:
            text=safe_artifact(root,ev['text']['path']).read_text(encoding='utf-8')
            if len(text)!=ev['text_codepoints']: raise ValueError('text offset/length mismatch')
            from PIL import Image
            with Image.open(safe_artifact(root,ev['image']['path'])) as image:
                if image.size != (ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels']):
                    raise ValueError('render pixel dimensions mismatch')
        evidence_ids[ev['id']] = ev
    for page in pages.values():
        if page['label']['status']=='verified' and page['label']['evidence'] not in evidence_ids:
            raise ValueError('printed label evidence missing')
        if page['label']['status']=='verified':
            ev = evidence_ids[page['label']['evidence']]
            if ev['page_id'] != page['id'] or ev['pdf_page'] != page['pdf_page']:
                raise ValueError('printed label evidence belongs to another physical page')
    if root is not None and file_pin(root,source['pdf']['path']) != source['pdf']:
        raise ValueError('PDF changed during validation')
    report = coverage(document)
    report['source_structure_verification'] = 'verified' if root is not None else 'unverified'
    return report


def coverage(document):
    """Structural region counts and explicit geometric gaps, never semantic proof."""
    inventory = [r for r in document['regions'] if r['denominator_role']=='inventory']
    levels = {level:{status:0 for status in STATUSES} for level in LEVELS}
    for region in inventory:
        for level in LEVELS: levels[level][region['coverage'][level]['status']] += 1
    pages=[]
    for page in document['pages']:
        assigned=sum(area(r['box']) for r in inventory if r['page_id']==page['id'])
        pages.append({'page_id':page['id'],'pdf_page':page['pdf_page'],
                      'inventory_regions':sum(r['page_id']==page['id'] for r in inventory),
                      'unaccounted_area_trillionths':SCALE*SCALE-assigned,
                      'gap_reason':'No inventory region accounts for this page area' if assigned<SCALE*SCALE else None})
    return {'denominator_regions':len(inventory),'context_regions':len(document['regions'])-len(inventory),
            'levels':levels,'pages':pages,'semantic_acceptance_granted':False,'executable_readiness':'unverified',
            'exclusion_claims':[{'region_id':r['id'],'level':level,
                                 'author_scope_freshness':'current' if cov['boundary'] is not None and cov['boundary']['partition_hash']==partition_hash(document) else 'stale',
                                 'source_ig_review_freshness':'unknown','human_authority':'unverified'}
                                for r in inventory for level,cov in r['coverage'].items() if cov['status']=='excluded'],
            'note':'Region counts and geometric accounting do not establish substantive source completeness.'}
