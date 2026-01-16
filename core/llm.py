from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from core.utils import enforce_char_limit

load_dotenv()

# Clean message templates (without LLM instructions)
NO_CONNECTION_TEMPLATE = """Hi {name}, {slot}. I'm a 3rd-year IT student exploring AI internships and would love to connect. Resume: {resume}"""

RESEARCH_TEMPLATE = """Hello Professor {surname},

I hope you're doing well. I'm a 3rd-year undergraduate in Information Science and Engineering, and I'm very interested in pursuing a 3–6 month research internship under your guidance on campus at {campus}.

{slot}

If you're open to it, I'd be grateful for a chance to discuss potential directions.

Resume: {resume}

Thank you for your time.
Best regards,
Rajarshi Datta"""

STARTUP_TEMPLATE = """Hi {name},

I'm Rajarshi, a 3rd-year IT student passionate about building real-world AI systems.

{slot}

I'd love to explore an AI internship opportunity where I can learn from your team and contribute meaningfully.

Resume: {resume}

Best regards,
Rajarshi"""

BIGTECH_TEMPLATE = """Hey {name},

I'm Rajarshi, a pre-final year IT student from BIT.

I came across {company}'s 2026 {position} Internship ({internship_link}) and was inspired by the scale your team works at.

{slot}

Would love any quick tips on applying or standing out.

Here's my resume: {resume}

Best regards,
Rajarshi Datta"""

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
        msg = NO_CONNECTION_TEMPLATE.format(name=name, slot=slot, resume=resume)
        msg = enforce_char_limit(msg, 200)
        return msg

    if category == "research":
        payload = {
            "context": context
        }
        slot = safe_invoke(CORRELATION_LINE_PROMPT | llm | parser, payload)
        msg = RESEARCH_TEMPLATE.format(
            surname=surname,
            campus=extra.get("campus", ""),
            slot=slot,
            resume=resume
        )
        return msg.strip()

    if category == "startup":
        payload = {
            "context": context,
            "company": extra.get("company", "")
        }
        slot = safe_invoke(WORK_LINE_PROMPT | llm | parser, payload)
        msg = STARTUP_TEMPLATE.format(name=name, slot=slot, resume=resume)
        return msg.strip()

    if category == "bigtech":
        payload = {
            "context": context
        }
        slot = safe_invoke(RELEVANCE_LINE_PROMPT | llm | parser, payload)
        msg = BIGTECH_TEMPLATE.format(
            name=name,
            company=extra.get("company", ""),
            position=extra.get("position", ""),
            internship_link=extra.get("internship_link", ""),
            slot=slot,
            resume=resume
        )
        return msg.strip()

    raise ValueError(f"Unknown category: {category}")
