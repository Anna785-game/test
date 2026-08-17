import os
import time

import face_recognition
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI(
    title="Biometric Test API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "biometric-test",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "face_recognition": "loaded",
    }


@app.post("/face/detect")
async def detect_face(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être une image."
        )

    image_bytes = await file.read()

    start = time.perf_counter()

    try:
        image = face_recognition.load_image_file(
            __import__("io").BytesIO(image_bytes)
        )

        locations = face_recognition.face_locations(image)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur reconnaissance faciale: {exc}"
        )

    elapsed = time.perf_counter() - start

    return {
        "face_detected": len(locations) > 0,
        "faces_count": len(locations),
        "processing_time_seconds": round(elapsed, 3),
        "image_size_bytes": len(image_bytes),
    }


@app.post("/face/encode")
async def encode_face(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être une image."
        )

    image_bytes = await file.read()

    start = time.perf_counter()

    try:
        image = face_recognition.load_image_file(
            __import__("io").BytesIO(image_bytes)
        )

        locations = face_recognition.face_locations(image)

        if not locations:
            return {
                "success": False,
                "message": "Aucun visage détecté.",
            }

        encodings = face_recognition.face_encodings(
            image,
            known_face_locations=locations,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur reconnaissance faciale: {exc}"
        )

    elapsed = time.perf_counter() - start

    return {
        "success": True,
        "faces_count": len(encodings),
        "encoding_size": len(encodings[0]) if encodings else 0,
        "processing_time_seconds": round(elapsed, 3),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )
