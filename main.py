import streamlit as st
from functions.email_validation import validar_email
from functions.exercise_selection import selecionar_exercicio
from functions.series_registration import ativar_registro_serie, registrar_serie
import database.database  # Importa o módulo para garantir que a tabela seja criada

# Sidebar para validação de email e seleção de exercício
with st.sidebar:
    st.header('Validação de Usuário')
    
    # Campo de texto para entrada do email
    email = st.text_input("Digite seu email para acesso:", key="email_input")
    
    # Botão para validar o email
    if st.button("Validar Email"):
        validar_email()
    
    # Verificar se o email foi aprovado
    if st.session_state.get('email_message') == "success":
        st.sidebar.success("Email aprovado! Acesso liberado.")
        
        # Opções de exercício
        exercicio_options = ['Selecione o exercício', 'Exercicio 1', 'Exercicio 2', 'Exercicio 3']
        
        # Dropdown para selecionar o exercício
        exercicio = st.selectbox(
            'Exercício:',
            exercicio_options,
            key="exercicio",
            on_change=selecionar_exercicio
        )
    elif st.session_state.get('email_message') == "error":
        st.sidebar.error("Email não autorizado. Tente novamente.")

# Container principal da página
with st.container() as main_container:
    # Container para título
    with st.container() as container_titulo:
        st.title('Registro de Treino')
        
        # Verificar se o email foi aprovado e um exercício foi selecionado
        if "email_aprovado" in st.session_state and st.session_state.email_aprovado:
            if "exercicio_selecionado" in st.session_state and st.session_state.exercicio_selecionado != 'Selecione o exercício':
                st.info(f'Exercício selecionado: {st.session_state.exercicio_selecionado}')
                
                # Mostrar mensagem de sucesso se existir
                if 'sucesso' in st.session_state:
                    st.success(st.session_state.sucesso)
                
                # Mostrar o botão "Registrar série" se não estiver ativo o registro
                if not st.session_state.get("registrar_serie_ativo"):
                    with st.container() as container_botao_registrar:
                        st.button("Registrar série", on_click=ativar_registro_serie, key="botao_registrar_serie")

    # Verificar se o email foi aprovado
    if "email_aprovado" in st.session_state and st.session_state.email_aprovado:
        # Verificar se um exercício foi selecionado
        if "exercicio_selecionado" in st.session_state and st.session_state.exercicio_selecionado != 'Selecione o exercício':
            # Verificar se o registro da série foi ativado
            if st.session_state.get("registrar_serie_ativo"):
                with st.form(key='formulario_registro_serie'):
                    st.subheader('Anotar aqui 👇🏻')
                    col1, col2 = st.columns([2, 3])

                    with col1:
                        # Campos obrigatórios
                        tipo_serie = st.selectbox(
                            'Tipo de Série:',
                            ['R1', 'R2', 'R3', 'R4', 'Working Set', 'Down Set'],
                            key="tipo_serie"
                        )
                        
                        carga = st.text_input("Carga:", key="carga")
                        reps = st.text_input("Reps:", key="reps")
                        descanso = st.text_input("Descanso (min):", key="descanso")
                        esforco_percebido = st.selectbox("Esforço percebido:", [str(i) for i in range(1, 11)], key="esforco_percebido")
                        
                        # Campo opcional
                        obs = st.text_area("Obs: (opcional)", key="obs")

                    # Botão para registrar a série
                    submit_button = st.form_submit_button(label="Guardar série")
                    if submit_button:
                        registrar_serie()
        else:
            st.info("Selecione um exercício na barra lateral.")
    else:
        st.error("Acesso não autorizado. Por favor, valide seu email na barra lateral.")
