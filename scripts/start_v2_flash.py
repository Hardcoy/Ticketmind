"""Launch the Phase 7 profile used by the final 2026-10-08 evaluation.

This is a runtime-only profile: do not edit .env or change the caller's environment.
The historical filename is retained for existing launch commands. Credentials,
database, Milvus address and ports continue to come from the existing .env.
"""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

PROFILE = {
    "TICKETMIND_KNOWLEDGE_DATASET": "synthetic-v2-9c0552c76c338a73e05990c3c0d7a588149d7b8471a3b0c9a8a648b8d06b488a",
    "TICKETMIND_CORPUS_PATH": str(ROOT / "data/synthetic/phase7_v1/historical_cases.jsonl"),
    "TICKETMIND_DECISION_MODEL": "qwen3.8-flash",
    "TICKETMIND_JUDGE_MODEL": "deepseek-v4.1-flash",
    "TICKETMIND_EMBEDDING_MODEL": "text-embedding-v4",
    "TICKETMIND_RETRIEVAL_MODE": "hybrid",
    "TICKETMIND_RETRIEVAL_TOP_K": "5",
    "TICKETMIND_RETRIEVAL_CANDIDATE_K": "20",
    "TICKETMIND_RETRIEVAL_RRF_K": "60",
    "TICKETMIND_DOCS_DATASET": "synthetic-phase7-docs-v1",
    "TICKETMIND_DOCS_RETRIEVAL_MODE": "bm25",
    "TICKETMIND_AGENT_VERSION": "ticketmind-tools-docs-v2",
    "TICKETMIND_MAX_SEARCH_ROUNDS": "2",
    "TICKETMIND_MAX_DOCS_SEARCH_ROUNDS": "2",
    "TICKETMIND_MAX_AGENT_STEPS": "8",
    "TICKETMIND_MAX_CLARIFICATION_ROUNDS": "2",
    "TICKETMIND_PROCESSING_TIMEOUT_SECONDS": "90",
    "LANGSMITH_TRACING": "false",
}


def profile_environment(base: dict[str, str] | None = None) -> dict[str, str]:
    """Overlay evaluation choices without changing secrets or the input mapping."""
    environment = dict(os.environ if base is None else base)
    environment.update(PROFILE)
    return environment


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    print("TicketMind profile: phase7 (120 Cases / 8 Docs) / qwen3.8-flash / Cases hybrid top-5 / Docs bm25", flush=True)
    return subprocess.call(
        [sys.executable, str(ROOT / "scripts" / "start_local.py"), *args],
        cwd=ROOT,
        env=profile_environment(),
    )


if __name__ == "__main__":
    raise SystemExit(main())
