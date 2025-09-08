import streamlit as st
import os
import json
from datetime import datetime
import speech_recognition as sr
import tempfile
import wave
import pandas as pd

PASTA_LAUDOS = "relatorios"
ARQUIVO_EXCEL = "historico_relatorios.xlsx"

# Função para listar relatórios disponíveis


def listar_relatorios():
    return [nome for nome in os.listdir(PASTA_LAUDOS) if os.path.isdir(os.path.join(PASTA_LAUDOS, nome))]

# Função para carregar descrições existentes


def carregar_descricoes(pasta_relatorio):
    arquivo_descricoes = os.path.join(pasta_relatorio, "descricoes.json")
    if os.path.exists(arquivo_descricoes):
        with open(arquivo_descricoes, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"ditado_pericia": []}

# Função para salvar descrições


def salvar_descricoes(pasta_relatorio, descricoes):
    arquivo_descricoes = os.path.join(pasta_relatorio, "descricoes.json")
    with open(arquivo_descricoes, 'w', encoding='utf-8') as f:
        json.dump(descricoes, f, ensure_ascii=False, indent=2)

# Função para salvar ditado pericial no arquivo Excel


def salvar_ditado_excel(relatorio_id, ditado_texto):
    """Salva o ditado pericial na última coluna do arquivo Excel"""
    try:
        # Verificar se o arquivo Excel existe
        if os.path.exists(ARQUIVO_EXCEL):
            df = pd.read_excel(ARQUIVO_EXCEL)
        else:
            st.error("Arquivo historico_relatorios.xlsx não encontrado!")
            return False

        # Verificar se o relatório existe no Excel
        if relatorio_id not in df["ID Relatório"].values:
            st.error(
                f"Relatório {relatorio_id} não encontrado no arquivo Excel!")
            return False

        # Adicionar coluna "Ditado Pericial" se não existir
        if "Ditado Pericial" not in df.columns:
            df["Ditado Pericial"] = ""

        # Atualizar o ditado pericial para o relatório específico
        df.loc[df["ID Relatório"] == relatorio_id,
               "Ditado Pericial"] = ditado_texto

        # Salvar o arquivo Excel
        df.to_excel(ARQUIVO_EXCEL, index=False)
        return True

    except Exception as e:
        st.error(f"Erro ao salvar ditado no Excel: {e}")
        return False


def carregar_ditado_excel(relatorio_id):
    """Carrega o ditado pericial do arquivo Excel"""
    try:
        # Verificar se o arquivo Excel existe
        if not os.path.exists(ARQUIVO_EXCEL):
            return ""

        # Carregar dados do Excel
        df = pd.read_excel(ARQUIVO_EXCEL)

        # Verificar se o relatório existe no Excel
        if relatorio_id not in df["ID Relatório"].values:
            return ""

        # Verificar se a coluna "Ditado Pericial" existe
        if "Ditado Pericial" not in df.columns:
            return ""

        # Obter o ditado pericial para o relatório específico
        ditado = df.loc[df["ID Relatório"] ==
                        relatorio_id, "Ditado Pericial"].iloc[0]

        # Retornar o ditado se não for NaN ou vazio
        if pd.isna(ditado) or ditado == "":
            return ""

        return str(ditado)

    except Exception as e:
        st.warning(f"Erro ao carregar ditado do Excel: {e}")
        return ""


def limpar_ditado_excel(relatorio_id):
    """Limpa o ditado pericial do arquivo Excel"""
    try:
        # Verificar se o arquivo Excel existe
        if not os.path.exists(ARQUIVO_EXCEL):
            return False

        # Carregar dados do Excel
        df = pd.read_excel(ARQUIVO_EXCEL)

        # Verificar se o relatório existe no Excel
        if relatorio_id not in df["ID Relatório"].values:
            return False

        # Verificar se a coluna "Ditado Pericial" existe
        if "Ditado Pericial" not in df.columns:
            return False

        # Limpar o ditado pericial para o relatório específico
        df.loc[df["ID Relatório"] == relatorio_id, "Ditado Pericial"] = ""

        # Salvar o arquivo Excel
        df.to_excel(ARQUIVO_EXCEL, index=False)
        return True

    except Exception as e:
        st.error(f"Erro ao limpar ditado do Excel: {e}")
        return False

# Função para transcrever áudio


