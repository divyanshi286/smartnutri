"""
Cycle tracking and women's health endpoints
Endpoints for tracking menstrual cycle, mood, symptoms, and hormone-aware nutrition
"""
from fastapi import APIRouter, HTTPException, Request, Query
from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId

from app.models import CycleDataSchema
from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()

# Cycle phase definitions
CYCLE_PHASES = {
    "menstrual": {
        "day_range": (1, 5),
        "label": "Menstrual Phase",
        "emoji": "🩸",
        "description": "Shedding uterine lining",
        "nutrition_tips": [
            "🥩 Iron-rich foods: red meat, spinach, lentils",
            "🧂 Salt intake may help with water retention",
            "☕ Magnesium for cramps: seeds, dark chocolate",
            "🥛 Increase calcium intake",
            "💧 Stay hydrated",
        ],
        "symptoms": ["heavy bleeding", "cramps", "fatigue", "mood swings"],
        "activity": "Light exercise (walking, yoga, stretching)"
    },
    "follicular": {
        "day_range": (6, 14),
        "label": "Follicular Phase",
        "emoji": "🌱",
        "description": "Estrogen rising, energy increasing",
        "nutrition_tips": [
            "🥕 Eat more raw fruits and vegetables",
            "💪 Increase protein & carbs for workouts",
            "🥗 Light, fresh foods work best",
            "🍌 Complex carbs for sustained energy",
            "🧅 Balance electrolytes",
        ],
        "symptoms": ["high energy", "clear skin", "good mood"],
        "activity": "High-intensity workouts, strength training"
    },
    "ovulation": {
        "day_range": (15, 17),
        "label": "Ovulation",
        "emoji": "⭐",
        "description": "Peak fertility, highest energy",
        "nutrition_tips": [
            "🔥 Peak energy - increase calorie needs",
            "🥒 May need more antioxidants",
            "🌰 Include omega-3 foods",
            "🥤 Stay heavily hydrated",
            "🍌 Carbs to support high activity",
        ],
        "symptoms": ["higher body temperature", "increased libido", "peak energy"],
        "activity": "Best time for PRs and challenging workouts"
    },
    "luteal": {
        "day_range": (18, 28),
        "label": "Luteal Phase",
        "emoji": "🌙",
        "description": "Progesterone rising, energy declining toward period",
        "nutrition_tips": [
            "🥜 Increase healthy fats (nuts, seeds, avocado)",
            "🍫 Magnesium-rich foods for mood",
            "🥛 Increase calcium (especially week before period)",
            "🥦 More vegetables, less processed food",
            "💤 May need more calories (200-300 extra)",
        ],
        "symptoms": ["mood swings", "bloating", "fatigue", "cravings"],
        "activity": "Resistance training, lower-intensity steady cardio"
    },
}

def calculate_cycle_phase(last_period_date: str, cycle_length: int = 28) -> dict:
    """Calculate current cycle phase based on last period date"""
    try:
        last_date = datetime.strptime(last_period_date, "%Y-%m-%d")
        days_since_period = (datetime.utcnow() - last_date).days
        
        # Handle different cycle lengths
        cycle_day = (days_since_period % cycle_length) + 1
        
        # Determine phase
        phase_key = None
        for phase, info in CYCLE_PHASES.items():
            day_range = info["day_range"]
            if day_range[0] <= cycle_day <= day_range[1]:
                phase_key = phase
                break
        
        if not phase_key:
            phase_key = "menstrual"  # Default
        
        phase_info = CYCLE_PHASES[phase_key]
        
        return {
            "phase": phase_key,
            "label": phase_info["label"],
            "emoji": phase_info["emoji"],
            "cycleDay": cycle_day,
            "daysUntilMenses": max(0, CYCLE_PHASES["menstrual"]["day_range"][1] - cycle_day),
            "description": phase_info["description"],
            "nutritionTips": phase_info["nutrition_tips"],
            "symptoms": phase_info["symptoms"],
            "recommendedActivity": phase_info["activity"],
        }
    except Exception as e:
        print(f"Error calculating cycle phase: {e}")
        return {
            "phase": "unknown",
            "label": "Tracking not started",
            "emoji": "❓",
            "cycleDay": 0,
            "daysUntilMenses": 0,
            "description": "Start tracking your cycle for personalized nutrition",
            "nutritionTips": ["Log your last period date to get started"],
            "symptoms": [],
            "recommendedActivity": "Moderate activity"
        }

