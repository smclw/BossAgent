# BossAgent

**O AI Workforce OS para fundadores, operadores e equipes ambiciosas.**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · Português · [Français](README.fr.md)

BossAgent é um workspace local-first e extensível para AI Agents. O usuário informa um objetivo ou envia documentos, e uma equipe coordenada de funcionários AI ajuda com pesquisa, planejamento, escrita, análise, follow-up de vendas, organização de documentos e relatórios executivos.

## Core Agents

| Agent | Status | Role |
| --- | --- | --- |
| Chief of Staff Agent | Available | Divide tarefas, coordena agentes e consolida o relatório final. |
| Opportunity Radar Agent | Available | Identifica tendências, oportunidades, janelas de mercado e riscos. |
| Strategy Advisor Agent | Available | Avalia se um projeto vale a pena e propõe validações de baixo custo. |
| Content Clone Agent | Available | Cria posts, roteiros curtos e falas para transmissões ao vivo. |
| Sales Follow-up Agent | Available | Ajuda com segmentação, mensagens de follow-up e negociação de preço. |
| Document Analyst Agent | Available | Lê PDF, Word, Excel e TXT para gerar resumos e listas de ação. |

## Features

- Available: fluxo multi-agent, UI local com Streamlit, APIs OpenAI-compatible, upload de arquivos, histórico, exportação Markdown / DOCX.
- Experimental: modo de pasta local para modelos GGUF.
- Planned: orquestração nativa com CrewAI, automação de navegador, ferramentas externas e permissões de equipe.

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

Não envie API keys, `.env`, dados privados de clientes nem arquivos confidenciais. Ações externas devem exigir confirmação humana.

## License

MIT License.
