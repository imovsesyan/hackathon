# ⚖️ Law in Plain Words — "Explain Like I'm 15" Law Summarizer

Takes any ARLIS legal article and shows a plain-Armenian explanation side by
side with the original. Built with **Streamlit + Groq**.

---

## 🚀 Quick Start (5 steps)

Everything runs inside VS Code: **Terminal → New Terminal** (⌃`).

### 1. Install dependencies

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Create your `.env` file

Sign up at https://console.groq.com/ → **API Keys** → create a key (it's free).

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Open `.env` and paste your key:

```
GROQ_API_KEY=gsk_...your_key...
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Verify your key works

```bash
python check_models.py
```

This prints all models available on your account. Pick one and set it as `GROQ_MODEL` in `.env`.
> ⚠️ As of mid-2026, `llama-3.3-70b-versatile` has been removed from Groq. Use
> `openai/gpt-oss-120b`, `qwen/qwen3.6-27b`, or whatever the script shows.

### 4. Run the app

```bash
streamlit run app.py
```

Opens in your browser (usually http://localhost:8501). Pick a law → pick an article →
click **"Explain in plain Armenian"**. 🎉

The app works immediately with sample data (3 laws in `data/laws.json`).
For real ARLIS data, see step 5.

### 5. (Optional) Load real ARLIS data

1. Download the dump from https://data.opendata.am/dataset/arlis-db
2. Put `arlis_docs.jsonl.xz` in the `data/` folder.
3. Run:

```bash
python prepare_data.py
```

This reads the dump, picks high-impact laws (Labor, Civil, Consumer...), splits each into
"Article N" chunks, and writes them to `data/laws.json`. Then run `streamlit run app.py` again.

---

## 🗂️ Project structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — original vs plain-language explanation side by side |
| `llm.py` | Groq calls + Armenian prompts (explain / example / quiz) |
| `prepare_data.py` | ARLIS dump → `data/laws.json` |
| `data/laws.json` | Law storage (sample data by default) |
| `check_models.py` | Lists models available on your API key |
| `.env` | Your secret keys (never committed to git) |

The architecture is intentionally simple: **no vector DB, no retrieval** — just a JSON
store and a single prompt template. That's all a hackathon needs.

---

## ❓ Troubleshooting

- **`GROQ_API_KEY missing`** → `.env` file doesn't exist or the key is empty.
- **`model not found` / 404** → run `python check_models.py` and update `GROQ_MODEL`.
- **Poor Armenian output** → try a larger model (`openai/gpt-oss-120b`).
- **`streamlit: command not found`** → you haven't activated `.venv` (see step 1).
