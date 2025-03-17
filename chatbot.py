import openai
import os
from dotenv import load_dotenv
from database import BancoDeDados 

load_dotenv()

class ChatBotIA:
    def __init__(self):
        self.client = openai.Client(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("API_URL"))
        self.model = os.getenv("IA_MODEL", "llama-3.3-70b-versatile")
        self.db = BancoDeDados()  

    def obter_dados_do_banco(self):
        vagas = self.db.listar_vagas()
        contexto_vagas = "\n".join([f"ID: {v['id']} | Título: {v['titulo']} | Status: {v['status']}" for v in vagas])

        contexto_candidaturas = ""
        for vaga in vagas:
            candidatos = self.db.listar_candidaturas_por_vaga(vaga['id'])
            for c in candidatos:
                contexto_candidaturas += (
                    f"\nVaga ID: {vaga['id']} - {vaga['titulo']}\n"
                    f"Nome: {c['nome']}, Email: {c['email']}, Telefone: {c['telefone']}, "
                    f"Experiência: {c['experiencia']}, Habilidades: {c['habilidades']}\n"
                )

        contexto = f"Vagas disponíveis:\n{contexto_vagas}\n\nCandidaturas:\n{contexto_candidaturas}"
        return contexto

    def perguntar(self, pergunta):
        """Gera uma resposta considerando os dados do banco como contexto."""
        contexto_dados = self.obter_dados_do_banco()

        contexto_ia = (
            "Você é um assistente virtual especializado em recrutamento e gestão de RH. "
            "Seu objetivo é fornecer informações sobre vagas abertas, candidatos e ajudar no processo seletivo sempre direcionado a ajudar o recrutador. "
            "Use as informações do banco de dados para responder de maneira precisa.\n\n"
            f"{contexto_dados}\n\n"
            "Responda sempre em portugues do Brasil."
            "Agora, responda à seguinte pergunta considerando essas informações:"
        )

        resposta = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": contexto_ia},
                {"role": "user", "content": pergunta}
            ]
        )

        return resposta.choices[0].message.content.strip()
    
    def calcular_aderencia_ia(self, candidato, vaga):
        prompt = f"""
        Avalie a aderência do candidato à vaga com base nas seguintes informações:

        **Candidato:**
        - Nome: {candidato['nome']}
        - Experiência: {candidato['experiencia']}
        - Habilidades: {candidato['habilidades']}

        **Vaga:**
        - Título: {vaga['titulo']}
        - Requisitos: {vaga['requisitos']}

        Com base nessas informações, forneça SOMENTE um percentual de aderência de 0% a 100%.
        """

        resposta = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "Você é um assistente especialista em recrutamento."},
                    {"role": "user", "content": prompt}]
        )

        return resposta.choices[0].message.content.strip()

