"""
Օրենքը պարզ բառերով — "Explain Like I'm 15" law summarizer for Armenian law.

Run it:
    streamlit run app.py
"""
import json
from pathlib import Path

import streamlit as st

import llm

DATA = Path("data/laws.json")

st.set_page_config(page_title="Օրենքը պարզ բառերով", page_icon="⚖️", layout="wide")


@st.cache_data
def load_laws():
    return json.loads(DATA.read_text(encoding="utf-8"))


# Cache LLM calls per (function, article text, model) so re-clicks are instant
# and we don't burn tokens during the demo.
@st.cache_data(show_spinner=False)
def cached_explain(text, model):
    return llm.explain(text, model=model)


@st.cache_data(show_spinner=False)
def cached_example(text, model):
    return llm.real_life_example(text, model=model)


@st.cache_data(show_spinner=False)
def cached_quiz(text, model):
    return llm.quiz(text, model=model)


laws = load_laws()

# ---- Header ---------------------------------------------------------------
st.title("⚖️ Օրենքը պարզ բառերով")
st.caption("Հայկական օրենքը՝ պարզ, մարդկային լեզվով — 15 տարեկանի համար հասկանալի:")

# ---- Sidebar: pick a law and an article -----------------------------------
with st.sidebar:
    st.header("Ընտրիր")
    law_titles = {l["law_title"]: l for l in laws}
    law = law_titles[st.selectbox("Օրենք", list(law_titles.keys()))]

    articles = law["articles"]
    labels = [f'{a["article_no"]} — {a.get("heading", "")}'.strip(" —") for a in articles]
    idx = st.radio("Հոդված", range(len(articles)), format_func=lambda i: labels[i])
    article = articles[idx]

    st.divider()
    show_example = st.toggle("Ցույց տալ առօրյա օրինակ", value=True)
    show_quiz = st.toggle("Ստուգիր ինձ (քվիզ)", value=False)
    model = st.text_input("Մոդել (Groq)", value=llm.DEFAULT_MODEL)
    if law.get("pdf_link"):
        st.markdown(f'[📄 Բնօրինակ ARLIS-ում]({law["pdf_link"]})')

# ---- Main: original vs plain-language, side by side -----------------------
left, right = st.columns(2, gap="large")

with left:
    st.subheader("📜 Բնօրինակ տեքստ")
    st.markdown(f"**{article['article_no']}**")
    st.write(article["text"])

with right:
    st.subheader("💬 Պարզ բացատրություն")
    go = st.button("✨ Բացատրիր պարզ հայերենով", type="primary", use_container_width=True)

    if go:
        try:
            with st.spinner("Բացատրում եմ..."):
                st.success(cached_explain(article["text"], model))

            if show_example:
                with st.spinner("Օրինակ եմ բերում..."):
                    st.info(cached_example(article["text"], model))

            if show_quiz:
                with st.spinner("Հարց եմ կազմում..."):
                    st.warning(cached_quiz(article["text"], model))
        except Exception as e:
            st.error(f"Սխալ: {e}")
            st.caption("Ստուգիր, որ .env-ում կա ճիշտ GROQ_API_KEY, և մոդելը հասանելի է "
                       "(`python check_models.py`):")
    else:
        st.write("Սեղմիր կոճակը՝ ձախ կողմի հոդվածը պարզ լեզվով բացատրելու համար: 👈")
