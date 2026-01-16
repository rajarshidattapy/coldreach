from langchain_core.prompts import PromptTemplate


# =========================
# CATEGORY 1 — RESEARCH INTERN
# =========================

RESEARCH_INTERN_DM = PromptTemplate(
    input_variables=[
        "surname",
        "context",
        "campus",
        "resume"
    ],
    template="""
You are filling placeholders in a fixed email/LinkedIn DM.
Do NOT rewrite any text.
Only generate content for <correlation_line>.

Rules for <correlation_line>:
- 2–3 sentences
- Explicitly connect professor's research to student's skills
- Based strictly on Context
- No praise, no exaggeration

Context:
{context}

Final message (return exactly this, filled in):

Hello Professor {surname},

I hope you’re doing well. I’m a 3rd-year undergraduate in Information Science and Engineering, and I’m very interested in pursuing a 3–6 month research internship under your guidance on campus at {campus}.

<correlation_line>

If you’re open to it, I’d be grateful for a chance to discuss potential directions.

Resume: {resume}

Thank you for your time.
Best regards,
Rajarshi Datta
"""
)


# =========================
# CATEGORY 1 — STARTUP INTERN
# =========================

STARTUP_INTERN_DM = PromptTemplate(
    input_variables=[
        "name",
        "context",
        "company",
        "resume"
    ],
    template="""
You are filling placeholders in a fixed LinkedIn DM.
Do NOT rewrite any text.
Only generate content for <startup_line>.

Rules for <startup_line>:
- ONE short sentence
- Mention startup mission or product
- Based strictly on Context
- No hype words

Context:
{context}

Final message (return exactly this, filled in):

Hi {name},

I'm Rajarshi, a 3rd-year IT student passionate about building real-world AI systems.

<startup_line>

I’d love to explore an AI internship opportunity where I can learn from your team and contribute meaningfully.

Resume: {resume}

Best regards,
Rajarshi
"""
)


# =========================
# CATEGORY 1 — BIG TECH (HR / SWE INTERN) — REFERRAL ASK
# =========================

BIGTECH_REFERRAL_DM = PromptTemplate(
    input_variables=[
        "name",
        "company",
        "position",
        "internship_link",
        "context",
        "resume"
    ],
    template="""
You are filling placeholders in a fixed LinkedIn DM.
Do NOT rewrite any text.
Only generate content for <relevance_line>.

Rules for <relevance_line>:
- ONE sentence
- Mention team, role, or domain
- Based strictly on Context
- Neutral tone

Context:
{context}

Final message (return exactly this, filled in):

Hey {name},

I'm Rajarshi, a pre-final year IT student from BIT.

I came across {company}'s 2026 {position} Internship ({internship_link}) and was inspired by the scale your team works at.

<relevance_line>

Would love any quick tips on applying or standing out.

Here's my resume: {resume}

Best regards,
Rajarshi Datta
"""
)


# =========================
# CATEGORY 2 — NO CONNECTION (≤200 CHARS TOTAL)
# =========================

NO_CONNECTION_200 = PromptTemplate(
    input_variables=[
        "name",
        "context",
        "resume"
    ],
    template="""
You are generating a LinkedIn connection note.
STRICT HARD LIMIT: 200 characters including spaces.
Do NOT exceed this limit.

Rules:
- ONE short paragraph
- Mention role or company
- Ask to connect
- Neutral, professional
- No emojis

Context:
{context}

Return ONLY the final message.

Format:

Hi {name}, <single short personalized line>. I’m a 3rd-year IT student exploring AI internships and would love to connect. Resume: {resume}
"""
)
