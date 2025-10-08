"""Exemplo de cliente Python para enviar arquivos e prompt ao workflow do Dify."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable, List

import requests


def upload_file(base_url: str, api_key: str, file_path: Path) -> str:
    """Realiza o upload de um arquivo para a API do Dify e retorna o file_id."""
    url = f"{base_url.rstrip('/')}/v1/files/upload"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    with file_path.open("rb") as file_handle:
        files = {"file": (file_path.name, file_handle)}
        response = requests.post(url, headers=headers, files=files, timeout=120)
    response.raise_for_status()
    payload = response.json()
    file_id = payload.get("data", {}).get("id") or payload.get("id")
    if not file_id:
        raise RuntimeError(f"Resposta inesperada ao enviar {file_path}: {payload}")
    return file_id


def run_workflow(base_url: str, api_key: str, workflow_id: str, prompt: str, file_ids: Iterable[str]) -> dict:
    """Executa o workflow com o prompt informado e os IDs dos arquivos."""
    url = f"{base_url.rstrip('/')}/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "workflow_id": workflow_id,
        "inputs": {
            "prompt_usuario": prompt,
            "arquivos": [
                {"type": "file", "file_id": file_id}
                for file_id in file_ids
            ],
        },
        "response_mode": "blocking",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    response.raise_for_status()
    return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Envia prompt e arquivos para o workflow do Dify.")
    parser.add_argument("workflow_id", help="Identificador do workflow disponível no Dify")
    parser.add_argument("prompt", help="Prompt a ser enviado ao modelo")
    parser.add_argument("files", nargs="+", help="Lista de caminhos de arquivos a anexar")
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

    file_paths: List[Path] = [Path(path) for path in args.files]
    missing = [str(path) for path in file_paths if not path.exists()]
    if missing:
        raise SystemExit(f"Arquivos não encontrados: {', '.join(missing)}")

    file_ids = [upload_file(args.base_url, args.api_key, path) for path in file_paths]
    result = run_workflow(args.base_url, args.api_key, args.workflow_id, args.prompt, file_ids)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
