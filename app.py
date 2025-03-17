import streamlit as st
from chatbot import ChatBotIA  
from database import BancoDeDados  

db = BancoDeDados()
chatbot = ChatBotIA()

st.set_page_config(page_title="Recrutamento - RH", layout="wide")

menu = st.sidebar.radio("Menu", ["RH", "Usuário"])

if menu == "RH":
    st.title("📌 Gestão de Vagas - RH")
    st.subheader("📊 Gerenciamento de Vagas")
    
    if st.button("➕ Criar Nova Vaga", key="criar_vaga"):
        st.session_state.show_form = True

    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    if st.session_state.show_form:
        with st.form("form_vaga"):
            st.header("Criar Nova Vaga")
            titulo = st.text_input("Título da Vaga")
            descricao = st.text_area("Descrição")
            responsavel = st.text_area("Responsável")
            requisitos = st.text_area("Requisitos")
            tipo_contrato = st.selectbox("Tipo de Contrato", ["CLT", "PJ", "Freelancer", "Estágio"])
            salario = st.number_input("Salário (opcional)", min_value=0, step=100, format="%d")
            submit_button = st.form_submit_button("Criar Vaga")             
            cancel_button = st.form_submit_button("Cancelar") 

        if cancel_button:
            st.session_state.show_form = False

        if submit_button:
            db.criar_vaga(titulo, descricao, responsavel, requisitos, tipo_contrato, salario)
            st.success("Vaga criada com sucesso!")
            st.session_state.show_form = False


    st.subheader("📌 Status das Vagas")
    vagas = db.listar_vagas()
    
    for index, vaga in enumerate(vagas):
        with st.expander(f"{vaga['titulo']} - Status: {vaga['status']}"):
            st.write(f"🙍‍♂️ **Responsável:** {vaga['responsavel']}")
            st.write(f"📃 **Tipo de Contrato:** {vaga['tipo_contrato']}")
            st.write(f"💰 **Salário:** R$ {vaga['salario']:.2f}" if vaga['salario'] else "💰 Salário: A combinar")
            st.write(f"📋 **Descrição:** {vaga['descricao']}")
            st.write(f"📌 **Requisitos:** {vaga['requisitos']}")

            if st.button("🗑️ Excluir Vaga", key=f"excluir_vaga_{index}"):
                st.info("Funcionalidade em desenvolvimento...")

            st.write("#### 📄 Candidato:") 

            if vaga["status"] != "Fechada":
        
                candidaturas = db.listar_candidaturas_por_vaga(vaga['id']) 
                if candidaturas:
                    for cand_index, candidato in enumerate(candidaturas):
                        st.write(f"**Nome:** {candidato['nome']}")
                        st.write(f"📧 Email: {candidato['email']}")
                        st.write(f"📞 Telefone: {candidato['telefone']}")
                        st.write(f"💼 Experiência: {candidato['experiencia']}")
                        st.write(f"🛠️ Habilidades: {candidato['habilidades']}")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("🤖 Gerar Aderência com IA", key=f"aderencia_{index}_{cand_index}"):
                                vaga_info = {
                                    "titulo": vaga["titulo"],
                                    "requisitos": vaga["requisitos"]
                                }
                                candidato_info = {
                                    "nome": candidato["nome"],
                                    "experiencia": candidato["experiencia"],
                                    "habilidades": candidato["habilidades"]
                                }
                                
                                resultado_aderencia = chatbot.calcular_aderencia_ia(candidato_info, vaga_info)
                                st.info(f"Aderência do Candidato: {resultado_aderencia}")

                        with col2:
                            if st.button(f"❌ Recusar {candidato['nome']}", key=f"recusar_{index}_{cand_index}"):
                                db.recusar_candidato(candidato['id'])
                                db.atualizar_status_vaga(vaga['id'], "Aberta")
                                st.info("O Candidato foi recusado. A vaga voltou a ficar aberta.")
                             

                        with col3:
                            if st.button(f"✅ Contratar {candidato['nome']}", key=f"contratar_{index}_{cand_index}"):
                                db.contratar_candidato(vaga['id'])
                                db.atualizar_status_vaga(vaga['id'], "Fechada")
                                st.success(f"{candidato['nome']} foi contratado! A vaga foi fechada.")

            else:
                st.success("Candidato contratado")
               

    st.subheader("🤖 Chat com IA")
    pergunta_ia = st.text_input("Digite sua pergunta para a IA:", key="pergunta_rh")

    if pergunta_ia:
        resposta_ia = chatbot.perguntar(pergunta_ia)
        st.info(resposta_ia)

elif menu == "Usuário":
    st.title("📌 Visualização de Vagas - Usuário")

    vagas = db.listar_vagas()
    
    for index, vaga in enumerate(vagas):
        status_exibido = "Candidatado" if vaga['status'] == "Em processo" else vaga['status']
        with st.expander(f"{vaga['titulo']} - Status: {status_exibido}"):
            st.write(f"📋 Descrição: {vaga['descricao']}")
            st.write(f"📌 Requisitos: {vaga['requisitos']}")
            st.write(f"📄 Tipo de Contrato: {vaga['tipo_contrato']}")
            st.write(f"💰 Salário: R$ {vaga['salario']:.2f}" if vaga['salario'] else "💰 Salário: A combinar")

            if vaga['status'] == "Aberta":
                with st.form(f"form_candidatura_{index}"):
                    nome = st.text_input("Nome Completo", key=f"nome_{index}")
                    email = st.text_input("Email", key=f"email_{index}")
                    telefone = st.text_input("Telefone", key=f"telefone_{index}")
                    experiencia = st.text_area("Experiência Profissional", key=f"experiencia_{index}")
                    habilidades = st.text_area("Habilidades e Competências", key=f"habilidades_{index}")
                    submit_candidatura = st.form_submit_button("Candidatar-se")
                
                if submit_candidatura:
                    db.criar_candidatura(vaga['id'], nome, email, telefone, experiencia, habilidades)
                    db.atualizar_status_vaga(vaga['id'], "Em processo")
                    st.success("Candidatura realizada com sucesso! Agora, a vaga está em processo de seleção.")

