# ⚖️ Օրենքը պարզ բառերով — "Explain Like I'm 15" Law Summarizer

Հայկական օրենքի ցանկացած հոդված՝ ցուցադրված **կողք կողքի**՝ ձախում բնօրինակը,
աջում պարզ, մարդկային հայերեն բացատրությունը (+ առօրյա օրինակ և քվիզ):

Takes any ARLIS legal article and shows a plain-Armenian explanation side by
side with the original. Built with **Streamlit + Groq**.

---

## 🚀 Արագ մեկնարկ (5 քայլ)

Ամեն ինչ արվում է VS Code-ի ներսում՝ **Terminal → New Terminal** (⌃`).

### 1. Տեղադրիր փաթեթները

```bash
python -m venv .venv
# mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Ստեղծիր `.env` ֆայլը քո բանալիով

Գրանցվիր՝ https://console.groq.com/ → **API Keys** → ստեղծիր բանալի (անվճար է):

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Բացիր `.env`-ը և տեղադրիր բանալին.

```
GROQ_API_KEY=gsk_...քո_բանալին...
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Ստուգիր, որ բանալին աշխատում է

```bash
python check_models.py
```

Կտպի քո account-ի հասանելի մոդելները: Ընտրիր մեկը և դիր `.env`-ի `GROQ_MODEL`-ում:
> ⚠️ 2026-ի կեսերին հին `llama-3.3-70b-versatile`-ը հանվել է Groq-ից: Օգտագործիր
> `openai/gpt-oss-120b` կամ `qwen/qwen3.6-27b`, կամ այն, ինչ ցույց է տալիս սկրիպտը:

### 4. Զապուսկ արա հավելվածը

```bash
streamlit run app.py
```

Բացվում է բրաուզերում (սովորաբար http://localhost:8501): Ընտրիր օրենք → հոդված →
սեղմիր **«Բացատրիր պարզ հայերենով»**: 🎉

Հավելվածը **անմիջապես աշխատում է** նմուշային տվյալներով (3 օրենք, `data/laws.json`):
Իրական ARLIS տվյալների համար՝ տես ստորև:

### 5. (Ընտրովի) Բեռնիր իրական ARLIS տվյալները

1. Ներբեռնիր dump-ը՝ https://data.opendata.am/dataset/arlis-db
2. Դիր `arlis_docs.jsonl.xz` ֆայլը `data/` պանակում:
3. Զապուսկ արա.

```bash
python prepare_data.py
```

Սա կկարդա dump-ը, կընտրի բարձր ազդեցության օրենքները (Աշխատանքային, Քաղաքացիական,
Սպառողների...), կբաժանի յուրաքանչյուրը «Հոդված N» կտորների և կվերագրի `data/laws.json`:
Հետո նորից `streamlit run app.py`:

---

## 🗂️ Ինչ կա նախագծում

| Ֆայլ | Ինչի համար է |
|------|-------------|
| `app.py` | Streamlit UI — կողք-կողքի բնօրինակ vs պարզ բացատրություն |
| `llm.py` | Groq կանչերը + հայերեն promptերը (explain / example / quiz) |
| `prepare_data.py` | ARLIS dump → `data/laws.json` (իրական տվյալ) |
| `data/laws.json` | Օրենքների պահոց (սկզբում՝ նմուշային) |
| `check_models.py` | Ցույց է տալիս, թե որ մոդելներն են հասանելի քո բանալիով |
| `.env` | Քո գաղտնի բանալիները (git-ում չի պահվում) |

Ճարտարապետությունը միտումնավոր պարզ է՝ **ոչ vector DB, ոչ retrieval** — պարզապես
JSON պահոց + մեկ prompt template: Դա հենց այն է, ինչ պետք է հաքաթոնի համար:

---

## 🎤 Դեմո խորհուրդ (30 վայրկյան)

1. Բացիր որևէ խիտ, դժվար հոդված (օր. Քաղաքացիական օրենսգիրք 606):
2. Ասա ժյուրիին. «Ահա, ինչ է կարդում սովորական քաղաքացին»:
3. Սեղմիր կոճակը → աջում հայտնվում է պարզ բացատրությունը + «Օրինակ՝ դու վարձով
   բնակարան ես վերցնում և...»:
4. Framing. *հասանելիություն արդարադատությանը և իրավական գրագիտություն Հայաստանում:*

---

## 🧩 Եթե շուտ ավարտեք — ընդլայնումներ

- **Voice readout** — բացատրությունը կարդալ բարձրաձայն (browser speech API):
- **Compare mode** — երկու հոդված կողք-կողքի:
- **Search** — որոնում բոլոր հոդվածների մեջ:
- **История** — պահել դիտված հոդվածները:

---

## ❓ Հաճախ հանդիպող խնդիրներ

- **`GROQ_API_KEY բացակայում է`** → `.env` ֆայլ չկա կամ բանալին դատարկ է:
- **`model not found` / 404** → `python check_models.py` և թարմացրու `GROQ_MODEL`-ը:
- **Հայերենը վատ է բացատրվում** → փորձիր ավելի մեծ մոդել (`openai/gpt-oss-120b`):
- **`streamlit: command not found`** → չես ակտիվացրել `.venv`-ը (տես քայլ 1):
