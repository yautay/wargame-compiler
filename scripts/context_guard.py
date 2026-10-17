"""Latch a refused helper request and hold it until the owning supervisor stops the session."""
from __future__ import annotations

from functools import wraps
import json
import os
from pathlib import Path
import sys
import subprocess
import time
import uuid

import workflow as w

DENIAL_SIGNAL = 'WGC_CONTEXT_DENIED: '


def json_text(value):
    """Lossless ASCII JSON for Windows pipes, independent of the console code page."""
    return json.dumps(value, ensure_ascii=True)


def configuration(root):
    rel = os.environ.get('WGC_CONTEXT_GUARD')
    if not rel:
        return None
    p = w.safe_path(root, rel)
    if w.digest(p) != os.environ.get('WGC_CONTEXT_GUARD_SHA256'):
        raise ValueError('Session context guard configuration changed')
    cfg = w.read_json(p)
    marker = w.safe_path(root, cfg['denial'])
    if (cfg.get('format') != 'wgc-context-guard-1' or cfg.get('task') != os.environ.get('WGC_TASK_ID') or
            marker.parent != p.parent or marker.name != 'context-denied.json'):
        raise ValueError('Invalid session context guard binding')
    return cfg, marker


def deny(root, helper, reason):
    rel = os.environ.get('WGC_CONTEXT_GUARD')
    if not rel:
        return
    # Derive only the stop-signal location from the binding, even if its JSON or
    # digest is invalid. This never authorizes a data read. Publication failures
    # must not turn a refusal into a completed helper call.
    try:
        path = w.safe_path(root, rel)
        if path.name != 'context-guard.json':
            raise ValueError('Invalid guard filename')
        marker = path.with_name('context-denied.json')
        if not marker.exists():
            payload = json.dumps({'format': 'wgc-context-denial-1',
                'task': os.environ.get('WGC_TASK_ID'), 'helper': helper,
                'reason': str(reason)[:500], 'pid': os.getpid()}).encode('utf-8')
            temp = marker.with_name(marker.name + '.' + uuid.uuid4().hex + '.pending')
            try:
                with temp.open('xb') as stream:
                    stream.write(payload)
                os.replace(temp, marker)
            except OSError:
                # A failed atomic rename/open still has a bounded best-effort
                # stop signal; the supervisor only needs marker existence.
                fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                try:
                    os.write(fd, payload)
                finally:
                    os.close(fd)
    except Exception:
        pass
    try:
        print(DENIAL_SIGNAL + 'Session latched; no direct-read or command fallback is permitted.',
              file=sys.stderr, flush=True)
    except Exception:
        pass
    # Even if all notification writes fail, hold until termination/deadline.
    # The serial context protocol cannot receive a completed refused request.
    while True:
        time.sleep(0.05)


def protect(helper):
    def decorate(fn):
        @wraps(fn)
        def wrapped(root, *args, **kwargs):
            try:
                active = configuration(root)
                if active and active[1].exists():
                    deny(root, helper, 'Session was already denied')
                return fn(root, *args, **kwargs)
            except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
                deny(root, helper, exc)
                raise
        return wrapped
    return decorate


def cli(root, helper, main):
    try:
        return main()
    except SystemExit as exc:
        if exc.code:
            deny(root, helper, 'Helper argument request was refused')
        raise
    except (OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.SubprocessError) as exc:
        deny(root, helper, exc)
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2) from exc
