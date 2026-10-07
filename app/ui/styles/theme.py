"""CSS for the AgentGuard execution console."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --bg: #FAFAFA;
  --surface: #FFFFFF;
  --text: #111111;
  --secondary: #525252;
  --muted: #737373;
  --border: #E5E5E5;
  --border-strong: #D4D4D4;
  --accent: #312E81;
  --ok: #0F766E;
  --ok-soft: #F0FDFA;
  --ok-line: #99F6E4;
  --warn: #B45309;
  --warn-soft: #FFFBEB;
  --warn-line: #FDE68A;
  --bad: #B91C1C;
  --bad-soft: #FEF2F2;
  --bad-line: #FECACA;
  --mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --radius: 6px;
}

html, body, [class*="css"], .stApp, button, input, textarea {
  font-family: var(--sans) !important;
}
.stApp { background: var(--bg); color: var(--text); }

div.block-container {
  max-width: 1240px !important;
  padding-top: 1.5rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 2.25rem !important;
  padding-right: 2.25rem !important;
}

#MainMenu, footer, div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
header[data-testid="stHeader"],
header.stAppHeader {
  background: transparent !important;
  height: 0 !important;
  min-height: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}

section[data-testid="stSidebar"] {
  background: var(--surface);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.25rem !important; }

/* ── Header ─────────────────────────────────────────── */
.ag-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1.5rem;
  padding-bottom: 1.1rem;
  margin-bottom: 1.35rem;
  border-bottom: 1px solid var(--border);
}
.ag-top h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.15;
  color: var(--text);
}
.ag-top .sub {
  margin: 0.28rem 0 0;
  color: var(--secondary);
  font-size: 0.875rem;
  font-weight: 450;
  letter-spacing: -0.01em;
}
.ag-top-right {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem 1.1rem;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 0.15rem;
}
.ag-stat {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--muted);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  letter-spacing: 0.01em;
}
.ag-stat i {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #10B981;
  display: inline-block;
  flex-shrink: 0;
}
.ag-stat.warn i { background: #D97706; }
.ag-stat.muted { color: var(--muted); }
.ag-stat.muted i { display: none; }

/* ── Section labels ─────────────────────────────────── */
.ag-kicker {
  margin: 0 0 0.55rem;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--muted);
}
.ag-title {
  margin: 0 0 0.2rem;
  font-size: 1.15rem;
  font-weight: 650;
  letter-spacing: -0.03em;
  line-height: 1.25;
}
.ag-lead {
  margin: 0 0 0.75rem;
  max-width: 36rem;
  color: var(--secondary);
  font-size: 0.875rem;
  line-height: 1.45;
}
.ag-section {
  margin-top: 1.35rem;
}
.ag-section-first {
  margin-top: 1.5rem;
  padding-top: 1.15rem;
  border-top: 1px solid var(--border);
}

/* ── Composer ───────────────────────────────────────── */
.ag-composer-label {
  margin: 0.55rem 0 0.35rem;
  font-size: 0.78rem;
  color: var(--muted);
  font-weight: 500;
}

div[data-testid="stTextArea"] textarea {
  background: var(--surface) !important;
  border: 1px solid var(--border-strong) !important;
  border-radius: var(--radius) !important;
  font-size: 0.95rem !important;
  line-height: 1.45 !important;
  min-height: 72px !important;
  max-height: 120px !important;
  box-shadow: none !important;
  color: var(--text) !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #A5B4FC !important;
  box-shadow: 0 0 0 2px rgba(49, 46, 129, 0.1) !important;
}

/* Primary actions — dark, restrained */
div.stButton > button[kind="primary"],
div.stButton > button[data-testid="baseButton-primary"] {
  background: var(--text) !important;
  color: #fff !important;
  border: 1px solid var(--text) !important;
  border-radius: var(--radius) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  box-shadow: none !important;
  padding: 0.4rem 1.1rem !important;
  min-height: 2.25rem !important;
}
div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="baseButton-primary"]:hover {
  background: #262626 !important;
  border-color: #262626 !important;
}

/* Secondary / reject */
div.stButton > button:not([kind="primary"]) {
  background: var(--surface) !important;
  color: var(--secondary) !important;
  border: 1px solid var(--border-strong) !important;
  border-radius: var(--radius) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  box-shadow: none !important;
  min-height: 2.25rem !important;
}
div.stButton > button:not([kind="primary"]):hover {
  background: #F5F5F5 !important;
  color: var(--text) !important;
}

/* Scenario pills — compact quick actions */
div[data-testid="stPills"],
div[data-testid="stButtonGroup"] {
  margin-top: 0.15rem !important;
  justify-content: flex-start !important;
  flex-wrap: wrap !important;
  gap: 0.35rem !important;
}
div[data-testid="stPills"] label,
div[data-testid="stPills"] > label {
  display: none !important;
}
div[data-testid="stPills"] button,
div[data-testid="stButtonGroup"] button {
  background: var(--surface) !important;
  color: var(--secondary) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  padding: 0.28rem 0.7rem !important;
  min-height: 1.85rem !important;
  box-shadow: none !important;
}
div[data-testid="stPills"] button:hover,
div[data-testid="stButtonGroup"] button:hover {
  border-color: var(--border-strong) !important;
  color: var(--text) !important;
  background: #F5F5F5 !important;
}
div[data-testid="stPills"] button[aria-pressed="true"],
div[data-testid="stButtonGroup"] button[kind="primary"] {
  background: #F5F5F5 !important;
  color: var(--text) !important;
  border-color: var(--border-strong) !important;
}

/* ── Evaluation: proposal | jev ─────────────────────── */
.ag-eval {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  overflow: hidden;
}
.ag-eval-pane {
  padding: 1rem 1.15rem 1.1rem;
  min-width: 0;
}
.ag-eval-pane + .ag-eval-pane {
  border-left: 1px solid var(--border);
}
.ag-tool-name {
  margin: 0 0 0.55rem;
  font-family: var(--mono);
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
}
.ag-args {
  margin: 0;
  font-family: var(--mono);
  font-size: 0.78rem;
  line-height: 1.5;
  background: #F5F5F5;
  border-radius: 4px;
  padding: 0.6rem 0.75rem;
  overflow-x: auto;
  color: var(--text);
  white-space: pre-wrap;
}
.ag-reason {
  margin: 0.6rem 0 0;
  color: var(--secondary);
  font-size: 0.84rem;
  line-height: 1.4;
}

/* Jev signals */
.ag-jev-stack {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.ag-signal .k {
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.2rem;
}
.ag-signal .v {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.15;
  color: var(--text);
  word-break: break-word;
}
.ag-signal .v.action {
  font-family: var(--mono);
  font-size: 1.05rem;
  font-weight: 600;
}
.ag-signal .v.emphasis {
  font-size: 1.65rem;
}
.ag-signal .d {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--muted);
  margin-top: 0.2rem;
}
.ag-bar {
  margin: 0.4rem 0 0.2rem;
  height: 6px;
  background: #E5E5E5;
  border-radius: 2px;
  overflow: hidden;
  max-width: 11rem;
}
.ag-bar > span {
  display: block;
  height: 100%;
  background: var(--accent);
  border-radius: 2px;
}
.ag-bar.risk-low > span { background: var(--ok); }
.ag-bar.risk-mid > span { background: var(--warn); }
.ag-bar.risk-high > span { background: var(--bad); }
.ag-demo-note {
  margin: 0.65rem 0 0;
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--muted);
}

/* ── Policy + approval (connected) ──────────────────── */
.ag-auth {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  overflow: hidden;
}
.ag-policy {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0 1.5rem;
  align-items: start;
  padding: 0.95rem 1.15rem;
  border-left: 3px solid var(--border-strong);
  background: var(--surface);
}
.ag-policy.execute {
  border-left-color: var(--ok);
  background: var(--ok-soft);
}
.ag-policy.confirm {
  border-left-color: var(--warn);
  background: var(--warn-soft);
}
.ag-policy.block {
  border-left-color: var(--bad);
  background: var(--bad-soft);
}
.ag-policy .verdict-block { min-width: 10rem; }
.ag-policy .label {
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 0.15rem;
}
.ag-policy .verdict {
  margin: 0;
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.15;
  color: var(--text);
}
.ag-policy.execute .verdict { color: var(--ok); }
.ag-policy.confirm .verdict { color: var(--warn); }
.ag-policy.block .verdict { color: var(--bad); }
.ag-policy .why {
  margin: 0 0 0.45rem;
  color: var(--secondary);
  font-size: 0.875rem;
  line-height: 1.45;
  max-width: 42rem;
}
.ag-policy-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--muted);
}

.ag-approval {
  border-top: 1px solid var(--border);
  padding: 0.85rem 1.15rem 1rem;
  background: #FCFCFC;
}
.ag-approval .ag-title {
  font-size: 1rem;
  margin-bottom: 0.15rem;
}
.ag-approval .ag-lead {
  margin-bottom: 0.65rem;
  font-size: 0.84rem;
}
.ag-approved-banner {
  border-top: 1px solid var(--border);
  padding: 0.7rem 1.15rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--ok-soft);
  font-size: 0.875rem;
}
.ag-approved-banner.reject { background: var(--bad-soft); }
.ag-approved-banner .mark {
  font-family: var(--mono);
  font-weight: 600;
  color: var(--ok);
  font-size: 0.78rem;
  letter-spacing: 0.04em;
}
.ag-approved-banner.reject .mark { color: var(--bad); }
.ag-approved-banner .txt { color: var(--secondary); }

/* ── Execution pipeline ─────────────────────────────── */
.ag-pipe {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  overflow: hidden;
}
.ag-node {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 0.2rem;
  padding: 0.7rem 0.95rem;
  min-width: 5.5rem;
  flex: 1 1 auto;
  position: relative;
}
.ag-node + .ag-node {
  border-left: 1px solid var(--border);
}
.ag-node .mark {
  font-family: var(--mono);
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1;
}
.ag-node .name {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--text);
}
.ag-node.ok .mark { color: var(--ok); }
.ag-node.warn .mark { color: var(--warn); }
.ag-node.fail .mark { color: var(--bad); }
.ag-node.pending .mark { color: var(--muted); }
.ag-node.pending .name { color: var(--muted); font-weight: 500; }
.ag-node.ok { background: var(--ok-soft); }
.ag-node.warn { background: var(--warn-soft); }
.ag-node.fail { background: var(--bad-soft); }

/* ── Tool result ────────────────────────────────────── */
.ag-result {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 0.85rem 1.15rem;
  border-left: 3px solid var(--border-strong);
}
.ag-result.ok { border-left-color: var(--ok); }
.ag-result.fail { border-left-color: var(--bad); }
.ag-result.warn { border-left-color: var(--warn); }
.ag-result .status {
  margin: 0 0 0.2rem;
  font-size: 0.95rem;
  font-weight: 650;
  letter-spacing: -0.02em;
}
.ag-result.ok .status { color: var(--ok); }
.ag-result.fail .status { color: var(--bad); }
.ag-result.warn .status { color: var(--warn); }
.ag-result .msg {
  margin: 0;
  color: var(--secondary);
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Checkbox for raw output */
div[data-testid="stCheckbox"] {
  margin-top: 0.55rem !important;
}
div[data-testid="stCheckbox"] label p {
  font-size: 0.8rem !important;
  color: var(--secondary) !important;
}
div[data-testid="stCheckbox"] [data-testid="stWidgetLabel"] {
  margin-bottom: 0 !important;
}

/* ── Trace log ──────────────────────────────────────── */
.ag-trace {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  overflow: hidden;
}
.ag-trace-head {
  display: grid;
  grid-template-columns: 4.75rem 1fr 4.5rem;
  gap: 0.75rem;
  padding: 0.45rem 0.9rem;
  border-bottom: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--muted);
  background: #FCFCFC;
}
.ag-trace-row {
  display: grid;
  grid-template-columns: 4.75rem 1fr 4.5rem;
  gap: 0.75rem;
  padding: 0.45rem 0.9rem;
  border-bottom: 1px solid #F0F0F0;
  align-items: start;
}
.ag-trace-row:last-child { border-bottom: none; }
.ag-trace-ts {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--muted);
  padding-top: 0.1rem;
}
.ag-trace-event {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.01em;
}
.ag-trace-meta {
  margin-top: 0.1rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--secondary);
  line-height: 1.35;
  word-break: break-word;
}
.ag-trace-dur {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--muted);
  text-align: right;
  padding-top: 0.1rem;
  white-space: nowrap;
}
.ag-trace-empty {
  padding: 0.75rem 0.9rem;
  color: var(--muted);
  font-size: 0.84rem;
}

/* ── Metrics ────────────────────────────────────────── */
.ag-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1.35rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
  margin-top: 1.15rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--secondary);
}
.ag-metrics strong { color: var(--text); font-weight: 600; }
.ag-metrics .run-id { color: var(--muted); }

/* Misc Streamlit cleanup */
hr {
  margin: 1.25rem 0 !important;
  border: none !important;
  border-top: 1px solid var(--border) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface);
}
div[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
}
div[data-testid="stExpander"] details > summary,
div[data-testid="stExpander"] details[open] > summary {
  background: #F5F5F5 !important;
  color: #111111 !important;
  -webkit-text-fill-color: #111111 !important;
}
div[data-testid="stExpander"] details > summary *,
div[data-testid="stExpander"] details[open] > summary * {
  color: #111111 !important;
  -webkit-text-fill-color: #111111 !important;
}

/* JSON / code blocks */
div[data-testid="stJson"],
.stJson {
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  background: #0A0A0A !important;
  font-size: 0.8rem !important;
}

@media (max-width: 900px) {
  .ag-eval { grid-template-columns: 1fr; }
  .ag-eval-pane + .ag-eval-pane {
    border-left: none;
    border-top: 1px solid var(--border);
  }
  .ag-policy {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .ag-top {
    flex-direction: column;
    align-items: flex-start;
  }
  .ag-top-right { justify-content: flex-start; }
  .ag-pipe { flex-direction: column; }
  .ag-node + .ag-node {
    border-left: none;
    border-top: 1px solid var(--border);
  }
  .ag-trace-head,
  .ag-trace-row {
    grid-template-columns: 3.75rem 1fr 3.5rem;
    gap: 0.4rem;
    padding-left: 0.65rem;
    padding-right: 0.65rem;
  }
  div.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
}
</style>
"""
