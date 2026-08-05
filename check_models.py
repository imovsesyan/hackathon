"""
Prints the models your API keys can currently use.
Run this first to confirm your key works and to pick a GROQ_MODEL for .env

    python check_models.py
"""
import os
from dotenv import load_dotenv

load_dotenv()


def groq_models():
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return [m.id for m in client.models.list().data]


def google_models():
    from google import genai
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    return [m.name for m in client.models.list()]


if __name__ == "__main__":
    if os.getenv("GROQ_API_KEY"):
        try:
            print("GROQ models available to you:")
            for m in sorted(groq_models()):
                print("  -", m)
        except Exception as e:
            print("GROQ error:", e)
    else:
        print("No GROQ_API_KEY found in .env")

    # Uncomment if you set up a Google key too:
    # if os.getenv("GOOGLE_API_KEY"):
    #     try:
    #         print("\nGOOGLE models:", google_models())
    #     except Exception as e:
    #         print("GOOGLE error:", e)
