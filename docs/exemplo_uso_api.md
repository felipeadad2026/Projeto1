# Exemplo de consumo do workflow via API do Dify

Este guia mostra como enviar arquivos e um prompt para o workflow a partir de uma aplicação externa.

## Pré-requisitos

- Workflow configurado no Dify com os campos `prompt_usuario` e `arquivos` conforme o blueprint fornecido.
- Uma API Key de **Server-side** obtida na interface do Dify.
- Python 3.9+ instalado no ambiente local com a biblioteca `requests`.

## 1. Instalando dependências

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests
```

## 2. Enviando arquivos e prompt via script Python

Utilize o script [`scripts/enviar_para_dify.py`](../scripts/enviar_para_dify.py) fornecido neste repositório. Ele realiza:

1. Upload de cada arquivo para o endpoint `/v1/files/upload`;
2. Execução do workflow através do endpoint `/v1/workflows/run` com `response_mode` igual a `blocking`;
3. Impressão da resposta completa em JSON.

### Uso

```bash
python scripts/enviar_para_dify.py \
  <WORKFLOW_ID> \
  "Elabore um resumo executivo dos documentos" \
  dados/relatorio_financeiro.xlsx anexos/resumo.txt \
  --base-url "https://api.sua-instancia-dify.com" \
  --api-key "SEU_API_KEY"
```

Substitua `WORKFLOW_ID` pelo identificador do workflow (disponível na interface do Dify) e adapte o prompt conforme a tarefa desejada. O script aceita múltiplos arquivos na mesma execução.

## 3. Consumindo via `curl`

Caso prefira uma chamada manual, o fluxo é dividido em duas etapas.

### 3.1 Upload dos arquivos

```bash
curl -X POST "https://api.sua-instancia-dify.com/v1/files/upload" \
  -H "Authorization: Bearer SEU_API_KEY" \
  -F "file=@anexos/resumo.txt"
```

A resposta conterá um `id`. Repita para cada arquivo que desejar anexar e guarde os `id`s.

### 3.2 Execução do workflow

```bash
curl -X POST "https://api.sua-instancia-dify.com/v1/workflows/run" \
  -H "Authorization: Bearer SEU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "WORKFLOW_ID",
    "inputs": {
      "prompt_usuario": "Construa um gráfico com base nos dados fornecidos",
      "arquivos": [
        {"type": "file", "file_id": "ID_DO_ARQUIVO"}
      ]
    },
    "response_mode": "blocking"
  }'
```

A resposta incluirá o texto resumido ou o HTML do gráfico, conforme o roteamento configurado no workflow.

## 4. Tratamento da resposta

O workflow retorna um JSON. Para tarefas de resumo, o texto principal estará no campo `data.outputs.resumo.resposta_texto`. Para tarefas de gráfico, utilize o `data.outputs.graficos.explicacao` para a descrição e `data.outputs.graficos.grafico_html` para o conteúdo visual.

## 5. Dicas adicionais

- Quando o arquivo for tabular, forneça instruções claras sobre o tipo de gráfico desejado.
- Para arquivos grandes, considere resumir ou limpar os dados previamente para reduzir o custo de tokens.
- Guarde os `file_id`s retornados pelo upload caso queira reutilizar o mesmo arquivo em múltiplas execuções.
- Em ambientes autogerenciados, valide se o backend do Dify está com suporte a uploads habilitado.
