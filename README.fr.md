# BossAgent

**L'AI Workforce OS pour fondateurs, opérateurs et équipes ambitieuses.**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · Français

BossAgent est un espace de travail local-first et extensible pour AI Agents. L'utilisateur saisit un objectif ou téléverse des documents, puis une équipe coordonnée d'employés AI aide à rechercher, planifier, rédiger, analyser, suivre les ventes, organiser les documents et produire un rapport exécutif.

## Core Agents

| Agent | Status | Role |
| --- | --- | --- |
| Chief of Staff Agent | Available | Décompose les tâches, coordonne les agents et consolide le rapport final. |
| Opportunity Radar Agent | Available | Détecte les tendances, opportunités, fenêtres de marché et risques. |
| Strategy Advisor Agent | Available | Évalue l'intérêt d'un projet et propose une validation à faible coût. |
| Content Clone Agent | Available | Rédige des contenus sociaux, scripts vidéo courts et scripts de live. |
| Sales Follow-up Agent | Available | Aide à segmenter les clients, relancer, négocier et faire avancer les ventes. |
| Document Analyst Agent | Available | Lit PDF, Word, Excel et TXT pour extraire résumés et listes d'action. |

## Features

- Available: workflow multi-agent, UI locale Streamlit, APIs OpenAI-compatible, import de fichiers, historique, export Markdown / DOCX.
- Experimental: mode dossier local pour modèles GGUF.
- Planned: orchestration native CrewAI, automatisation navigateur, outils externes et permissions d'équipe.

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

Ne commitez jamais d'API keys, `.env`, données client privées ni fichiers confidentiels. Toute action externe doit demander une confirmation humaine.

## License

MIT License.
