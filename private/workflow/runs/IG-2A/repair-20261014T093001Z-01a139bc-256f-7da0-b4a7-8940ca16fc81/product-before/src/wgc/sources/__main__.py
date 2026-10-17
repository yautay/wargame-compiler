"""Local CLI; publisher inputs and all derived outputs must remain private."""
import argparse
import json
from pathlib import Path
import sys
from wgc.contracts.source import canonical_bytes, load_json
from .inventory import safe_artifact, seal, validate
from .pdf import structural_inventory, extract_evidence


def private_path(value):
    if not value.startswith('private/'):
        raise argparse.ArgumentTypeError('Publisher input/output path must be under private/')
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    sub=parser.add_subparsers(dest='operation',required=True)
    inventory=sub.add_parser('inventory'); inventory.add_argument('--pdf',type=private_path,required=True)
    inventory.add_argument('--provenance',type=private_path,required=True); inventory.add_argument('--sha256',required=True)
    inventory.add_argument('--source-id',required=True); inventory.add_argument('--registry',type=private_path)
    inventory.add_argument('--output',type=private_path,required=True)
    evidence=sub.add_parser('evidence'); evidence.add_argument('--inventory',type=private_path,required=True)
    evidence.add_argument('--pages',type=int,nargs='+',required=True); evidence.add_argument('--output',type=private_path,required=True)
    evidence.add_argument('--dpi',type=int,default=144)
    check=sub.add_parser('validate'); check.add_argument('inventory',type=private_path)
    args=parser.parse_args(); root=args.root.resolve()
    try:
        if args.operation=='validate':
            print(json.dumps(validate(load_json(safe_artifact(root,args.inventory)),root),indent=2)); return 0
        if args.operation=='inventory':
            registry=load_json(safe_artifact(root,args.registry)) if args.registry else None
            doc=structural_inventory(root,args.pdf,args.provenance,args.source_id,args.sha256,registry)
        else:
            doc=load_json(safe_artifact(root,args.inventory)); validate(doc,root)
            if len(args.pages)!=len(set(args.pages)) or any(p not in range(1,doc['source']['page_count']+1) for p in args.pages):
                raise ValueError('invalid or duplicate verification page')
        out=safe_artifact(root,args.output)
        if out.exists(): raise ValueError('output must be new; immutable artifacts are never overwritten')
        out.mkdir(parents=True,exist_ok=False)
        if args.operation=='evidence':
            for number in args.pages:
                page=next(p for p in doc['pages'] if p['pdf_page']==number)
                regions=[r for r in doc['regions'] if r['page_id']==page['id']]
                for index,region in enumerate(regions):
                    doc['evidence'].append(extract_evidence(doc,region['id'],root,f'{args.output}/page-{number:03d}-region-{index:03d}',dpi=args.dpi))
                    doc=seal(doc)
            doc=seal(doc)
        report=validate(doc,root)
        (out/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n')
        (out/'identity-registry.json').write_bytes(canonical_bytes(doc['registry'])+b'\n')
        (out/'coverage.json').write_bytes(canonical_bytes(report)+b'\n')
        print(str(out)); return 0
    except (ValueError,OSError) as error:
        print(str(error),file=sys.stderr); return 1


if __name__=='__main__': raise SystemExit(main())