def transcrever_audio(audio_data):
    recognizer = sr.Recognizer()

    try:
        # Converter áudio para formato compatível
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        # Carregar o arquivo de áudio
        with sr.AudioFile(temp_file_path) as source:
            audio = recognizer.record(source)

        # Transcrever usando Google Speech Recognition
        texto = recognizer.recognize_google(audio, language='pt-BR')

        # Limpar arquivo temporário
        os.unlink(temp_file_path)

        return texto
    except sr.UnknownValueError:
        st.error("Não foi possível entender o áudio. Tente falar mais claramente.")
        return None
    except sr.RequestError as e:
        st.error(f"Erro na requisição ao serviço de reconhecimento: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None


# Título da página
st.markdown("## 🎤 Ditado de Perícia")
st.markdown("### Transcreva suas observações da cena de crime")

# Selecionar relatório existente
relatorios_existentes = listar_relatorios()
relatorio_selecionado = st.sidebar.selectbox(
    "Selecionar Relatório", ["Nenhum"] + relatorios_existentes)

if relatorio_selecionado != "Nenhum":
    st.sidebar.title(f"Relatório {relatorio_selecionado}")

    # Definir caminho do relatório selecionado
    pasta_relatorio = os.path.join(PASTA_LAUDOS, relatorio_selecionado)

    # Carregar descrições existentes
    descricoes = carregar_descricoes(pasta_relatorio)

    # Seção de ditado
    st.markdown("### 🎙️ Gravação de Áudio")

    # Upload de arquivo de áudio
    uploaded_audio = st.file_uploader(
        "Carregar arquivo de áudio (WAV, MP3, M4A)",
        type=["wav", "mp3", "m4a", "ogg"]
    )

    if uploaded_audio is not None:
        st.audio(uploaded_audio, format='audio/wav')

        if st.button("🎤 Transcrever Áudio"):
            with st.spinner("Transcrevendo áudio..."):
                audio_data = uploaded_audio.read()
                texto_transcrito = transcrever_audio(audio_data)

                if texto_transcrito:
                    st.success("Transcrição concluída!")
                    st.text_area("Texto Transcrito:",
                                 texto_transcrito, height=150)

                    # Botão para salvar a transcrição
                    if st.button("💾 Salvar Transcrição"):
                        # Criar entrada de ditado
                        entrada_ditado = {
                            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "texto": texto_transcrito,
                            "arquivo_original": uploaded_audio.name
                        }

                        # Salvar no arquivo Excel
                        if salvar_ditado_excel(relatorio_selecionado, texto_transcrito):
                            st.success(
                                "Transcrição salva com sucesso!")
                        else:
                            st.error("Erro ao salvar transcrição.")
                        st.rerun()

    # Seção de ditado manual
    st.markdown("### ✍️ Ditado Manual")

    # Campo para entrada manual de texto
    texto_manual = st.text_area(
        "Digite suas observações:",
        height=200,
        placeholder="Descreva detalhadamente o que foi observado..."
    )

    if st.button("💾 Salvar Observação Manual"):
        if texto_manual.strip():
            # Criar entrada de ditado manual
            entrada_ditado = {
                "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "texto": texto_manual.strip(),
                "tipo": "manual"
            }

            # Salvar no arquivo Excel
            if salvar_ditado_excel(relatorio_selecionado, texto_manual.strip()):
                st.success("Observação salva com sucesso!")
            else:
                st.error("Erro ao salvar observação.")
            st.rerun()
        else:
            st.warning("Digite uma observação antes de salvar.")

    # Seção de histórico de ditados
    st.markdown("### 📋 Histórico de Ditados")

    # Carregar ditado do Excel para exibição
    ditado_excel = carregar_ditado_excel(relatorio_selecionado)

    if ditado_excel:
        with st.expander("Ditado Pericial Atual"):
            st.write(f"**Texto:**")
            st.text_area("Texto do ditado:", ditado_excel, height=150,
                         disabled=True, label_visibility="collapsed")

            # Botão para limpar ditado
            if st.button("🗑️ Limpar Ditado"):
                if limpar_ditado_excel(relatorio_selecionado):
                    st.success("Ditado limpo com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao limpar ditado.")

    # Estatísticas
    ditado_excel = carregar_ditado_excel(relatorio_selecionado)

    if ditado_excel:
        total_caracteres = len(ditado_excel)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ditado Pericial", "Ativo")
        with col2:
            st.metric("Total de Caracteres", total_caracteres)
    else:
        st.info("Nenhum ditado pericial registrado.")

else:
    st.warning(
        "Selecione um relatório no painel lateral para começar a usar o ditado de perícia.")

    # Instruções de uso
    st.markdown("### 📖 Como usar:")
    st.markdown("""
    1. **Selecione um relatório** no painel lateral
    2. **Carregue um arquivo de áudio** ou use a entrada manual
    3. **Transcreva o áudio** ou digite suas observações
    4. **Salve as observações** para incluí-las no relatório final
    5. **Visualize o histórico** de todos os ditados salvos
    """)
