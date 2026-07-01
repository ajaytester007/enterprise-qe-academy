const panel = document.getElementById('contentPanel');
const title = document.getElementById('panelTitle');
let platformData = {};

function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}

function readinessScore(data) {
  const dash = data.readinessDashboard || {};
  const direct = dash.overall_readiness_score || dash.overallScore || dash.score;
  if (typeof direct === 'number') return Math.round(direct);
  const analyses = data.jdReadiness || [];
  const scores = analyses.map(a => a.readiness_score || a.score).filter(v => typeof v === 'number');
  if (scores.length) return Math.round(scores.reduce((a,b)=>a+b,0) / scores.length);
  return null;
}

function renderOverview(data) {
  title.textContent = 'Platform Overview';
  const nodes = data.knowledgeNodes || [];
  document.getElementById('nodeCount').textContent = `${nodes.length} knowledge nodes`;
  panel.innerHTML = `
    <div class="item"><strong>Available modules:</strong> ${nodes.length}</div>
    <div class="item"><strong>JD analyses:</strong> ${(data.jdReadiness || []).length}</div>
    <div class="item"><strong>Quality report:</strong> ${Object.keys(data.qualityReport || {}).length ? 'Available' : 'Not generated yet'}</div>
    <div class="item"><strong>Next best action:</strong> Launch a practice session from the top matched JD skills, then review readiness gaps.</div>
  `;
}

function renderInterview(data) {
  title.textContent = 'Interview Simulator';
  const nodes = (data.knowledgeNodes || []).slice(0, 10);
  if (!nodes.length) {
    panel.innerHTML = '<div class="item">No knowledge nodes found. Run the v4/v5 build scripts first.</div>';
    return;
  }
  panel.innerHTML = nodes.map((n, i) => `
    <div class="item">
      <strong>Question ${i + 1}: ${esc(n.title || n.id || 'Practice node')}</strong>
      <p>${esc(n.problem || n.summary || n.description || 'Explain the solution, risks, validation strategy, evidence, and production-readiness considerations.')}</p>
      <span class="badge">${esc(n.domain || 'Domain')}</span>
      <span class="badge">${esc(n.difficulty || 'Difficulty')}</span>
      <span class="badge">${esc(n.role || 'Role')}</span>
    </div>
  `).join('');
}

function renderJD(data) {
  title.textContent = 'JD Readiness Dashboard';
  const analyses = data.jdReadiness || [];
  if (!analyses.length) {
    panel.innerHTML = '<div class="item">No JD analysis found. Run build_v4_jd_readiness_release.py first.</div>';
    return;
  }
  panel.innerHTML = analyses.map(a => `
    <div class="item">
      <strong>${esc(a.job_title || a.jd_name || a.file || 'JD analysis')}</strong>
      <p>Readiness score: <strong>${esc(a.readiness_score ?? a.score ?? '--')}</strong></p>
      <p>${esc(a.summary || 'Review skill matches, gaps, and recommended practice modules.')}</p>
      <div>${(a.required_skills || a.skills || []).slice(0, 18).map(s => `<span class="badge">${esc(s)}</span>`).join('')}</div>
    </div>
  `).join('');
}

function renderQuality(data) {
  title.textContent = 'Quality Intelligence';
  const q = data.qualityReport || {};
  panel.innerHTML = `<pre>${esc(JSON.stringify(q, null, 2).slice(0, 8000))}</pre>`;
}

fetch('data/platform-data.json')
  .then(r => r.json())
  .then(data => {
    platformData = data;
    const score = readinessScore(data);
    document.getElementById('readinessScore').textContent = score == null ? '--' : score;
    document.getElementById('readinessLabel').textContent = score == null ? 'Run readiness build' : score >= 80 ? 'Strong alignment' : score >= 60 ? 'Moderate alignment' : 'Needs targeted practice';
    renderOverview(data);
  })
  .catch(err => {
    panel.innerHTML = `<div class="item">Unable to load platform data: ${esc(err.message)}</div>`;
  });

document.getElementById('launchInterview').addEventListener('click', () => renderInterview(platformData));
document.getElementById('showJD').addEventListener('click', () => renderJD(platformData));
document.getElementById('showQuality').addEventListener('click', () => renderQuality(platformData));
