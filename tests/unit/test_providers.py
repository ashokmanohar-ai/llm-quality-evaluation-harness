from llm_quality_harness.models import EvaluationCase
from llm_quality_harness.providers import CallableProvider, DatasetReplayProvider


def test_provider_contracts() -> None:
    case = EvaluationCase(id="one", prompt="p", response="r", reference_answer="r")
    assert DatasetReplayProvider().respond(case) == "r"
    assert CallableProvider("upper", lambda item: item.response.upper()).respond(case) == "R"

