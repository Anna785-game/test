import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI(title="Supabase Connection Tester")

# Configuration de la base de données
# Sur Render, tu pourras configurer DATABASE_URL directement dans les variables d'environnement
# Configuration corrigée pour passer par le Pooler IPv4
USER = "postgres.hpratqkkfnevjrytnitp" # Format obligatoire pour le pooler
PASSWORD = "anna33quinzel"
HOST = "aws-0-eu-central-1.pooler.supabase.com" # Vérifie bien cet hôte dans ton dashboard
PORT = 6543
DBNAME = "postgres"

DEFAULT_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_URL)

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {
        "message": "FastAPI is running",
        "tip": "Go to /test-db to check Supabase connection"
    }

@app.get("/test-db")
def test_db_connection():
    try:
        # On utilise text() pour une simple requête SQL de santé
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {
                "status": "success",
                "message": "✅ Connection to Supabase successful!",
                "database_url_used": DATABASE_URL.split('@')[-1] # Affiche l'hôte pour vérification
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "❌ Failed to connect to Supabase",
            "details": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    # Récupère le port de Render ou utilise 8000 par défaut
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
