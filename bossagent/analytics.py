from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd


SUPPORTED_DATA_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_ANALYTICS_ROWS = 5000
MAX_CONTEXT_CHARS = 30000


@dataclass
class DataProfile:
    file_name: str
    sheet_name: str
    rows: int
    columns: int
    column_names: List[str]
    missing_summary: Dict[str, int]
    numeric_summary: str
    category_summary: str
    preview_markdown: str


def is_supported_data_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_DATA_EXTENSIONS


def load_dataframes(paths: Iterable[Path]) -> Dict[str, pd.DataFrame]:
    datasets: Dict[str, pd.DataFrame] = {}
    for path in paths:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            datasets[path.name] = _read_csv(path)
        elif suffix in {".xlsx", ".xls"}:
            sheets = pd.read_excel(path, sheet_name=None)
            for sheet_name, df in sheets.items():
                datasets[f"{path.name}::{sheet_name}"] = _clean_frame(df)
    return datasets


def profile_datasets(datasets: Dict[str, pd.DataFrame]) -> List[DataProfile]:
    profiles: List[DataProfile] = []
    for dataset_name, df in datasets.items():
        file_name, sheet_name = _split_dataset_name(dataset_name)
        clean_df = _clean_frame(df)
        profiles.append(_profile_frame(file_name, sheet_name, clean_df))
    return profiles


def profiles_to_markdown(profiles: List[DataProfile], goal: str = "") -> str:
    chunks = []
    if goal.strip():
        chunks.append(f"# 分析目标\n{goal.strip()}")
    for profile in profiles:
        chunks.append(
            f"""# 数据集：{profile.file_name} / {profile.sheet_name}

- 行数：{profile.rows}
- 列数：{profile.columns}
- 字段：{", ".join(profile.column_names)}

## 缺失值
{_dict_to_markdown(profile.missing_summary)}

## 数值字段摘要
{profile.numeric_summary or "未检测到数值字段。"}

## 类别字段高频值
{profile.category_summary or "未检测到适合汇总的类别字段。"}

## 数据预览
{profile.preview_markdown}
"""
        )
    context = "\n\n".join(chunks).strip()
    if len(context) <= MAX_CONTEXT_CHARS:
        return context
    return context[:MAX_CONTEXT_CHARS] + "\n\n[数据画像过长，已截断用于本地 MVP 分析。]"


def chart_candidates(datasets: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, pd.DataFrame]]:
    candidates: Dict[str, Dict[str, pd.DataFrame]] = {}
    for dataset_name, df in datasets.items():
        clean_df = _clean_frame(df)
        numeric_cols = clean_df.select_dtypes(include="number").columns.tolist()
        object_cols = clean_df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        charts: Dict[str, pd.DataFrame] = {}

        if numeric_cols:
            charts["数值字段均值"] = clean_df[numeric_cols].mean(numeric_only=True).sort_values(ascending=False).head(12).to_frame("mean")

        if numeric_cols and object_cols:
            group_col = object_cols[0]
            value_col = numeric_cols[0]
            grouped = (
                clean_df[[group_col, value_col]]
                .dropna()
                .groupby(group_col)[value_col]
                .mean()
                .sort_values(ascending=False)
                .head(12)
                .to_frame(value_col)
            )
            charts[f"{group_col} 分组 {value_col} 均值"] = grouped

        if object_cols:
            category_col = object_cols[0]
            charts[f"{category_col} 高频分布"] = clean_df[category_col].astype(str).value_counts().head(12).to_frame("count")

        candidates[dataset_name] = charts
    return candidates


def _read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return _clean_frame(pd.read_csv(path, encoding=encoding))
        except UnicodeDecodeError:
            continue
    return _clean_frame(pd.read_csv(path, encoding="utf-8", encoding_errors="ignore"))


def _clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    clean_df.columns = [str(column).strip() or f"column_{index + 1}" for index, column in enumerate(clean_df.columns)]
    clean_df = clean_df.dropna(how="all")
    if len(clean_df) > MAX_ANALYTICS_ROWS:
        clean_df = clean_df.head(MAX_ANALYTICS_ROWS)
    return clean_df


def _profile_frame(file_name: str, sheet_name: str, df: pd.DataFrame) -> DataProfile:
    missing = df.isna().sum()
    missing_summary = {column: int(value) for column, value in missing.items() if int(value) > 0}
    numeric_df = df.select_dtypes(include="number")
    category_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()[:6]

    numeric_summary = ""
    if not numeric_df.empty:
        numeric_summary = numeric_df.describe().round(3).transpose().to_markdown()

    category_chunks = []
    for column in category_cols:
        counts = df[column].astype(str).value_counts(dropna=True).head(6)
        category_chunks.append(f"### {column}\n{counts.to_frame('count').to_markdown()}")

    return DataProfile(
        file_name=file_name,
        sheet_name=sheet_name,
        rows=int(df.shape[0]),
        columns=int(df.shape[1]),
        column_names=[str(column) for column in df.columns.tolist()],
        missing_summary=missing_summary,
        numeric_summary=numeric_summary,
        category_summary="\n\n".join(category_chunks),
        preview_markdown=df.head(20).to_markdown(index=False),
    )


def _split_dataset_name(dataset_name: str) -> tuple[str, str]:
    if "::" not in dataset_name:
        return dataset_name, "default"
    file_name, sheet_name = dataset_name.split("::", 1)
    return file_name, sheet_name


def _dict_to_markdown(values: Dict[str, int]) -> str:
    if not values:
        return "未检测到缺失值。"
    rows = [{"field": key, "missing": value} for key, value in values.items()]
    return pd.DataFrame(rows).to_markdown(index=False)
