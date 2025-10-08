"""Cliente CLI simples para disparar o workflow do Dify enviando apenas um prompt de texto."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict

import requests


def run_workflow(base_url: str, api_key: str, workflow_id: str, prompt: str) -> Dict[str, Any]:
    """Executa o workflow mínimo que consome apenas o campo `prompt_usuario`."""
    url = f"{base_url.rstrip('/')}/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "workflow_id": workflow_id,
        "inputs": {
            "prompt_usuario": prompt,
        },
        "response_mode": "blocking",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    response.raise_for_status()
    return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Envia apenas um prompt para o workflow do Dify.")
    parser.add_argument("workflow_id", help="Identificador do workflow disponível no Dify")
    parser.add_argument("prompt", help="Prompt a ser enviado ao modelo")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("DIFY_BASE_URL", "https://api.dify.ai"),
        help="URL base da instância Dify (padrão: https://api.dify.ai)",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("DIFY_API_KEY"),
        help="API Key do Dify. Pode ser informada via variável de ambiente DIFY_API_KEY.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.api_key:
        raise SystemExit("API Key não fornecida. Use --api-key ou defina DIFY_API_KEY.")

    result = run_workflow(args.base_url, args.api_key, args.workflow_id, args.prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
