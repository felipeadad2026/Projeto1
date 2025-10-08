# Exemplo de consumo do workflow via API do Dify

Este guia mostra como enviar apenas um prompt de texto para o workflow e recuperar a resposta retornada pela LLM. Os exemplos
refletem o comportamento do blueprint [`../workflow/dify_app.yml`](../workflow/dify_app.yml), derivado de um export válido do Dify.

## Pré-requisitos

- Workflow publicado no Dify com o campo `prompt_usuario` conforme o blueprint [`../workflow/dify_app.yml`](../workflow/dify_app.yml);
- Uma API Key de **Server-side** obtida na interface do Dify;
- Python 3.9+ instalado no ambiente local com a biblioteca `requests` (caso utilize o script fornecido).

## 1. Instalando dependências

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests
```

## 2. Enviando prompt via script Python

Use o script [`scripts/enviar_para_dify.py`](../scripts/enviar_para_dify.py). Ele envia o prompt diretamente para o endpoint
`/v1/workflows/run` e imprime a resposta completa em JSON.

### Uso

```bash
python scripts/enviar_para_dify.py \
  <WORKFLOW_ID> \
  "Explique em poucas linhas o que é o Dify" \
  --base-url "https://api.sua-instancia-dify.com" \
  --api-key "SEU_API_KEY"
```

Substitua `WORKFLOW_ID` pelo identificador do workflow exibido na interface do Dify e adapte o prompt conforme necessário.

## 3. Consumindo via `curl`

Se preferir fazer a chamada manualmente:

```bash
curl -X POST "https://api.sua-instancia-dify.com/v1/workflows/run" \
  -H "Authorization: Bearer SEU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "WORKFLOW_ID",
    "inputs": {
      "prompt_usuario": "Gere uma lista de ideias para um workshop"
    },
    "response_mode": "blocking"
  }'
```

A resposta conterá o JSON do workflow, incluindo o texto retornado pelo nó Answer. No blueprint fornecido, você encontrará o
conteúdo em `data.outputs["2003"].result`.

## 4. Dicas adicionais

- Ajuste os parâmetros do nó LLM (temperatura, max tokens) diretamente no Dify se quiser respostas mais criativas ou concisas.
- Para registrar apenas a mensagem final, você pode extrair `data.outputs["2002"].text`, que é a saída bruta do nó LLM.
- Utilize `response_mode: streaming` se desejar receber tokens gradualmente (lembre-se de adaptar o cliente HTTP para lidar com
  stream).
