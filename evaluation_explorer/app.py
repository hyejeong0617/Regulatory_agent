"""AI Architecture Evaluation Explorer — historical, read-only Project 003 demo.

Five implementations and ten related questions, using original public frozen
records. No generation, legal advice, hidden grading, or API credentials.
"""
from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st

A_REPO = "hyejeong0617/Regulatory_agent"
B_REPO = "hyejeong0617/regulatory-investigation-agent"
# Pin exact public revisions to preserve historical result identity.
A_REV = "db9803c2f0b8c39ccb6aa4dcd825eefd48c9c5ac"
B_REV = "73d4ce039183ec8d395cf8b6cd02613b01a668e6"
A_RAW = "https://raw.githubusercontent.com/" + A_REPO + "/" + A_REV + "/"
B_RAW = "https://raw.githubusercontent.com/" + B_REPO + "/" + B_REV + "/"
A_WEB = "https://github.com/" + A_REPO + "/blob/" + A_REV + "/"
B_WEB = "https://github.com/" + B_REPO + "/blob/" + B_REV + "/"

BUILD_NAMES = {
    "Build 01": "Prompt-only",
    "Build 02": "Static hybrid RAG",
    "Build 03-B": "Tools + targeted retrieval",
    "Build 04 v3": "Multi-step investigation",
    "Codex-built v1": "Independent Codex-led implementation",
}
COUNTS = {
    "Build 01": (5, 0, 2),
    "Build 02": (5, 9, 2),
    "Build 03-B": (9, 6, 4),
    "Build 04 v3": (8, 10, 3),
    "Codex-built v1": (5, 8, 2),
}
# These question-level labels are published only for Track B.
B_GRADES = {
    "Q1": ("Yes", "Yes", "Yes"),
    "Q2": ("No", "Partial", "No"),
    "Q3": ("Yes", "Yes", "Yes"),
    "Q4": ("Partial", "Yes", "Partial"),
    "Q5": ("Partial", "Yes", "No"),
    "Q6": ("Yes", "Yes", "Partial"),
    "Q7": ("Yes", "Yes", "Partial"),
    "Q8": ("Yes", "Yes", "Partial"),
    "Q9": ("No", "No", "No"),
    "Q10": ("Partial", "Yes", "No"),
}
B_SLUG = {
    "Q1": "32d833f3", "Q2": "8845886b", "Q3": "9fc58f1a",
    "Q4": "6866b007", "Q5": "a08c925f", "Q6": "f8bdff3f",
    "Q7": "0f27e1c3", "Q8": "6fbba5df", "Q9": "c7c58bd6",
    "Q10": "80548726",
}
FAILURES = {
    "Q1": "Compare how each architecture identifies relevant EU-law instruments.",
    "Q2": "Codex v1 rejected the 6/10 µg/kg numerical claims from accepted legal requirements, although the values appeared in unresolved commentary.",
    "Q3": "The handling of dried-fig sorting and processing conditions can differ across architectures.",
    "Q4": "Codex v1 identified import-control provisions but did not conclusively resolve Annex II hazard and check-frequency pairing.",
    "Q5": "Codex v1 did not settle the certificate, prior notification and applicable inspection-frequency requirements. Its retained run was development-exposed.",
    "Q6": "Compare the coverage of operator and competent-authority responsibilities.",
    "Q7": "Review how conditional non-compliance and regulatory actions were synthesized.",
    "Q8": "Distinguish historical legal snapshots from provisions requiring current verification.",
    "Q9": "Codex v1 ended with an incomplete execution. Its No/No/No outcome does not establish a legal-reasoning error.",
    "Q10": "Codex v1 lacked a fully supported synthesis of key import documentation and obligations.",
}

