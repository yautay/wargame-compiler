"""GLU: execution and orchestration layer (jobs, routing, providers, cache, incremental builds).

GLU is domain-agnostic: it executes task specs registered by WGC and never owns domain knowledge.
Accepted results reach the Knowledge Base only through WGC validators.
"""
__version__ = "0.0.1"
