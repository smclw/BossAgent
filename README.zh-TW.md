# BossAgent：老闆 AI 分身系統 / AI 員工工作台

**不是又一個聊天機器人，而是為老闆配置一組 24 小時 AI 員工。**

[English](README.md) · [简体中文](README.zh-CN.md) · 繁體中文 · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Français](README.fr.md)

BossAgent 是一個 local-first、可擴充的 AI Agent 工作台。使用者輸入目標或上傳資料後，系統會協調多個 AI 員工完成研究、規劃、寫作、分析、銷售跟進、資料整理與最終報告。

## 核心 Agent

| Agent | 狀態 | 職責 |
| --- | --- | --- |
| Chief of Staff Agent | Available | 拆解任務、協調 Agent、彙整報告。 |
| Opportunity Radar Agent | Available | 分析趨勢、機會窗口、資源與風險。 |
| Strategy Advisor Agent | Available | 判斷專案是否值得投入，設計低成本試錯方案。 |
| Content Clone Agent | Available | 生成社群文案、短影片腳本與直播話術。 |
| Sales Follow-up Agent | Available | 客戶分層、成交話術、報價溝通與復購提醒。 |
| Document Analyst Agent | Available | 讀取 PDF、Word、Excel、TXT，提煉摘要和行動清單。 |

## 功能

- Available：多 Agent 工作流、Streamlit 本地 UI、OpenAI-compatible API、文件上傳、SQLite 歷史任務、Markdown / DOCX 匯出。
- Experimental：本地 GGUF 模型文件夾模式。
- Planned：CrewAI 原生編排、瀏覽器自動化、外部工具、團隊權限。

## Quick Start

```bash
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Windows PowerShell 可使用：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## 安全

不要提交 API Key、`.env`、客戶資料或使用者上傳的隱私文件。所有外部系統修改、發送、付款、下單和刪除動作都必須人工確認。

## License

MIT License.