@router.get("/api/cycle")
async def get_cycle_info(request: Request):
    """Get current cycle phase and nutrition recommendations"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get user profile
        profile = await db.profiles.find_one({"user_id": user_id})
        
        if not profile or not profile.get("cycle_data"):
            return {
                "success": True,
                "data": {
                    "phase": "not_started",
                    "label": "Not tracking",
                    "emoji": "❓",
                    "cycleDay": 0,
                    "message": "Start cycle tracking to get personalized nutrition advice",
                    "nutritionTips": [],
                }
            }
        
        cycle_data = profile.get("cycle_data", {})
        last_period_date = cycle_data.get("lastPeriodDate")
        cycle_length = cycle_data.get("cycleLength", 28)
        
        if not last_period_date:
            return {
                "success": True,
                "data": {
                    "phase": "not_started",
                    "label": "No tracking data",
                    "emoji": "❓",
                    "cycleDay": 0,
                    "message": "Log your last period date to get started",
                    "nutritionTips": [],
                }
            }
        
        # Calculate phase
        phase_info = calculate_cycle_phase(last_period_date, cycle_length)
        
        # Get recent mood logs
        mood_logs = []
        cursor = db.cycle_mood_logs.find({"user_id": user_id}).sort("date", -1).limit(7)
        mood_logs_list = await cursor.to_list(None)
        for log in mood_logs_list:
            mood_logs.append({
                "date": log.get("date"),
                "mood": log.get("mood"),
                "symptom": log.get("symptom"),
            })
        
        phase_info["recentMoodLogs"] = mood_logs
        
        return {
            "success": True,
            "data": phase_info
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Cycle error: {e}")
        raise HTTPException(
            status_code=500,
            detail={"code": "CYCLE_ERROR", "message": "Failed to fetch cycle info"}
        )

@router.put("/api/cycle/update")
async def update_cycle_data(cycle_data: CycleDataSchema, request: Request):
    """Update cycle tracking data"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Update user profile with cycle data
        result = await db.profiles.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "cycle_data": {
                        "lastPeriodDate": cycle_data.lastPeriodDate,
                        "cycleLength": cycle_data.cycleLength,
                        "symptoms": cycle_data.symptoms,
                    },
                    "updated_at": datetime.utcnow(),
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Profile not found"})
        
        # Recalculate phase
        phase_info = calculate_cycle_phase(
            cycle_data.lastPeriodDate,
            cycle_data.cycleLength or 28
        )
        
        return {
            "success": True,
            "data": {
                "message": "Cycle data updated",
                **phase_info
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "UPDATE_ERROR", "message": str(e)}
        )

@router.post("/api/cycle/mood")
async def log_mood(request: Request, mood: Optional[str] = None, symptom: Optional[str] = None, notes: Optional[str] = None):
    """Log mood and symptoms for cycle tracking"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get today's date
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Check if already logged today
        existing = await db.cycle_mood_logs.find_one({
            "user_id": user_id,
            "date": today
        })
        
        mood_log = {
            "user_id": user_id,
            "date": today,
            "mood": mood or "neutral",
            "symptom": symptom or "",
            "notes": notes or "",
            "created_at": datetime.utcnow(),
        }
        
        if existing:
            # Update existing entry
            await db.cycle_mood_logs.update_one(
                {"_id": existing["_id"]},
                {"$set": mood_log}
            )
            return {
                "success": True,
                "data": {"message": "Mood updated"}
            }
        else:
            # Create new entry
            result = await db.cycle_mood_logs.insert_one(mood_log)
            return {
                "success": True,
                "data": {
                    "id": str(result.inserted_id),
                    "message": "Mood logged"
                }
            }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "MOOD_ERROR", "message": str(e)}
        )

@router.get("/api/cycle/predictions")
async def get_cycle_predictions(request: Request, days_ahead: int = 30):
    """Get predictions for upcoming cycle phases"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        profile = await db.profiles.find_one({"user_id": user_id})
        
        if not profile or not profile.get("cycle_data"):
            return {
                "success": True,
                "data": []
            }
        
        cycle_data = profile.get("cycle_data", {})
        last_period_date = cycle_data.get("lastPeriodDate")
        cycle_length = cycle_data.get("cycleLength", 28)
        
        if not last_period_date:
            return {
                "success": True,
                "data": []
            }
        
        # Generate predictions
        predictions = []
        last_date = datetime.strptime(last_period_date, "%Y-%m-%d")
        
        for day_offset in range(days_ahead):
            future_date = last_date + timedelta(days=day_offset + 1)
            days_since = (future_date - last_date).days
            cycle_day = (days_since % cycle_length) + 1
            
            # Get phase for this day
            phase_key = None
            for phase, info in CYCLE_PHASES.items():
                day_range = info["day_range"]
                if day_range[0] <= cycle_day <= day_range[1]:
                    phase_key = phase
                    break
            
            if phase_key:
                phase_info = CYCLE_PHASES[phase_key]
                predictions.append({
                    "date": future_date.strftime("%Y-%m-%d"),
                    "cycleDay": cycle_day,
                    "phase": phase_key,
                    "label": phase_info["label"],
                    "emoji": phase_info["emoji"],
                })
        
        return {
            "success": True,
            "data": predictions
        }
    
    except Exception as e:
        import traceback
        error_msg = str(e) or traceback.format_exc()
        print(f"[PREDICTION_ERROR] {error_msg}")
        raise HTTPException(
            status_code=500,
            detail={"code": "PREDICTION_ERROR", "message": error_msg}
        )

@router.get("/api/cycle/stats")
async def get_cycle_stats(request: Request, days: int = 90):
    """Get cycle statistics and patterns"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get mood logs for the period
        start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        mood_logs = []
        cursor = db.cycle_mood_logs.find({
            "user_id": user_id,
            "date": {"$gte": start_date}
        }).sort("date", 1)
        mood_logs = await cursor.to_list(None)
        
        # Count moods
        mood_counts = {}
        symptom_counts = {}
        
        for log in mood_logs:
            mood = log.get("mood", "neutral")
            symptom = log.get("symptom", "")
            
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            if symptom:
                symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        
        return {
            "success": True,
            "data": {
                "totalLogs": len(mood_logs),
                "period": f"{days} days",
                "moodDistribution": mood_counts,
                "commonSymptoms": sorted(
                    [(s, c) for s, c in symptom_counts.items()],
                    key=lambda x: x[1],
                    reverse=True
                )[:5],
            }
        }
    
    except Exception as e:
        import traceback
        error_msg = str(e) or traceback.format_exc()
        print(f"[STATS_ERROR] {error_msg}")
        raise HTTPException(
            status_code=500,
            detail={"code": "STATS_ERROR", "message": error_msg}
        )
