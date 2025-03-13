import streamlit as st

st.set_page_config(page_title="Gestão de Vagas - RH", layout="wide")

st.title("📌 Gestão de Vagas - RH")

st.sidebar.header("Criar Nova Vaga")
with st.sidebar.form("form_vaga"):
    titulo = st.text_input("Título da Vaga")
    descricao = st.text_area("Descrição")
    requisitos = st.text_area("Requisitos")
    localizacao = st.text_input("Localização")
    tipo_contrato = st.selectbox("Tipo de Contrato", ["CLT", "PJ", "Freelancer", "Estágio"])
    salario = st.number_input("Salário (opcional)", min_value=0, step=100, format="%d")
    submit_button = st.form_submit_button("Criar Vaga")


if submit_button:
    vaga_data = {
        "titulo": titulo,
        "descricao": descricao,
        "requisitos": requisitos,
        "localizacao": localizacao,
        "tipo_contrato": tipo_contrato,
        "salario": salario if salario > 0 else None
    }

    
    st.success(" Vaga criada com sucesso!")

vagas = [
    {"titulo": "Desenvolvedor Python", "localizacao": "São Paulo", "tipo_contrato": "CLT", "salario": 7000},
    {"titulo": "Analista de Dados", "localizacao": "Remoto", "tipo_contrato": "PJ", "salario": 9000},
    {"titulo": "Estagiário em TI", "localizacao": "Rio de Janeiro", "tipo_contrato": "Estágio", "salario": 1500}
]

st.subheader("📋 Vagas Disponíveis")
for vaga in vagas:
    with st.expander(vaga["titulo"]):
        st.write(f"📍 Localização: {vaga['localizacao']}")
        st.write(f"📄 Tipo de Contrato: {vaga['tipo_contrato']}")
        st.write(f"💰 Salário: R$ {vaga['salario']:.2f}" if vaga['salario'] else "💰 Salário: A combinar")
        st.button("Candidatar-se", key=vaga['titulo'])