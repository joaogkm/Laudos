# 🎤 Ditado de Perícia

## Descrição
A página `03_DitadoPericia.py` permite ao usuário ditar suas observações da cena de crime, que são transcritas automaticamente para texto e salvas para posterior análise e inclusão no relatório final.

## Funcionalidades

### 🎙️ Transcrição de Áudio
- **Upload de arquivos de áudio**: WAV, MP3, M4A, OGG
- **Transcrição automática**: Usando Google Speech Recognition
- **Idioma**: Português brasileiro (pt-BR)
- **Visualização**: Player de áudio integrado

### ✍️ Entrada Manual
- **Campo de texto**: Para digitação direta de observações
- **Interface intuitiva**: Área de texto com placeholder
- **Validação**: Impede salvamento de texto vazio

### 📋 Gerenciamento de Ditados
- **Histórico completo**: Lista todos os ditados salvos
- **Metadados**: Data/hora, arquivo original, tipo
- **Exclusão individual**: Remove ditados específicos
- **Estatísticas**: Contador de ditados e caracteres

### 💾 Armazenamento
- **Formato JSON**: Estrutura organizada e legível
- **Localização**: Arquivo `descricoes.json` na pasta do relatório
- **Estrutura**:
```json
{
  "ditado_pericia": [
    {
      "data_hora": "2025-01-27 14:30:00",
      "texto": "Texto transcrito ou digitado",
      "arquivo_original": "audio.wav",
      "tipo": "manual"
    }
  ]
}
```

## Como Usar

### 1. Selecionar Relatório
- Escolha um relatório existente no painel lateral
- A página só funciona com um relatório selecionado

### 2. Transcrição de Áudio
1. Clique em "Carregar arquivo de áudio"
2. Selecione um arquivo de áudio (WAV, MP3, M4A, OGG)
3. Clique em "🎤 Transcrever Áudio"
4. Aguarde a transcrição
5. Revise o texto transcrito
6. Clique em "💾 Salvar Transcrição"

### 3. Entrada Manual
1. Digite suas observações no campo de texto
2. Clique em "💾 Salvar Observação Manual"

### 4. Visualizar Histórico
- Todos os ditados salvos aparecem em expansores
- Clique para expandir e ver detalhes
- Use o botão "🗑️ Excluir" para remover ditados

## Requisitos Técnicos

### Dependências
```bash
pip install SpeechRecognition PyAudio
```

### Configuração do Sistema
- **Microfone**: Funcional para gravação (se usar gravação direta)
- **Internet**: Necessária para transcrição via Google Speech Recognition
- **Permissões**: Acesso ao microfone (se aplicável)

## Integração com Relatório Final

Os ditados salvos são automaticamente incluídos no relatório final através do arquivo `descricoes.json`, que é lido pelas outras páginas do sistema para gerar o documento final.

## Dicas de Uso

### Para Melhor Transcrição
1. **Fale claramente**: Articule bem as palavras
2. **Ambiente silencioso**: Evite ruídos de fundo
3. **Volume adequado**: Não muito baixo nem muito alto
4. **Formato de áudio**: WAV oferece melhor qualidade

### Para Observações Eficazes
1. **Seja específico**: Descreva detalhes importantes
2. **Use linguagem técnica**: Termos periciais apropriados
3. **Organize o pensamento**: Estruture suas observações
4. **Revise antes de salvar**: Corrija erros de transcrição

## Solução de Problemas

### Erro de Transcrição
- Verifique a qualidade do áudio
- Tente falar mais claramente
- Confirme conexão com internet
- Teste com arquivo de áudio diferente

### Erro de Salvamento
- Verifique se um relatório está selecionado
- Confirme que o texto não está vazio
- Verifique permissões de escrita na pasta

### Problemas de Áudio
- Teste o arquivo em outro player
- Converta para formato WAV se necessário
- Verifique se o arquivo não está corrompido

## Estrutura de Arquivos

```
relatorios/
└── [ID_RELATORIO]/
    ├── descricoes.json          # Ditados salvos
    ├── [imagens].jpg           # Fotos do caso
    └── relatorio_gerado.docx   # Relatório final
```

## Contribuição

Para melhorias ou correções:
1. Teste a funcionalidade
2. Documente mudanças
3. Mantenha compatibilidade com outras páginas
4. Atualize este README se necessário 