# TaskPilot (PBL) — mini Kanban + komentarze + log

## Problem
W małych projektach studenckich często pojawia się chaos: trudno śledzić kto co robi, jaki jest status oraz gdzie są ustalenia.

## Rozwiązanie
TaskPilot to prosta aplikacja webowa (Python + FastAPI + SQLite), która pozwala:
- tworzyć zadania, edytować je i usuwać,
- ustawiać status (TODO/DOING/DONE),
- dodawać komentarze,
- śledzić log aktywności.

## Uruchomienie (lokalnie)
1) Python 3.11+
2) W katalogu projektu:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
## Demo
- Aplikacja: http://127.0.0.1:8000
- Swagger (API): http://127.0.0.1:8000/docs
- Wideo demo: https://drive.google.com/drive/folders/1Pj6u0u1qZ-_0dN1g3kTsPVnoBkv_siO7?hl=pl