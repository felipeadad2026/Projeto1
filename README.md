# Aplicativo Dify para Resumo e Visualização de Arquivos

Este repositório contém os artefatos necessários para configurar, no Dify, um aplicativo de Workflow capaz de:

1. Receber uma lista de arquivos (upload pelo usuário ou via API);
2. Receber um prompt com a tarefa desejada;
3. Preparar o conteúdo dos arquivos e encaminhar para um modelo da OpenAI (GPT-4o/GPT-3.5, etc.);
4. Retornar um resumo textual ou gerar gráficos de acordo com o pedido do usuário.

O objetivo é fornecer um blueprint reproduzível que possa ser importado e customizado em uma instância Dify autogerenciada ou na nuvem. As instruções completas estão em [`docs/configuracao_app.md`](docs/configuracao_app.md) e incluem os detalhes de cada nó do workflow, prompts recomendados e scripts auxiliares em Python para processamento dos arquivos e criação das visualizações.

## Estrutura do Repositório

```
├── docs/
│   └── configuracao_app.md  # Tutorial detalhado para criar o app no Dify
├── workflow/
│   ├── blueprint.json       # Blueprint exportável do workflow
│   └── snippets/
│       ├── ingestao_arquivos.py  # Script de nó "Code" para leitura e junção dos arquivos
│       └── graficos.py           # Script de nó "Code" para gerar gráficos a partir de dados tabulares
├── scripts/
│   └── enviar_para_dify.py  # Script CLI para disparar o workflow via API
└── README.md
```

## Pré-requisitos

Antes de importar o blueprint ou montar o fluxo manualmente, garanta que:

- Você tem acesso a uma instância do [Dify](https://dify.ai/) com suporte a aplicativos do tipo **Workflow**;
- Uma credencial da OpenAI (ou outro provedor compatível) está configurada no Dify;
- O ambiente de execução de blocos de código Python possui as bibliotecas `pandas`, `numpy`, `altair` e `vega_datasets` disponíveis. Caso use Dify autogerenciado, instale-as no contêiner de execução de código.

## Como usar

1. Leia o guia em [`docs/configuracao_app.md`](docs/configuracao_app.md) para entender a arquitetura e, se necessário, montar o fluxo manualmente pela interface do Dify.
2. Consulte [`docs/exemplo_uso_api.md`](docs/exemplo_uso_api.md) para aprender como anexar arquivos e executar o workflow via API.
3. Se desejar importar diretamente, utilize o arquivo [`workflow/blueprint.json`](workflow/blueprint.json) através da funcionalidade **Import Workflow** do Dify.
4. Ajuste o prompt do bloco de LLM para adequar o tom/idioma desejado ou para trabalhar com modelos específicos.
5. Publique o aplicativo e utilize a interface de chat ou a API (com o script [`scripts/enviar_para_dify.py`](scripts/enviar_para_dify.py)) para enviar o prompt, anexar os arquivos e receber o resumo ou gráfico retornado.

## Como enviar este projeto para o GitHub

Caso queira publicar este repositório em uma conta do GitHub, siga o passo a passo:

1. Crie um repositório vazio no GitHub (sem README inicial) ou escolha um repositório existente onde deseja enviar os arquivos.
2. No terminal deste projeto, verifique o status do Git e confirme os arquivos versionados:

   ```bash
   git status
   ```

3. Configure o repositório remoto apontando para a URL HTTPS ou SSH do projeto no GitHub:

   ```bash
   git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
   # ou, usando SSH:
   git remote add origin git@github.com:<seu-usuario>/<seu-repo>.git
   ```

   > Se o nome `origin` já existir, atualize-o com `git remote set-url origin <URL>`.

4. Envie o conteúdo da branch atual para o GitHub. Caso deseje usar a branch `main` (ou outra), ajuste o comando conforme necessário:

   ```bash
   git push -u origin main
   ```

5. Após o envio, confirme no GitHub que os arquivos foram carregados. A partir daí, utilize `git push` para novas atualizações e `git pull` para sincronizar alterações feitas diretamente no GitHub.

## Licença

Distribuído sob a licença MIT.
