"""CSS for the AgentGuard landing / explainer page."""

LANDING_CSS = """
<style>
:root {
  --lp-max: 1240px;
  --lp-narrow: 44rem;
}

/* Wider reading shell on landing */
div.block-container {
  max-width: var(--lp-max) !important;
  padding-top: 0.75rem !important;
  padding-bottom: 4rem !important;
}

/* Hide default Streamlit chrome extras on landing */
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeaderActionElements"],
[data-testid="stMarkdownContainer"] a[data-testid="stHeaderActionLink"] {
  display: none !important;
}

/* ── Nav ─────────────────────────────────────────────── */
.lp-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 0 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0.5rem;
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(250,250,250,0.92);
  backdrop-filter: blur(8px);
}
.lp-nav-brand {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text);
  text-decoration: none;
}
.lp-nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1.15rem;
  align-items: center;
  font-size: 0.9rem;
}
.lp-nav-links a {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 500;
}
.lp-nav-links a:hover { color: var(--text); }
.lp-nav-links a.lp-nav-cta {
  color: var(--text);
  font-weight: 600;
}

/* Streamlit page_link in nav / CTAs */
div[data-testid="stPageLink"] a {
  font-weight: 600 !important;
  text-decoration: none !important;
  border-radius: var(--radius) !important;
}
div[data-testid="stPageLink"] a p {
  font-size: 0.92rem !important;
}
/* Stronger header playground CTA (marker + :has — widgets cannot nest in HTML) */
div[data-testid="stVerticalBlock"]:has(.lp-nav-cta-wrap) div[data-testid="stPageLink"] a {
  background: var(--text) !important;
  color: #fff !important;
  padding: 0.4rem 0.85rem !important;
  border: 1px solid var(--text) !important;
}
div[data-testid="stVerticalBlock"]:has(.lp-nav-cta-wrap) div[data-testid="stPageLink"] a p {
  color: #fff !important;
  -webkit-text-fill-color: #fff !important;
  font-size: 0.84rem !important;
}

/* ── Hero ────────────────────────────────────────────── */
.lp-hero {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 2.5rem;
  align-items: start;
  padding: 2.5rem 0 2.75rem;
}
.lp-kicker {
  margin: 0 0 0.65rem;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--muted);
}
.lp-hero h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1.12;
  color: var(--text);
}
.lp-hero .lp-sub {
  margin: 0.45rem 0 0;
  font-size: 1.05rem;
  color: var(--secondary);
  font-weight: 500;
}
.lp-hero .lp-lead {
  margin: 1.35rem 0 0;
  font-size: 1.35rem;
  font-weight: 600;
  letter-spacing: -0.03em;
  line-height: 1.35;
  color: var(--text);
  max-width: 28rem;
}
.lp-hero .lp-body {
  margin: 1rem 0 0;
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--secondary);
  max-width: var(--lp-narrow);
}
.lp-cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1.25rem;
  align-items: center;
  margin-top: 1.5rem;
}
.lp-link-secondary {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  border-bottom: 1px solid var(--border-strong);
  padding-bottom: 1px;
}
.lp-link-secondary:hover { border-color: var(--text); }

/* Hero / architecture diagrams */
.lp-diagram {
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 1.35rem 1.35rem 1.4rem;
  font-family: var(--mono);
  font-size: 0.82rem;
  line-height: 1.45;
}
.lp-diagram.lp-diagram-hero .node {
  padding: 0.55rem 0.75rem;
  font-size: 0.84rem;
}
.lp-diagram .lp-d-label {
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.85rem;
}
.lp-diagram .node {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.55rem 0.75rem;
  background: #FAFAFA;
  color: var(--text);
  text-align: center;
}
.lp-diagram .node.core {
  background: var(--surface);
  border-color: #A3A3A3;
  border-width: 1.5px;
  padding: 0.9rem 1rem;
  text-align: left;
}
.lp-diagram .node.core strong {
  display: block;
  font-size: 0.95rem;
  font-family: var(--sans);
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}
.lp-diagram .arrow {
  text-align: center;
  color: var(--secondary);
  padding: 0.45rem 0;
  font-size: 0.78rem;
}
.lp-diagram .outcomes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
  margin-top: 0.4rem;
}
.lp-diagram .out {
  text-align: center;
  padding: 0.45rem 0.3rem;
  border-radius: 4px;
  border: 1px solid var(--border);
  font-size: 0.75rem;
  font-weight: 600;
}
.lp-diagram .out.ok { color: var(--ok); border-color: var(--ok-line); background: var(--ok-soft); }
.lp-diagram .out.warn { color: var(--warn); border-color: var(--warn-line); background: var(--warn-soft); }
.lp-diagram .out.bad { color: var(--bad); border-color: var(--bad-line); background: var(--bad-soft); }

/* Featured architecture block */
.lp-arch {
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 1.5rem 1.5rem 1.35rem;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 1.75rem;
  align-items: start;
}
.lp-arch .lp-diagram {
  border: none;
  padding: 0;
  max-width: none;
}
.lp-arch .lp-arch-note {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.55;
  color: var(--secondary);
  max-width: none;
}
.lp-arch .lp-chips { margin-top: 1.1rem; }

/* ── Sections ────────────────────────────────────────── */
.lp-section {
  padding: 3.25rem 0;
  border-top: 1px solid var(--border);
}
.lp-section h2 {
  margin: 0 0 0.75rem;
  font-size: clamp(1.5rem, 2.5vw, 1.95rem);
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.2;
  color: var(--text);
}
.lp-section .lp-intro {
  margin: 0 0 1.5rem;
  font-size: 1.08rem;
  line-height: 1.55;
  color: var(--secondary);
  max-width: var(--lp-narrow);
}
.lp-section p {
  margin: 0 0 0.85rem;
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--secondary);
  max-width: var(--lp-narrow);
}
.lp-section p:last-child { margin-bottom: 0; }

/* Alternate section treatments — break the label→heading→card rhythm */
.lp-section-band {
  border-top: none;
  margin: 0.5rem 0;
  padding: 2.75rem 1.5rem;
  background: #F4F4F5;
  border-radius: var(--radius);
}
.lp-section-band .lp-compare { margin-bottom: 0; }
.lp-section-quiet {
  padding: 2.5rem 0;
}
.lp-section-quiet h2 {
  font-size: clamp(1.25rem, 2vw, 1.5rem);
  font-weight: 650;
}
.lp-section-feature {
  padding-top: 3.5rem;
}

/* Action class list */
.lp-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.65rem;
  margin-top: 1.25rem;
}
.lp-action {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.75rem 0.9rem;
  background: var(--surface);
}
/* Avoid <code> when we can — Streamlit forces dark terminal chips. */
.lp-mono {
  font-family: var(--mono) !important;
  font-size: 0.84rem !important;
  font-weight: 600 !important;
  color: #111111 !important;
  -webkit-text-fill-color: #111111 !important;
  background: #F5F5F5 !important;
  border: 1px solid #E5E5E5 !important;
  border-radius: 4px !important;
  padding: 0.15rem 0.4rem !important;
  display: inline-block;
}
.lp-action .lp-mono {
  display: inline-block;
  margin-bottom: 0.15rem;
}

/* Nuclear override: Streamlit markdown <code> is dark-on-dark by default */
div[data-testid="stMarkdownContainer"] code,
.stMarkdown code,
.lp-action code,
.lp-section code {
  font-family: var(--mono) !important;
  font-size: 0.84rem !important;
  font-weight: 600 !important;
  color: #111111 !important;
  -webkit-text-fill-color: #111111 !important;
  background: #F5F5F5 !important;
  background-color: #F5F5F5 !important;
  border: 1px solid #E5E5E5 !important;
  border-radius: 4px !important;
  padding: 0.15rem 0.4rem !important;
}
.lp-action span:not(.lp-mono) {
  display: block;
  margin-top: 0.35rem;
  font-size: 0.88rem;
  color: var(--muted);
}

/* Core question — deliberate visual break */
.lp-question {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.25rem;
  align-items: center;
  text-align: left;
  padding: 2.25rem 1.75rem;
  margin: 1.25rem 0 0.75rem;
  border: 1px solid var(--border-strong);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius);
  background: var(--surface);
}
.lp-question .a,
.lp-question .b {
  font-size: clamp(1.15rem, 2vw, 1.4rem);
  font-weight: 650;
  letter-spacing: -0.025em;
  line-height: 1.35;
  margin: 0;
}
.lp-question .a { color: var(--secondary); }
.lp-question .arrow {
  margin: 0;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 1.1rem;
  text-align: center;
}
.lp-question .b { color: var(--text); }
.lp-question .b em {
  font-style: normal;
  color: var(--accent);
  font-weight: 700;
}

/* Primitive cards */
.lp-prims {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.85rem;
  margin-top: 1.25rem;
}
.lp-prim {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.05rem;
  background: var(--surface);
}
.lp-prim .name {
  font-family: var(--mono);
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.35rem;
}
.lp-prim h3 {
  margin: 0 0 0.55rem;
  font-size: 1.1rem;
  font-weight: 650;
  letter-spacing: -0.02em;
}
.lp-prim p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.45;
  max-width: none;
}
.lp-prim .ex {
  margin-top: 0.75rem;
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--secondary);
  line-height: 1.5;
  background: #F5F5F5;
  border-radius: 4px;
  padding: 0.55rem 0.65rem;
}
.lp-bar-demo {
  margin: 0.45rem 0;
  height: 6px;
  background: #E5E5E5;
  border-radius: 2px;
  overflow: hidden;
}
.lp-bar-demo > span {
  display: block;
  height: 100%;
  background: var(--accent);
}

/* Compare LLM vs Jev */
.lp-compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
  margin: 1.25rem 0;
}
.lp-compare-col {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  background: var(--surface);
}
.lp-compare-col h3 {
  margin: 0 0 0.65rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
}
.lp-compare-col.typed {
  border-color: var(--border-strong);
}
.lp-compare-col pre {
  margin: 0;
  font-family: var(--mono);
  font-size: 0.78rem;
  line-height: 1.5;
  white-space: pre-wrap;
  color: var(--text);
}

/* Signal vs policy */
.lp-split {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  align-items: center;
  margin: 1.25rem 0;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.15rem;
  background: var(--surface);
}
.lp-split .box {
  padding: 0.75rem 0.9rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: #FAFAFA;
}
.lp-split .box h4 {
  margin: 0 0 0.45rem;
  font-size: 0.88rem;
  font-weight: 650;
}
.lp-split .box ul {
  margin: 0;
  padding-left: 1.1rem;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--secondary);
  line-height: 1.55;
}
.lp-split .mid {
  font-family: var(--mono);
  color: var(--muted);
  font-size: 0.85rem;
}
.lp-callout {
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  border-left: 3px solid var(--accent);
  background: #F8F8FC;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--secondary);
  max-width: none;
}

/* Flow steps */
.lp-section-flow {
  padding-top: 3.75rem;
  padding-bottom: 3.75rem;
}
.lp-section-flow h2 {
  font-size: clamp(1.65rem, 2.8vw, 2.15rem);
}
.lp-flow {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.85rem;
  margin-top: 1.5rem;
  padding: 1.35rem;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  background: var(--surface);
}
.lp-flow-step {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.05rem;
  background: #FAFAFA;
}
.lp-flow-step .num {
  font-family: var(--mono);
  font-size: 0.74rem;
  color: var(--muted);
  letter-spacing: 0.06em;
  margin-bottom: 0.35rem;
}
.lp-flow-step h4 {
  margin: 0 0 0.45rem;
  font-size: 1rem;
  font-weight: 650;
  letter-spacing: -0.015em;
}
.lp-flow-step p, .lp-flow-step pre {
  margin: 0;
  font-size: 0.88rem;
  line-height: 1.45;
  color: var(--secondary);
  max-width: none;
}
.lp-flow-step pre {
  font-family: var(--mono);
  white-space: pre-wrap;
  margin-top: 0.4rem;
  color: var(--text);
  font-size: 0.84rem;
}
.lp-flow-step.outcome {
  border-left: 3px solid var(--bad);
  background: var(--bad-soft);
}
.lp-flow-step.outcome h4 { color: var(--bad); }

/* Outcomes trio */
.lp-outcomes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-top: 1.25rem;
}
.lp-out {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.05rem;
  background: var(--surface);
  border-left-width: 3px;
}
.lp-out.execute { border-left-color: var(--ok); }
.lp-out.confirm { border-left-color: var(--warn); }
.lp-out.block { border-left-color: var(--bad); }
.lp-out .tag {
  font-family: var(--mono);
  font-size: 0.78rem;
  font-weight: 650;
  margin-bottom: 0.45rem;
}
.lp-out.execute .tag { color: var(--ok); }
.lp-out.confirm .tag { color: var(--warn); }
.lp-out.block .tag { color: var(--bad); }
.lp-out p {
  margin: 0;
  font-size: 0.84rem;
  max-width: none;
}

/* Example rows */
.lp-examples {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-top: 1.25rem;
}
.lp-ex {
  display: grid;
  grid-template-columns: 1.4fr 1fr auto;
  gap: 1rem;
  align-items: center;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  background: var(--surface);
}
.lp-ex .q {
  font-size: 0.88rem;
  color: var(--text);
  font-weight: 500;
}
.lp-ex .meta {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--secondary);
}
.lp-ex .badge {
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 650;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  white-space: nowrap;
}
.lp-ex .badge.ok { color: var(--ok); background: var(--ok-soft); }
.lp-ex .badge.warn { color: var(--warn); background: var(--warn-soft); }
.lp-ex .badge.bad { color: var(--bad); background: var(--bad-soft); }

/* Tech / eval lists */
.lp-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 1rem;
}
.lp-chip {
  font-family: var(--mono);
  font-size: 0.72rem;
  padding: 0.3rem 0.55rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--surface);
  color: var(--secondary);
}
.lp-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
  margin-top: 1.25rem;
}
.lp-two .panel {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  background: var(--surface);
}
.lp-two .panel h3 {
  margin: 0 0 0.55rem;
  font-size: 0.9rem;
  font-weight: 650;
}
.lp-two .panel ul {
  margin: 0;
  padding-left: 1.15rem;
  color: var(--secondary);
  font-size: 0.88rem;
  line-height: 1.55;
}

/* Playground CTA band */
.lp-cta-band {
  margin-top: 0.5rem;
  padding: 2.75rem 2rem 2.5rem;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  background: var(--surface);
  text-align: center;
}
.lp-cta-band h2 {
  margin: 0 0 0.55rem;
  font-size: clamp(1.75rem, 3vw, 2.1rem);
  letter-spacing: -0.035em;
}
.lp-cta-band p {
  margin: 0 auto 1.35rem;
  max-width: 34rem;
  text-align: center;
  font-size: 1.05rem;
}
.lp-cta-previews {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.25rem;
  font-family: var(--mono);
  font-size: 0.82rem;
  color: var(--secondary);
}
.lp-cta-band + div,
div[data-testid="stVerticalBlock"]:has(.lp-cta-actions) {
  margin-top: 1.1rem !important;
}
div[data-testid="stVerticalBlock"]:has(.lp-cta-actions) div[data-testid="stPageLink"] a {
  background: var(--text) !important;
  color: #fff !important;
  padding: 0.7rem 1.35rem !important;
  border: 1px solid var(--text) !important;
  justify-content: center !important;
}
div[data-testid="stVerticalBlock"]:has(.lp-cta-actions) div[data-testid="stPageLink"] a p {
  color: #fff !important;
  -webkit-text-fill-color: #fff !important;
  font-size: 0.95rem !important;
  font-weight: 650 !important;
}

/* Footer */
.lp-footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1.5rem;
}
.lp-footer strong {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.2rem;
}
.lp-footer p {
  margin: 0;
  font-size: 0.84rem;
  color: var(--muted);
  max-width: 28rem;
  line-height: 1.45;
}
.lp-footer .links {
  font-size: 0.84rem;
  color: var(--secondary);
  text-align: right;
}
.lp-footer .links a {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 500;
}
.lp-footer .links a:hover { color: var(--text); }

/* Hide floating CTA near bottom CTA via scroll is hard in Streamlit;
   keep it subtle. */

@media (max-width: 900px) {
  .lp-hero { grid-template-columns: 1fr; gap: 1.75rem; padding-top: 1.5rem; }
  .lp-prims, .lp-compare, .lp-actions, .lp-outcomes, .lp-two, .lp-flow, .lp-arch {
    grid-template-columns: 1fr;
  }
  .lp-question {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 0.65rem;
  }
  .lp-question .arrow { transform: none; }
  .lp-split { grid-template-columns: 1fr; }
  .lp-split .mid { text-align: center; transform: rotate(90deg); margin: 0.25rem 0; }
  .lp-ex { grid-template-columns: 1fr; gap: 0.35rem; }
  .lp-nav-links a:not(.lp-nav-cta) { display: none; }
  .lp-footer { grid-template-columns: 1fr; }
  .lp-footer .links { text-align: left; }
}
</style>
"""
