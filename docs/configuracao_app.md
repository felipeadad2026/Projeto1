# Configuração do App no Dify

Este guia explica como criar, no Dify, um workflow mínimo que recebe um prompt de texto, envia para uma LLM da OpenAI e mostra a
resposta na interface do app. O fluxo descrito reflete fielmente o arquivo [`../workflow/dify_app.yml`](../workflow/dify_app.yml),
que foi modelado com base em um export válido fornecido pelo próprio Dify.

Caso prefira importar tudo pronto, utilize o arquivo [`../workflow/dify_app.yml`](../workflow/dify_app.yml).

## 1. Criar o aplicativo de Workflow

1. Acesse o Dify e clique em **Create App** > **Workflow**.
2. Escolha um nome, por exemplo, `Perguntas para GPT`.
3. Defina o provedor como OpenAI (ou outro compatível) e selecione o modelo que deseja usar (ex.: `gpt-4o-mini`, `gpt-3.5-turbo`).
   > O blueprint já referencia o plugin de marketplace `langgenius/openai:0.2.6`. Ao montar manualmente, basta garantir que o mesmo
   > provedor esteja configurado na sua instância.

## 2. Configurar o nó Start

1. Clique no nó **Start**.
2. Adicione um campo chamado `prompt_usuario`:
   - Tipo: `Text Input` (texto curto);
   - Placeholder sugerido: "Descreva o que deseja perguntar à LLM";
   - Obrigatório: `Yes`;
   - Label sugerido: "Prompt do usuário".
3. Não é necessário adicionar campos de upload ou outras variáveis.

## 3. Adicionar o nó de LLM

1. Arraste um nó **LLM** para o canvas e conecte a saída do Start à entrada do LLM.
2. Configure o modelo (provider OpenAI, modelo conforme disponível na sua conta).
3. Use o prompt abaixo como ponto de partida:

   ```text
   Você é um assistente útil que responde diretamente às solicitações do usuário.

   {{#2001.prompt_usuario#}}
   ```

   > O identificador `2001` corresponde ao nó Start exportado pelo Dify. Caso tenha criado o fluxo manualmente, basta inserir a
   > variável de entrada usando o botão `Insert variable`.

4. Ajuste parâmetros como temperatura ou limite de tokens conforme preferência. No blueprint importado, os principais ajustes são:
   - Temperatura: `0.5`;
   - `top_p`: `0.85`;
   - Penalidades de frequência/presença zeradas;
   - `response_format` definido como `text`.

## 4. Exibir a resposta

1. Adicione um nó **Answer** após o LLM e conecte a saída do LLM à entrada do Answer.
2. Em **Answer**, informe `{{#LLMNode.text#}}` (ou selecione a saída `text` do nó LLM pela interface). No arquivo exportado, o nó
   final (id `2003`) expõe a variável `result`, que já encapsula essa saída.
3. Opcionalmente, personalize o título exibido no Answer.

## 5. Publicar e testar

1. Clique em **Publish** para disponibilizar o app.
2. Acesse a aba **Debug & Test** ou a interface pública do aplicativo.
3. Digite qualquer pergunta no campo `prompt_usuario` e verifique se a resposta retornada é exibida diretamente.

## Dica

Se desejar trocar o modelo ou personalizar a voz da resposta (Text-to-Speech), basta ajustar as configurações do nó LLM ou ativar
os recursos correspondentes no painel de features do workflow.
