from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"

@app.get("/api/classify")
async def classify_name(name: str = Query(...)):
    
    # Validate empty string
    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Name parameter cannot be empty"}
        )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})
        
        if response.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"status": "error", "message": "Upstream API failure"}
            )

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # Edge case handling
        if gender is None or count == 0:
            return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "message": "No prediction available for the provided name"
                }
            )

        # Compute confidence
        is_confident = probability >= 0.7 and count >= 100

        # Generate timestamp (UTC ISO 8601)
        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "status": "success",
            "data": {
                "name": name.lower(),
                "gender": gender,
                "probability": probability,
                "sample_size": count,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }

    except httpx.RequestError:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"}
        )