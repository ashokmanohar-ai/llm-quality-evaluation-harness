const runButton = document.querySelector('#run-demo');
const state = document.querySelector('#run-state');

const pct = (value) => `${Math.round(value * 100)}%`;

function render(result, gate) {
  document.querySelector('#suite-score').textContent = pct(result.summary.mean_score);
  document.querySelector('#cases-passed').textContent = `${result.summary.passed_cases}/${result.summary.total_cases}`;
  document.querySelector('#safety-rate').textContent = pct(result.summary.safety_case_pass_rate);
  document.querySelector('#latency').textContent = `${result.summary.latency_p95_ms.toFixed(0)} ms`;

  const gatePill = document.querySelector('#gate-pill');
  gatePill.textContent = gate.decision === 'pass' ? 'Release gate passed' : 'Release gate failed';
  gatePill.className = `gate ${gate.decision}`;

  document.querySelector('#metrics').innerHTML = Object.entries(result.summary.metric_means)
    .map(([name, score]) => `<div class="metric"><div><span>${name.replace('_', ' ')}</span><strong>${pct(score)}</strong></div><div class="bar"><i style="width:${score * 100}%"></i></div></div>`)
    .join('');

  document.querySelector('#case-results').innerHTML = result.cases
    .map((item) => `<tr><td>${item.case_id}</td><td>${item.tags.join(', ')}</td><td>${pct(item.score)}</td><td><span class="status ${item.status}">${item.status}</span></td><td>${item.schema_compliant ? 'Pass' : 'Fail'}</td></tr>`)
    .join('');
}

runButton.addEventListener('click', async () => {
  runButton.disabled = true;
  state.textContent = 'Evaluating…';
  try {
    const response = await fetch('/api/demo', { method: 'POST' });
    if (!response.ok) throw new Error(`Evaluation failed (${response.status})`);
    const result = await response.json();
    const gateResponse = await fetch(`/api/results/${encodeURIComponent(result.suite_id)}/gate`);
    if (!gateResponse.ok) throw new Error(`Gate failed (${gateResponse.status})`);
    render(result, await gateResponse.json());
    state.textContent = 'Evidence captured';
  } catch (error) {
    state.textContent = error.message;
  } finally {
    runButton.disabled = false;
  }
});

