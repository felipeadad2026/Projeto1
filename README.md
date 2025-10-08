# Aplicativo Dify para Perguntas Diretas à LLM

Este repositório reúne os artefatos necessários para importar ou reconstruir, no Dify, um workflow bem simples: receber um texto
de entrada, encaminhar para um modelo da OpenAI e exibir exatamente a resposta retornada pela LLM.

O objetivo é fornecer um ponto de partida mínimo para quem só precisa de uma interface estilo chat, sem campos de upload ou
roteamento complexo.

## Estrutura do Repositório

```
├── docs/
│   ├── configuracao_app.md   # Passo a passo para montar o fluxo manualmente no Dify
│   └── exemplo_uso_api.md    # Como chamar o workflow via API
├── scripts/
│   └── enviar_para_dify.py   # Script CLI que dispara o workflow informando apenas o prompt
├── workflow/
│   └── dify_app.yml          # Export em DSL v0.4.0 pronto para importação
└── README.md
```

## Pré-requisitos

Antes de importar o blueprint ou recriar o fluxo manualmente, confirme que:

- Você possui acesso a uma instância do [Dify](https://dify.ai/) com suporte a aplicativos do tipo **Workflow**;
- Um provedor OpenAI (ou compatível) está configurado na instância do Dify para uso nos blocos de LLM;
- Você tem uma API Key de **Server-side** para testar o fluxo via API, se desejar.

## Como usar

1. Para entender cada passo e montar o fluxo manualmente, siga o guia em [`docs/configuracao_app.md`](docs/configuracao_app.md).
2. Se preferir importar tudo pronto, utilize o arquivo [`workflow/dify_app.yml`](workflow/dify_app.yml) na função **Import Workflow**
   do Dify.
3. Para disparar o workflow por API, consulte [`docs/exemplo_uso_api.md`](docs/exemplo_uso_api.md) ou execute o script
   [`scripts/enviar_para_dify.py`](scripts/enviar_para_dify.py).
4. Publique o aplicativo e utilize a interface de chat ou a API para enviar o prompt de texto e receber a resposta da LLM.

## Como enviar este projeto para o GitHub

Caso deseje publicar este repositório em uma conta do GitHub, siga os passos abaixo:

1. Crie um repositório vazio no GitHub (sem README inicial) ou escolha um repositório existente onde deseja enviar os arquivos.
2. No terminal deste projeto, verifique o status do Git para confirmar os arquivos versionados:

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

4. Envie o conteúdo da branch atual para o GitHub. Caso deseje usar a branch `main` (ou outra), ajuste o comando conforme
   necessário:

   ```bash
   git push -u origin main
   ```

5. Após o envio, confirme no GitHub que os arquivos foram carregados. A partir daí, utilize `git push` para novas atualizações e
   `git pull` para sincronizar alterações feitas diretamente no GitHub.

## Licença

Distribuído sob a licença MIT.
