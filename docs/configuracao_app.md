# Configuração do App no Dify

Este guia explica como criar, no Dify, um workflow mínimo que recebe um prompt de texto, envia para uma LLM da OpenAI e mostra a
resposta na interface do app.

Caso prefira importar tudo pronto, utilize o arquivo [`../workflow/dify_app.yml`](../workflow/dify_app.yml).

## 1. Criar o aplicativo de Workflow

1. Acesse o Dify e clique em **Create App** > **Workflow**.
2. Escolha um nome, por exemplo, `Perguntas para GPT`.
3. Defina o provedor como OpenAI (ou outro compatível) e selecione o modelo que deseja usar (ex.: `gpt-4o-mini`, `gpt-3.5-turbo`).

## 2. Configurar o nó Start

1. Clique no nó **Start**.
2. Adicione um campo chamado `prompt_usuario`:
   - Tipo: `Paragraph` (texto longo);
   - Obrigatório: `Yes`;
   - Label sugerido: "Sua pergunta".
3. Não é necessário adicionar campos de upload ou outras variáveis.

## 3. Adicionar o nó de LLM

1. Arraste um nó **LLM** para o canvas e conecte a saída do Start à entrada do LLM.
2. Configure o modelo (provider OpenAI, modelo conforme disponível na sua conta).
3. Use o prompt abaixo como ponto de partida:

   ```text
   Você é um assistente útil que responde diretamente às solicitações do usuário.

   {{#1001.prompt_usuario#}}
   ```

   > O identificador `1001` corresponde ao nó Start exportado pelo Dify. Caso tenha criado o fluxo manualmente, basta inserir a
   > variável de entrada usando o botão `Insert variable`.

4. Ajuste parâmetros como temperatura ou limite de tokens conforme preferência.

## 4. Exibir a resposta

1. Adicione um nó **Answer** após o LLM e conecte a saída do LLM à entrada do Answer.
2. Em **Answer**, informe `{{#LLMNode.text#}}` (ou selecione a saída `text` do nó LLM pela interface).
3. Opcionalmente, personalize o título exibido no Answer.

## 5. Publicar e testar

1. Clique em **Publish** para disponibilizar o app.
2. Acesse a aba **Debug & Test** ou a interface pública do aplicativo.
3. Digite qualquer pergunta no campo `prompt_usuario` e verifique se a resposta retornada é exibida diretamente.

## Dica

Se desejar trocar o modelo ou personalizar a voz da resposta (Text-to-Speech), basta ajustar as configurações do nó LLM ou ativar
os recursos correspondentes no painel de features do workflow.
