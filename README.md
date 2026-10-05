# OCR: candidate interview-form extractor

Streamlit app that reads candidate interview forms (PDF), extracts the text with Google Cloud Vision, structures it with Gemini and stores candidates in a local SQLite database. Built December 2024; not actively maintained.

## How it works

1. `UI.py`: Streamlit front end. Upload a PDF, review the parsed details, search stored candidates.
2. `text_vision.py`: sends the PDF to the Google Cloud Vision API and returns the text.
3. `data_extractor.py`: asks Gemini (`gemini-pro`) to turn the raw text into structured JSON (personal, education, training, certification, family and reference details).
4. `DatabaseManager.py`: SQLite (`candidate.db`, created on first run) with `Candidates`, `Education`, `Training`, `Certifications`, `Family` and `Reference` tables.
5. `resize.py`, `delete_files.py`: image resizing and cleanup of the `temp/` working files.

`test.py` is a scratch Streamlit demo of a table with buttons, not a test suite.

## Run

```bash
pip install -r requirements.txt
streamlit run UI.py
```

Needs a `.env` with `GEMINI_API_KEY` and Google Cloud Vision credentials (`key.json`). Both are git-ignored; never commit them.

## Notes

- `temp/` holds sample forms and images used during development.
- `gemini-pro` is a retired model name; update it in `data_extractor.py` before use.
