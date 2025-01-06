# app/services/model_registry.py

model_registry = [
    # OpenAI Models
    {
        "name": "text-davinci-003",
        "acc_text": 0.88,
        "lat_text": 0.25,
        "cost_text": 0.15,
        "load": 0.40,
        "conf_text": 0.85,
    },
    {
        "name": "text-curie-001",
        "acc_text": 0.80,
        "lat_text": 0.15,
        "cost_text": 0.10,
        "load": 0.30,
        "conf_text": 0.75,
    },
    {
        "name": "text-babbage-001",
        "acc_text": 0.72,
        "lat_text": 0.10,
        "cost_text": 0.08,
        "load": 0.35,
        "conf_text": 0.70,
    },
    {
        "name": "text-ada-001",
        "acc_text": 0.65,
        "lat_text": 0.05,
        "cost_text": 0.05,
        "load": 0.20,
        "conf_text": 0.60,
    },
    {
        "name": "gpt-3.5-turbo",
        "acc_text": 0.85,
        "lat_text": 0.20,
        "cost_text": 0.10,
        "load": 0.50,
        "conf_text": 0.80,
    },
    {
        "name": "gpt-4",
        "acc_text": 0.90,
        "lat_text": 0.35,
        "cost_text": 0.25,
        "load": 0.40,
        "conf_text": 0.95,
    },
    # Groq Models (hypothetical)
    {
        "name": "groq-l80",
        "acc_text": 0.70,
        "lat_text": 0.04,
        "cost_text": 0.03,
        "load": 0.15,
        "conf_text": 0.65,
    },
    {
        "name": "groq-l120",
        "acc_text": 0.78,
        "lat_text": 0.07,
        "cost_text": 0.05,
        "load": 0.25,
        "conf_text": 0.72,
    }
    # ... add more as needed
]