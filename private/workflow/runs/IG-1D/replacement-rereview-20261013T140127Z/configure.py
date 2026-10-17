from datetime import datetime, timezone
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
confirmed = {'model': 'gpt-6.1-sol', 'reasoning': 'high',
    'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high',
    'configuration_evidence': {'source': 'Direct operator confirmation in this replacement reviewer chat in reply to an explicit request to inspect settings of this new chat.',
        'question': 'Nie mam narzędzia ujawniającego rzeczywisty model i poziom reasoning tej sesji. Proszę sprawdzić ustawienia właśnie tego nowego czatu i potwierdzić, czy są GPT-6.1 Sol / high; jeśli inne, podać rzeczywiste wartości. Do tego czasu zapisuję je jako null i kontynuuję inspekcję.',
        'verbatim_response': 'potwierdzam', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'exact_confirmation_timestamp': None, 'independent_of_previous_reviewer_and_executor': True},
    'tokens': None, 'cost': None, 'operator_seconds': None}
with (RUN / 'configuration-confirmed.json').open('x', encoding='utf-8') as f:
    json.dump(confirmed, f, ensure_ascii=False, indent=2); f.write('\n')
with (RUN / 'measurement-correction.json').open('x', encoding='utf-8') as f:
    json.dump({'note': 'The reconstructed first-tool time in checkpoint.json is an estimate and must not be used as an actual measured UTC start. Exact evidence-run start comes from checkpoint.evidence_run_started_utc; the unmeasured earlier reading phase is excluded from measured wall time.',
        'first_tool_started_utc': None, 'elapsed_reading_before_evidence_run_seconds': None}, f, indent=2); f.write('\n')
print('Fresh replacement reviewer configuration confirmed; measurement scope corrected explicitly.')
