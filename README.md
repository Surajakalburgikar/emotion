# 🧠 Emotion Detector AI — Full-Stack Application

An extremely premium, responsive full-stack emotion detection application. It uses a **hybrid AI inference pipeline** leveraging multiple Google Gemini Models with an automatic local offline fallback to a Transformers DistilRoBERTa model if quota/network issues occur.

---

## ✨ Features

- **🧠 Hybrid AI Inference Pipeline:**
  - **Auto Mode:** Automatically cascades through high-performance LLM models (`gemini-2.5-flash` → `gemini-2.0-flash-lite` → `gemma-4-31b-it`).
  - **Offline Local Fallback:** Automatically switches to a local deep learning model (`j-hartmann/emotion-english-distilroberta-base` via PyTorch & HuggingFace) if your Gemini API key runs out of quota.
- **🎨 Premium Dark UI:**
  - Sleek dark-glassmorphism theme styled with curated CSS.
  - Interactive header showing the current active model and real-time **character counter** (1000 char cap).
  - Emoji-powered animated **Emotion Dashboard** displaying confidence percentages and model source labels.
  - Precise **Response Time** metrics.
- **📋 Sidebar Control Center:**
  - **Inference Model Selector:** Switch between *Auto*, *Gemini Only*, and *Local Only* modes on the fly.
  - **Analysis History:** A neat history feed showing your last 8 runs with their specific emoji, source, and quick clear button.
- **🔌 Robust Silent Health Check:**
  - The UI silently polls the backend to verify it's responsive. If it ever goes offline, a beautiful diagnostic overlay appears with setup instructions.

---

## 📂 Project Structure

```bash
emotion-detector/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # FastAPI routes (/api/analyze, /api/health)
│   │   ├── core/
│   │   │   ├── config.py          # Environment settings loader
│   │   │   └── logger.py          # Structured logging
│   │   ├── models/
│   │   │   ├── gemini_model.py    # Gemini API client with cascading logic
│   │   │   └── local_model.py     # Offline HuggingFace transformer model
│   │   ├── schemas/
│   │   │   └── emotion_schema.py  # Pydantic schemas (validations)
│   │   ├── services/
│   │   │   └── emotion_service.py # Dynamic model selector & fallback logic
│   │   │   └── response_helper.py # Standardized JSON payloads
│   │   └── main.py                # FastAPI main app entry & CORS config
│   ├── .env                       # API Key configuration
│   └── requirements.txt           # Backend dependencies
├── frontend/
│   ├── app.py                     # Streamlit premium application
│   └── requirements.txt           # Frontend dependencies
├── run.bat                        # Double-clickable Windows Batch launcher
└── README.md                      # Documentation
```

---

## ⚡ Quick Start (Windows Users)

We have bundled a simple, bulletproof **one-click launcher** (`run.bat`) that automatically detects your Anaconda environment and starts both backend and frontend servers in separate clean terminal windows:

*   **Simply double-click `run.bat`** directly from your Windows File Explorer!
*   **Or** open your terminal (Command Prompt/CMD) in the `emotion-detector` directory and run:
    ```cmd
    run.bat
    ```
This will automatically open two separate command prompt windows running the FastAPI backend (`http://127.0.0.1:8000`) and the Streamlit app (`http://localhost:8501`).

---

## 🛠️ Manual Installation & Launch

If you prefer to set up and run the servers manually (e.g., inside an activated Anaconda or Virtual Environment), follow these steps:

### 1. Configure the API Key
Open `backend/.env` and paste your Google Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Start the Backend Server
Navigate to the `backend` directory, install requirements, and run the FastAPI server:
```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
*Note: The first time you launch or run in Local/Auto mode, PyTorch will automatically download the 260MB DistilRoBERTa model weights. This only happens once!*

### 3. Start the Frontend Server
Open a **new** terminal, navigate to the `frontend` directory, install requirements, and run Streamlit:
```powershell
cd frontend
pip install -r requirements.txt
python -m streamlit run app.py
```
Your browser will automatically open `http://localhost:8501` and display the interface!

---

## ⚙️ Model Configurations

When analyzing emotions, select your preference from the **Sidebar Settings**:
- **Auto (Recommended):** Calls the Gemini API using `gemini-2.5-flash`. If your API key hits daily quota limits, it silently falls back to your local CPU model so your app never fails.
- **Gemini AI Only:** Direct API connection. Shows clear warnings if rate limits or quota caps are reached.
- **Local Model Only:** Runs completely offline on your CPU. Perfect if you don't have internet access or want zero API latency.
