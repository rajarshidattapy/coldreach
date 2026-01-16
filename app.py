import streamlit as st
from core.llm import get_llm, generate_message
from core.linkedin import extract_profile

st.title("ColdReach — LinkedIn Outreach Agent")

urls = st.text_area("LinkedIn URLs (one per line)")
template = st.selectbox(
    "Message Type",
    ["dm", "connection"]
)
resume = st.text_input("Resume Drive Link")

if st.button("Generate"):
    llm = get_llm()

    for url in urls.splitlines():
        if not url.strip():
            continue

        profile = extract_profile(url)
        msg = generate_message(llm, profile, template, resume)

        st.subheader(profile["name"])
        st.text_area("Message", msg, height=120)
