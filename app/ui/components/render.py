"""AgentGuard execution-console UI."""

from __future__ import annotations

import html
import json
import textwrap

import streamlit as st

from app.agent.scenarios import SCENARIOS
from app.guard.models import AgentRun, PolicyOutcome

_EVENT_LABELS: dict[str, str] = {
    "request_received": "Request received",
    "tool_proposed": "Tool proposed",
    "arguments_validated": "Arguments validated",
    "decision_received": "Jev decision",
    "decision_made": "Policy decision",
    "awaiting_human_approval": "Awaiting approval",
    "approved": "Human approved",
    "rejected": "Human rejected",
    "executed": "Tool executed",
    "execution_failed": "Tool failed",
    "execution_prevented": "Execution prevented",
    "evaluation_failed": "Jev evaluation failed",
}


def _html(markup: str) -> None:
    """Render HTML without Streamlit treating indented lines as code fences."""
    cleaned = textwrap.dedent(markup).strip()
    cleaned = "\n".join(line.lstrip() for line in cleaned.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def _sec(label: str, *, first: bool = False) -> None:
    cls = "ag-section-first" if first else "ag-section"
    _html(f'<p class="ag-kicker {cls}">{html.escape(label)}</p>')


def _short_reason(text: str) -> str:
    """Keep agent reasoning concise in the console."""
    t = (text or "").strip()
    if not t:
        return "Selected to satisfy the user's request."
    replacements = (
        ("The agent selected ", "Selected "),
        (" because the user asked to read project notes.", " to satisfy the user's request."),
        (" to store the requested note in the sandbox.", "."),
        (" because the user requested report removal.", "."),
        (" for an external side-effect demo.", "."),
        (" for a predefined cleanup simulation.", "."),
        (" to update demo config.", "."),
        (" to show the demo workspace.", "."),
    )
    for old, new in replacements:
        t = t.replace(old, new)
    return t


def render_header(*, demo_mode: bool, jev_model: str) -> None:
    """Legacy product header (unused by multipage entry; kept for reuse)."""
    jev_status = (
        '<span class="ag-stat warn"><i></i>DEMO MODE</span>'
        if demo_mode
        else '<span class="ag-stat"><i></i>Jev Connected</span>'
    )
    _html(
        f"""
        <div class="ag-top">
          <div>
            <h1>AgentGuard</h1>
            <p class="sub">AI Agent Safety Gateway</p>
          </div>
          <div class="ag-top-right">
            <span class="ag-stat"><i></i>Agent Ready</span>
            {jev_status}
            <span class="ag-stat"><i></i>Policy Active</span>
            <span class="ag-stat muted">{html.escape(jev_model)}</span>
          </div>
        </div>
        """
    )


def render_playground_header(
    *,
    demo_mode: bool,
    jev_model: str,
    home_page: object | None = None,
) -> None:
    """Playground chrome with return link to the landing page."""
    jev_status = (
        '<span class="ag-stat warn"><i></i>DEMO MODE</span>'
        if demo_mode
        else '<span class="ag-stat"><i></i>Jev Connected</span>'
    )
    top_l, top_r = st.columns([1.4, 2], gap="medium")
    with top_l:
        if home_page is not None:
            st.page_link(home_page, label="← AgentGuard", width="content")
        _html('<p class="sub" style="margin:0.15rem 0 0;">Interactive Playground</p>')
    with top_r:
        _html(
            f"""
            <div class="ag-top-right" style="padding-top:0.45rem;">
              <span class="ag-stat"><i></i>Agent Ready</span>
              {jev_status}
              <span class="ag-stat"><i></i>Policy Active</span>
              <span class="ag-stat muted">{html.escape(jev_model)}</span>
            </div>
            """
        )
    _html('<div style="border-bottom:1px solid var(--border);margin:0.65rem 0 1.1rem;"></div>')


def render_composer() -> tuple[str | None, bool]:
    _html('<p class="ag-kicker">Evaluate an agent action</p>')
    _html('<p class="ag-title">Tell the agent what to do</p>')

    if "request_draft" not in st.session_state:
        st.session_state.request_draft = "Read the project notes."

    st.text_area(
        "Request",
        key="request_draft",
        height=72,
        label_visibility="collapsed",
        placeholder="Run the deployment cleanup.",
    )

    run = st.button("Run Agent", type="primary")

    _html('<p class="ag-composer-label">Try an example</p>')
    labels = [str(s["label"]) for s in SCENARIOS]
    choice = st.pills(
        "Examples",
        labels,
        selection_mode="single",
        key="scenario_pills",
        label_visibility="collapsed",
        width="content",
        wrap=True,
    )

    if choice and st.session_state.get("_scenario_fired") != choice:
        st.session_state._scenario_fired = choice
        for scenario in SCENARIOS:
            if scenario["label"] == choice:
                return str(scenario["request"]), True

    if run:
        return (st.session_state.request_draft or "").strip() or None, True
    return None, False


def render_run(run: AgentRun) -> None:
    if run.error and run.tool_call is None:
        st.error(run.error)
        return

    _render_evaluation(run)

    if run.policy_decision:
        _render_authorization(run)

    _sec("Execution flow")
    _render_pipeline(run)

    _render_result(run)

    if run.error:
        st.error(run.error)

    _sec("Execution trace")
    _render_trace(run)
    _render_metrics(run)


def _render_evaluation(run: AgentRun) -> None:
    _sec("Evaluation", first=True)

    left = _proposal_html(run)
    right = _jev_html(run)
    _html(
        f"""
        <div class="ag-eval">
          <div class="ag-eval-pane">
            <p class="ag-kicker">Agent proposal</p>
            {left}
          </div>
          <div class="ag-eval-pane">
            <p class="ag-kicker">Jev decision</p>
            {right}
          </div>
        </div>
        """
    )


def _proposal_html(run: AgentRun) -> str:
    if not run.tool_call:
        return '<p class="ag-reason">No tool call proposed.</p>'
    args = json.dumps(run.tool_call.arguments, indent=2)
    reason = _short_reason(run.tool_call.agent_reasoning_summary)
    return (
        f'<p class="ag-tool-name">{html.escape(run.tool_call.tool_name)}</p>'
        f'<pre class="ag-args">{html.escape(args)}</pre>'
        f'<p class="ag-reason">{html.escape(reason)}</p>'
    )


def _jev_html(run: AgentRun) -> str:
    j = run.jev_decision
    if j is None:
        return '<p class="ag-reason">Waiting for evaluation.</p>'

    risk_label, risk_cls, fill = _risk_visual(j.risk_score)
    conf = f"{j.action_type_confidence * 100:.0f}%" if j.action_type_confidence else "—"
    demo = (
        '<p class="ag-demo-note">DEMO MODE — deterministic mock signals, not live Jev.</p>'
        if j.demo_mode
        else ""
    )
    return f"""
      <div class="ag-jev-stack">
        <div class="ag-signal">
          <div class="k">Action type</div>
          <div class="v action">{html.escape(j.action_type.value)}</div>
          <div class="d">confidence {html.escape(conf)}</div>
        </div>
        <div class="ag-signal">
          <div class="k">Risk</div>
          <div class="v emphasis">{j.risk_score:.1f} / 5</div>
          <div class="ag-bar {risk_cls}"><span style="width:{fill}%"></span></div>
          <div class="d">{html.escape(risk_label)}</div>
        </div>
        <div class="ag-signal">
          <div class="k">Safe to execute</div>
          <div class="v emphasis">{j.safe_probability * 100:.0f}%</div>
          <div class="d">noul · auto-approval suitability</div>
        </div>
      </div>
      {demo}
    """


def _risk_visual(score: float) -> tuple[str, str, int]:
    fill = int(max(0, min(100, (score / 5.0) * 100)))
    if score <= 2.0:
        return "LOW", "risk-low", fill
    if score <= 3.5:
        return "MODERATE", "risk-mid", fill
    return "HIGH", "risk-high", fill


def _render_authorization(run: AgentRun) -> None:
    """Policy decision + approval controls as one connected unit."""
    p = run.policy_decision
    j = run.jev_decision
    assert p is not None

    awaiting = (
        p.outcome == PolicyOutcome.REQUIRE_CONFIRMATION
        and run.human_decision is None
        and run.execution_result is None
    )
    approved_done = run.human_decision == "approved"
    rejected = run.human_decision == "rejected"

    css = {
        PolicyOutcome.EXECUTE: "execute",
        PolicyOutcome.REQUIRE_CONFIRMATION: "confirm",
        PolicyOutcome.BLOCK: "block",
    }[p.outcome]
    title = {
        PolicyOutcome.EXECUTE: "EXECUTE",
        PolicyOutcome.REQUIRE_CONFIRMATION: "APPROVAL REQUIRED",
        PolicyOutcome.BLOCK: "BLOCKED",
    }[p.outcome]

    if (
        run.execution_result
        and run.execution_result.executed
        and run.execution_result.success
        and p.outcome == PolicyOutcome.REQUIRE_CONFIRMATION
        and approved_done
    ):
        css = "execute"
        title = "EXECUTED"
    elif approved_done and p.outcome == PolicyOutcome.REQUIRE_CONFIRMATION:
        css = "execute"
        title = "EXECUTED"
    elif rejected:
        css = "block"
        title = "REJECTED"

    risk = f"{j.risk_score:.1f} / 5" if j else "—"
    safe = f"{j.safe_probability * 100:.0f}%" if j else "—"
    action = j.action_type.value if j else "—"

    _sec("Policy decision")

    footer = ""
    if approved_done:
        footer = """
          <div class="ag-approved-banner">
            <span class="mark">✓ APPROVED</span>
            <span class="txt">Human approval received · tool executed</span>
          </div>
        """
    elif rejected:
        footer = """
          <div class="ag-approved-banner reject">
            <span class="mark">× REJECTED</span>
            <span class="txt">Operator rejected · tool not executed</span>
          </div>
        """
    elif awaiting:
        footer = """
          <div class="ag-approval">
            <p class="ag-kicker">Human approval</p>
            <p class="ag-title">This action will not execute until you approve it.</p>
            <p class="ag-lead">
                Jev signals inform the policy; AgentGuard owns the final policy decision.
            </p>
          </div>
        """

    _html(
        f"""
        <div class="ag-auth">
          <div class="ag-policy {css}">
            <div class="verdict-block">
              <p class="label">Final policy decision</p>
              <p class="verdict">{title}</p>
            </div>
            <div>
              <p class="why">{html.escape(p.reason)}</p>
              <div class="ag-policy-meta">
                <span>Risk {html.escape(risk)}</span>
                <span>Safe {html.escape(safe)}</span>
                <span>{html.escape(action)}</span>
                <span>policy v{html.escape(p.policy_version)}</span>
              </div>
            </div>
          </div>
          {footer}
        </div>
        """
    )

    if awaiting:
        c1, c2, _ = st.columns([1.15, 0.85, 2.5], gap="small")
        with c1:
            if st.button("Approve action", type="primary", use_container_width=True):
                st.session_state.pending_human = "approve"
                st.rerun()
        with c2:
            if st.button("Reject", use_container_width=True):
                st.session_state.pending_human = "reject"
                st.rerun()


def _render_pipeline(run: AgentRun) -> None:
    stages: list[tuple[str, str]] = [
        ("Agent", "ok"),
        ("Tool Call", "ok" if run.tool_call else "pending"),
        ("Jev", "ok" if run.jev_decision else "pending"),
        ("Policy", "ok" if run.policy_decision else "pending"),
    ]

    if run.policy_decision and run.policy_decision.outcome == PolicyOutcome.REQUIRE_CONFIRMATION:
        if run.human_decision == "approved":
            stages.append(("Approval", "ok"))
        elif run.human_decision == "rejected":
            stages.append(("Approval", "fail"))
        else:
            stages.append(("Approval", "warn"))

    if run.execution_result and run.execution_result.executed:
        stages.append(("Tool", "ok" if run.execution_result.success else "fail"))
    elif run.policy_decision and run.policy_decision.outcome == PolicyOutcome.BLOCK:
        stages.append(("Tool", "fail"))
    elif run.human_decision == "rejected":
        stages.append(("Tool", "fail"))
    elif run.policy_decision and run.policy_decision.outcome == PolicyOutcome.EXECUTE:
        stages.append(("Tool", "ok"))
    else:
        stages.append(("Tool", "pending"))

    marks = {"ok": "✓", "warn": "!", "fail": "×", "pending": "·"}
    parts: list[str] = []
    for name, state in stages:
        mark = marks[state]
        parts.append(
            f'<div class="ag-node {state}">'
            f'<span class="mark">{mark}</span>'
            f'<span class="name">{html.escape(name)}</span>'
            f"</div>"
        )
    _html(f'<div class="ag-pipe">{"".join(parts)}</div>')


def _render_result(run: AgentRun) -> None:
    if run.execution_result:
        _sec("Tool result")
        er = run.execution_result
        if er.executed and er.success:
            cls, status = "ok", "✓ Executed"
        elif er.executed:
            cls, status = "warn", "! Completed with errors"
        else:
            cls, status = "fail", "× Not executed"
        _html(
            f"""
            <div class="ag-result {cls}">
              <p class="status">{status}</p>
              <p class="msg">{html.escape(er.message)}</p>
            </div>
            """
        )
        if er.output is not None:
            if st.checkbox("Show raw output", value=False, key=f"raw_{run.run_id}"):
                st.json(er.output)
        return

    if run.policy_decision and run.policy_decision.outcome == PolicyOutcome.BLOCK:
        _sec("Tool result")
        _html(
            """
            <div class="ag-result fail">
              <p class="status">× Not executed</p>
              <p class="msg">AgentGuard policy prevented this tool from running.</p>
            </div>
            """
        )
        return

    if run.human_decision == "rejected":
        _sec("Tool result")
        _html(
            """
            <div class="ag-result fail">
              <p class="status">× Not executed</p>
              <p class="msg">Rejected by the operator.</p>
            </div>
            """
        )


def _render_trace(run: AgentRun) -> None:
    if not run.events:
        _html('<div class="ag-trace"><div class="ag-trace-empty">No events recorded.</div></div>')
        return

    rows: list[str] = [
        '<div class="ag-trace">',
        '<div class="ag-trace-head"><span>Time</span><span>Event</span><span>Duration</span></div>',
    ]
    for ev in run.events:
        ts = ev.timestamp.strftime("%H:%M:%S")
        label = _EVENT_LABELS.get(ev.event, ev.event.replace("_", " ").title())
        meta_bits: list[str] = []
        if ev.metadata:
            for key in (
                "tool",
                "outcome",
                "risk",
                "safe_probability",
                "action_type",
                "message",
                "reason",
            ):
                if key not in ev.metadata:
                    continue
                val = ev.metadata[key]
                if key == "safe_probability" and isinstance(val, (int, float)):
                    meta_bits.append(f"safe={val:.2f}")
                elif key == "risk" and isinstance(val, (int, float)):
                    meta_bits.append(f"risk={val:.1f}")
                elif key == "reason":
                    reason = str(val)
                    if len(reason) > 90:
                        reason = reason[:87] + "…"
                    meta_bits.append(f"reason={reason}")
                else:
                    meta_bits.append(f"{key}={val}")
        meta = " · ".join(meta_bits)
        dur = f"{ev.duration_ms:.0f} ms" if ev.duration_ms is not None else ""
        meta_html = (
            f'<div class="ag-trace-meta">{html.escape(meta)}</div>' if meta else ""
        )
        rows.append(
            f"""
            <div class="ag-trace-row">
              <div class="ag-trace-ts">{html.escape(ts)}</div>
              <div>
                <div class="ag-trace-event">{html.escape(label)}</div>
                {meta_html}
              </div>
              <div class="ag-trace-dur">{html.escape(dur)}</div>
            </div>
            """
        )
    rows.append("</div>")
    _html("".join(rows))


def _render_metrics(run: AgentRun) -> None:
    def fmt(v: float | None) -> str:
        if v is None:
            return "—"
        if v < 1:
            return "<1 ms"
        return f"{v:.0f} ms"

    _html(
        f"""
        <div class="ag-metrics">
          <span><strong>{html.escape(fmt(run.total_latency_ms))}</strong> total</span>
          <span><strong>{html.escape(fmt(run.jev_latency_ms))}</strong> Jev</span>
          <span><strong>{html.escape(fmt(run.policy_latency_ms))}</strong> policy</span>
          <span><strong>{html.escape(fmt(run.execution_latency_ms))}</strong> tool</span>
          <span class="run-id">run {html.escape(run.run_id)}</span>
        </div>
        """
    )
