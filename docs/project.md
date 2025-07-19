# 🧠 Personal Technical Achievements Tracker — Project Overview

## 🎯 Goal

Design a **free**, modular, and offline-friendly system to:
- Record weekly technical achievements (professional or personal)
- Store them locally in structured format
- Use LLMs (e.g., ChatGPT) to assist in transforming raw input into content:
  - Blog articles
  - Project summaries
  - Social media posts

---

## 🏗️ Architecture Overview

### 1. Input Sources
- Manual input: Markdown file, text editor, or simple CLI
- AI chat input: Paste raw notes into ChatGPT or Cursor

### 2. LLM Workflow Roles (Agent-Based)

| Agent        | Role                                  | Input                  | Output                         |
|--------------|---------------------------------------|-------------------------|--------------------------------|
| **Listener** | Parses raw log/thoughts               | Free text / bullets     | Normalized structured data     |
| **Summarizer** | Compresses into key points           | Listener output         | Weekly summary                 |
| **Archivist** | Stores data in structured format      | Summary                 | Markdown/JSON/YAML file        |
| **Curator**   | Browses/searches stored entries       | User query              | Related topics/entries         |
| **Analyst**   | Extracts trends/insights              | Multiple logs           | Keynotes/themes/tags           |
| **Creator**   | Generates publishable content         | Highlights/summary      | Blog draft, social post, etc.  |

---

## 💾 Data Storage

- Local filesystem-based
- Suggested structure:

/data/
└── logs/
└── 2025-W29.md
└── summaries/
└── 2025-W29.yaml
└── content/
├── blogs/
└── social/


- Formats:
- Markdown for human-readable logs
- YAML or JSON for structured metadata
- Optional SQLite for querying/searching

---

## 🔁 Weekly Workflow (Manual + LLM-Guided)

1. Write weekly achievements as raw notes or bullet points.
2. Paste into **Listener Agent** (ChatGPT prompt) → get structured data.
3. Use **Summarizer Agent** → extract key outcomes and ideas.
4. Use **Archivist Agent** → format and store data locally.
5. Use **Creator Agent** (optional) → generate blog or post drafts.
6. Use **Curator** or **Analyst** (optional) → browse/search trends.

---

## 🐍 Python Tool (Future Plan)

- CLI or minimal GUI:
- Add/edit/view logs
- Browse summaries
- Generate prompts or content
- Local-only
- Interact with Markdown/YAML/JSON files

---

## ✅ Next Planning Steps

- Define the detailed step-by-step workflow
- Draft file/folder structure template
- Write prompt templates for each agent
- List Python CLI features

