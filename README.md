# Modular AI Proxy 

A production-ready reference project that demonstrates how to build a **modular AI proxy** using **FastAPI**. This proxy routes requests to multiple AI backends — including **OpenAI** and other models — based on a dynamic scoring formula. It showcases:

- Dynamic Weighting for model selection (accuracy, cost, latency, load, etc.)
- Rate Limiting with a naive in-memory approach (extendable to Redis)
- Cost Usage tracking and a budget limit with optional fallback
- Thread-Safe concurrency for updating weights
- Well-Structured code for easy extension and maintenance

------------------------------------------------------------------------------
Table of Contents
------------------------------------------------------------------------------

1. Features
2. Project Structure
3. Getting Started
4. Usage
5. Configuration
6. Contributing
7. License

------------------------------------------------------------------------------
1) Features
------------------------------------------------------------------------------

1. **Multi-Model Routing**  
   - Supports both **OpenAI** and **Groq** (hypothetical) models.

2. **Dynamic Scoring**  
   - Weights can be updated on-the-fly without redeploying.
   - Adjust how you value accuracy, latency, cost, load, complexity, and confidence.

3. **Rate Limiting**  
   - Simple in-memory approach (extendable to Redis or a gateway-based solution).
   - Prevents misuse or overload.

4. **Cost Control**  
   - Tracks usage against a monthly budget.
   - Optional fallback model if the cost limit is exceeded (e.g., cheaper or offline model).

5. **Health Check**  
   - `/health` endpoint for status monitoring (integrate with Kubernetes, etc.).

------------------------------------------------------------------------------
2) Project Structure
------------------------------------------------------------------------------

Below is a file layout for the project:
```
app/
├── __init__.py
├── main.py               # FastAPI entry point (creates and configures the app)
├── config.py             # Central configuration (API keys, rate limits, budgets)
├── models.py             # Pydantic models for request validation
├── managers/
│   ├── __init__.py
│   └── weight_manager.py # Manages dynamic scoring weights with thread-safe lock
├── services/
│   ├── __init__.py
│   ├── model_registry.py # List of available AI models (OpenAI & Groq)
│   ├── rate_limiting.py  # Naive in-memory rate-limiting logic
│   ├── scoring.py        # Scoring formula & model selection
│   └── usage_monitoring.py # Cost tracking & budget enforcement
└── routers/
    ├── __init__.py
    ├── predict.py        # /predict endpoint routing logic
    └── weights.py        # /update_weights endpoint for dynamic weights

docs/
├── README.md
├── Features.md
├── InstallationAndUsage.md
├── Configuration.md
├── Contributing.md
└── License.md

requirements.txt
```


Key Files:
- **app/main.py**: App entry point. Initializes FastAPI, registers routers, and provides a /health endpoint.  
- **app/config.py**: Central location for environment-based configurations (e.g., API keys, rate limits).  
- **app/managers/weight_manager.py**: Thread-safe manager for dynamic scoring weights.  
- **app/services/model_registry.py**: Defines the AI “models” (OpenAI & Groq) and their metrics.  
- **app/services/scoring.py**: Contains the main scoring logic and model selection functions.  
- **app/routers/predict.py**: Orchestrates the entire “predict” flow (rate limiting, cost check, fallback).  
- **app/routers/weights.py**: Lets authorized clients update the scoring weights at runtime.

------------------------------------------------------------------------------
3) Getting Started
------------------------------------------------------------------------------

### Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- (Recommended) A virtual environment

### Installation

1. **Clone** the repository:
```
git clone https://github.com/sakomws/aiproxy.git
cd aiproxy
```

2. **Create and activate** a virtual environment (optional but recommended):
```
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**:
```
pip install -r requirements.txt
```

------------------------------------------------------------------------------
4) Usage
------------------------------------------------------------------------------

1. **Configure** your settings in app/config.py, especially:
   - OPENAI_API_KEY
   - API_KEY_FOR_UPDATES
   - RATE_LIMIT_COUNT, RATE_LIMIT_WINDOW
   - MAX_MONTHLY_BUDGET
   - FALLBACK_MODEL

2. **Run** the application:
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Access the service at: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

3. **Endpoints**:
```
- POST /predict  
  Expects a JSON body like { "text": "Hello world" }, returns a chosen model and inference result.
- POST /update_weights?api_key=...  
  Lets you dynamically update the scoring weights.
  {
    "alpha1": 3.0,
    "alpha2": 0.5,
    "alpha3": 1.0,
    "alpha4": 1.0,
    "alpha5": 1.0,
    "alpha6": 2.0
  }
- GET /health  
  Simple health-check endpoint returns { "status": "ok" }.
```
------------------------------------------------------------------------------
5) Configuration
------------------------------------------------------------------------------

All configuration is defined in app/config.py. Key variables:
```
class Config:
    OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"
    API_KEY_FOR_UPDATES: str = "secret-weight-key"
    RATE_LIMIT_COUNT: int = 10
    RATE_LIMIT_WINDOW: float = 60.0
    MAX_MONTHLY_BUDGET: float = 5.0
    FALLBACK_MODEL: str = "text-ada-001"
```
- **OpenAI API Key**: Replace "YOUR_OPENAI_API_KEY" with your actual key (or load from environment variables).
- **API Key for Updates**: Used by /update_weights to protect dynamic scoring changes.
- **Rate Limiting**: Adjust RATE_LIMIT_COUNT and RATE_LIMIT_WINDOW as needed.
- **Cost/Budget**: MAX_MONTHLY_BUDGET enforces a monthly usage limit (in your chosen currency).
- **Fallback Model**: If cost limit is exceeded, you can fallback to a cheaper model (e.g., "text-ada-001", "groq-l80", etc.).

------------------------------------------------------------------------------
6) Contributing
------------------------------------------------------------------------------

Contributions are welcome! Feel free to:

1. Fork this repo.
2. Create a feature branch (git checkout -b my-new-feature).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to the branch (git push origin my-new-feature).
5. Open a Pull Request.

Guidelines:
- Follow **PEP 8** for Python code style.
- Add docstrings for any new methods or classes.
- Update or add tests if you have a tests/ folder.

------------------------------------------------------------------------------
7) License
------------------------------------------------------------------------------

This project is open-sourced under the MIT License. You are free to use, modify, and redistribute it for personal or commercial purposes.

Happy hacking!  
For questions or feedback, open an issue or reach out to the maintainers.
