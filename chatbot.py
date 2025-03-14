import openai
import os
from dotenv import load_dotenv

load_dotenv()

class ChatBotIA:
    def __init__(self, tipo_usuario):
        self.tipo_usuario = tipo_usuario
        self.client = openai.Client(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("API_URL"))
        self.model = os.getenv("IA_MODEL", "llama-3.3-70b-versatile")
        
    def perguntar(self, pergunta):
        if self.tipo_usuario == "usuario":
            contexto = (
                "Você é um assistente virtual para candidatos a vagas de emprego. "
                "Seu objetivo é fornecer dicas sobre entrevistas, currículos, processos seletivos e "
                "orientações sobre como se destacar no mercado de trabalho. Responda de forma clara, "
                "motivacional e objetiva."
                "Responda sempre em portugues do Brasil."
            )
        elif self.tipo_usuario == "recrutador":
            contexto = (
                "Você é um assistente virtual para recrutadores e gestores de RH. "
                "Seu objetivo é auxiliar no processo de recrutamento, fornecendo análises de candidatos, "
                "estratégias de seleção, boas práticas de entrevista e otimização do funil de contratação. "
                "Responda de forma clara, objetiva e profissional."
                "Responda sempre em portugues do Brasil."
            )
        else:
            contexto = "Você é um assistente virtual especializado em recrutamento e seleção."
        
        resposta = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": pergunta}
            ]
        )
        
        return resposta.choices[0].message.content.strip()

