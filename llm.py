"""
LLM layer for "Օրենքը պարզ բառերով".

All calls go to Groq. Each function takes the original Armenian legal text and
returns plain-Armenian output. Prompts are tuned to keep answers short, simple,
and grounded ONLY in the given article (no invented law).
"""
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


@lru_cache(maxsize=1)
def _client():
    """Create the Groq client once and reuse it."""
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY բացակայում է: Ստեղծիր .env ֆայլ և ավելացրու քո բանալին "
            "(տես .env.example):"
        )
    return Groq(api_key=api_key)


def _chat(system: str, user: str, *, model: str | None = None,
          temperature: float = 0.3, max_tokens: int = 500) -> str:
    resp = _client().chat.completions.create(
        model=model or DEFAULT_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# 1) Explain like I'm 15
# ---------------------------------------------------------------------------
_EXPLAIN_SYSTEM = (
    "Դու հայկական իրավաբանական տեքստը պարզ, մարդկային հայերենով բացատրող օգնական ես: "
    "Բացատրիր այնպես, կարծես խոսում ես 15 տարեկան դեռահասի հետ: "
    "Օգտագործիր միայն տրված հոդվածի բովանդակությունը, ոչինչ մի հորինիր: "
    "Խուսափիր իրավաբանական ժարգոնից: Պատասխանիր ՄԻԱՅՆ հայերենով:"
)

_EXPLAIN_USER = (
    "Ահա օրենքի հոդվածը.\n\n«{text}»\n\n"
    "Բացատրիր այն պարզ հայերենով, առավելագույնը 100 բառ: "
    "Հստակ նշիր, թե ինչ ԻՐԱՎՈՒՆՔ կամ ՊԱՐՏԱԿԱՆՈՒԹՅՈՒՆ է այս հոդվածը ստեղծում "
    "և ում համար:"
)


def explain(text: str, model: str | None = None) -> str:
    return _chat(_EXPLAIN_SYSTEM, _EXPLAIN_USER.format(text=text), model=model)


# ---------------------------------------------------------------------------
# 2) Real-life example
# ---------------------------------------------------------------------------
_EXAMPLE_SYSTEM = (
    "Դու իրավական հոդվածները առօրյա, կոնկրետ օրինակներով բացատրող օգնական ես: "
    "Պատասխանիր միայն հայերենով, պարզ լեզվով:"
)

_EXAMPLE_USER = (
    "Ահա օրենքի հոդվածը.\n\n«{text}»\n\n"
    "Բեր մեկ կոնկրետ, առօրյա կյանքից վերցված օրինակ (առավելագույնը 80 բառ), "
    "որը ցույց է տալիս, թե ինչպես է այս հոդվածը գործում իրական իրավիճակում: "
    "Սկսիր «Օրինակ՝» բառով:"
)


def real_life_example(text: str, model: str | None = None) -> str:
    return _chat(_EXAMPLE_SYSTEM, _EXAMPLE_USER.format(text=text),
                 model=model, temperature=0.6)


# ---------------------------------------------------------------------------
# 3) Quiz-me (optional extra)
# ---------------------------------------------------------------------------
_QUIZ_SYSTEM = (
    "Դու ուսուցիչ ես, որ ստուգում է՝ մարդը հասկացե՞լ է օրենքի հոդվածը: "
    "Պատասխանիր միայն հայերենով:"
)

_QUIZ_USER = (
    "Ահա օրենքի հոդվածը.\n\n«{text}»\n\n"
    "Կազմիր 1 պարզ ընտրովի հարց (A/B/C տարբերակներով) այս հոդվածի մասին: "
    "Վերջում առանձին տողով գրիր «Ճիշտ պատասխան՝ X»:"
)


def quiz(text: str, model: str | None = None) -> str:
    return _chat(_QUIZ_SYSTEM, _QUIZ_USER.format(text=text),
                 model=model, temperature=0.5)
