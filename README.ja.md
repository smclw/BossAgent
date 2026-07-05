# BossAgent

**創業家、オペレーター、チームのための AI Workforce OS。**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · 日本語 · [한국어](README.ko.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Français](README.fr.md)

BossAgent は、ローカル優先で動作する拡張可能な AI Agent ワークスペースです。ユーザーが目標を入力するか資料をアップロードすると、複数の AI 従業員が連携し、リサーチ、計画、文章作成、分析、営業フォロー、資料整理、実行レポート作成を支援します。

## Core Agents

| Agent | Status | Role |
| --- | --- | --- |
| Chief of Staff Agent | Available | タスク分解、Agent の調整、最終レポート作成。 |
| Opportunity Radar Agent | Available | トレンド、機会、業界ウィンドウ、リスクを分析。 |
| Strategy Advisor Agent | Available | 参入判断、投資対効果、最小検証プランを設計。 |
| Content Clone Agent | Available | SNS 投稿、短尺動画台本、ライブ配信用トークを作成。 |
| Sales Follow-up Agent | Available | 顧客分類、商談スクリプト、見積もりコミュニケーションを支援。 |
| Document Analyst Agent | Available | PDF、Word、Excel、TXT から要点と行動リストを抽出。 |

## Features

- Available: multi-agent workflow, Streamlit UI, OpenAI-compatible APIs, document upload, task history, Markdown / DOCX export.
- Experimental: local GGUF model folder mode.
- Planned: native CrewAI orchestration, browser automation, external tools, team permissions.

## Quick Start

```bash
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Security

Do not commit API keys, `.env`, private customer data, or uploaded confidential files. External actions must require human confirmation.

## License

MIT License.
