import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Caminho do arquivo Excel
arquivo_excel = "historico_relatorios.xlsx"
pasta_relatorios = "relatorios"  # Diretório base para os relatórios

# Criar a pasta base se não existir
if not os.path.exists(pasta_relatorios):
    os.makedirs(pasta_relatorios)

# Título do aplicativo
st.markdown("## Gerador de Relatório Pericial")

# Função para converter DataFrame para formato compatível com Streamlit


def converter_dataframe_compativel(df):
    """Converte DataFrame para formato compatível com Streamlit"""
    df_copy = df.copy()

    # Converter colunas de data para string
    colunas_data = ["Data da Ocorrência", "Data da Perícia"]
    for col in colunas_data:
        if col in df_copy.columns:
            # Se a coluna contém objetos datetime, converte para string
            if df_copy[col].dtype == 'object':
                df_copy[col] = df_copy[col].astype(str)
            # Se a coluna é datetime64, converte para string
            elif 'datetime' in str(df_copy[col].dtype):
                df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d')

    return df_copy


# Verifica se o arquivo existe e carrega os dados
if os.path.exists(arquivo_excel):
    try:
        df_historico = pd.read_excel(arquivo_excel)
        # Converte para formato compatível
        df_historico = converter_dataframe_compativel(df_historico)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        df_historico = pd.DataFrame(
            columns=["ID Relatório", "Número do BO", "Requisitante", "Natureza",
                     "Local do Fato", "Destinatário", "Data da Ocorrência",
                     "Nome do Perito", "Data da Perícia", "Histórico da Requisição",
                     "Quesito da Perícia", "Placa", "Marca", "Modelo", "Cor"]
        )
else:
    df_historico = pd.DataFrame(
        columns=["ID Relatório", "Número do BO", "Requisitante", "Natureza",
                 "Local do Fato", "Destinatário", "Data da Ocorrência",
                 "Nome do Perito", "Data da Perícia", "Histórico da Requisição",
                 "Quesito da Perícia", "Placa", "Marca", "Modelo", "Cor", "Pneus", "Sistemas"]
    )

# Exibe a tabela de histórico de relatórios
st.dataframe(df_historico)

# Campos de entrada organizados em colunas
st.header("Novo Relatório")

# Organizar os campos em seções mais intuitivas e com dicas/contexto para o usuário

st.markdown("### 1️⃣ **Informações do Boletim de Ocorrência**")
col1, col2 = st.columns(2)
with col1:
    boletim_ocorrencia = st.text_input(
        "Número do BO (único)",
        help="Digite o número do Boletim de Ocorrência sem espaços ou caracteres especiais."
    ).upper()

    data_ocorrencia = st.date_input(
        "Data da Ocorrência",
        help="Selecione a data em que ocorreu o fato."
    )
    natureza = st.text_input(
        "Natureza do BO",
        help="Exemplo: Acidente, Furto, Roubo, etc."
    )
with col2:
    local_fato = st.text_input(
        "Local do Fato",
        help="Informe o endereço ou descrição do local do fato."
    )
    destinatario = st.text_input(
        "Destinatário",
        help="Nome da autoridade ou órgão destinatário do laudo."
    )
    requisitante = st.text_input(
        "Requisitante",
        help="Nome de quem requisitou a perícia."
    )

st.markdown("---")
st.markdown("### 2️⃣ **Informações do Perito e da Perícia**")
col3, col4 = st.columns(2)
with col3:
    nome_perito = st.text_input(
        "Nome do Perito",
        help="Nome completo do perito responsável."
    )
    data_pericia = st.date_input(
        "Data da Perícia",
        value=datetime.today(),
        help="Data em que a perícia foi realizada."
    )
with col4:
    historico_requisicao = st.text_area(
        "Histórico da Requisição",
        help="Descreva brevemente o histórico da requisição."
    )
    quesito_pericia = st.text_area(
        "Quesito da Perícia",
        help="Informe o quesito principal da perícia."
    )

