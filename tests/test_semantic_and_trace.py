from llm_quality_harness.deepeval_adapter import DeepEvalAdapter
from llm_quality_harness.langgraph_trace import evaluate_agent_trace
from llm_quality_harness.rag_semantic import SemanticRAGEvaluator


def test_semantic_rag_scores_and_weighted_result() -> None:
    evaluator = SemanticRAGEvaluator(
        lambda _: {
            'faithfulness': 0.96,
            'context_precision': 0.93,
            'context_recall': 0.91,
            'answer_relevance': 0.97,
        }
    )
    result = evaluator.evaluate({'id': 'rag-001'})
    assert result.faithfulness == 0.96
    assert result.weighted_score == 0.945


def test_deepeval_adapter_scores_semantic_quality() -> None:
    adapter = DeepEvalAdapter(
        lambda _: {
            'groundedness': 0.95,
            'hallucination_resistance': 0.98,
            'task_completion': 0.97,
            'policy_adherence': 1.0,
        }
    )
    result = adapter.evaluate({'id': 'llm-001'})
    assert result.groundedness == 0.95
    assert result.weighted_score == 0.9705


def test_agent_trace_normalization_and_evaluation() -> None:
    events = [
        {'node': 'planner', 'success': True, 'latency_ms': 20},
        {
            'node': 'retriever',
            'tool': 'policy_search',
            'expected_tool': 'policy_search',
            'success': True,
            'latency_ms': 35,
        },
        {'node': 'reviewer', 'success': True, 'latency_ms': 10},
    ]
    result = evaluate_agent_trace(
        'trace-001', events, task_completed=True, max_expected_steps=3
    )
    assert result.step_count == 3
    assert result.tool_calls == 1
    assert result.score.task_completion == 1.0
    assert result.score.tool_selection == 1.0
    assert result.score.weighted_score == 1.0


def test_agent_trace_penalizes_wrong_tool_and_retries() -> None:
    events = [
        {'node': 'planner', 'success': True},
        {
            'node': 'tool',
            'tool': 'customer_lookup',
            'expected_tool': 'policy_search',
            'success': False,
            'retry_count': 1,
        },
        {'node': 'fallback', 'tool': 'policy_search', 'success': True},
    ]
    result = evaluate_agent_trace(
        'trace-002', events, task_completed=True, max_expected_steps=2
    )
    assert result.score.tool_selection == 0.0
    assert result.score.recovery_success == 1.0
    assert result.score.trajectory_efficiency < 1.0
    assert result.score.weighted_score < 1.0
