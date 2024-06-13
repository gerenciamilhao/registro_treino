import streamlit as st

emails_aprovados = ["teste.com"]

def validar_email():
    email = st.session_state.email_input
    if email in emails_aprovados:
        st.session_state.email_aprovado = True
        st.session_state.email_message = "success"
    else:
        st.session_state.email_aprovado = False
        st.session_state.email_message = "error"