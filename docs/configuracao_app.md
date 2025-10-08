# Configuração do App no Dify

Este guia descreve passo a passo como criar, no Dify, um aplicativo de Workflow capaz de receber múltiplos arquivos, interpretar um
prompt do usuário, enviar as informações para um modelo GPT e responder com um resumo ou com gráficos baseados nos dados.

> **Dica:** Todas as strings de prompt e scripts mencionados abaixo estão neste repositório para facilitar o copiar/colar.

## 1. Criar o aplicativo de Workflow

1. Acesse o Dify e clique em **Create App** > **Workflow**.
2. Dê um nome, por exemplo, `Resumo e Gráficos com GPT`.
3. Selecione o provedor OpenAI (ou outro compatível) e escolha o modelo desejado (ex.: `gpt-4o` ou `gpt-4-turbo`).

## 2. Formulário de entrada

1. Clique no nó **Start** e configure os campos de entrada:
   - `prompt_usuario` (tipo `Paragraph`, obrigatório): instruções que o usuário deseja executar (resumir, gerar gráfico, etc.).
   - `arquivos` (tipo `File`, múltiplo, obrigatório): os arquivos que serão enviados para análise.
2. Opcionalmente, adicione um placeholder no prompt orientando o usuário a especificar se deseja **resumo** ou **gráfico**.

## 3. Ingestão e pré-processamento de arquivos

1. Adicione um nó **Code** (Python) chamado `Ingestão` logo após o Start.
2. Cole o conteúdo de [`workflow/snippets/ingestao_arquivos.py`](../workflow/snippets/ingestao_arquivos.py) no editor de código.
3. Configure as **Entradas** do nó:
   - `arquivos`: conecte ao campo `arquivos` do Start.
4. Configure as **Saídas** do nó (todas do tipo `string`):
   - `conteudo_concatenado`
   - `metadados`
   - `tabelas_disponiveis`

O script faz o parsing dos uploads aceitando `.txt`, `.md`, `.csv`, `.tsv`, `.json`, `.xlsx` e `.parquet`. Ele combina o conteúdo textual
em um único texto, além de detectar dados tabulares e disponibilizá-los em JSON para o bloco de geração de gráficos.

## 4. Definir a decisão entre resumo e gráfico

1. Adicione um nó **LLM** (por exemplo, `gpt-4o`) chamado `Roteador`.
2. Use como **Prompt** o texto abaixo (disponível em [`workflow/prompts/router.txt`](../workflow/prompts/router.txt)):

   ```text
   Você atua como um roteador de tarefas. Analise o pedido do usuário (`{{prompt_usuario}}`) e o conteúdo disponível nos arquivos.
   Responda apenas com `resumo` quando o usuário pedir sínteses ou insights textuais. Responda com `grafico` quando houver pedido
   explícito para gráficos, visualizações, charts, plotagens ou comparações numéricas que se beneficiem de gráficos.
   Se houver dúvidas, prefira `resumo`.
   ```

3. Conecte as **Entradas** do nó:
   - `prompt_usuario`: do Start
   - `conteudo_concatenado`: saída do nó Ingestão
4. Nas **Saídas**, crie um campo `tarefa` (tipo `string`) e utilize a resposta direta do modelo.

## 5. Branch para resumo

1. Adicione um nó **Condition** e defina:
   - Expressão: `{{Roteador.tarefa}} == "resumo"`
   - Ramo Verdadeiro: continuará para o nó `Resumo`
   - Ramo Falso: continuará para o nó `Geração de gráfico`

2. Crie um nó **LLM** chamado `Resumo` usando o modelo escolhido. Prompt sugerido (arquivo [`workflow/prompts/resumo.txt`](../workflow/prompts/resumo.txt)):

   ```text
   Você é um assistente especializado em análise de documentos. Utilize o conteúdo a seguir para gerar um resumo estruturado:

   ### Instruções do usuário
   {{prompt_usuario}}

   ### Conteúdo disponível
   {{Ingestão.conteudo_concatenado}}

   Produza uma resposta em Markdown com:
   - Visão geral (2-3 frases)
   - Principais pontos ou insights (lista numerada)
   - Caso o usuário peça recomendações ou próximos passos, inclua uma seção opcional "Recomendações".
   ```

3. Configure as entradas do nó:
   - `prompt_usuario`: Start
   - `conteudo_concatenado`: Ingestão
4. Defina a saída `resposta_texto` (string) com a mensagem retornada pelo LLM.

## 6. Branch para gráfico

1. Adicione um nó **Code** chamado `Preparar gráfico` após o caminho falso do Condition.
2. Cole o conteúdo de [`workflow/snippets/graficos.py`](../workflow/snippets/graficos.py).
3. Entradas do nó:
   - `prompt_usuario`: Start
   - `tabelas_disponiveis`: Ingestão
4. Saídas do nó:
   - `grafico_html` (string): gráfico interativo em HTML (Vega-Lite via Altair)
   - `explicacao` (string): explicação textual resumida

O script utiliza o modelo `altair` para transformar os dados em gráficos com base nas instruções do usuário. Ele também faz parsing de
pedidos comuns (linha, barra, pizza, dispersão) e suporta seleção de colunas.

## 7. Montar a resposta final

1. Após o Condition, adicione um nó **Response**.
2. Conecte o caminho verdadeiro (resumo) com o campo `mensagem` usando `Resumo.resposta_texto` (tipo `text`).
3. Conecte o caminho falso (gráfico) com dois blocos no Response:
   - `mensagem` (tipo `text`) usando `Preparar gráfico.explicacao`
   - `grafico` (tipo `rich_text`) contendo o HTML retornado pelo script (`Preparar gráfico.grafico_html`)

Assim, quando o usuário pedir um gráfico, ele receberá a explicação e o gráfico embutido (ou um link/base64 conforme o front-end).

## 8. Testes

- Faça upload de um arquivo `vendas.csv` (com colunas `mes`, `receita`) e use o prompt: "Crie um gráfico de linhas comparando a receita por mês". O fluxo deve retornar um gráfico de linha.
- Faça upload de um relatório `.txt` e solicite: "Resuma os principais insights". O fluxo deve seguir pelo ramo de resumo e retornar o texto estruturado.

## 9. Publicação

1. Clique em **Publish** para disponibilizar o app.
2. Use a interface de chat do Dify ou chame a API `/chat-messages` enviando o `prompt_usuario` e anexando os arquivos como `file_ids`.

## 10. Personalizações Sugeridas

- Ajuste o prompt do Roteador para suportar mais tipos de tarefas.
- Inclua um nó adicional de "Validação" para confirmar se os dados tabulares possuem colunas adequadas antes de gerar o gráfico.
- Adicione suporte a mais formatos de arquivo no script de ingestão (por exemplo, PDF usando PyPDF2).
- Crie um bloco de `Caching` para reutilizar resumos de documentos já analisados, economizando tokens.

## Referências

- [Documentação oficial do Dify](https://docs.dify.ai/)
- [Documentação do Altair](https://altair-viz.github.io/)
- [OpenAI API](https://platform.openai.com/docs/overview)
