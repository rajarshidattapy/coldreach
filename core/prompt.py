from langchain_core.prompts import PromptTemplate

DM_PROMPT_AI_INTERN = PromptTemplate(
    input_variables=["name", "context", "resume"],
    template="""
You are filling placeholders in a fixed LinkedIn DM.
Do NOT rewrite the message.
Only generate the content for <work_line>.

Rules for <work_line>:
- ONE short sentence
- Based strictly on the Context
- Mention role, team, or company
- No compliments, no hype

Context:
{context}

Final message format (return exactly this, filled in):

Hey {name},

<work_line>

I'm a student exploring AI internship opportunities and wanted to ask if your team is currently hiring interns.

Here's my resume: {resume}
"""
)


DM_PROMPT_NO_CONN = PromptTemplate(
    input_variables=["name", "context", "resume"],
    template="""
You are filling placeholders in a fixed LinkedIn DM.
Do NOT rewrite the message.
Only generate the content for <work_line>.

Rules for <work_line>:
- ONE short sentence
- Based strictly on the Context
- Mention role, team, or company
- No compliments, no hype

Context:
{context}

Final message format (return exactly this, filled in):

Hey {name},

<work_line>

I'm a student exploring AI internship opportunities and wanted to ask if your team is currently hiring interns.

Here's my resume: {resume}
"""
)

DM_PROMPT_RESEARCH_INTERN = PromptTemplate(
    input_variables=["name", "context", "resume"],
    template="""
You are filling placeholders in a fixed LinkedIn DM.
Do NOT rewrite the message.
Only generate the content for <work_line>.

Rules for <work_line>:
- ONE short sentence
- Based strictly on the Context
- Mention role, team, or company
- No compliments, no hype

Context:
{context}

Final message format (return exactly this, filled in):

Hey {name},

<work_line>

I'm a student exploring AI internship opportunities and wanted to ask if your team is currently hiring interns.

Here's my resume: {resume}
"""
)

