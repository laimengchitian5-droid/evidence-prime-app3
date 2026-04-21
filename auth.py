import streamlit as st

def require_auth(func):
    def wrapper(*args, **kwargs):
        if "authenticated" not in st.session_state: st.session_state.authenticated = False
        if not st.session_state.authenticated:
            st.title("🛡️ Quantum Auth")
            pw = st.text_input("パスキーを入力", type="password")
            if st.button("Unlock"):
                if pw == st.secrets["PASSKEY"]:
                    st.session_state.authenticated = True
                    st.session_state.api_key = st.secrets["GROQ_API_KEY"]
                    st.rerun()
                else: st.error("Invalid")
            return None
        return func(*args, **kwargs)
    return wrapper
