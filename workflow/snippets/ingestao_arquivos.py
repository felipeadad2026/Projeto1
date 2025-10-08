"""Script para nó de código no Dify responsável por ler os arquivos enviados.

Entradas esperadas (inputs):
- "arquivos": lista de objetos representando os uploads. O script tenta utilizar os campos
  `path`, `local_file`, `tmp_file_path` ou `url` para obter o conteúdo.

Saídas (outputs):
- "conteudo_concatenado": texto único com o conteúdo textual dos arquivos.
- "metadados": JSON com informações de cada arquivo processado.
- "tabelas_disponiveis": JSON com tabelas em formato consistente para uso posterior.
"""

from __future__ import annotations

import io
import json
import os
from typing import Any, Dict, List, Tuple

import pandas as pd

TEXT_EXTENSIONS = {"txt", "md", "markdown", "log"}
TABULAR_EXTENSIONS = {"csv", "tsv", "json", "xlsx", "xls", "parquet"}


def _read_file_bytes(file_info: Dict[str, Any]) -> Tuple[bytes | None, str]:
    """Tenta obter os bytes do arquivo a partir de diferentes campos."""
    possible_keys = [
        "path",
        "local_file",
        "local_path",
        "tmp_file_path",
        "tmp_path",
    ]
    for key in possible_keys:
        path = file_info.get(key)
        if path and os.path.exists(path):
            with open(path, "rb") as file:
                return file.read(), file_info.get("name", os.path.basename(path))

    url = file_info.get("url") or file_info.get("download_url")
    if url:
        import requests  # type: ignore

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content, file_info.get("name", os.path.basename(url))

    content = file_info.get("content")
    if content:
        return content.encode("utf-8"), file_info.get("name", "conteudo_inline.txt")

    return None, file_info.get("name", "desconhecido")


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8", "latin-1", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def _load_tabular(data: bytes, extension: str) -> pd.DataFrame:
    buffer = io.BytesIO(data)
    if extension == "csv":
        return pd.read_csv(buffer)
    if extension == "tsv":
        return pd.read_csv(buffer, sep="\t")
    if extension == "json":
        return pd.read_json(buffer)
    if extension in {"xlsx", "xls"}:
        return pd.read_excel(buffer)
    if extension == "parquet":
        return pd.read_parquet(buffer)
    raise ValueError(f"Extensão de tabela não suportada: {extension}")


def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    arquivos_entrada = inputs.get("arquivos") or []
    if isinstance(arquivos_entrada, list):
        arquivos = list(arquivos_entrada)
    elif arquivos_entrada:
        raise ValueError("Esperava-se uma lista de arquivos em 'arquivos'.")
    else:
        arquivos = []

    anexos_start = inputs.get("anexos_start") or []
    if isinstance(anexos_start, list):
        arquivos.extend(anexos_start)
    elif anexos_start:
        raise ValueError("Esperava-se uma lista de arquivos em 'anexos_start'.")

    textos: List[str] = []
    tabelas: Dict[str, List[Dict[str, Any]]] = {}
    metadados: List[Dict[str, Any]] = []

    for arquivo in arquivos:
        data, nome = _read_file_bytes(arquivo)
        if not data:
            metadados.append({"nome": nome, "status": "falha", "motivo": "Não foi possível ler o arquivo."})
            continue

        extension = arquivo.get("extension") or nome.split(".")[-1].lower()
        extension = extension.lower()

        registro_metadado = {"nome": nome, "extensao": extension}

        try:
            if extension in TEXT_EXTENSIONS:
                texto = _decode_text(data)
                textos.append(f"\n\n# Arquivo: {nome}\n{texto}")
                registro_metadado["tipo"] = "texto"
            elif extension in TABULAR_EXTENSIONS:
                df = _load_tabular(data, extension)
                registros = df.to_dict(orient="records")
                tabelas[nome] = registros
                registro_metadado["tipo"] = "tabela"
                registro_metadado["colunas"] = list(df.columns)
                registro_metadado["linhas"] = len(df)
            else:
                textos.append(
                    f"\n\n# Arquivo: {nome}\nFormato {extension} não suportado diretamente. Forneça instruções específicas ao modelo."
                )
                registro_metadado["tipo"] = "desconhecido"
        except Exception as exc:  # noqa: BLE001
            registro_metadado["status"] = "falha"
            registro_metadado["motivo"] = str(exc)
        else:
            registro_metadado["status"] = "ok"

        metadados.append(registro_metadado)

    conteudo_concatenado = "\n".join(textos).strip()
    if not conteudo_concatenado:
        conteudo_concatenado = "Nenhum conteúdo textual foi identificado."

    outputs = {
        "conteudo_concatenado": conteudo_concatenado,
        "metadados": json.dumps(metadados, ensure_ascii=False, indent=2),
        "tabelas_disponiveis": json.dumps(tabelas, ensure_ascii=False),
    }
    return outputs