st.set_page_config(
    page_title="EU Regulatory Agent | Architecture Evaluation Explorer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    .stApp {background-color: #F7F9FC; color: #17253A;}
    .block-container {max-width: 1560px; padding-top: 1.6rem; padding-bottom: 4rem;}
    [data-testid="stSidebar"] {background: #13273C;}
    [data-testid="stSidebar"] * {color: #ECF3F7 !important;}
    [data-testid="stSidebar"] [data-baseweb="select"] * {color: #17253A !important;}
    .kicker {font-size: .75rem; font-weight: 750; letter-spacing: .13em; color: #287A82; text-transform: uppercase;}
    .hero {border: 1px solid #DCE5EB; border-radius: 18px; padding: 1.6rem 1.8rem; background: #FFF;}
    .hero h1 {font-size: 2rem; font-weight: 800; color: #17334C; margin: .28rem 0 .5rem;}
    .hero p {font-size: 1rem; color: #506679; margin: 0;}
    .subtle {font-size: .86rem; color: #647689;}
    div[data-testid="stMetric"] {background: #FFF; border: 1px solid #DFE7ED; padding: 1rem; border-radius: 13px;}
    div[data-testid="stVerticalBlockBorderWrapper"] {background: #FFF;}
    a {color: #167682;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600, show_spinner=False)
def get_text(url: str) -> str:
    """Read version-pinned public GitHub raw files; fail closed on HTTP errors."""
    response = requests.get(url, timeout=22, headers={"User-Agent": "Project003-Evaluation-Explorer/1.0"})
    response.raise_for_status()
    return response.text


@st.cache_data(ttl=3600, show_spinner=False)
def get_baselines() -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    path = "results/build01_02/nb04b_context_repaired_openai_luna_generation_results.jsonl"
    for line in get_text(A_RAW + path).splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        name = {"prompt_only": "Build 01", "rag": "Build 02"}.get(item.get("mode"))
        qid = item.get("qid")
        if name and qid:
            records[(qid, name)] = {
                "question": item.get("question", ""),
                "answer": item.get("answer", ""),
                "status": "Saved generation",
                "evidence": [],
                "metrics": {"input_tokens": item.get("input_tokens"),
                            "output_tokens": item.get("output_tokens")},
                "url": A_WEB + path,
                "notes": "Build 01 has no retrieval evidence." if name == "Build 01" else "Answer citation tags refer to retrieved source evidence; the frozen result record may not contain an expanded evidence trail.",
            }
    return records


@st.cache_data(ttl=3600, show_spinner=False)
def get_questions() -> list[dict[str, str]]:
    # Prefer the actual questions attached to canonical saved baseline outputs.
    baselines = get_baselines()
    questions = []
    for i in range(1, 11):
        qid = "Q" + str(i)
        record = baselines.get((qid, "Build 01"), baselines.get((qid, "Build 02"), {}))
        questions.append({"qid": qid, "question": record.get("question", "")})
    return questions


@st.cache_data(ttl=3600, show_spinner=False)
def get_build(qid: str, name: str) -> dict[str, Any]:
    if name in ("Build 01", "Build 02"):
        return get_baselines()[(qid, name)]
    if name == "Build 03-B":
        path = "results/build03/" + qid + ".json"
        rec = json.loads(get_text(A_RAW + path))
        evidence = []
        for call in rec.get("search_calls", []):
            for hit in call.get("results", []):
                evidence.append({
                    "id": hit.get("chunk_id", ""),
                    "regulation": hit.get("regulation_title", ""),
                    "location": hit.get("location", ""),
                    "text": hit.get("text", ""),
                    "url": "",
                })
        return {
            "question": rec.get("question", ""), "answer": rec.get("final_output", ""),
            "status": "Saved run (historic status: " + str(rec.get("status", "unknown")) + ")",
            "evidence": evidence, "metrics": {"search_calls": len(rec.get("search_calls", []))},
            "url": A_WEB + path,
            "notes": "Search results are retrieved evidence, not necessarily cited or accepted legal conclusions.",
        }
    if name == "Build 04 v3":
        path = "results/build04/" + qid + ".json"
        rec = json.loads(get_text(A_RAW + path))
        evidence = []
        for hit in rec.get("evidence", []):
            evidence.append({
                "id": hit.get("evidence_id", ""), "regulation": hit.get("regulation_id", ""),
                "location": hit.get("location", ""), "text": hit.get("text", ""),
                "url": hit.get("source_url", ""),
            })
        return {
            "question": rec.get("question", ""), "answer": rec.get("final_output", ""),
            "status": "Saved run (historic status: " + str(rec.get("status", "unknown")) + ")",
            "evidence": evidence,
            "metrics": {"llm_calls": rec.get("llm_calls"), "search_calls": rec.get("search_calls"),
                        "time_sec": rec.get("latency_seconds"),
                        "tokens": sum(int(rec.get("usage", {}).get(k) or 0) for k in ("input_tokens", "output_tokens"))},
            "url": A_WEB + path,
            "notes": "Evidence includes retrieved snippets; not every snippet necessarily supports the final answer.",
        }
    slug = B_SLUG[qid]
    path = "evaluation/v1/raw/" + qid + "/question-" + qid + "-" + slug + ".json"
    rec = json.loads(get_text(B_RAW + path))
    evidence = []
    for hit in rec.get("evidence", []):
        evidence.append({
            "id": hit.get("id", ""), "regulation": hit.get("regulation", ""),
            "location": hit.get("location", ""), "text": hit.get("text", ""),
            "url": "",
        })
    return {
        "question": rec.get("question", ""), "answer": rec.get("final_answer", ""),
        "status": str(rec.get("status", "unknown")).upper(),
        "evidence": evidence, "metrics": rec.get("metrics", {}),
        "url": B_WEB + path,
        "notes": "Workflow status (partial/incomplete) is separate from Correct/Grounded/Complete quality scores.",
    }


def safe_external_link(url: str) -> str:
    """Restrict rendering of arbitrary external URLs to source HTTP(S) links."""
    return url if isinstance(url, str) and re.match(r"^https://", url) else ""


def show_evidence(rec: dict[str, Any], prefix: str, max_items: int = 15) -> None:
    items = rec.get("evidence", [])
    if not items:
        st.info("No expanded evidence records in this saved output. See the original answer and source file.")
        return
    st.caption(str(len(items)) + " recorded retrieved evidence items. The first " + str(min(len(items), max_items)) + " are displayed; retrieval is not equivalent to legal validation.")
    for i, e in enumerate(items[:max_items]):
        label = str(e.get("regulation") or "Legal source") + " · " + str(e.get("location") or e.get("id") or ("item " + str(i + 1)))
        with st.expander(label[:160]):
            if e.get("text"):
                st.write(str(e["text"])[:3500])
            if safe_external_link(e.get("url", "")):
                st.link_button("Open historical source URL", e["url"], key=prefix + "_ev_" + str(i))


st.sidebar.markdown("### ⚖️ Scientific AI Builder")
st.sidebar.caption("Project 003 · Historical evaluation")
st.sidebar.markdown("---")
st.sidebar.markdown("**Scope**")
st.sidebar.write("One dried-fig/aflatoxin B1 regulatory case; ten related questions; five implementations.")
st.sidebar.markdown("**Provenance**")
st.sidebar.markdown("[Track A repository](https://github.com/hyejeong0617/Regulatory_agent)")
st.sidebar.markdown("[Track B repository](https://github.com/hyejeong0617/regulatory-investigation-agent)")
st.sidebar.markdown("[Evaluation methodology](https://github.com/hyejeong0617/Regulatory_agent/blob/main/docs/PROJECT003_COMPARISON.md)")
st.sidebar.markdown("---")
st.sidebar.caption("Research prototype · No model inference · Not legal advice")

st.markdown(
    '<div class="hero"><div class="kicker">Food Safety × Applied AI · Interactive Research</div>'
    '<h1>AI Architecture Evaluation Explorer</h1>'
    '<p>Explore original saved Q1–Q10 outputs from Prompt-only, Hybrid RAG, Tools, '
    'Investigation Agent and an independently Codex-built Agent.</p></div>',
    unsafe_allow_html=True,
)
st.write("")
st.info(
    "This app replays historical public research artifacts. It does not run an AI model, "
    "verify current EU law or produce new regulatory assessments. Scores are exploratory, "
    "and the ten questions belong to one case."
)

overview, compare, evidence_tab = st.tabs(["Overview & findings", "Compare original answers", "Evidence & limitations"])

with overview:
    st.subheader("Architecture comparison · Frozen Yes-only counts")
    frame = pd.DataFrame([
        {"Implementation": n, "Correct": vals[0], "Grounded": vals[1], "Complete": vals[2]}
        for n, vals in COUNTS.items()
    ]).set_index("Implementation")
    st.dataframe(frame, use_container_width=True, column_config={
        "Correct": st.column_config.ProgressColumn("Correct Yes / 10", min_value=0, max_value=10),
        "Grounded": st.column_config.ProgressColumn("Grounded Yes / 10", min_value=0, max_value=10),
        "Complete": st.column_config.ProgressColumn("Complete Yes / 10", min_value=0, max_value=10),
    })
    st.caption(
        "Correct, Grounded and Complete are separate owner-reviewed Yes/Partial/No dimensions. "
        "Only Yes is counted. Track A public worksheets do not reconstruct all final question-level grades; "
        "the detailed legal reference is private. Track B's AI-assisted ratings were owner-confirmed 2026-10-23, "
        "not independently externally validated."
    )
    a, b, c = st.columns(3)
    with a:
        st.metric("Cases", "1", help="One selected Türkiye dried-fig/aflatoxin B1 case.")
    with b:
        st.metric("Related questions", "10")
    with c:
        st.metric("Implementations", "5", help="Four Track A builds and one independent Track B implementation.")
    st.markdown("#### Research narrative")
    st.markdown(
        "**Historical RASFF EDA (2020–2025)** → three candidate scenarios → "
        "**Türkiye dried figs / aflatoxin B1** → ten fixed questions → five implementations."
    )
    st.markdown(
        "The original [RASFF candidate artifacts](https://github.com/hyejeong0617/rasff_risk_predictor/tree/main/RASFF_Rebuild/artifacts) "
        "informed **case selection**, not model training, runtime retrieval, or the legal reference. "
        "Case counts are notifications, not incidence or risk rates."
    )
    st.markdown("#### Key observations")
    st.markdown(
        "1. Greater source grounding did **not** consistently produce higher correctness or completeness.\n"
        "2. Exact-quote checking may reject useful but poorly traced claims; Annex-table interpretation "
        "and issue coverage remain distinct challenges.\n"
        "3. A stopped execution (Codex Q9) is a reliability problem, not proof of a legal-reasoning error."
    )

with compare:
    try:
        questions = get_questions()
        labels = {q["qid"]: q["qid"] + " · " + q["question"] for q in questions}
        selected_qid = st.selectbox("Benchmark question", list(labels), format_func=lambda x: labels[x], index=0)
        st.markdown("**Original question**")
        st.write(next(q["question"] for q in questions if q["qid"] == selected_qid))
        selected_builds = st.multiselect(
            "Implementations to compare", list(BUILD_NAMES), default=list(BUILD_NAMES),
        )
        if not selected_builds:
            st.warning("Select at least one implementation.")
        else:
            st.caption("Answer text is drawn from version-pinned public results. Expand the source evidence for supporting snippets.")
            for offset in range(0, len(selected_builds), 2):
                cols = st.columns(2)
                for i, name in enumerate(selected_builds[offset:offset + 2]):
                    with cols[i]:
                        with st.container(border=True):
                            st.markdown("#### " + name)
                            st.caption(BUILD_NAMES[name])
                            try:
                                rec = get_build(selected_qid, name)
                                status = rec.get("status", "Unknown")
                                if name == "Codex-built v1" and status == "INCOMPLETE":
                                    st.warning("Execution incomplete — not a completed legal answer.")
                                else:
                                    st.caption("Historical run status: " + status)
                                if name == "Codex-built v1":
                                    grades = B_GRADES[selected_qid]
                                    st.markdown(
                                        "**Question-level owner-confirmed grading:** "
                                        "Correct " + grades[0] + " · Grounded " + grades[1] +
                                        " · Complete " + grades[2]
                                    )
                                else:
                                    st.caption("Question-level final grading not fully published for Track A; see aggregate summary on Overview.")
                                answer = rec.get("answer", "")
                                st.markdown(answer if answer else "_No completed answer available in the frozen record._")
                                st.link_button("Open original saved output", rec["url"], use_container_width=True)
                                with st.expander("Retrieved evidence and source snippets"):
                                    show_evidence(rec, selected_qid + "_" + name.replace(" ", "_"))
                                with st.expander("Recorded execution metadata"):
                                    st.json({"status": status, "metrics": rec.get("metrics", {}),
                                             "source": rec["url"]})
                                    st.caption(rec.get("notes", ""))
                            except (requests.RequestException, ValueError, KeyError) as exc:
                                st.error("This source record could not be loaded. The app will not fabricate a replacement answer.")
                                st.caption(type(exc).__name__ + ": " + str(exc)[:180])
            st.markdown("#### Recorded interpretation for this question")
            st.info(FAILURES[selected_qid])
            st.caption("These failure notes are descriptive research annotations, not fresh question-level adjudications for all five builds.")
    except (requests.RequestException, ValueError, KeyError, StopIteration) as exc:
        st.error("Unable to load the canonical questions from GitHub. Check network access or try again later.")
        st.caption(type(exc).__name__ + ": " + str(exc)[:200])

with evidence_tab:
    st.subheader("Methods, evaluation provenance & known boundaries")
    st.markdown(
        "**Original records:** Track A Build 01/02 JSONL and Build 03/04 per-question JSON; "
        "Track B original per-question JSON. Source links within each card lead to immutable revisions."
    )
    st.markdown(
        "**Evidence display:** Build 01 has no retrieval. Build 02 answers include citation tokens, "
        "but expanded evidence links are not uniformly embedded in the saved baseline JSONL. "
        "Build 03/04 and Codex records preserve retrieved source snippets at differing levels of detail. "
        "An extracted snippet is not automatically a validated legal conclusion."
    )
    st.markdown(
        "**Scores:** Aggregate counts are historical owner-reviewed results; individual Track A "
        "final ratings cannot all be independently reconstructed from the published worksheets. "
        "Track B individual grading is published but its reference remains private. "
        "The comparison is exploratory, not an independently validated general benchmark."
    )
    st.markdown(
        "**Boundary conditions:** One case and ten related development-exposed questions; "
        "five historical EU-law snapshots; unequal prompts, development sequences and budgets; "
        "no verified current-law applicability or production compliance performance."
    )
    st.markdown(
        "**Further research (not implemented):** Unseen independent cases (Extension B); "
        "a larger standardized and independently adjudicated benchmark (Extension C)."
    )
    st.markdown(
        "[Track A evaluation](https://github.com/hyejeong0617/Regulatory_agent/blob/main/docs/EVALUATION.md) · "
        "[Track B quality evaluation](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md) · "
        "[Shared methodology](https://github.com/hyejeong0617/Regulatory_agent/blob/main/docs/PROJECT003_COMPARISON.md)"
    )
