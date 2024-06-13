import streamlit as st

def selecionar_exercicio():
    if st.session_state.exercicio != 'Selecione o exercício':
        st.session_state.exercicio_selecionado = st.session_state.exercicio