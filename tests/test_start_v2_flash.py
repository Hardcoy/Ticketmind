"""The launch profile must not mutate .env, environment variables or launch services in tests."""
from pathlib import Path

from scripts import start_v2_flash
from ticketmind.knowledge.sources import load_sources


def test_profile_matches_final_evaluation_and_preserves_credentials():
    original = {
        "TICKETMIND_KNOWLEDGE_DATASET": "production-v1",
        "TICKETMIND_DECISION_MODEL": "qwen3.8-max-0902",
        "TICKETMIND_RETRIEVAL_MODE": "hybrid",
        "TICKETMIND_JUDGE_MODEL": "another-local-judge",
        "DASHSCOPE_API_KEY": "local-secret-for-test",
        "TICKETMIND_DATABASE_URL": "postgresql+psycopg://local-only",
    }
    actual = start_v2_flash.profile_environment(original)
    assert {key: actual[key] for key in start_v2_flash.PROFILE} == start_v2_flash.PROFILE
    assert actual["TICKETMIND_JUDGE_MODEL"] == "deepseek-v4.1-flash"
    assert actual["TICKETMIND_RETRIEVAL_MODE"] == "hybrid"
    assert actual["TICKETMIND_RETRIEVAL_TOP_K"] == "5"
    assert actual["TICKETMIND_DOCS_DATASET"] == "synthetic-phase7-docs-v1"
    assert actual["TICKETMIND_CORPUS_PATH"].endswith("historical_cases.jsonl")
    assert actual["DASHSCOPE_API_KEY"] == original["DASHSCOPE_API_KEY"]
    assert actual["TICKETMIND_DATABASE_URL"] == original["TICKETMIND_DATABASE_URL"]
    assert original["TICKETMIND_KNOWLEDGE_DATASET"] == "production-v1"
    assert original["TICKETMIND_JUDGE_MODEL"] == "another-local-judge"


def test_profile_dataset_matches_current_frozen_case_content():
    corpus = load_sources(Path(start_v2_flash.PROFILE["TICKETMIND_CORPUS_PATH"]))
    assert len(corpus.cases) == 120
    assert corpus.version == start_v2_flash.PROFILE["TICKETMIND_KNOWLEDGE_DATASET"]


def test_launcher_forwards_existing_startup_flags_without_starting_services(monkeypatch):
    recorded = {}
    monkeypatch.setattr(
        start_v2_flash.subprocess,
        "call",
        lambda command, *, cwd, env: recorded.update(command=command, cwd=cwd, env=env) or 0,
    )
    assert start_v2_flash.main(["--skip-infra", "--check"]) == 0
    assert recorded["command"][-2:] == ["--skip-infra", "--check"]
    assert recorded["command"][1] == str(start_v2_flash.ROOT / "scripts" / "start_local.py")
    assert recorded["cwd"] == start_v2_flash.ROOT
    assert all(recorded["env"][key] == value for key, value in start_v2_flash.PROFILE.items())
