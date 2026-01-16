from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from core.prompt import DM_PROMPT_AI_INTERN, DM_PROMPT_NO_CONN, DM_PROMPT_RESEARCH_INTERN
from core.utils import enforce_char_limit
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
load_dotenv()


def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.4,
        api_key=None  # loaded via env: GROQ_API_KEY
    )

parser = StrOutputParser()

def generate_message(llm, profile, template, resume):
    prompt = DM_PROMPT_AI_INTERN if template == "dm" else DM_PROMPT_NO_CONN

    chain = prompt | llm | StrOutputParser()

    msg = chain.invoke({
        "name": profile["name"],
        "context": profile["context"],
        "resume": resume
    })

    if template == "connection":
        msg = enforce_char_limit(msg, 200)

    return msg
