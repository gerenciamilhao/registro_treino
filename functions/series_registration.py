import streamlit as st
from database.database import get_db_connection, create_tables
from datetime import datetime

# Chama a função para criar as tabelas quando o script é carregado
create_tables()

def ativar_registro_serie():
    st.session_state.registrar_serie_ativo = True

def registrar_serie():
    try:
        carga = float(st.session_state.get("carga"))
        reps = int(st.session_state.get("reps"))
        descanso = int(st.session_state.get("descanso"))
        esforco_percebido = int(st.session_state.get("esforco_percebido"))
    except ValueError:
        st.error("Por favor, insira valores numéricos válidos para carga, reps, descanso e esforço percebido.")
        return

    if not all([st.session_state.get("tipo_serie"), st.session_state.get("carga"),
                st.session_state.get("reps"), st.session_state.get("descanso"),
                st.session_state.get("esforco_percebido")]):
        st.error("Todos os campos são obrigatórios, exceto o campo 'Obs:'")
        return
    
    dados = {
        "email": st.session_state.email_input,
        "exercicio": st.session_state.exercicio_selecionado,
        "tipo_serie": st.session_state.tipo_serie,
        "carga": carga,
        "reps": reps,
        "descanso": descanso,
        "esforco_percebido": esforco_percebido,
        "obs": st.session_state.get("obs", "")
    }

    # Salvar no banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO series (email, exercicio, tipo_serie, carga, reps, descanso, esforco_percebido, obs, data_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (dados["email"], dados["exercicio"], dados["tipo_serie"], dados["carga"], dados["reps"], dados["descanso"], dados["esforco_percebido"], dados["obs"]))
    conn.commit()
    conn.close()

    st.session_state.sucesso = f'Série registrada com sucesso: {st.session_state.exercicio_selecionado} - {st.session_state.tipo_serie}'

    for key in ['tipo_serie', 'carga', 'reps', 'descanso', 'esforco_percebido', 'obs']:
        st.session_state.pop(key, None)
    st.session_state.pop('registrar_serie_ativo', None)
    st.experimental_rerun()
