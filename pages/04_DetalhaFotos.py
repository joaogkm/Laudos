import streamlit as st
import openai
import json
import os
from base64 import b64encode
from dotenv import load_dotenv
from PIL import Image
import pandas as pd


PASTA_LAUDOS = "relatorios"
ARQUIVO_EXCEL = "historico_relatorios.xlsx"

# Carrega arquivo .env
load_dotenv('.env')
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Categorias específicas para danos de veículos
CATEGORIAS_DANOS = {
    "Estrutural": "Danos na estrutura/carcaça do veículo",
    "Pintura": "Arranhões, riscos e danos na pintura",
    "Vidros": "Trincas, quebras e danos em vidros",
    "Faróis": "Quebras e danos em faróis e lanternas",
    "Para-choques": "Deformações e quebras em para-choques",
    "Portas": "Deformações e problemas de funcionamento",
    "Capô": "Deformações no capô e tampa do porta-malas",
    "Rodas": "Danos em rodas e pneus",
    "Suspensao": "Danos na suspensão e direção",
    "Motor": "Danos no motor e componentes mecânicos"
}


def descrever_imagem_veicular(image_path, contexto_ditado="", categoria_dano=""):
    """
    Descreve uma imagem de dano veicular com foco específico em perícia automotiva.

    Args:
        image_path: Caminho para a imagem
        contexto_ditado: Texto do ditado pericial para contextualizar a descrição
        categoria_dano: Categoria específica do dano (opcional)
    """
    with open(image_path, "rb") as img_file:
        img_base64 = b64encode(img_file.read()).decode("utf-8")

    # Prompt especializado para perícia veicular
    prompt_base = """Você é um perito criminal especializado em perícia veicular e constatação de danos.

INSTRUÇÕES ESPECÍFICAS PARA ANÁLISE VEICULAR:
1. **Identifique o tipo de veículo** (carro, moto, caminhão, etc.)
2. **Localize a área danificada** (frente, traseira, lateral, teto, etc.)
3. **Descreva a natureza do dano**:
   - Deformação estrutural (amassado, torcido, quebrado)
   - Danos na pintura (arranhão, risco, descascamento)
   - Quebras em componentes (vidros, faróis, para-choques)
   - Estado dos componentes (funcionando, travado, solto)
4. **Informe a orientação do dano (de frente para trás, da esquerda para a direta)
5. **Avalie a severidade** (leve, moderado, grave, crítico)
6. **Identifique possíveis causas** baseado no padrão do dano
7. **Use terminologia técnica automotiva** apropriada

FORMATO DA DESCRIÇÃO:
- Tipo de veículo e área afetada
- Descrição detalhada do dano
- Severidade e impacto funcional
- Observações técnicas relevantes"""

    # Se há contexto do ditado, adiciona ao prompt
    if contexto_ditado:
        prompt = f"""{prompt_base}

CONTEXTO DO DITADO PERICIAL:
{contexto_ditado}

ANÁLISE ESPECÍFICA:
- Correlacione o dano visual com as informações do ditado
- Destaque evidências que confirmem ou complementem as observações
- Identifique inconsistências entre o dano visual e o relato
- Avalie se o padrão do dano é compatível com a descrição do acidente

Descreva a imagem seguindo o formato especificado:"""
    else:
        prompt = prompt_base

    # Se há categoria específica, adiciona foco
    if categoria_dano:
        prompt += f"\n\nFOCO ESPECÍFICO: Analise especialmente os danos relacionados à categoria '{categoria_dano}'."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um perito criminal especializado em perícia veicular com vasta experiência em análise de danos automotivos."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base64}"}},
                ],
            },
        ],
        max_tokens=300,  # Aumentado para descrições técnicas mais detalhadas
    )
    return response.choices[0].message.content.strip()

# ... existing code ...


def listar_relatorios():
    """Retorna a lista de pastas de relatórios disponíveis."""
    return [nome for nome in os.listdir(PASTA_LAUDOS) if os.path.isdir(os.path.join(PASTA_LAUDOS, nome))]


