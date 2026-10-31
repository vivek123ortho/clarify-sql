import pandas as pd
import streamlit as st

from ambiguity import check_ambiguity
from clarify import generate_clarifications
from text_to_sql import generate_sql, generate_sql_with_choices, run_sql

st.set_page_config(page_title="Clarify SQL", page_icon="🔎")
st.title("🔎 Clarify SQL")
st.caption("Ask a question about the shop database. If it's ambiguous, I'll ask.")

# Session state: survives reruns caused by button clicks
defaults = {"stage": "ask", "question": "", "check": None, "cset": None, "result": None}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


def reset():
    for key, value in defaults.items():
        st.session_state[key] = value


def show_results(result):
    st.subheader("Generated SQL")
    st.code(result.sql, language="sql")
    st.caption(result.explanation)
    try:
        cols, rows = run_sql(result.sql)
        df = pd.DataFrame(rows, columns=list(cols))
        st.subheader("Results")
        if df.empty:
            st.info("No rows returned.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"The query could not be run: {e}")
    st.button("Ask another question", on_click=reset)


# Stage 1: ask
if st.session_state.stage == "ask":
    q = st.text_input("Your question", placeholder="Who is the top customer?")
    if st.button("Ask") and q.strip():
        st.session_state.question = q.strip()
        with st.spinner("Checking the question..."):
            check = check_ambiguity(q.strip())
            st.session_state.check = check
            if check.is_ambiguous:
                st.session_state.cset = generate_clarifications(
                    q.strip(), check.ambiguous_terms, check.reason
                )
                st.session_state.stage = "clarify"
            else:
                st.session_state.result = generate_sql(q.strip())
                st.session_state.stage = "done"
        st.rerun()

# Stage 2: clarify
elif st.session_state.stage == "clarify":
    st.write(f"**Your question:** {st.session_state.question}")
    st.warning(f"This is ambiguous: {st.session_state.check.reason}")

    picks = []
    for i, cq in enumerate(st.session_state.cset.questions[:3]):
        labels = [o.label for o in cq.options]
        choice = st.radio(cq.question, labels, index=None, key=f"q{i}")
        picks.append((choice, cq))

    all_answered = all(choice is not None for choice, _ in picks)
    if st.button("Get answer", disabled=not all_answered):
        hints = [
            next(o.sql_hint for o in cq.options if o.label == choice)
            for choice, cq in picks
        ]
        with st.spinner("Writing the query..."):
            st.session_state.result = generate_sql_with_choices(
                st.session_state.question, hints
            )
        st.session_state.stage = "done"
        st.rerun()
    st.button("Start over", on_click=reset)

# Stage 3: done
elif st.session_state.stage == "done":
    st.write(f"**Your question:** {st.session_state.question}")
    show_results(st.session_state.result)