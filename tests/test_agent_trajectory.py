from llm_quality_harness.agent_trajectory import AgentStep, score_trajectory


def test_scores_correct_tool_use_and_completion() -> None:
    score = score_trajectory(
        [
            AgentStep('plan'),
            AgentStep('retrieve', tool='policy_search', expected_tool='policy_search'),
            AgentStep('answer'),
        ],
        task_completed=True,
        max_expected_steps=3,
    )

    assert score.task_completion == 1.0
    assert score.tool_selection == 1.0
    assert score.trajectory_efficiency == 1.0
    assert score.weighted_score == 1.0


def test_penalizes_wrong_tool_retries_and_incomplete_task() -> None:
    score = score_trajectory(
        [
            AgentStep('plan'),
            AgentStep(
                'lookup',
                tool='customer_lookup',
                expected_tool='policy_search',
                success=False,
                retry_count=1,
            ),
            AgentStep('retry', tool='policy_search', expected_tool='policy_search'),
            AgentStep('answer', success=False),
        ],
        task_completed=False,
        max_expected_steps=3,
    )

    assert score.task_completion == 0.0
    assert score.tool_selection == 0.5
    assert score.trajectory_efficiency < 1.0
    assert score.weighted_score < 0.6