def carregar_descricoes(pasta_relatorio):
    """Carrega o arquivo JSON com as descrições das imagens."""
    caminho_json = os.path.join(pasta_relatorio, "descricoes.json")

    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_descricoes(pasta_relatorio, descricoes):
    """Salva as descrições no arquivo JSON."""
    caminho_json = os.path.join(pasta_relatorio, "descricoes.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(descricoes, f, indent=4, ensure_ascii=False)


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


# Interface principal
st.title(" Perícia Veicular - Análise de Danos")
st.markdown("### Sistema especializado para constatação de danos veiculares")

# Selecionar relatório existente
relatorios_existentes = listar_relatorios()
relatorio_selecionado = st.sidebar.selectbox(
    "Selecionar Relatório", ["Nenhum"] + relatorios_existentes)

if relatorio_selecionado != "Nenhum":
    st.sidebar.markdown(f"### 📋 Relatório {relatorio_selecionado}")

    # Caminho da pasta do relatório selecionado
    pasta_relatorio = os.path.join(PASTA_LAUDOS, relatorio_selecionado)

    # Listar imagens na pasta
    imagens_existentes = [img for img in os.listdir(
        pasta_relatorio) if img.lower().endswith((".jpg", ".jpeg", ".png"))]

    # Carregar descrições salvas
    descricoes = carregar_descricoes(pasta_relatorio)

    # Extrair contexto do ditado pericial (Excel)
    contexto_ditado = ""
    contexto_fontes = []

    # Carregar ditado do Excel
    ditado_excel = carregar_ditado_excel(relatorio_selecionado)
    if ditado_excel:
        contexto_ditado = ditado_excel
        contexto_fontes.append("Excel: 1 observação")

    # Mostrar resumo do contexto disponível
    if contexto_fontes:
        st.sidebar.markdown("### 🎤 Contexto do Ditado")
        st.sidebar.info(
            f"**Fontes:** {' + '.join(contexto_fontes)} disponíveis para contextualizar as descrições")

        # Botão para visualizar o contexto completo
        if st.sidebar.button("👁️ Ver Contexto Completo"):
            st.sidebar.expander(
                "Contexto do Ditado Pericial").markdown(contexto_ditado)

    if imagens_existentes:
        st.markdown("###  Veículo em Análise")

        # Informação sobre o contexto disponível
        if contexto_ditado:
            st.success(
                f"✅ **Contexto disponível:** {' + '.join(contexto_fontes)} do ditado pericial serão consideradas na análise")
        else:
            st.warning(
                "⚠️ **Sem contexto:** Nenhum ditado pericial encontrado. A análise será baseada apenas na imagem.")

        # Seleção de categoria de dano para análise
        st.markdown("#### 🎯 Categoria de Dano (Opcional)")
        categoria_selecionada = st.selectbox(
            "Selecione a categoria principal do dano para focar a análise:",
            ["Geral (todas as categorias)"] + list(CATEGORIAS_DANOS.keys()),
            help="Selecionar uma categoria específica ajuda a focar a análise em aspectos particulares do dano"
        )

        colunas = st.columns(3)  # Organiza as imagens em colunas

        for i, imagem in enumerate(imagens_existentes):
            img_path = os.path.join(pasta_relatorio, imagem)
            img = Image.open(img_path)

            with colunas[i % 3]:  # Distribui entre colunas
                st.image(img, caption=imagem, use_container_width=True)

                # Botão para gerar descrição da imagem
                if st.button(f"🔍 Analisar {imagem}", key=f"desc_{imagem}"):
                    with st.spinner(f"Analisando danos em {imagem}..."):
                        # Determina a categoria para análise
                        categoria_analise = ""
                        if categoria_selecionada != "Geral (todas as categorias)":
                            categoria_analise = categoria_selecionada

                        # Passa o contexto do ditado e categoria para a função de descrição
                        descricao_gerada = descrever_imagem_veicular(
                            img_path, contexto_ditado, categoria_analise)
                        # Salva a nova descrição
                        descricoes[imagem] = descricao_gerada
                        salvar_descricoes(pasta_relatorio, descricoes)
                        st.rerun()  # Atualiza a página para exibir a descrição

    # Exibir e editar descrições já salvas
    if descricoes:
        st.markdown("### ⛓️‍💥 Relatório de Danos")

        # Se há contexto do ditado, mostrar correlações
        if contexto_ditado and any(img in descricoes for img in imagens_existentes):
            st.markdown("#### 🎤 Correlação com Ditado Pericial")
            st.info(
                f"As análises abaixo foram geradas considerando o contexto do ditado pericial, tornando-as mais precisas e relevantes para o caso.")

        for imagem, descricao in descricoes.items():
            # Pular se não for uma imagem (ex: ditado_pericia)
            if not imagem.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            st.markdown(f"**🚗 {imagem}**")

            # Mostrar a descrição em um text area editável
            nova_descricao = st.text_area(
                f"Análise de Danos - {imagem}",
                value=descricao,
                height=200,  # Aumentado para acomodar descrições técnicas mais longas
                key=f"desc_text_{imagem}",
                help="Edite a análise conforme necessário. As descrições são especializadas para perícia veicular."
            )

            # Botão para regenerar descrição com contexto atualizado
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"Reanalisar {imagem}", key=f"regenerar_{imagem}"):
                    with st.spinner(f"Reanalisando danos em {imagem}..."):
                        # Recarrega o contexto atualizado (Excel)
                        contexto_atualizado = ""

                        # Carregar ditado do Excel
                        ditado_excel = carregar_ditado_excel(
                            relatorio_selecionado)
                        if ditado_excel:
                            contexto_atualizado = ditado_excel

                        # Define o caminho da imagem para regenerar
                        img_path_regenerar = os.path.join(
                            pasta_relatorio, imagem)

                        # Determina a categoria para análise (usar a mesma selecionada anteriormente)
                        categoria_analise = ""
                        if categoria_selecionada != "Geral (todas as categorias)":
                            categoria_analise = categoria_selecionada

                        nova_descricao = descrever_imagem_veicular(
                            img_path_regenerar, contexto_atualizado, categoria_analise)
                        descricoes[imagem] = nova_descricao
                        salvar_descricoes(pasta_relatorio, descricoes)
                        st.rerun()

            st.divider()

        # Botão para salvar alterações nas descrições
        if st.button("💾 Salvar Todas as Análises"):
            novas_descricoes = {}
            for img in descricoes.keys():
                if img.lower().endswith((".jpg", ".jpeg", ".png")):
                    novas_descricoes[img] = st.session_state[f"desc_text_{img}"]

            salvar_descricoes(pasta_relatorio, novas_descricoes)
            st.success("✅ Todas as análises foram atualizadas com sucesso!")
            st.rerun()

    # Seção de estatísticas e resumo
    if imagens_existentes:
        st.markdown("### 📊 Resumo da Perícia Veicular")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_imagens = len(imagens_existentes)
            st.metric("Total de Imagens", total_imagens)

        with col2:
            imagens_analisadas = len(
                [img for img in imagens_existentes if img in descricoes])
            st.metric("Imagens Analisadas",
                      f"{imagens_analisadas}/{total_imagens}")

        with col3:
            # Verificar ditado do Excel
            ditado_excel = carregar_ditado_excel(relatorio_selecionado)
            total_ditados = 1 if ditado_excel else 0

            st.metric("Observações do Ditado",
                      f"{total_ditados} (Excel)")

        # Barra de progresso para análises
        if total_imagens > 0:
            progresso = imagens_analisadas / total_imagens
            st.progress(
                progresso, text=f"Progresso das análises: {imagens_analisadas}/{total_imagens}")

            if progresso == 1.0:
                st.success("🎉 Todas as imagens foram analisadas!")
            elif progresso > 0.5:
                st.info(
                    f"📈 {total_imagens - imagens_analisadas} imagens ainda precisam ser analisadas")
            else:
                st.warning(
                    f"⚠️ {total_imagens - imagens_analisadas} imagens ainda precisam ser analisadas")


else:
    st.warning(
        "⚠️ Selecione um relatório no painel lateral para começar a análise veicular.")

    # Instruções de uso especializadas
    st.markdown("### Como usar para Perícia Veicular:")
    st.markdown("""
    1. **Selecione um relatório** no painel lateral
    2. **Verifique o contexto** do ditado pericial disponível
    3. **Selecione categoria de dano** (opcional, para foco específico)
    4. **Analise as imagens** do veículo danificado
    5. **Gere análises técnicas** especializadas em danos automotivos
    """)

    st.markdown("### 🚗 Tipos de Danos Analisados:")
    for categoria, descricao in CATEGORIAS_DANOS.items():
        st.markdown(f"- **{categoria.title()}:** {descricao}")
