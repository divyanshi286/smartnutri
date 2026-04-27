"""
Meal logging and nutrition routes
Endpoints for logging meals, getting daily/weekly nutrition, etc.
"""
from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
import json

from app.models import MealLogRequest, MealLogResponse
from app.database import get_db
from app.routes.auth_routes import get_current_user
from app.json_encoder import to_json_serializable

router = APIRouter()

@router.post("/meals/log")
async def log_meal(req: MealLogRequest, request: Request):
    """Log a meal for the user"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    # Calculate totals
    total_calories = sum(f.calories for f in req.foods)
    total_protein = sum(f.protein_g for f in req.foods)
    total_carbs = sum(f.carbs_g for f in req.foods)
    total_fats = sum(f.fats_g for f in req.foods)
    
    meal_log = {
        "user_id": user_id,
        "meal_type": req.meal_type,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "foods": [dict(f) for f in req.foods],
        "total_calories": total_calories,
        "total_protein_g": total_protein,
        "total_carbs_g": total_carbs,
        "total_fats_g": total_fats,
        "notes": req.notes,
        "photo_url": req.photo_url,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    result = await db.meal_logs.insert_one(meal_log)
    meal_log["_id"] = str(result.inserted_id)
    
    return {
        "success": True,
        "data": {
            "id": str(result.inserted_id),
            "mealType": req.meal_type,
            "totalCalories": total_calories,
            "totalProtein": total_protein,
            "totalCarbs": total_carbs,
            "totalFats": total_fats,
        }
    }

@router.get("/meals/date/{date_str}")
async def get_meals_by_date(date_str: str, request: Request):
    """Get all meals for a specific date (format: YYYY-MM-DD)"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    try:
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail={"code": "INVALID_DATE", "message": "Date must be YYYY-MM-DD"})
    
    # Get nutrition targets for reference
    targets = await db.nutrition_targets.find_one({"user_id": user_id})
    
    # Get all meals for this date
    meals = await db.meal_logs.find({
        "user_id": user_id,
        "date": date_str
    }).sort("created_at", 1).to_list(None)
    
    # Calculate daily totals
    total_calories = sum(m["total_calories"] for m in meals)
    total_protein = sum(m["total_protein_g"] for m in meals)
    total_carbs = sum(m["total_carbs_g"] for m in meals)
    total_fats = sum(m["total_fats_g"] for m in meals)
    total_water = 0  # Would need separate water log
    
    # Format meals for frontend
    formatted_meals = []
    for meal in meals:
        formatted_meals.append({
            "id": str(meal["_id"]),
            "name": meal.get("notes", f"{meal['meal_type'].capitalize()} - {meal['total_calories']:.0f} cal"),
            "type": meal["meal_type"],
            "emoji": get_meal_emoji(meal["meal_type"]),
            "calories": meal["total_calories"],
            "time": get_meal_time(meal["meal_type"]),
            "bg": get_meal_color(meal["meal_type"]),
            "foods": to_json_serializable(meal.get("foods", [])),
        })
    
    # Build targets array
    targets_data = [
        {
            "label": "Calories",
            "current": total_calories,
            "goal": targets.get("calories", 2000) if targets else 2000,
            "color": "#FF6B6B",
            "valueColor": "#FF6B6B",
            "warn": total_calories > (targets.get("calories", 2000) if targets else 2000) * 1.1,
        },
        {
            "label": "Protein",
            "current": total_protein,
            "goal": targets.get("protein_g", 110) if targets else 110,
            "color": "#4169E1",
            "valueColor": "#4169E1",
            "warn": total_protein < (targets.get("protein_g", 110) if targets else 110) * 0.8,
        },
        {
            "label": "Carbs",
            "current": total_carbs,
            "goal": targets.get("carbs_g", 250) if targets else 250,
            "color": "#FFB84D",
            "valueColor": "#FFB84D",
            "warn": False,
        },
        {
            "label": "Fats",
            "current": total_fats,
            "goal": targets.get("fats_g", 70) if targets else 70,
            "color": "#90EE90",
            "valueColor": "#90EE90",
            "warn": False,
        },
    ]
    
    return {
        "success": True,
        "data": {
            "date": date_str,
            "totalCalories": total_calories,
            "totalProtein": total_protein,
            "totalCarbs": total_carbs,
            "totalFats": total_fats,
            "totalWater": total_water,
            "items": formatted_meals,
            "targets": targets_data,
        }
    }