st.markdown("---")
st.markdown("### 3️⃣ **Informações do Veículo**")
col5, col6 = st.columns(2)
with col5:
    placa = st.text_input(
        "Placa do veículo",
        help="Digite a placa do veículo (ex: ABC1D23)."
    )
    marca = st.text_input(
        "Marca do veículo",
        help="Exemplo: Fiat, Ford, Toyota, etc."
    )
    modelo = st.text_input(
        "Modelo do veículo",
        help="Exemplo: Uno, Fiesta, Corolla, etc."
    )
    cor = st.text_input(
        "Cor do veículo",
        help="Cor predominante do veículo."
    )
with col6:
    pneus = st.selectbox(
        "Condição dos pneus",
        options=["Bons", "Ruins"],
        help="Selecione a condição geral dos pneus."
    )
    sistemas = st.radio(
        "Condição dos sistemas veiculares",
        options=["Direção, freio e luzes OK", "Prejudicado"],
        help="Informe se os sistemas essenciais do veículo estão em bom estado ou prejudicados."
    )

# Função para gerar relatório e armazenar no Excel


def CriarRelatorio():
    # Validações com return para parar execução em caso de erro
    if not boletim_ocorrencia:
        st.warning("O número do BO é obrigatório!")
        return
    if not requisitante:
        st.warning("O nome do requisitante é obrigatório!")
        return
    if not natureza:
        st.warning("A natureza do BO é obrigatória!")
        return
    if not local_fato:
        st.warning("O local do fato é obrigatório!")
        return
    if not destinatario:
        st.warning("O destinatario é obrigatório!")
        return
    if not data_ocorrencia:
        st.warning("A data da ocorrência é obrigatória!")
        return
    if not nome_perito:
        st.warning("O nome do perito é obrigatório!")
        return
    if not data_pericia:
        st.warning("A data da perícia é obrigatória!")
        return

    # Criar ID único do relatório
    ano = data_pericia.year
    id_relatorio = f"{ano}_{boletim_ocorrencia}"

    # Criar pasta para o relatório, se não existir
    pasta_relatorio = os.path.join(pasta_relatorios, id_relatorio)
    if not os.path.exists(pasta_relatorio):
        os.makedirs(pasta_relatorio)

    # Criar um DataFrame com os dados inseridos
    # IMPORTANTE: Converter datas para string para evitar problemas de compatibilidade
    novo_registro = pd.DataFrame(
        [[id_relatorio, boletim_ocorrencia, requisitante, natureza, local_fato, destinatario,
          data_ocorrencia.strftime("%Y-%m-%d"), nome_perito,
          data_pericia.strftime("%Y-%m-%d"), historico_requisicao, quesito_pericia, placa, marca, modelo, cor, pneus, sistemas]],
        columns=["ID Relatório", "Número do BO", "Requisitante", "Natureza", "Local do Fato", "Destinatário", "Data da Ocorrência",
                 "Nome do Perito", "Data da Perícia", "Histórico da Requisição", "Quesito da Perícia", "Placa", "Marca", "Modelo", "Cor", "Pneus", "Sistemas"]
    )

    # Se o arquivo já existe, carrega os dados e verifica duplicatas
    if os.path.exists(arquivo_excel):
        try:
            df_existente = pd.read_excel(arquivo_excel)

            # Converter para formato compatível
            df_existente = converter_dataframe_compativel(df_existente)

            # Verifica se o BO já foi cadastrado
            if boletim_ocorrencia in df_existente["Número do BO"].astype(str).values:
                st.error("Erro: Esse número de BO já está cadastrado!")
                return

            # Adiciona a nova entrada ao histórico
            df_final = pd.concat(
                [df_existente, novo_registro], ignore_index=True)
        except Exception as e:
            st.error(f"Erro ao carregar dados existentes: {e}")
            df_final = novo_registro
    else:
        df_final = novo_registro

    try:
        # Salva os dados no arquivo Excel
        df_final.to_excel(arquivo_excel, index=False)
        st.success(f"Relatório gerado com sucesso! ID: {id_relatorio}")

        # Atualiza a exibição da tabela
        # st.dataframe(df_final)

    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")


# Botão para criar relatório
st.button("Criar Relatório", on_click=CriarRelatorio)
