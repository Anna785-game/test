import os
from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

# Utilise une variable d'environnement sur Render pour plus de sécurité
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.get("/")
def test_db():
    try:
        with engine.connect() as connection:
            return {"status": "✅ Connection to Supabase successful!"}
    except Exception as e:
        return {"status": "❌ Connection failed", "error": str(e)}