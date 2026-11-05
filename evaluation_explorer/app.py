"""AI Architecture Evaluation Explorer — immutable saved-result viewer.

No network calls, model inference, credentials, new grading, or live legal advice.
All Q1–Q10 answers are bundled from the two publicly released research tracks.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"
TRACK_A = "https://github.com/hyejeong0617/Regulatory_agent"
TRACK_B = "https://github.com/hyejeong0617/regulatory-investigation-agent"

BUILDS = {
    "Build 01": "Prompt-only baseline",
    "Build 02": "Static hybrid RAG",
    "Build 03-B": "Tools + targeted retrieval",
    "Build 04 v3": "Multi-step investigation",
    "Codex-built v1": "Separate Codex-led investigation",
}
SCORES = {
    "Build 01": (5, 0, 2),
    "Build 02": (5, 9, 2),
    "Build 03-B": (9, 6, 4),
    "Build 04 v3": (8, 10, 3),
    "Codex-built v1": (5, 8, 2),
}
# Only the Codex-built track has publicly available final individual ratings.
CODEX_GRADES = {
    "Q1": ("Yes", "Yes", "Yes"), "Q2": ("No", "Partial", "No"),
    "Q3": ("Yes", "Yes", "Yes"), "Q4": ("Partial", "Yes", "Partial"),
    "Q5": ("Partial", "Yes", "No"), "Q6": ("Yes", "Yes", "Partial"),
    "Q7": ("Yes", "Yes", "Partial"), "Q8": ("Yes", "Yes", "Partial"),
    "Q9": ("No", "No", "No"), "Q10": ("Partial", "Yes", "No"),
}
QUESTION_NOTES = {
    "Q1": "Compare which relevant EU legal instruments each approach identified.",
    "Q2": "Codex v1 rejected the 6 and 10 µg/kg numbers as accepted legal claims; the values remained in its unresolved-issues commentary.",
    "Q3": "Processing and sorting exceptions require careful interpretation of the dried-fig-specific provisions.",
    "Q4": "Codex v1 did not fully resolve Annex II hazard/check-frequency pairing.",
    "Q5": "Codex v1 left certificate, prior-notification and check-frequency conditions unresolved. Its Q5 result was retained from a development smoke test.",
    "Q6": "Compare the coverage of food-business-operator and competent-authority obligations.",
    "Q7": "Review how each answer distinguishes established facts from conditional corrective measures.",
    "Q8": "Historical legal snapshots are not proof of current requirements.",
    "Q9": "Codex v1 ended with incomplete execution; this is not evidence of incorrect legal reasoning.",
    "Q10": "Codex v1 did not completely synthesize the relevant border documentation and other conditions.",
}

st.set_page_config(
    page_title="AI Architecture Evaluation Explorer | Scientific AI Builder",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Deliberately scoped CSS and a light Streamlit theme. No generic "*"/"p,li,div"
# overrides: those caused unreadable native tabs, metrics and table widgets.
st.markdown(
    """
    <style>
    .stApp { background: #F5F8FB; }
    .block-container { max-width: 1510px; padding-top: 1.55rem; padding-bottom: 3.6rem; }
    [data-testid="stSidebar"] { background: #E8F0F5; border-right: 1px solid #D1DFE8; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] a { color: #223B50 !important; }
    [data-testid="stSidebar"] a { text-decoration: none; font-weight: 600; }
    [data-testid="stSidebar"] a:hover { color: #087E85 !important; text-decoration: underline; }
    [data-testid="stSidebar"] hr { border-color: #CDDAE3; }
    [data-testid="stMain"] h1, [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 { color: #16364E; }
    .hero { background: #FFF; border: 1px solid #DBE6ED; border-radius: 17px;
            padding: 1.4rem 1.65rem; box-shadow: 0 3px 14px rgba(25,55,79,.035); }
    .hero .eyebrow { font-size: .72rem; letter-spacing: .13em; font-weight: 800;
                     color: #0F8588; text-transform: uppercase; }
    .hero h1 { margin: .25rem 0 .52rem; font-size: clamp(1.5rem, 3vw, 2.12rem);
               font-weight: 790; color: #16364E; line-height: 1.2; }
    .hero p { margin: 0; color: #577084; font-size: .95rem; line-height: 1.55; }
    .kpi { background: white; border: 1px solid #DBE6ED; border-radius: 14px;
           padding: 1rem 1.2rem; min-height: 106px; }
    .kpi .label { font-size: .84rem; color: #526A7D; font-weight: 680; }
    .kpi .num { font-size: 2rem; font-weight: 790; color: #16364E; line-height: 1.35; }
    .kpi .detail { font-size: .78rem; color: #697D8F; }
    .scorewrap { background: white; border: 1px solid #DBE6ED; border-radius: 14px;
                 padding: 1.05rem 1.25rem; overflow-x: auto; }
    .scoregrid { display: grid; grid-template-columns: minmax(160px, 1.55fr)
                 repeat(3, minmax(100px, 1fr)); min-width: 545px;
                 align-items: center; gap: .7rem 1.05rem; }
    .scorehead { font-size: .78rem; font-weight: 750; color: #4C6477;
                 border-bottom: 1px solid #DFE8EE; padding: .1rem 0 .72rem; }
    .scorename { font-weight: 700; font-size: .9rem; color: #1B3A51; }
    .scorecell { font-size: .85rem; font-weight: 650; color: #2E4B61; }
    .barback { background: #E7EEF3; height: 7px; border-radius: 12px;
               margin-top: .34rem; overflow: hidden; }
    .barfill { background: #208C91; height: 100%; border-radius: 12px; }
    .tagline { color: #527087; font-size: .83rem; }
    .grade { padding: .22rem .6rem; border-radius: 99px; font-size: .76rem;
             font-weight: 740; display: inline-block; margin: .15rem .3rem .2rem 0; }
    .grade-yes { background: #E5F5ED; color: #176B45; }
    .grade-no { background: #FCEDEC; color: #A34441; }
    .grade-partial { background: #FFF2D9; color: #895D0C; }
    .grade-none { background: #ECF1F5; color: #576E81; }
    .statusnote { padding: .58rem .82rem; background: #EEF5F8;
                  border-left: 3px solid #238B90; color: #36586C;
                  border-radius: 5px; font-size: .85rem; margin-bottom: .65rem; }
    .stButton > button, [data-testid="stLinkButton"] a { border-radius: 9px; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color: #DBE6ED; border-radius: 13px; }
    [data-testid="stRadio"] [role="radiogroup"] { gap: .55rem; }
    [data-testid="stRadio"] label { border-radius: 8px; }
    [data-testid="stAlert"] { border-radius: 10px; }

    /* Contrast guard: Streamlit deployment can retain a dark text theme even
       when the page background is light. Scope overrides to the main content. */
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        color: #213A50 !important;
        background-color: #F5F8FB;
    }
    [data-testid="stMain"] [data-testid="stMarkdownContainer"],
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] em,
    [data-testid="stMain"] [data-testid="stText"],
    [data-testid="stMain"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
    [data-testid="stMain"] [data-testid="stHeading"] {
        color: #213A50 !important;
    }
    [data-testid="stMain"] [data-testid="stCaptionContainer"] p {
        color: #546B7D !important;
    }
    /* Navigation radio: visible labeled cards, not anonymous colored dots. */
    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: stretch;
        gap: .55rem !important;
        margin: .45rem 0 1rem;
    }
    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label {
        display: inline-flex !important;
        align-items: center;
        min-height: 2.55rem;
        background: #FFFFFF;
        border: 1px solid #C9D9E4;
        border-radius: 10px !important;
        padding: .44rem .8rem;
        cursor: pointer;
    }
    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
        background: #DFF2F1;
        border-color: #13858B;
        box-shadow: inset 0 0 0 1px #13858B;
    }
    [data-testid="stMain"] [data-testid="stRadio"] label p,
    [data-testid="stMain"] [data-testid="stRadio"] label span,
    [data-testid="stMain"] [data-testid="stRadio"] label div,
    [data-testid="stMain"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #183B53 !important;
        font-weight: 650 !important;
        opacity: 1 !important;
    }
    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p {
        color: #086F73 !important;
    }
    /* Text-entry labels, selectors and multi-select tags must retain contrast. */
    [data-testid="stMain"] [data-baseweb="select"] > div,
    [data-testid="stMain"] [data-baseweb="select"] [role="combobox"],
    [data-testid="stMain"] [data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        color: #20384E !important;
        border-color: #CADAE5 !important;
    }
    [data-testid="stMain"] [data-baseweb="select"] input,
    [data-testid="stMain"] [data-baseweb="select"] span,
    [data-testid="stMain"] [data-baseweb="select"] div,
    [data-testid="stMain"] [data-baseweb="input"] input {
        color: #20384E !important;
        -webkit-text-fill-color: #20384E !important;
    }
    [data-testid="stMain"] [data-baseweb="tag"] {
        background-color: #DCF2F0 !important;
        color: #145E63 !important;
    }
    [data-testid="stMain"] [data-baseweb="tag"] span {
        color: #145E63 !important;
        -webkit-text-fill-color: #145E63 !important;
    }
    [data-testid="stMain"] [data-testid="stExpander"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        color: #213A50 !important;
    }
    [data-testid="stMain"] [data-testid="stExpander"] summary,
    [data-testid="stMain"] [data-testid="stExpander"] summary p,
    [data-testid="stMain"] [data-testid="stExpander"] summary span {
        color: #213A50 !important;
    }
    [data-testid="stMain"] a:not([data-testid="stLinkButton"] a) {
        color: #087984 !important;
    }
    [data-testid="stMain"] [data-testid="stLinkButton"] a {
        background: #FFFFFF !important;
        color: #106B75 !important;
        border: 1px solid #B9D2DC !important;
    }
    [data-testid="stMain"] [data-testid="stAlert"] p {
        color: #25475B !important;
    }
    @media (max-width: 760px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .hero { padding: 1.05rem 1.15rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def read_question(qid: str) -> dict:
    """Read bundled, fixed public results. The app never fetches from GitHub at runtime."""
    if qid not in [f"Q{i}" for i in range(1, 11)]:
        raise ValueError("Unrecognized benchmark question")
    path = DATA_DIR / f"{qid}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("qid") != qid or not isinstance(data.get("builds"), dict):
        raise ValueError(f"Malformed bundled {qid} record")
    return data


def grade_badge(label: str, value: str) -> str:
    klass = value.lower() if value in ("Yes", "No", "Partial") else "none"
    return '<span class="grade grade-' + klass + '">' + html.escape(label) + ": " + html.escape(value) + "</span>"


def kpi(label: str, number: str, detail: str) -> None:
    st.markdown(
        '<div class="kpi"><div class="label">' + html.escape(label)
        + '</div><div class="num">' + html.escape(number)
        + '</div><div class="detail">' + html.escape(detail) + "</div></div>",
        unsafe_allow_html=True,
    )


def scoring_table() -> None:
    items = ['<div class="scorewrap"><div class="scoregrid">',
             '<div class="scorehead">Implementation</div>',
             '<div class="scorehead">Correct</div>',
             '<div class="scorehead">Grounded</div>',
             '<div class="scorehead">Complete</div>']
    for build, counts in SCORES.items():
        items.append('<div class="scorename">' + html.escape(build) + "</div>")
        for val in counts:
            items.append(
                '<div class="scorecell">' + str(val) + ' / 10'
                + '<div class="barback"><div class="barfill" style="width:'
                + str(val * 10) + '%"></div></div></div>'
            )
    items.append("</div></div>")
    st.markdown("".join(items), unsafe_allow_html=True)


def evidence_list(records: list, build: str) -> None:
    if not records:
        if build == "Build 01":
            st.info("Prompt-only: no retrieval evidence was used.")
        else:
            st.info("Expanded evidence snippets are not included in this bundled result. Original answer citation markers are retained.")
        return
    st.caption(
        f"{len(records)} selected evidence snippets from the original run. "
        "These are retrieved excerpts, not independently verified accepted legal claims."
    )
    for index, row in enumerate(records):
        title = str(row.get("regulation") or "Legal source")
        where = str(row.get("location") or row.get("id") or f"Item {index + 1}")
        with st.expander(f"{title} · {where}"[:155]):
            st.write(row.get("text") or "(No snippet text stored.)")
            url = row.get("url") or ""
            if url.startswith("https://"):
                st.link_button("Historical legal source", url)


def show_answer(build: str, data: dict, qid: str) -> None:
    item = data.get("builds", {}).get(build)
    with st.container(border=True):
        st.subheader(build)
        st.caption(BUILDS[build])
        if not isinstance(item, dict):
            st.error(f"The stored {build} record is missing for {qid}.")
            return
        status = str(item.get("status", "unknown"))
        if build == "Codex-built v1" and status == "incomplete":
            st.warning("Execution incomplete: this is not a completed regulatory answer.")
        else:
            st.markdown(
                '<div class="statusnote">Saved execution status: '
                + html.escape(status) + "</div>",
                unsafe_allow_html=True,
            )
        if build == "Codex-built v1":
            grades = CODEX_GRADES[qid]
            st.markdown(
                grade_badge("Correct", grades[0])
                + grade_badge("Grounded", grades[1])
                + grade_badge("Complete", grades[2]),
                unsafe_allow_html=True,
            )
            st.caption("Owner-confirmed assessment of AI-assisted ratings; not externally validated.")
        else:
            st.caption("Individual final Track A grades are not fully public. Aggregate Yes-only counts are on Overview.")

        st.markdown("**Original recorded response**")
        answer = item.get("answer")
        if isinstance(answer, str) and answer.strip():
            st.markdown(answer)
        else:
            st.info("No completed response available in the archived record.")

        source = item.get("url", "")
        if isinstance(source, str) and source.startswith("https://github.com/"):
            st.link_button("View original frozen record on GitHub", source)

        with st.expander("Retrieved legal excerpts"):
            evidence_list(item.get("evidence") or [], build)
        with st.expander("Recorded execution information"):
            st.json({"status": status, "metrics": item.get("metrics") or {}, "original_source": source})


with st.sidebar:
    st.markdown("### 🔬 Scientific AI Builder")
    st.caption("Project 003 · Research portfolio")
    st.divider()
    st.markdown("**Case study**")
    st.write("Türkiye · Dried figs · Aflatoxin B1")
    st.markdown("**Study design**")
    st.write("One case · 10 related questions · 5 implementations")
    st.divider()
    st.markdown("**Research sources**")
    st.markdown(f"[Track A · Architecture lab]({TRACK_A})")
    st.markdown(f"[Track B · Codex-built v1]({TRACK_B})")
    st.markdown(f"[Full comparison]({TRACK_A}/blob/main/docs/PROJECT003_COMPARISON.md)")
    st.divider()
    st.caption("Historical evidence only. No live inference or legal advice.")

st.markdown(
    '<section class="hero"><div class="eyebrow">Food Safety × Applied AI · Interactive Research</div>'
    '<h1>AI Architecture Evaluation Explorer</h1>'
    '<p>Compare original saved answers across prompt-only LLM, hybrid RAG, targeted tools, '
    'multi-step investigation and an independent Codex-built agent.</p></section>',
    unsafe_allow_html=True,
)
st.write("")
st.caption("Historical, read-only research viewer · No API key · No new model calls · Not a current-law compliance service")

page = st.radio(
    "Explore",
    ["Overview & findings", "Compare original answers", "Evidence & limitations"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "Overview & findings":
    st.subheader("Five architectures · Frozen evaluation")
    st.markdown(
        "Only **Yes** ratings are counted. Each dimension is scored separately; "
        "a better source-grounding score does not necessarily indicate greater answer quality."
    )
    scoring_table()
    st.write("")
    a, b, c = st.columns(3)
    with a:
        kpi("Case studies", "1", "One Türkiye dried-fig case")
    with b:
        kpi("Benchmark questions", "10", "Related, not independent")
    with c:
        kpi("Implementations", "5", "Four Track A + one Track B")

    st.info(
        "Track A scores are historical owner-reviewed aggregates; public grading worksheets "
        "do not reproduce all question-level final judgments. Track B individual ratings "
        "were AI-assisted and owner-confirmed on 2026-10-23, not externally validated."
    )
    st.subheader("From RASFF evidence to regulatory AI", divider="gray")
    st.markdown(
        "**RASFF EDA (2020–2025)** → three regulatory case candidates → "
        "**Türkiye dried figs / aflatoxin B1** → ten questions → architecture evaluation."
    )
    st.markdown(
        "The [public RASFF analysis artifacts]"
        "(https://github.com/hyejeong0617/rasff_risk_predictor/tree/main/RASFF_Rebuild/artifacts) "
        "were used to **identify a case**, not for LLM training, runtime retrieval or legal grading. "
        "Notification counts are not population risk or incident rates."
    )
    st.subheader("Key observations", divider="gray")
    st.markdown(
        "- Greater grounding did **not consistently** increase correctness or completeness.\n"
        "- Exact-quotation checks, complex Annex interpretation and issue coverage can fail independently.\n"
        "- An incomplete workflow (Codex Q9) demonstrates execution reliability limits, not proven legal reasoning error."
    )

elif page == "Compare original answers":
    st.subheader("Compare original answers")
    try:
        options = {f"Q{i}": read_question(f"Q{i}")["question"] for i in range(1, 11)}
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as err:
        st.error("Saved local benchmark files could not be read. Please check the deployed repository bundle.")
        st.code(str(err))
        st.stop()

    qid = st.selectbox(
        "Select benchmark question",
        list(options),
        format_func=lambda value: f"{value} · {options[value]}",
    )
    st.markdown("**Question**")
    st.write(options[qid])
    chosen = st.multiselect(
        "Implementations",
        list(BUILDS),
        default=list(BUILDS),
        help="Select one or more frozen runs; no new AI response is generated.",
    )
    view = st.radio(
        "Answer layout",
        ["Single-column reading", "Two-column comparison"],
        horizontal=True,
    )
    st.caption(
        "Each card contains the original stored response, source link, selected evidence "
        "and execution information. The answer text is not regenerated."
    )
    try:
        record = read_question(qid)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as err:
        st.error(f"The bundled record for {qid} cannot be opened.")
        st.code(str(err))
        st.stop()

    if not chosen:
        st.info("Select at least one implementation to compare.")
    elif view == "Single-column reading":
        for build in chosen:
            show_answer(build, record, qid)
    else:
        for start in range(0, len(chosen), 2):
            columns = st.columns(2, gap="medium")
            for index, build in enumerate(chosen[start:start + 2]):
                with columns[index]:
                    show_answer(build, record, qid)

    st.subheader(f"Research note · {qid}", divider="gray")
    st.info(QUESTION_NOTES[qid])
    st.caption("Interpretive notes are sourced from existing project evaluations; not fresh grading across all five runs.")

else:
    st.subheader("Evidence provenance and research boundaries")
    st.markdown(
        "**Source preservation:** Q1–Q10 answer texts and selected evidence excerpts are bundled "
        "from the two public frozen GitHub revisions. Each answer card links to its full "
        "original record. Build 01 and 02 originated in one generation JSONL; Builds 03 "
        "and 04 and Codex v1 originated in question-level JSON files."
    )
    st.markdown(
        "**Evidence display:** Build 01 did not retrieve sources. Build 02's archived answers "
        "include citation markers but the expanded supporting evidence is not stored in the "
        "same JSONL record. Build 03, Build 04 and Codex preserved different kinds of "
        "retrieved legal excerpts. The app shows selected excerpts, not all tool logs."
    )
    st.markdown(
        "**Scores:** Track A public worksheets do not fully reconstruct its historical "
        "owner-reviewed individual ratings. The detailed legal reference remains private. "
        "Track B's initial AI-assisted question-level labels were confirmed by the owner "
        "but not independently externally validated. Workflow states (e.g., incomplete) "
        "and regulatory-answer grades are distinct."
    )
    st.markdown(
        "**Scientific constraints:** One development-exposed case with ten related questions; "
        "historical EUR-Lex snapshots; unequal development conditions, prompts and budgets; "
        "no prospective legal-validity or real-world regulatory-compliance assessment."
    )
    st.markdown(
        "**Future extensions (not implemented):** independently selected unseen cases "
        "(Extension B) and a standardized multi-case benchmark with reproducible "
        "question-level adjudication (Extension C)."
    )
    st.markdown(
        f"[Track A evaluation]({TRACK_A}/blob/main/docs/EVALUATION.md) · "
        f"[Track B evaluation]({TRACK_B}/blob/main/docs/QUALITY_EVALUATION.md) · "
        f"[Shared methodology]({TRACK_A}/blob/main/docs/PROJECT003_COMPARISON.md)"
    )
