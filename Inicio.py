import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Sistema de Laudos Periciais",
    page_icon="🕵️‍♂️",
    layout="centered"
)

# Logo ou imagem institucional (opcional)
logo_path = os.path.join("imagens_relatorio", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

st.title("🕵️‍♂️ Sistema de Auxílio ao Perito Criminal")

st.markdown(
    """
    Bem-vindo ao sistema de geração de laudos periciais!
    
    Este sistema foi desenvolvido para facilitar e agilizar o trabalho do perito criminal na elaboração de laudos técnicos, organização de fotos e geração de relatórios.
    
    **Funcionalidades principais:**
    - Criação e organização de relatórios periciais
    - Upload e detalhamento de imagens
    - Geração automática de documentos finais
    - Histórico de laudos gerados
    
    ---
    
    **Como começar:**
    1. Utilize o menu lateral para navegar entre as etapas do processo.
    2. Crie um novo relatório ou selecione um existente.
    3. Carregue as imagens e adicione descrições detalhadas.
    4. Gere o laudo final em formato DOCX ou TXT.
    
    > Em caso de dúvidas, consulte o manual do usuário ou entre em contato com o suporte técnico.
    """
)

st.info("Para começar, selecione uma opção no menu lateral.")
