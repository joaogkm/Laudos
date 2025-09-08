# 🔗 Integração Ditado Pericial + Descrição de Fotos

## 📋 Visão Geral

O sistema agora integra automaticamente as informações do **ditado pericial** com a **descrição de fotos**, tornando o processo muito mais eficiente e contextualizado. As descrições geradas são mais precisas, relevantes e alinhadas com o contexto do caso.

## ✨ Novas Funcionalidades

### 1. **Contexto Inteligente**
- As descrições das imagens agora consideram automaticamente todas as observações do ditado pericial
- O sistema extrai e concatena todas as observações para fornecer contexto rico
- Descrições mais focadas e relevantes para o caso específico

### 2. **Prompt Contextualizado**
- Prompt baseado no contexto do ditado pericial
- Instruções específicas para peritos criminais
- Foco em elementos que corroboram ou complementam as observações
- Linguagem forense apropriada

### 3. **Interface Melhorada**
- Indicadores visuais de contexto disponível
- Botão para visualizar contexto completo
- Estatísticas de progresso das descrições
- Botão de regeneração com contexto atualizado

### 4. **Correlação Automática**
- Identificação de elementos mencionados no ditado
- Destaque de correlações entre texto e imagem
- Consistência entre observações e descrições

## 🎯 Como Funciona

### **Fluxo de Trabalho:**

1. **Ditado Pericial** → Usuário registra observações via áudio ou texto
2. **Contexto Extração** → Sistema extrai e organiza todas as observações
3. **Análise de Imagem** → IA analisa imagem considerando o contexto
4. **Descrição Contextualizada** → Gera descrição técnica e relevante
5. **Edição e Refinamento** → Usuário pode editar e regenerar descrições

### **Exemplo de Prompt Contextualizado:**

```
Você é um perito criminal analisando uma imagem de cena de crime.

CONTEXTO DO DITADO PERICIAL:
[Observações do usuário sobre o caso]

INSTRUÇÕES:
1. Analise a imagem considerando o contexto fornecido
2. Foque nos elementos que corroboram ou complementam as observações do ditado
3. Descreva detalhadamente: cores, objetos, disposição espacial, evidências visíveis
4. Se a imagem mostrar algo mencionado no ditado, destaque essa correlação
5. Seja objetivo, técnico e preciso na descrição
6. Use linguagem forense apropriada
```

## 🚀 Benefícios

### **Para Peritos:**
- ⚡ **Eficiência:** Menos tempo editando descrições
- 🎯 **Precisão:** Foco em elementos relevantes para o caso
- 🔗 **Contexto:** Descrições alinhadas com observações
- 📝 **Consistência:** Padrão uniforme nas descrições

### **Para o Sistema:**
- 🔍 **Qualidade:** Descrições mais técnicas e forenses
- 📊 **Rastreabilidade:** Correlação clara entre ditado e fotos
- 🎨 **Interface:** Experiência mais intuitiva e informativa
- 📈 **Progresso:** Acompanhamento visual do trabalho

## 📱 Interface do Usuário

### **Painel Lateral:**
- 📝 **Contexto do Ditado:** Mostra quantas observações estão disponíveis
- 👁️ **Ver Contexto Completo:** Botão para visualizar todas as observações

### **Área Principal:**
- ✅ **Indicador de Contexto:** Mostra se há contexto disponível
- 📸 **Visualização de Imagens:** Organizadas em colunas
- 🔄 **Botão Regenerar:** Para atualizar descrições com contexto atualizado
- 📊 **Estatísticas:** Progresso das descrições e métricas

### **Seção de Descrições:**
- 🔗 **Correlação:** Explica como as descrições consideram o contexto
- ✏️ **Edição:** Campos editáveis para refinamento
- 💾 **Salvamento:** Botão para salvar todas as alterações

## 🔧 Configurações Técnicas

### **Modelo de IA:**
- **Modelo:** GPT-4o-mini
- **Tokens:** 400 (aumentado para descrições mais detalhadas)
- **Sistema:** Perito criminal com precisão técnica e forense

### **Estrutura de Dados:**
```json
{
  "imagem1.jpg": "Descrição contextualizada...",
  "imagem2.jpg": "Descrição contextualizada...",
  "ditado_pericia": [
    {
      "data_hora": "2025-01-XX XX:XX:XX",
      "texto": "Observação do perito...",
      "tipo": "manual/audio"
    }
  ]
}
```

## 📖 Instruções de Uso

### **1. Preparação:**
- Certifique-se de ter registrado observações no ditado pericial
- Selecione o relatório correto no painel lateral

### **2. Geração de Descrições:**
- Clique em "Descrever [nome_imagem]" para cada foto
- O sistema automaticamente considerará o contexto do ditado
- Aguarde a análise da IA

### **3. Edição e Refinamento:**
- Revise as descrições geradas
- Use o botão "Regenerar" se necessário
- Edite manualmente conforme necessário

### **4. Salvamento:**
- Clique em "Salvar Todas as Alterações"
- Confirme que as alterações foram salvas

## 🔍 Casos de Uso

### **Cena de Crime:**
- Ditado: "Veículo com danos na lateral esquerda"
- Foto: Imagem do veículo
- Descrição: Foca nos danos mencionados, detalhando localização e extensão

### **Evidências:**
- Ditado: "Manchas de sangue no asfalto"
- Foto: Imagem da rua
- Descrição: Destaque das manchas, padrão de distribuição, cores

### **Local:**
- Ditado: "Poste de iluminação danificado"
- Foto: Imagem do poste
- Descrição: Análise dos danos, altura, tipo de poste

## 🚨 Considerações Importantes

### **Dependências:**
- Arquivo `.env` com chave da API OpenAI
- Conexão com internet para análise de IA
- Relatório com ditado pericial registrado

### **Limitações:**
- Qualidade da descrição depende da qualidade do ditado
- Contexto muito extenso pode limitar tokens disponíveis
- Necessidade de revisão humana para validação final

### **Recomendações:**
- Mantenha o ditado pericial atualizado
- Revise sempre as descrições geradas
- Use o botão regenerar quando houver novas observações
- Salve as alterações regularmente

## 🔄 Atualizações Futuras

### **Funcionalidades Planejadas:**
- Análise de múltiplas imagens simultaneamente
- Sugestões de correlação automática
- Templates de descrição por tipo de evidência
- Integração com outros módulos do sistema

---

**Desenvolvido para melhorar a eficiência e precisão dos laudos periciais através da integração inteligente de contexto e análise de imagens.** 