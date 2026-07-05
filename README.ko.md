# BossAgent

**창업자, 운영자, 팀을 위한 AI Workforce OS.**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · 한국어 · [Español](README.es.md) · [Português](README.pt-BR.md) · [Français](README.fr.md)

BossAgent는 로컬 우선으로 실행되는 확장 가능한 AI Agent 워크스페이스입니다. 사용자가 목표를 입력하거나 문서를 업로드하면 여러 AI 직원이 협업하여 리서치, 기획, 작성, 분석, 영업 후속 조치, 문서 정리, 실행 보고서를 만듭니다.

## Core Agents

| Agent | Status | Role |
| --- | --- | --- |
| Chief of Staff Agent | Available | 작업을 분해하고 Agent를 조율하며 최종 보고서를 작성합니다. |
| Opportunity Radar Agent | Available | 트렌드, 기회, 산업 진입 시점, 리스크를 분석합니다. |
| Strategy Advisor Agent | Available | 프로젝트 진입 여부와 최소 검증 방안을 설계합니다. |
| Content Clone Agent | Available | 소셜 콘텐츠, 숏폼 스크립트, 라이브 세일즈 멘트를 작성합니다. |
| Sales Follow-up Agent | Available | 고객 분류, 후속 메시지, 견적 커뮤니케이션을 지원합니다. |
| Document Analyst Agent | Available | PDF, Word, Excel, TXT에서 요약과 실행 목록을 추출합니다. |

## Features

- Available: multi-agent workflow, Streamlit UI, OpenAI-compatible APIs, file upload, task history, Markdown / DOCX export.
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

API 키, `.env`, 고객 데이터, 업로드된 비공개 파일을 커밋하지 마세요. 외부 시스템 작업은 반드시 사람의 확인을 거쳐야 합니다.

## License

MIT License.
