"""Script de nó de código no Dify para gerar gráficos com Altair a partir de dados tabulares."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Tuple

import altair as alt
import pandas as pd


CHART_KEYWORDS = {
    "line": {"linha", "linhas", "line"},
    "bar": {"barra", "barras", "coluna", "colunas", "bar"},
    "area": {"area", "área"},
    "pie": {"pizza", "pie", "setor"},
    "scatter": {"dispersao", "dispersão", "scatter", "pontos"},
}


def _detect_chart_type(prompt: str) -> str:
    normalized = prompt.lower()
    for chart, keywords in CHART_KEYWORDS.items():
        if any(word in normalized for word in keywords):
            return chart
    return "line"


def _find_columns(prompt: str, columns: Iterable[str]) -> Tuple[str | None, str | None]:
    normalized = prompt.lower()
    matches = [col for col in columns if col.lower() in normalized]
    if len(matches) >= 2:
        return matches[0], matches[1]
    if len(matches) == 1:
        return matches[0], None
    return None, None


def _default_columns(columns: Iterable[str]) -> Tuple[str, str | None]:
    cols = list(columns)
    if not cols:
        raise ValueError("Tabela sem colunas disponíveis.")
    if len(cols) == 1:
        return cols[0], None
    return cols[0], cols[1]


def _prepare_dataframe(tabelas: Dict[str, Any]) -> Tuple[str, pd.DataFrame]:
    if not tabelas:
        raise ValueError("Nenhuma tabela foi fornecida pelo nó de ingestão.")
    # Seleciona a tabela com mais linhas
    chosen_name = max(tabelas, key=lambda name: len(tabelas[name]))
    dataframe = pd.DataFrame(tabelas[chosen_name])
    if dataframe.empty:
        raise ValueError(f"A tabela {chosen_name} está vazia.")
    return chosen_name, dataframe


def _render_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str | None) -> alt.Chart:
    if chart_type == "pie":
        if y_col is None:
            y_col = x_col
        chart = alt.Chart(df).mark_arc().encode(
            theta=alt.Theta(field=y_col, type="quantitative"),
            color=alt.Color(field=x_col, type="nominal"),
        )
        return chart.properties(width=500, height=500)

    mark_chart = {
        "line": alt.Chart(df).mark_line(),
        "bar": alt.Chart(df).mark_bar(),
        "area": alt.Chart(df).mark_area(opacity=0.7),
        "scatter": alt.Chart(df).mark_point(size=80, filled=True),
    }.get(chart_type, alt.Chart(df).mark_line())

    x_type = "temporal" if _looks_temporal(df[x_col]) else "nominal"
    y_field = y_col if y_col else x_col
    chart = mark_chart.encode(
        x=alt.X(field=x_col, type=x_type),
        y=alt.Y(field=y_field, type="quantitative"),
    )
    if y_col is None:
        chart = chart.encode(color=alt.Color(field=x_col, type="nominal"))
    return chart.properties(width=600, height=400)


def _looks_temporal(series: pd.Series) -> bool:
    try:
        pd.to_datetime(series)
        return True
    except Exception:  # noqa: BLE001
        return False


def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    prompt = inputs.get("prompt_usuario", "")
    tabelas_raw = inputs.get("tabelas_disponiveis", "{}")

    if isinstance(tabelas_raw, str):
        tabelas = json.loads(tabelas_raw or "{}")
    else:
        tabelas = tabelas_raw

    nome_tabela, df = _prepare_dataframe(tabelas)

    chart_type = _detect_chart_type(prompt)
    x_col, y_col = _find_columns(prompt, df.columns)
    if x_col is None:
        x_col, y_col = _default_columns(df.columns)
    elif y_col is None:
        remaining = [col for col in df.columns if col != x_col]
        if remaining:
            y_col = remaining[0]

    chart = _render_chart(df, chart_type, x_col, y_col)

    explicacao = (
        f"Gráfico do tipo **{chart_type}** gerado a partir da tabela `{nome_tabela}`. "
        f"Eixo X: `{x_col}`. "
        + (f"Eixo Y: `{y_col}`." if y_col else "Foi utilizada apenas a coluna selecionada.")
    )

    html = chart.to_html()

    return {"grafico_html": html, "explicacao": explicacao}
