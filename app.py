import streamlit as st

from core.llm import get_llm, generate_message
from core.linkedin import extract_profile

st.title("ColdReach — LinkedIn Outreach Agent")

urls = st.text_area("LinkedIn Profile URLs (one per line)")

category = st.selectbox(
    "Category",
    ["startup", "bigtech", "research"]
)

connected = st.radio(
    "Connection Status",
    ["Already connected", "Not connected"],
    horizontal=True
)

resume = st.text_input("Resume Drive Link")

extra = {}

if category == "research":
    extra["campus"] = st.text_input("Campus / Institute")

if category == "bigtech":
    extra["company"] = st.text_input("Company")
    extra["position"] = st.text_input("Internship Position")
    extra["internship_link"] = st.text_input("Internship Link")

if st.button("Generate"):
    llm = get_llm()
    connected_flag = connected == "Already connected"

    for url in urls.splitlines():
        url = url.strip()
        if not url:
            continue

        try:
            profile = extract_profile(url)

            msg = generate_message(
                llm=llm,
                profile=profile,
                category=category,
                connected=connected_flag,
                resume=resume,
                extra=extra
            )



            with st.expander(profile.get("name", "Unknown")):
                st.text_area("Message", msg, height=220, key=url)
                st.button("Copy", key="copy_" + url, on_click=st.session_state.update, kwargs={"clipboard": msg})

        except Exception as e:
            with st.expander(url):
                st.error(str(e))
