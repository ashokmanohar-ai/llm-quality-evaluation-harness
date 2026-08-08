from llm_quality_harness.schema import required_fields_present


def test_required_fields() -> None:
    assert required_fields_present('{"decision":"pass"}', ["decision"])
    assert not required_fields_present("not-json", ["decision"])
    assert not required_fields_present("[]", ["decision"])
    assert required_fields_present("anything", [])

