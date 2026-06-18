from fastapi import APIRouter, HTTPException, Query
import pendulum

router = APIRouter()

AREAS = {
    "johannesburg": "City of Johannesburg",
    "pretoria": "City of Tshwane",
    "cape_town": "City of Cape Town",
    "durban": "eThekwini",
    "ekurhuleni": "City of Ekurhuleni",
}

STAGES = [0, 1, 2, 3, 4, 5, 6, 7, 8]
MOCK_SOURCE = "mock_data"


def _mock_schedule(area: str, days: int) -> list[dict]:
    now = pendulum.now()
    schedule = []
    for d in range(days):
        date = now.add(days=d)
        stage = (hash(area + date.to_date_string()) % 9) % 6  # stage 0-5
        schedule.append({
            "date": date.to_date_string(),
            "stage": stage,
            "start": "06:00",
            "end": "08:30",
            "areas_affected": list(AREAS.keys())[:stage] if stage > 0 else [],
            "source": MOCK_SOURCE,
        })
    return schedule


def _mock_predictions(area: str, hours: int) -> list[dict]:
    now = pendulum.now()
    predictions = []
    for h in range(hours):
        ts = now.add(hours=h)
        day_offset = (ts.date() - now.date()).days
        hour = ts.hour
        base = (hash(area + str(day_offset)) % 9) % 5
        if 6 <= hour <= 8 or 16 <= hour <= 18:
            stage = min(8, base + 1)
        else:
            stage = base
        predictions.append({
            "timestamp": ts.isoformat(),
            "predicted_stage": stage,
            "confidence_lower": max(0, stage - 1),
            "confidence_upper": min(8, stage + 1),
            "source": MOCK_SOURCE,
        })
    return predictions


@router.get("/health")
async def health_check(mock: bool = Query(True, description="Use mock data")):
    return {"status": "ok", "system": "EskomSense AI", "data_source": MOCK_SOURCE if mock else "live"}


@router.get("/schedule")
async def get_schedule(
    area: str = Query(..., description="Municipal area code"),
    days: int = Query(7, ge=1, le=14, description="Forecast days"),
    mock: bool = Query(True, description="Use mock data"),
):
    if area not in AREAS:
        raise HTTPException(404, f"Unknown area '{area}'. Options: {list(AREAS.keys())}")
    schedule = _mock_schedule(area, days) if mock else []
    return {
        "area": AREAS[area],
        "days": days,
        "schedule": schedule,
        "source": MOCK_SOURCE if mock else "eskom_api",
    }


@router.get("/predict")
async def predict_load_shedding(
    area: str = Query(..., description="Municipal area code"),
    hours: int = Query(48, ge=1, le=168, description="Prediction horizon in hours"),
    mock: bool = Query(True, description="Use mock data"),
):
    if area not in AREAS:
        raise HTTPException(404, f"Unknown area '{area}'. Options: {list(AREAS.keys())}")
    predictions = _mock_predictions(area, hours) if mock else []
    return {
        "area": AREAS[area],
        "horizon_hours": hours,
        "predictions": predictions,
        "confidence": 0.75,
        "model": "mock-v1",
        "source": MOCK_SOURCE if mock else "prophet-v1",
    }


@router.get("/areas")
async def list_areas(mock: bool = Query(True, description="Use mock data")):
    return {"areas": [{"code": k, "name": v} for k, v in AREAS.items()]}


@router.get("/optimize/battery")
async def optimize_battery(
    capacity_kwh: float = Query(..., description="Battery capacity in kWh"),
    current_charge: float = Query(..., description="Current charge level in kWh"),
    critical_load_kw: float = Query(..., description="Essential load in kW"),
    mock: bool = Query(True, description="Use mock data"),
):
    backup_hours = current_charge / critical_load_kw if critical_load_kw > 0 else 0
    soc_pct = (current_charge / capacity_kwh * 100) if capacity_kwh > 0 else 0
    return {
        "capacity_kwh": capacity_kwh,
        "current_charge_kwh": current_charge,
        "state_of_charge_pct": round(soc_pct, 1),
        "critical_load_kw": critical_load_kw,
        "estimated_backup_hours": round(backup_hours, 1),
        "recommendation": "Charge to full before next scheduled stage"
        if backup_hours < 4
        else "Sufficient charge for next 24h",
        "source": MOCK_SOURCE if mock else "optimizer",
    }
