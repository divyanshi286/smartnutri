"""
Parent dashboard and family management endpoints
Endpoints for parents to monitor children's nutrition and progress
"""
from fastapi import APIRouter, HTTPException, Request, Query
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()


def calculate_streak_for_user(logs):
    """Calculate logging streak from progress logs"""
    if not logs:
        return 0
    
    current_streak = 0
    today = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Check if logged today or yesterday
    first_log_date = logs[0].get("date") if logs else None
    
    if first_log_date == today or first_log_date == yesterday:
        current_streak = 1
        
        # Count back from yesterday
        current_date = datetime.strptime(first_log_date, "%Y-%m-%d") - timedelta(days=1)
        
        for log in logs[1:]:
            if log.get("date") == current_date.strftime("%Y-%m-%d"):
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
    
    return current_streak


@router.get("/parent/dashboard")
async def get_parent_dashboard(request: Request, child: Optional[str] = Query(None)):
    """
    Get parent dashboard data.
    - If no child param: return list of children
    - If child name given: return child's nutrition and progress stats
    """
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get parent profile to verify they're a parent
        parent_profile = await db.profiles.find_one({"user_id": user_id})
        if not parent_profile or not parent_profile.get("isParent"):
            raise HTTPException(
                status_code=403,
                detail={"code": "NOT_PARENT", "message": "User is not registered as a parent"}
            )
        
        # If no child specified, return list of children
        if not child:
            children_cursor = db.users.find({"parent_id": user_id})
            children = await children_cursor.to_list(None)
            
            child_list = []
            for child_user in children:
                child_profile = await db.profiles.find_one({"user_id": str(child_user.get("_id"))})
                child_list.append({
                    "name": child_user.get("name"),
                    "userId": str(child_user.get("_id")),
                    "segment": child_profile.get("segment") if child_profile else None,
                    "age": child_user.get("age")
                })
            
            return {
                "success": True,
                "data": {
                    "children": child_list,
                    "total": len(child_list)
                }
            }
        
        # If child name specified, get that child's detailed dashboard
        child_user = await db.users.find_one({
            "name": child,
            "parent_id": user_id
        })
        
        if not child_user:
            raise HTTPException(
                status_code=404,
                detail={"code": "CHILD_NOT_FOUND", "message": f"Child '{child}' not found"}
            )
        
        child_id = str(child_user.get("_id"))
        
        # Get today's meals
        today = datetime.utcnow().strftime("%Y-%m-%d")
        meals_cursor = db.meal_logs.find({"user_id": child_id, "date": today})
        today_meals = await meals_cursor.to_list(None)
        
        # Calculate today's calories
        today_calories = sum(m.get("total_calories", 0) for m in today_meals)
        
        # Get last 30 progress logs for streak calculation
        start_date = datetime.utcnow() - timedelta(days=30)
        progress_cursor = db.progress_logs.find({
            "user_id": child_id,
            "created_at": {"$gte": start_date}
        }).sort("date", -1)
        progress_logs = await progress_cursor.to_list(None)
        
        # Calculate streak
        streak = calculate_streak_for_user(progress_logs)
        
        # Get last logged date
        last_logged = None
        if progress_logs:
            last_logged = progress_logs[0].get("date")
        
        # Format recent meals
        recent_meals = [
            {
                "name": m.get("name", "Unknown meal"),
                "calories": m.get("total_calories", 0),
                "mealType": m.get("meal_type", "other"),
                "time": m.get("created_at", ""),
            }
            for m in today_meals
        ]
        
        return {
            "success": True,
            "data": {
                "childName": child_user.get("name"),
                "userId": child_id,
                "stats": {
                    "todayCalories": today_calories,
                    "streak": streak,
                    "lastLogged": last_logged
                },
                "recentMeals": recent_meals
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "PARENT_DASHBOARD_ERROR", "message": str(e)}
        )