@router.get("/meals/week")
async def get_weekly_meals(request: Request):
    """Get meals summary for the last 7 days"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    # Get meals for last 7 days
    start_date = (datetime.utcnow() - timedelta(days=7))
    
    meals = await db.meal_logs.find({
        "user_id": user_id,
        "created_at": {"$gte": start_date}
    }).to_list(None)
    
    # Group by date
    meals_by_date = {}
    for meal in meals:
        date = meal["date"]
        if date not in meals_by_date:
            meals_by_date[date] = {
                "date": date,
                "totalCalories": 0,
                "protein": 0,
                "count": 0,
            }
        meals_by_date[date]["totalCalories"] += meal["total_calories"]
        meals_by_date[date]["protein"] += meal["total_protein_g"]
        meals_by_date[date]["count"] += 1
    
    return {
        "success": True,
        "data": {
            "period": "7_days",
            "daily": meals_by_date,
            "totalMeals": len(meals),
        }
    }

@router.delete("/api/meals/{meal_id}")
async def delete_meal(meal_id: str, request: Request):
    """Delete a meal log"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    try:
        meal_oid = ObjectId(meal_id)
    except:
        raise HTTPException(status_code=400, detail={"code": "INVALID_ID", "message": "Invalid meal ID"})
    
    # Verify ownership
    meal = await db.meal_logs.find_one({"_id": meal_oid, "user_id": user_id})
    if not meal:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Meal not found"})
    
    await db.meal_logs.delete_one({"_id": meal_oid})
    
    return {
        "success": True,
        "data": {"message": "Meal deleted"}
    }

@router.get("/nutrition/today")
async def get_today_nutrition(request: Request):
    """Get today's nutrition summary"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Get today's meals
    meals = await db.meal_logs.find({
        "user_id": user_id,
        "date": today
    }).to_list(None)
    
    # Get targets
    targets = await db.nutrition_targets.find_one({"user_id": user_id})
    
    # Calculate totals
    total_calories = sum(m["total_calories"] for m in meals)
    total_protein = sum(m["total_protein_g"] for m in meals)
    total_carbs = sum(m["total_carbs_g"] for m in meals)
    total_fats = sum(m["total_fats_g"] for m in meals)
    
    return {
        "success": True,
        "data": {
            "date": today,
            "nutrition": {
                "calories": {
                    "current": total_calories,
                    "goal": targets.get("calories", 2000) if targets else 2000,
                    "remaining": max(0, (targets.get("calories", 2000) if targets else 2000) - total_calories),
                },
                "protein": {
                    "current": total_protein,
                    "goal": targets.get("protein_g", 110) if targets else 110,
                    "remaining": max(0, (targets.get("protein_g", 110) if targets else 110) - total_protein),
                },
                "carbs": {
                    "current": total_carbs,
                    "goal": targets.get("carbs_g", 250) if targets else 250,
                },
                "fats": {
                    "current": total_fats,
                    "goal": targets.get("fats_g", 70) if targets else 70,
                },
            },
            "mealsLogged": len(meals),
        }
    }

# Helper functions
def get_meal_emoji(meal_type: str) -> str:
    """Get emoji for meal type"""
    emoji_map = {
        "breakfast": "🍳",
        "lunch": "🥗",
        "dinner": "🍽",
        "snack": "🍌",
    }
    return emoji_map.get(meal_type, "🍽")

def get_meal_time(meal_type: str) -> str:
    """Get typical meal time"""
    time_map = {
        "breakfast": "08:00 AM",
        "lunch": "12:30 PM",
        "dinner": "07:00 PM",
        "snack": "03:00 PM",
    }
    return time_map.get(meal_type, "12:00 PM")

def get_meal_color(meal_type: str) -> str:
    """Get color for meal type"""
    color_map = {
        "breakfast": "#FFD700",
        "lunch": "#FF6347",
        "dinner": "#4169E1",
        "snack": "#90EE90",
    }
    return color_map.get(meal_type, "#808080")
