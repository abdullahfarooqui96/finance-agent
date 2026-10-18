# Finance Agent

**Author:** Muhammad Abdullah Farooqui
**Student ID:** 62404051

A simple AI stock assistant. You chat with it in the browser, and it gets real-time stock data from Yahoo Finance to answer your questions.

![Finance Agent screenshot](screenshot.png)

## Tech Stack

- **Backend:** Python, FastAPI, LangChain, LangGraph, yfinance
- **Frontend:** React, TypeScript, Vite (C1 Chat UI)
- **Package managers:** `uv` (Python) and `npm` (frontend)

## Project Structure

```
finance_agent/
├── backend/
│   ├── main.py
│   ├── pyproject.toml
│   └── .env          <- you create this
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.ts
```

## Setup

### 1. API key (add it yourself)

The API key is not included in this repository. Create your own key and add it yourself.

Create a file called `.env` inside the `backend` folder:

```
THESYS_API_KEY=your_api_key_here
```

### 2. Run the backend

```bash
cd backend
uv run main.py
```

The backend runs on http://localhost:8888

### 3. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on http://localhost:3000 and forwards `/api` requests to the backend.

## Credits

- Thanks to my professor **Bruce** for the course and guidance.
- Based on the YouTube tutorial: https://www.youtube.com/watch?v=AE_6F8cuXsA
