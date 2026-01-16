from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from core.prompt import (
    RESEARCH_INTERN_DM,
    STARTUP_INTERN_DM,
    BIGTECH_REFERRAL_DM,
    NO_CONNECTION_200
)
from core.utils import enforce_char_limit

load_dotenv()

# -------------------------
# LLM SETUP
# -------------------------

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment")

    return ChatGroq(
        model="openai/gpt-oss-120b",   # ✅ Groq-supported
        temperature=0.4,
        groq_api_key=api_key
    )


parser = StrOutputParser()

# -------------------------
# MESSAGE GENERATION
# -------------------------

def generate_message(
    llm,
    profile: dict,
    category: str,
    connected: bool,
    resume: str,
    extra: dict = None
):
    """
    category: 'research' | 'startup' | 'bigtech'
    connected: True / False
    extra: additional fields like campus, company, position, internship_link
    """

    extra = extra or {}

    # -------- Prompt routing --------
    if not connected:
        prompt = NO_CONNECTION_200

    elif category == "research":
        prompt = RESEARCH_INTERN_DM

    elif category == "startup":
        prompt = STARTUP_INTERN_DM

    elif category == "bigtech":
        prompt = BIGTECH_REFERRAL_DM

    else:
        raise ValueError(f"Unknown category: {category}")

    chain = prompt | llm | parser

    # -------- Payload --------
    payload = {
        "context": profile.get("context", ""),
        "resume": resume,
        **extra
    }

    # name / surname handling
    if "surname" in prompt.input_variables:
        payload["surname"] = profile["name"].split()[-1]
    if "name" in prompt.input_variables:
        payload["name"] = profile["name"]

    msg = chain.invoke(payload)

    # -------- Hard limit for no-connection --------
    if not connected:
        msg = enforce_char_limit(msg, 200)

    return msg.strip()
