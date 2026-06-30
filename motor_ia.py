import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Configuração da Página Web (Aba do Navegador)
st.set_page_config(page_title="Karakuria AI", page_icon="🤖", layout="centered")
st.title("⚡ Karakuria Core")
st.caption("Sistema de Inteligência e Infraestrutura Operante")

# 2. Conexão com o Cofre e o Motor
load_dotenv()
chave_secreta = os.getenv("GROQ_API_KEY")
if chave_secreta:
    cliente = Groq(api_key=chave_secreta.strip())
else:
    st.error("Erro crítico: Chave de API não encontrada.")
    st.stop() # Para a execução do site

# 3. Gerenciamento da Memória no Servidor (Session State)
# Se a memória estiver vazia, criamos a lista e adicionamos a regra do sistema
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Você é a Karakuria, uma assistente de infraestrutura e dados irônica, direta e altamente inteligente."}
    ]

# 4. Renderização da Interface (Desenhando o chat na tela)
# O Streamlit lê o histórico e desenha os balões de conversa
for mensagem in st.session_state.historico:
    if mensagem["role"] != "system": # Escondemos a regra do sistema da tela
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])

# 5. O Input do Usuário (A caixa de texto lá embaixo)
comando = st.chat_input("Fale com a Karakuria...")

if comando:
    # Mostra a mensagem do usuário na tela imediatamente
    with st.chat_message("user"):
        st.markdown(comando)
    
    # Salva na memória do servidor
    st.session_state.historico.append({"role": "user", "content": comando})
    
    # 6. A Sinapse (Chamada para a Groq)
    with st.spinner("Processando dados..."):
        resposta = cliente.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.historico
        )
        
        conteudo_resposta = resposta.choices[0].message.content
        
        # Mostra a resposta da IA na tela
        with st.chat_message("assistant"):
            st.markdown(conteudo_resposta)
        
        # Salva a resposta na memória
        st.session_state.historico.append({"role": "assistant", "content": conteudo_resposta})