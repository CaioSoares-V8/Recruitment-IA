import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def conectar_bd():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def criar_vaga(titulo, descricao, responsavel, requisitos, tipo_contrato, salario):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO vagas (titulo, descricao, responsavel, requisitos, tipo_contrato, salario)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (titulo, descricao, responsavel, requisitos, tipo_contrato, salario)
    )
    conn.commit()
    cursor.close()
    conn.close()

def listar_vagas():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vagas")
    vagas = cursor.fetchall()
    cursor.close()
    conn.close()
    return vagas

def criar_candidatura(vaga_id, nome, email, telefone, experiencia, habilidades):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO candidaturas (vaga_id, nome, email, telefone, experiencia, habilidades)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (vaga_id, nome, email, telefone, experiencia, habilidades)
    )
    cursor.execute("UPDATE vagas SET status = %s WHERE id = %s", ("Em processo", vaga_id))
    conn.commit()
    cursor.close()
    conn.close()

def listar_candidaturas_por_vaga(vaga_id):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidaturas WHERE vaga_id = %s", (vaga_id,))
    candidaturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return candidaturas

def contratar_candidato(vaga_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE vagas SET status = %s WHERE id = %s", ("Fechada", vaga_id))
    conn.commit()
    cursor.close()
    conn.close()


st.set_page_config(page_title="Recrutamento - RH", layout="wide")

menu = st.sidebar.radio("Menu", ["RH", "Usuário"])

if menu == "RH":
    st.title("📌 Gestão de Vagas - RH")
    st.subheader("📊 Gerenciamento de Vagas")
    
    if st.button("➕ Criar Nova Vaga"):
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
            criar_vaga(titulo, descricao, responsavel, requisitos, tipo_contrato, salario)
            st.success("Vaga criada com sucesso!")
            st.session_state.show_form = False
    
    st.subheader("📌 Status das Vagas")
    vagas = listar_vagas()
    for vaga in vagas:
        with st.expander(f"{vaga['titulo']} - Status: {vaga['status']}"):
            st.write(f"🙍‍♂️ Responsável: {vaga['responsavel']}")
            st.write(f"📃 Tipo de Contrato: {vaga['tipo_contrato']}")
            st.write(f"💰 Salário: R$ {vaga['salario']:.2f}" if vaga['salario'] else "💰 Salário: A combinar")
            if st.button(f"🗑️ Excluir Vaga"):
                st.info('Funcionalidade em desenvolvimento...')
            st.markdown("---")

            st.write("#### 📄 Candidato:")
            candidaturas = listar_candidaturas_por_vaga(vaga['id'])
            if candidaturas:
                for candidato in candidaturas:
                    st.write(f"**Nome:** {candidato['nome']}")
                    st.write(f"📧 Email: {candidato['email']}")
                    st.write(f"📞 Telefone: {candidato['telefone']}")
                    st.write(f"💼 Experiência: {candidato['experiencia']}")
                    st.write(f"🛠️ Habilidades: {candidato['habilidades']}")


                    if vaga["status"] != "Fechada":
                        if st.button(f"🤖 Gerar Aderência com IA"):
                            st.info("Funcionalidade em desenvolvimento...")

                        if st.button(f"❌ Recusar {candidato['nome']}"):
                            st.info("Funcionalidade em desenvolvimento...")

                        if st.button(f"✅ Contratar {candidato['nome']}", key=f"contratar_{vaga['id']}_{candidato['nome']}"):
                            contratar_candidato(vaga['id'])
                            st.success(f"{candidato['nome']} foi contratado com sucesso!")

                    
            else:
                st.write("Nenhum candidato para esta vaga.")


    st.subheader("🤖 Chat com IA")
    user_input = st.text_input("Digite sua pergunta para a IA:")
    if user_input:
        st.info("Resposta da IA")

elif menu == "Usuário":
    st.title("📌 Visualização de Vagas - Usuário")

    vagas = listar_vagas()
    for vaga in vagas:
        status_exibido = "Candidatado" if vaga['status'] == "Em processo" else vaga['status']
        with st.expander(f"{vaga["titulo"]} - Status: {status_exibido}"):
            st.write(f"📋 Descrição: {vaga['descricao']}")
            st.write(f"📌 Requisitos: {vaga['requisitos']}")
            st.write(f"📄 Tipo de Contrato: {vaga['tipo_contrato']}")
            st.write(f"💰 Salário: R$ {vaga['salario']:.2f}" if vaga['salario'] else "💰 Salário: A combinar")
            if vaga['status'] == "Aberta":
                with st.form(f"form_candidatura_{vaga['id']}"):
                    nome = st.text_input("Nome Completo")
                    email = st.text_input("Email")
                    telefone = st.text_input("Telefone")
                    experiencia = st.text_area("Experiência Profissional")
                    habilidades = st.text_area("Habilidades e Competências")
                    submit_candidatura = st.form_submit_button("Candidatar-se")
                    
                if submit_candidatura:
                    criar_candidatura(vaga['id'], nome, email, telefone, experiencia, habilidades)
                    st.success("Candidatura realizada com sucesso!")
                    
    st.subheader("🤖 Chat com IA")
    user_input = st.text_input("Digite sua pergunta para a IA:")
    if user_input:
        st.info("Resposta da IA")
            

