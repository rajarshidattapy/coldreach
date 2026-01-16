from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from core.templates import (
    NO_CONNECTION_TEMPLATE,
    STARTUP_TEMPLATE,
    BIGTECH_TEMPLATE,
    RESEARCH_TEMPLATE
)

from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from core.prompt import (
    RESEARCH_INTERN_DM,
    STARTUP_INTERN_DM,
    BIGTECH_REFERRAL_DM,
    NO_CONNECTION_200
)
from core.utils import enforce_char_limit

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment")
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        groq_api_key=api_key
    )

parser = StrOutputParser()

# Slot-only PromptTemplates (return ONLY slot text)
WORK_LINE_PROMPT = PromptTemplate(
    input_variables=["context", "company"],
    template=(
        "Generate ONE short, personalized sentence for a LinkedIn DM.\n"
        "- Mention why you are inspired by {company}'s mission and the recipient's work.\n"
        "- Use only the information in the context.\n"
        "- No hype words, no praise, no adjectives, no fluff.\n"
        "Return ONLY the sentence.\n"
        "Context:\n{context}\n"
    )
)

CORRELATION_LINE_PROMPT = PromptTemplate(
    input_variables=["context"],
    template=(
        "Generate 2–3 sentences connecting the professor's research to the student's AI/ML or systems background.\n"
        "Base it strictly on the context.\n"
        "Return ONLY the sentences.\n"
        "Context:\n{context}\n"
    )
)

RELEVANCE_LINE_PROMPT = PromptTemplate(
    input_variables=["context"],
    template=(
        "Generate ONE sentence mentioning team, role, or domain for a big tech referral.\n"
        "Base it strictly on the context.\n"
        "Neutral tone. Return ONLY the sentence.\n"
        "Context:\n{context}\n"
    )
)

def safe_invoke(chain, payload):
    try:
        result = chain.invoke(payload)
        if result is None or not str(result).strip():
            return ""
        return str(result).strip()
    except Exception:
        return ""

def generate_message(
    llm,
    profile: dict,
    category: str,
    connected: bool,
    resume: str,
    extra: dict = None
):
    extra = extra or {}
    name = profile.get("name", "").strip()
    surname = name.split()[-1] if name else ""
    context = profile.get("context", "")


    if not connected:
        payload = {
            "context": context,
            "company": extra.get("company", "")
        }
        slot = safe_invoke(WORK_LINE_PROMPT | llm | parser, payload)
        template = NO_CONNECTION_200.template
        msg = template.replace("{name}", name)\
                      .replace("{context}", context)\
                      .replace("{resume}", resume)\
                      .replace("<single short personalized line>", slot)
        msg = enforce_char_limit(msg, 200)
        return msg

    if category == "research":
        payload = {
            "context": context
        }
        slot = safe_invoke(CORRELATION_LINE_PROMPT | llm | parser, payload)
        template = RESEARCH_INTERN_DM.template
        msg = template.replace("{surname}", surname)\
                      .replace("{context}", context)\
                      .replace("{campus}", extra.get("campus", ""))\
                      .replace("{resume}", resume)\
                      .replace("<correlation_line>", slot)
        return msg.strip()

    if category == "startup":
        payload = {
            "context": context,
            "company": extra.get("company", "")
        }
        slot = safe_invoke(WORK_LINE_PROMPT | llm | parser, payload)
        template = STARTUP_INTERN_DM.template
        msg = template.replace("{name}", name)\
                      .replace("{context}", context)\
                      .replace("{company}", extra.get("company", ""))\
                      .replace("{resume}", resume)\
                      .replace("<startup_line>", slot)
        return msg.strip()

    if category == "bigtech":
        payload = {
            "context": context
        }
        slot = safe_invoke(RELEVANCE_LINE_PROMPT | llm | parser, payload)
        template = BIGTECH_REFERRAL_DM.template
        msg = template.replace("{name}", name)\
                      .replace("{company}", extra.get("company", ""))\
                      .replace("{position}", extra.get("position", ""))\
                      .replace("{internship_link}", extra.get("internship_link", ""))\
                      .replace("{context}", context)\
                      .replace("{resume}", resume)\
                      .replace("<relevance_line>", slot)
        return msg.strip()

    raise ValueError(f"Unknown category: {category}")
