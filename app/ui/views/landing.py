"""AgentGuard landing / explainer page."""

from __future__ import annotations

import textwrap

import streamlit as st

from app.ui.styles.landing import LANDING_CSS
from app.ui.styles.theme import APP_CSS


def _html(markup: str) -> None:
    cleaned = textwrap.dedent(markup).strip()
    cleaned = "\n".join(line.lstrip() for line in cleaned.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def _playground_page():
    return st.session_state.get("page_playground")


def render_landing() -> None:
    """Default entry — conceptual explanation. Does not init AgentGuard/Jev."""
    st.markdown(APP_CSS + LANDING_CSS, unsafe_allow_html=True)

    play = _playground_page()

    # ── Navigation ─────────────────────────────────────
    nav_cols = st.columns([1.2, 3.5, 1.3], gap="small")
    with nav_cols[0]:
        _html('<div class="lp-nav-brand">AgentGuard</div>')
    with nav_cols[1]:
        _html(
            """
            <div class="lp-nav-links" style="justify-content:flex-end;padding-top:0.35rem;">
              <a href="#problem">How it works</a>
              <a href="#jev">Jev</a>
              <a href="#architecture">Architecture</a>
            </div>
            """
        )
    with nav_cols[2]:
        if play is not None:
            # Marker for CSS :has() — Streamlit cannot nest widgets inside HTML wraps.
            _html('<span class="lp-nav-cta-wrap" hidden></span>')
            st.page_link(play, label="Playground →", width="stretch")

    # ── Hero ───────────────────────────────────────────
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        _html(
            """
            <div style="padding:1.75rem 0 0.5rem;">
              <p class="lp-kicker">AI Agent Safety Gateway</p>
              <h1 style="font-size:clamp(2rem,4vw,2.75rem);font-weight:700;
                letter-spacing:-0.04em;line-height:1.12;margin:0;">AgentGuard</h1>
              <p class="lp-lead" style="margin-top:1.25rem;font-size:1.3rem;font-weight:600;
                letter-spacing:-0.03em;line-height:1.35;max-width:28rem;">
                When an AI agent can act,<br/>who decides what it is allowed to do?
              </p>
              <p class="lp-body" style="margin-top:1rem;font-size:1.05rem;line-height:1.55;color:#525252;max-width:42rem;">
                AgentGuard evaluates AI-generated tool calls before they execute,
                combining typed decisions from Jev with deterministic application policy.
              </p>
            </div>
            """
        )
        c1, c2, _ = st.columns([1.35, 1.2, 1.5], gap="small")
        with c1:
            _html('<a class="lp-link-secondary" href="#problem">Explore how it works ↓</a>')
        with c2:
            if play is not None:
                st.page_link(play, label="Open Playground →", width="content")

    with right:
        _html(
            """
            <div class="lp-diagram lp-diagram-hero" style="margin-top:1.75rem;" role="img"
              aria-label="Architecture: AI Agent proposes an action to AgentGuard,
              which uses Jev signals and policy to Execute, Confirm, or Block.">
              <div class="lp-d-label">Decision path</div>
              <div class="node">AI Agent</div>
              <div class="arrow">proposes action ↓</div>
              <div class="node core">
                <strong>AgentGuard</strong>
                Jev → choice · score · noul<br/>
                Policy → decision
              </div>
              <div class="arrow">↓</div>
              <div class="outcomes">
                <div class="out ok">Execute</div>
                <div class="out warn">Confirm</div>
                <div class="out bad">Block</div>
              </div>
            </div>
            """
        )

    # ── Problem ────────────────────────────────────────
    _html(
        """
        <div class="lp-section" id="problem">
          <p class="lp-kicker">The problem</p>
          <h2>AI agents can act.<br/>Tool calls have consequences.</h2>
          <p class="lp-intro">
            Modern AI agents can reason about a task and select tools to accomplish it.
            Tool execution can have side effects — some informational, some persistent,
            some external, some destructive.
          </p>
          <div class="lp-actions">
            <div class="lp-action"><span class="lp-mono">read_file()</span><span>informational</span></div>
            <div class="lp-action"><span class="lp-mono">create_note()</span><span>persistent change</span></div>
            <div class="lp-action"><span class="lp-mono">send_notification()</span><span>external side effect</span></div>
            <div class="lp-action"><span class="lp-mono">delete_file()</span><span>destructive action</span></div>
          </div>
          <p style="margin-top:1.25rem;">
            AgentGuard explores what happens when a decision layer sits between
            an agent’s intent and tool execution.
          </p>
        </div>
        """
    )

    # ── Core question ──────────────────────────────────
    _html(
        """
        <div class="lp-question" role="region" aria-label="Core question">
          <p class="a">“The agent wants to do this.”</p>
          <div class="arrow" aria-hidden="true">→</div>
          <p class="b">“The system decides <em>whether it should</em>.”</p>
        </div>
        """
    )

    # ── What is Jev ────────────────────────────────────
    _html(
        """
        <div class="lp-section" id="jev">
          <p class="lp-kicker">What is Jev?</p>
          <h2>Jev makes decisions software can act on.</h2>
          <p class="lp-intro">
            Jev is a typed decision model designed for small, structured decisions
            inside software systems — not a conversational chatbot.
          </p>
          <p>
            AgentGuard uses three Jev primitives in one request:
            <strong>choice</strong>, <strong>score</strong>, and <strong>noul</strong>.
          </p>
          <div class="lp-prims">
            <div class="lp-prim">
              <div class="name">Choice</div>
              <h3>Pick one option</h3>
              <p>Classify the proposed action into a risk-relevant category.</p>
              <div class="ex">read_only<br/>local_write<br/>filesystem_delete<br/>code_execution<br/>external_side_effect</div>
            </div>
            <div class="lp-prim">
              <div class="name">Score</div>
              <h3>Rate an ordered value</h3>
              <p>Estimate consequence level — not a probability.</p>
              <div class="ex">1 ──────────── 5<br/>LOW → HIGH<br/><br/>Risk: 4.3 / 5
                <div class="lp-bar-demo"><span style="width:86%"></span></div>
              </div>
            </div>
            <div class="lp-prim">
              <div class="name">Noul</div>
              <h3>Yes/no probability</h3>
              <p>Estimate suitability for automatic execution. A signal — not authorization.</p>
              <div class="ex">Safe to execute?<br/>0% ────────── 100%<br/><br/><strong>7%</strong></div>
            </div>
          </div>
        </div>
        """
    )

    # ── Why Jev ────────────────────────────────────────
    _html(
        """
        <div class="lp-section lp-section-band">
          <p class="lp-kicker">Why Jev?</p>
          <h2>Why use a decision model here?</h2>
          <p class="lp-intro">
            Free-form model prose is hard for software to branch on.
            Typed decision signals are not.
          </p>
          <div class="lp-compare">
            <div class="lp-compare-col">
              <h3>Generative LLM</h3>
              <pre>"I think this action is probably
safe because…"</pre>
              <p style="margin-top:0.75rem;font-size:0.9rem;">
                Free-form output → the application must interpret it.
              </p>
            </div>
            <div class="lp-compare-col typed">
              <h3>Jev</h3>
              <pre>choice → filesystem_delete
score  → 4.3 / 5
noul   → 0.07</pre>
              <p style="margin-top:0.75rem;font-size:0.9rem;">
                Typed signals → the application can branch directly.
              </p>
            </div>
          </div>
          <p style="margin-top:1.15rem;">
            AgentGuard does not need another model to generate a paragraph about the action.
            It needs structured decision signals as inputs to a deterministic policy.
          </p>
        </div>
        """
    )

    # ── How AgentGuard uses Jev ────────────────────────
    _html(
        """
        <div class="lp-section">
          <p class="lp-kicker">How AgentGuard uses Jev</p>
          <h2>One tool call. Three questions.</h2>
          <p class="lp-intro">
            AgentGuard evaluates the proposed action using multiple typed decision
            signals in a single Jev request.
          </p>
          <div class="lp-diagram" style="max-width:28rem;margin:0 auto 1.25rem;">
            <div class="node">Proposed tool call · <strong>delete_demo_file</strong></div>
            <div class="arrow">↓</div>
            <div class="node core" style="text-align:center;"><strong>Jev</strong></div>
            <div class="arrow">↓</div>
            <div class="outcomes">
              <div class="out">choice<br/><strong>filesystem_delete</strong></div>
              <div class="out">score<br/><strong>4.3 / 5</strong></div>
              <div class="out">noul<br/><strong>7%</strong></div>
            </div>
          </div>
          <p>
            Action type, risk, and safe-to-execute probability become inputs —
            not the final policy decision.
          </p>
        </div>
        """
    )

    # ── Jev ≠ policy ───────────────────────────────────
    _html(
        """
        <div class="lp-section" id="architecture">
          <p class="lp-kicker">Signals vs policy</p>
          <h2>Jev provides signals.<br/>AgentGuard makes the policy decision.</h2>
          <div class="lp-split">
            <div class="box">
              <h4>Jev</h4>
              <ul>
                <li>Action type</li>
                <li>Risk score</li>
                <li>Safe probability</li>
              </ul>
            </div>
            <div class="mid">→</div>
            <div class="box">
              <h4>AgentGuard policy</h4>
              <ul>
                <li>EXECUTE</li>
                <li>REQUIRE CONFIRMATION</li>
                <li>BLOCK</li>
              </ul>
            </div>
          </div>
          <p class="lp-callout">
            Jev does not directly authorize or execute a tool call.
            AgentGuard applies deterministic application policy to those signals.
            Prefer “AgentGuard blocked the action based on Jev decision signals”
            — not “Jev blocked the action.”
          </p>
        </div>
        """
    )

    # ── Full flow ──────────────────────────────────────
    _html(
        """
        <div class="lp-section lp-section-flow">
          <p class="lp-kicker">The full flow</p>
          <h2>From intent to execution.</h2>
          <div class="lp-flow">
            <div class="lp-flow-step">
              <div class="num">01 · USER</div>
              <h4>Request</h4>
              <p>“Delete the old report.”</p>
            </div>
            <div class="lp-flow-step">
              <div class="num">02 · AGENT</div>
              <h4>Proposal</h4>
              <pre>delete_demo_file
path: old-report.pdf</pre>
            </div>
            <div class="lp-flow-step">
              <div class="num">03 · AGENTGUARD</div>
              <h4>Validate</h4>
              <p>Confirm the tool exists and arguments are admissible.</p>
            </div>
            <div class="lp-flow-step">
              <div class="num">04 · JEV</div>
              <h4>Signals</h4>
              <pre>choice → filesystem_delete
score  → 4.3 / 5
noul   → 0.07</pre>
            </div>
            <div class="lp-flow-step">
              <div class="num">05 · POLICY</div>
              <h4>Decide</h4>
              <p>Deterministic thresholds and hard rules.</p>
            </div>
            <div class="lp-flow-step outcome">
              <div class="num">06 · OUTCOME</div>
              <h4>× BLOCK</h4>
              <p>Tool never executes. Audit trail recorded.</p>
            </div>
          </div>
        </div>
        """
    )

    # ── Three outcomes ─────────────────────────────────
    _html(
        """
        <div class="lp-section">
          <p class="lp-kicker">Policy outcomes</p>
          <h2>Every action has a policy outcome.</h2>
          <div class="lp-outcomes">
            <div class="lp-out execute">
              <div class="tag">✓ EXECUTE</div>
              <p>Low risk · high safe-to-execute probability · auto-run allowed.</p>
            </div>
            <div class="lp-out confirm">
              <div class="tag">! REQUIRE CONFIRMATION</div>
              <p>Moderate risk or gated action type · human approval required.</p>
            </div>
            <div class="lp-out block">
              <div class="tag">× BLOCK</div>
              <p>High risk or hard rule · automatic execution prevented.</p>
            </div>
          </div>
          <p class="lp-kicker" style="margin-top:2rem;">Representative examples</p>
          <p style="margin-bottom:0.75rem;font-size:0.84rem;">
            Illustrative of typical playground paths. Live Jev values can vary.
          </p>
          <div class="lp-examples">
            <div class="lp-ex">
              <div class="q">“Read the project notes.”</div>
              <div class="meta">read_file · ~1.0/5 · ~97%</div>
              <div class="badge ok">→ EXECUTE</div>
            </div>
            <div class="lp-ex">
              <div class="q">“Create a note saying I finished the experiment.”</div>
              <div class="meta">create_note · ~1.9/5 · ~95%</div>
              <div class="badge warn">→ CONFIRM</div>
            </div>
            <div class="lp-ex">
              <div class="q">“Delete the old demo report permanently.”</div>
              <div class="meta">delete_demo_file · ~4.3/5 · ~7%</div>
              <div class="badge bad">→ BLOCK</div>
            </div>
          </div>
        </div>
        """
    )

    # ── Under the hood ─────────────────────────────────
    _html(
        """
        <div class="lp-section lp-section-feature">
          <p class="lp-kicker">Under the hood</p>
          <h2>Architecture &amp; stack</h2>
          <div class="lp-arch">
            <div class="lp-diagram" role="img"
              aria-label="User to Agent to AgentGuard with Jev and Policy to Execute, Confirm, or Block.">
              <div class="lp-d-label">Runtime path</div>
              <div class="node">User</div>
              <div class="arrow">↓</div>
              <div class="node">Agent → Tool Call</div>
              <div class="arrow">↓</div>
              <div class="node core" style="text-align:center;">
                <strong>AgentGuard</strong>
                Jev (choice · score · noul)<br/>Policy · Executor
              </div>
              <div class="arrow">↓</div>
              <div class="outcomes">
                <div class="out ok">Execute</div>
                <div class="out warn">Confirm</div>
                <div class="out bad">Block</div>
              </div>
            </div>
            <div>
              <p class="lp-arch-note">
                Module boundaries keep proposal, typed evaluation, deterministic policy,
                and sandboxed execution separate — Jev never runs tools.
              </p>
              <div class="lp-chips">
                <span class="lp-chip">Python</span>
                <span class="lp-chip">Streamlit</span>
                <span class="lp-chip">Jev</span>
                <span class="lp-chip">Pydantic</span>
                <span class="lp-chip">pytest</span>
                <span class="lp-chip">uv</span>
              </div>
            </div>
          </div>
        </div>
        """
    )

    # ── Tool isolation ─────────────────────────────────
    _html(
        """
        <div class="lp-section">
          <p class="lp-kicker">Tool isolation</p>
          <h2>Designed for a safe demonstration</h2>
          <p class="lp-intro">
            AgentGuard does not execute arbitrary shell commands.
            The playground uses controlled demo tools so the architecture can be
            explored without creating an arbitrary command-execution surface.
          </p>
          <div class="lp-chips">
            <span class="lp-chip">read_file</span>
            <span class="lp-chip">list_files</span>
            <span class="lp-chip">create_note</span>
            <span class="lp-chip">delete_demo_file</span>
            <span class="lp-chip">send_notification</span>
            <span class="lp-chip">execute_demo_task</span>
          </div>
          <p style="margin-top:1rem;">
            Paths stay inside <span class="lp-mono">demo/workspace</span>.
            External side effects are simulated.
          </p>
        </div>
        """
    )

    # ── Evaluation ─────────────────────────────────────
    _html(
        """
        <div class="lp-section">
          <p class="lp-kicker">Evaluation</p>
          <h2>Does the gateway behave as intended?</h2>
          <p class="lp-intro">
            A controlled scenario set in
            <span class="lp-mono">tests/evaluation/scenarios.json</span>
            covers gateway behavior. It is not a security certification.
          </p>
          <div class="lp-chips">
            <span class="lp-chip">Safe actions</span>
            <span class="lp-chip">Destructive actions</span>
            <span class="lp-chip">External side effects</span>
            <span class="lp-chip">Ambiguous actions</span>
            <span class="lp-chip">Sensitive operations</span>
            <span class="lp-chip">Reversible / irreversible</span>
          </div>
          <p style="margin-top:1rem;">
            Metric focus: <strong>false allow rate</strong> — plus confirmation rate and
            decision latency where measured in tests. Numerical production claims are
            intentionally omitted here; see the evaluation dataset and unit tests.
          </p>
        </div>
        """
    )

    # ── Limitations ────────────────────────────────────
    _html(
        """
        <div class="lp-section lp-section-quiet">
          <p class="lp-kicker">Limitations</p>
          <h2>What this project is — and isn’t</h2>
          <div class="lp-two">
            <div class="panel">
              <h3>It is</h3>
              <ul>
                <li>An exploration of typed AI decisions as a control layer around agent tool execution</li>
                <li>A working gateway with audit traces and policy outcomes</li>
                <li>A safe sandbox for demonstrating the pattern</li>
              </ul>
            </div>
            <div class="panel">
              <h3>It is not</h3>
              <ul>
                <li>A production security boundary</li>
                <li>A replacement for authorization, sandboxing, or access control</li>
                <li>A guarantee that an AI-generated decision is correct</li>
              </ul>
            </div>
          </div>
        </div>
        """
    )

    # ── Playground CTA ─────────────────────────────────
    _html(
        """
        <div class="lp-section" id="playground-cta">
          <div class="lp-cta-band">
            <p class="lp-kicker">Interactive demo</p>
            <h2>See AgentGuard in action</h2>
            <p>
              You have seen how the decision layer works. Now try it —
              watch the pipeline evaluate requests in real time.
            </p>
            <div class="lp-cta-previews">
              <span>Read a file → Execute</span>
              <span>Create a note → Confirm</span>
              <span>Delete a file → Block</span>
            </div>
          </div>
        </div>
        """
    )
    cta_l, cta_c, cta_r = st.columns([1.35, 1.4, 1.35])
    with cta_c:
        if play is not None:
            _html('<span class="lp-cta-actions" hidden></span>')
            st.page_link(play, label="Open Playground →", width="stretch")

    # ── Footer ─────────────────────────────────────────
    _html(
        """
        <div class="lp-footer">
          <div>
            <strong>AgentGuard</strong>
            <p>
              AI Agent Safety Gateway — an experiment in typed decisions,
              agent safety, and deterministic policy.
            </p>
          </div>
          <div class="links">
            Built by Mohamad Mohamad
          </div>
        </div>
        """
    )
