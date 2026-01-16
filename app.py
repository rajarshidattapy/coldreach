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
    results = []
    for url in urls.splitlines():
        url = url.strip()
        if not url:
            continue
        try:
            profile = extract_profile(url)
            msg = generate_message(llm, profile, template, resume)
            results.append((profile, msg))
        except Exception as e:
            results.append(({"name": url, "error": str(e)}, None))

    for profile, msg in results:
        name = profile.get("name", "Unknown")
        with st.expander(name):
            if msg:
                st.text_area("Message", msg, height=120, key=name)
            else:
                st.error(f"Error: {profile.get('error', 'Unknown error')}")
