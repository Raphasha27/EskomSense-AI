from fastapi import FastAPI
import random

app = FastAPI(title="EskomSense AI Inference API")

@app.get("/predict")
async def predict_stage(hours_ahead: int = 24):
    """
    Mock endpoint simulating the LSTM model inference.
    In production, this loads the PyTorch model and runs forward pass.
    """
    predictions = []
    for i in range(hours_ahead):
        predictions.append({
            "hour_offset": i + 1,
            "predicted_stage": random.choice([0, 1, 2, 3, 4, 5, 6]),
            "confidence": round(random.uniform(0.65, 0.95), 2)
        })
        
    return {"area": "Cape Town", "predictions": predictions}
