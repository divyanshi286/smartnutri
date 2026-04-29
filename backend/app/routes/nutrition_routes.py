"""
Nutrition tracking and analysis routes
Endpoints for fetching nutrition data, targets, and breakdowns
"""
from fastapi import APIRouter, Request
from datetime import datetime
from bson import ObjectId
from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()

@router.get("/nutrition/today")
async def get_nutrition_today(request: Request):
    """Get today's nutrition breakdown"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Get today's meals
    meals = await db.meal_logs.find({
        "user_id": user_id,
        "date": today
    }).to_list(None)
    
    # Calculate nutrition totals
    total_calories = sum(m.get("total_calories", 0) for m in meals)
    total_protein = sum(m.get("total_protein_g", 0) for m in meals)
    total_carbs = sum(m.get("total_carbs_g", 0) for m in meals)
    total_fats = sum(m.get("total_fats_g", 0) for m in meals)
    total_fiber = sum(m.get("total_fiber_g", 0) for m in meals)
    
    # Get nutrition targets
    targets = await db.nutrition_targets.find_one({"user_id": user_id})
    
    # Default targets if not set
    default_targets = {
        "calories": 2000,
        "protein_g": 110,
        "carbs_g": 300,
        "fats_g": 65,
        "fiber_g": 25
    }
    
    if not targets:
        targets = default_targets
    else:
        # Merge with defaults for missing values
        for key, value in default_targets.items():
            if key not in targets:
                targets[key] = value
    
    # Calculate percentages
    cal_percent = round((total_calories / targets["calories"]) * 100) if targets["calories"] > 0 else 0
    protein_percent = round((total_protein / targets["protein_g"]) * 100) if targets["protein_g"] > 0 else 0
    carbs_percent = round((total_carbs / targets["carbs_g"]) * 100) if targets["carbs_g"] > 0 else 0
    fats_percent = round((total_fats / targets["fats_g"]) * 100) if targets["fats_g"] > 0 else 0
    
    return {
        "success": True,
        "data": {
            "date": today,
            "meals_count": len(meals),
            "nutrition": {
                "calories": {
                    "current": total_calories,
                    "goal": targets.get("calories", 2000),
                    "percent": min(cal_percent, 100),  # Cap at 100 for visual
                    "unit": "kcal"
                },
                "protein": {
                    "current": round(total_protein, 1),
                    "goal": targets.get("protein_g", 110),
                    "percent": min(protein_percent, 100),
                    "unit": "g"
                },
                "carbs": {
                    "current": round(total_carbs, 1),
                    "goal": targets.get("carbs_g", 300),
                    "percent": min(carbs_percent, 100),
                    "unit": "g"
                },
                "fats": {
                    "current": round(total_fats, 1),
                    "goal": targets.get("fats_g", 65),
                    "percent": min(fats_percent, 100),
                    "unit": "g"
                },
                "fiber": {
                    "current": round(total_fiber, 1),
                    "goal": targets.get("fiber_g", 25),
                    "percent": min(round((total_fiber / targets.get("fiber_g", 25)) * 100), 100) if targets.get("fiber_g", 25) > 0 else 0,
                    "unit": "g"
                }
            },
            "meals": [
                {
                    "name": m.get("food_name", ""),
                    "type": m.get("meal_type", ""),
                    "calories": m.get("total_calories", 0),
                    "protein": round(m.get("total_protein_g", 0), 1),
                    "time": m.get("time", "")
                }
                for m in sorted(meals, key=lambda x: x.get("time", ""))
            ]
        }
    }


@router.get("/nutrition/summary")
async def get_nutrition_summary(request: Request, days: int = 7):
    """Get nutrition summary for past N days"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    from datetime import timedelta
    
    # Get meals for last N days
    start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    meals = await db.meal_logs.find({
        "user_id": user_id,
        "date": {"$gte": start_date}
    }).to_list(None)
    
    # Group by date and calculate averages
    by_date = {}
    for meal in meals:
        date = meal.get("date", "")
        if date not in by_date:
            by_date[date] = {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fats": 0,
                "count": 0
            }
        by_date[date]["calories"] += meal.get("total_calories", 0)
        by_date[date]["protein"] += meal.get("total_protein_g", 0)
        by_date[date]["carbs"] += meal.get("total_carbs_g", 0)
        by_date[date]["fats"] += meal.get("total_fats_g", 0)
        by_date[date]["count"] += 1
    
    # Calculate averages
    avg_calories = sum(d["calories"] for d in by_date.values()) / len(by_date) if by_date else 0
    avg_protein = sum(d["protein"] for d in by_date.values()) / len(by_date) if by_date else 0
    avg_carbs = sum(d["carbs"] for d in by_date.values()) / len(by_date) if by_date else 0
    avg_fats = sum(d["fats"] for d in by_date.values()) / len(by_date) if by_date else 0
    
    return {
        "success": True,
        "data": {
            "period_days": days,
            "meals_logged": len(meals),
            "days_with_logs": len(by_date),
            "averages": {
                "calories": round(avg_calories),
                "protein": round(avg_protein, 1),
                "carbs": round(avg_carbs, 1),
                "fats": round(avg_fats, 1)
            },
            "daily": [
                {
                    "date": date,
                    "calories": by_date[date]["calories"],
                    "protein": round(by_date[date]["protein"], 1),
                    "carbs": round(by_date[date]["carbs"], 1),
                    "fats": round(by_date[date]["fats"], 1),
                    "meals": by_date[date]["count"]
                }
                for date in sorted(by_date.keys())
            ]
        }
    }
