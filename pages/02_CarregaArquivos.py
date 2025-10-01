import streamlit as st
import os
from PIL import Image

PASTA_LAUDOS = "relatorios"

# Função para listar relatórios disponíveis


st.title("Carregar Arquivos")
st.markdown("""
### Bem-vindo(a) à etapa de Carregamento de Fotografias

Esta etapa permite nomear e carregar as fotografias para o relatório selecionado.

Siga as instruções abaixo:
- **1. Selecionar Relatório**: Use a **sidebar** para escolher um relatório existente.
- **2. Nomear a Foto**: Na **sidebar**, preencha o campo "Nome da Foto".
- **3. Escolher a Fotografia**: Ainda na **sidebar**, selecione a(s) imagem(ns) a carregar.
- **4. Confirmar**: Clique no botão **CARREGAR FOTOS** para concluir.
""")

st.caption("Após concluir o carregamento, as imagens já incluídas no relatório serão exibidas abaixo (na página principal de Carregamento).")


def listar_relatorios():
    return [nome for nome in os.listdir(PASTA_LAUDOS) if os.path.isdir(os.path.join(PASTA_LAUDOS, nome))]


# Selecionar relatório existente
relatorios_existentes = listar_relatorios()
relatorio_selecionado = st.sidebar.selectbox(
    "Selecionar Relatório", ["Nenhum"] + relatorios_existentes)

if relatorio_selecionado != "Nenhum":
    st.sidebar.title(f"Relatório {relatorio_selecionado}")

    # Definir caminho do relatório selecionado
    pasta_relatorio = os.path.join(PASTA_LAUDOS, relatorio_selecionado)

    # Reset do campo nome_foto se necessário
    if "reset_nome_foto" in st.session_state and st.session_state["reset_nome_foto"]:
        st.session_state["nome_foto"] = ""
        st.session_state["reset_nome_foto"] = False

    # ETAPA 1: Campo para nomear a imagem
    st.sidebar.markdown("### 📝 **Etapa 1: Nomear a Foto**")
    nome_foto = st.sidebar.text_input(
        "Nome da Foto (sem extensão)", key="nome_foto",
        help="Digite um nome descritivo para a foto (ex: 'FrenteVeiculo', 'DanosPorta')")

    # ETAPA 2: Upload de imagens
    st.sidebar.markdown("### 📁 **Etapa 2: Escolher a Fotografia**")
    uploaded_files = st.sidebar.file_uploader(
        "Selecionar Imagem(s)", type=["jpg", "png", "jpeg"],
        accept_multiple_files=True,
        help="Selecione uma ou mais imagens para carregar")

    # ETAPA 3: Botão de confirmação para salvar as imagens
    st.sidebar.markdown("### ✅ **Etapa 3: Confirmar Carregamento**")

    # Verificar se ambas as etapas foram completadas
    nome_preenchido = nome_foto.strip() != ""
    arquivos_selecionados = uploaded_files is not None

    # Botão de confirmação (só ativo quando ambas as etapas estão completas)
    if st.sidebar.button(
        "🚀 **CARREGAR FOTOS**",
        type="primary",
        disabled=not (nome_preenchido and arquivos_selecionados),
        help="Clique aqui para confirmar o carregamento das fotos selecionadas"
    ):
        if nome_preenchido and arquivos_selecionados:
            # Processar cada arquivo carregado
            for uploaded_file in uploaded_files:
                # Definir nome final do arquivo
                extensao = os.path.splitext(uploaded_file.name)[
                    1]  # Mantém a extensão original
                nome_arquivo = nome_foto.strip() + extensao
                file_path = os.path.join(pasta_relatorio, nome_arquivo)

                # Verificar se já existe um arquivo com o mesmo nome
                if os.path.exists(file_path):
                    st.sidebar.warning(
                        f"⚠️ Arquivo '{nome_arquivo}' já existe! Será sobrescrito.")

                # Salvar imagem
                try:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.sidebar.success(
                        f"✅ Foto '{nome_arquivo}' carregada com sucesso!")
                except Exception as e:
                    st.sidebar.error(
                        f"❌ Erro ao salvar '{nome_arquivo}': {str(e)}")

            # Sinaliza para resetar o campo nome_foto na próxima execução
            st.session_state["reset_nome_foto"] = True
            st.rerun()

    # Mensagens de orientação
    if not nome_preenchido and not arquivos_selecionados:
        st.sidebar.info(
            "ℹ️ Complete as etapas 1 e 2 para habilitar o carregamento")
    elif nome_preenchido and not arquivos_selecionados:
        st.sidebar.info("ℹ️ Agora selecione a(s) foto(s) na Etapa 2")
    elif not nome_preenchido and arquivos_selecionados:
        st.sidebar.info("ℹ️ Primeiro nomeie a foto na Etapa 1")
    elif nome_preenchido and arquivos_selecionados:
        st.sidebar.success(
            "🎯 Todas as etapas completas! Clique em 'CARREGAR FOTOS' para confirmar.")

    # Listar e exibir imagens já carregadas
    imagens_existentes = [img for img in os.listdir(
        pasta_relatorio) if img.lower().endswith((".jpg", ".jpeg", ".png"))]

    if imagens_existentes:
        st.markdown("### 📸 Imagens Carregadas")
        colunas = st.columns(3)  # Exibir imagens em colunas

        for i, imagem in enumerate(imagens_existentes):
            img_path = os.path.join(pasta_relatorio, imagem)
            img = Image.open(img_path)

            with colunas[i % 3]:  # Distribui as imagens entre as colunas
                st.image(img, caption=imagem, use_container_width=True)

                # Botão para excluir a imagem
                if st.button(f"🗑️ Excluir {imagem}", key=imagem):
                    try:
                        os.remove(img_path)
                        st.success(
                            f"✅ Imagem '{imagem}' removida com sucesso!")
                        st.rerun()  # Atualiza a interface após a exclusão
                    except Exception as e:
                        st.error(f"❌ Erro ao excluir '{imagem}': {str(e)}")
