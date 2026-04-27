"""
Food database and food search endpoints
Endpoints for searching foods, getting nutrition info, etc.
"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()

# Common Indian & Western foods with nutrition data (per 100g)
DEFAULT_FOODS = [
    # Grains
    {"name": "Rice (cooked)", "category": "grains", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4},
    {"name": "Wheat bread", "category": "grains", "calories": 269, "protein": 9, "carbs": 49, "fats": 3.3, "fiber": 7},
    {"name": "Roti (wheat)", "category": "grains", "calories": 265, "protein": 9.2, "carbs": 48, "fats": 3.7, "fiber": 7.3},
    {"name": "Oatmeal", "category": "grains", "calories": 389, "protein": 17, "carbs": 66, "fats": 7, "fiber": 10.6},
    {"name": "Basmati rice", "category": "grains", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4},
    
    # Proteins
    {"name": "Chicken breast", "category": "protein", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "fiber": 0},
    {"name": "Egg", "category": "protein", "calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "fiber": 0},
    {"name": "Lentils (cooked)", "category": "protein", "calories": 116, "protein": 9, "carbs": 20, "fats": 0.4, "fiber": 8},
    {"name": "Chickpeas (cooked)", "category": "protein", "calories": 134, "protein": 8.9, "carbs": 22, "fats": 2.4, "fiber": 6.4},
    {"name": "Paneer cheese", "category": "protein", "calories": 265, "protein": 26, "carbs": 3.6, "fats": 17, "fiber": 0},
    {"name": "Fish (salmon)", "category": "protein", "calories": 206, "protein": 22, "carbs": 0, "fats": 13, "fiber": 0},
    {"name": "Tofu", "category": "protein", "calories": 76, "protein": 8, "carbs": 2, "fats": 4.8, "fiber": 1.2},
    {"name": "Moong dal (cooked)", "category": "protein", "calories": 106, "protein": 7.7, "carbs": 19, "fats": 0.4, "fiber": 2.4},
    {"name": "Yogurt (plain)", "category": "protein", "calories": 59, "protein": 10, "carbs": 3.3, "fats": 0.4, "fiber": 0},
    
    # Vegetables
    {"name": "Spinach", "category": "vegetables", "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "fiber": 2.2},
    {"name": "Broccoli", "category": "vegetables", "calories": 34, "protein": 2.8, "carbs": 7, "fats": 0.4, "fiber": 2.4},
    {"name": "Tomato", "category": "vegetables", "calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2},
    {"name": "Carrot", "category": "vegetables", "calories": 41, "protein": 0.9, "carbs": 10, "fats": 0.2, "fiber": 2.8},
    {"name": "Bell pepper", "category": "vegetables", "calories": 31, "protein": 1, "carbs": 6, "fats": 0.3, "fiber": 2.2},
    {"name": "Cucumber", "category": "vegetables", "calories": 16, "protein": 0.7, "carbs": 3.6, "fats": 0.1, "fiber": 0.5},
    {"name": "Potato", "category": "vegetables", "calories": 77, "protein": 2, "carbs": 17, "fats": 0.1, "fiber": 2.1},
    
    # Fruits
    {"name": "Banana", "category": "fruits", "calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3, "fiber": 2.6},
    {"name": "Apple", "category": "fruits", "calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "fiber": 2.4},
    {"name": "Orange", "category": "fruits", "calories": 47, "protein": 0.9, "carbs": 12, "fats": 0.1, "fiber": 2.4},
    {"name": "Mango", "category": "fruits", "calories": 60, "protein": 0.8, "carbs": 15, "fats": 0.4, "fiber": 1.6},
    {"name": "Grape", "category": "fruits", "calories": 67, "protein": 0.6, "carbs": 17, "fats": 0.2, "fiber": 0.9},
    {"name": "Berry (mixed)", "category": "fruits", "calories": 45, "protein": 0.7, "carbs": 10, "fats": 0.3, "fiber": 2.4},
    
    # Nuts & Seeds
    {"name": "Almonds", "category": "nuts", "calories": 579, "protein": 21, "carbs": 22, "fats": 50, "fiber": 12.5},
    {"name": "Peanut butter", "category": "nuts", "calories": 588, "protein": 25, "carbs": 20, "fats": 50, "fiber": 6},
    {"name": "Sunflower seeds", "category": "nuts", "calories": 584, "protein": 23, "carbs": 20, "fats": 51, "fiber": 8.6},
    
    # Dairy
    {"name": "Milk (full fat)", "category": "dairy", "calories": 61, "protein": 3.2, "carbs": 4.8, "fats": 3.3, "fiber": 0},
    {"name": "Milk (skimmed)", "category": "dairy", "calories": 35, "protein": 3.4, "carbs": 4.7, "fats": 0.1, "fiber": 0},
    {"name": "Cheese", "category": "dairy", "calories": 402, "protein": 25, "carbs": 1.3, "fats": 33, "fiber": 0},
    
    # Oils & Condiments
    {"name": "Olive oil", "category": "oils", "calories": 884, "protein": 0, "carbs": 0, "fats": 100, "fiber": 0},
    {"name": "Coconut oil", "category": "oils", "calories": 884, "protein": 0, "carbs": 0, "fats": 100, "fiber": 0},
    
    # Prepared dishes (popular)
    {"name": "Dal makhani", "category": "prepared", "calories": 180, "protein": 12, "carbs": 15, "fats": 8, "fiber": 5},
    {"name": "Dal rice", "category": "prepared", "calories": 250, "protein": 11, "carbs": 42, "fats": 2, "fiber": 5},
    {"name": "Chicken curry", "category": "prepared", "calories": 150, "protein": 20, "carbs": 5, "fats": 6, "fiber": 1},
    {"name": "Butter chicken", "category": "prepared", "calories": 210, "protein": 18, "carbs": 8, "fats": 11, "fiber": 1},
    {"name": "Biryani", "category": "prepared", "calories": 280, "protein": 14, "carbs": 35, "fats": 9, "fiber": 2},
    {"name": "Samosa", "category": "snacks", "calories": 262, "protein": 3.4, "carbs": 32, "fats": 13, "fiber": 1.9},
    {"name": "Chikhalwali", "category": "snacks", "calories": 380, "protein": 12, "carbs": 45, "fats": 16, "fiber": 3},
]

@router.get("/foods/search")
async def search_foods(q: str = Query(..., min_length=1), category: Optional[str] = None, limit: int = 10):
    """
    Search for foods by name.
    
    Query Parameters:
    - q: Search query (required)
    - category: Filter by category (optional): grains, protein, vegetables, fruits, nuts, dairy, oils, prepared, snacks
    - limit: Max results to return (default 10)
    """
    if not q or len(q) < 1:
        raise HTTPException(status_code=400, detail={"code": "INVALID_QUERY", "message": "Search query required"})
    
    db = get_db()
    
    # Build search filter
    filters = {
        "name": {"$regex": q, "$options": "i"}  # Case-insensitive search
    }
    
    if category:
        filters["category"] = category
    
    # Search in database
    results = []
    cursor = db.food_database.find(filters).limit(limit)
    foods_list = await cursor.to_list(None)
    for food in foods_list:
        results.append({
            "id": str(food["_id"]),
            "name": food["name"],
            "category": food.get("category", "other"),
            "calories": food["calories"],
            "protein": food.get("protein", 0),
            "carbs": food.get("carbs", 0),
            "fats": food.get("fats", 0),
            "fiber": food.get("fiber", 0),
        })
    
    return {
        "success": True,
        "data": results
    }

@router.get("/foods/categories")
async def get_food_categories():
    """Get all available food categories"""
    categories = [
        {"id": "grains", "label": "Grains & Cereals", "emoji": "🌾"},
        {"id": "protein", "label": "Proteins", "emoji": "🥩"},
        {"id": "vegetables", "label": "Vegetables", "emoji": "🥗"},
        {"id": "fruits", "label": "Fruits", "emoji": "🍎"},
        {"id": "nuts", "label": "Nuts & Seeds", "emoji": "🥜"},
        {"id": "dairy", "label": "Dairy & Yogurt", "emoji": "🥛"},
        {"id": "oils", "label": "Oils & Fats", "emoji": "🌿"},
        {"id": "prepared", "label": "Ready Meals", "emoji": "🍜"},
        {"id": "snacks", "label": "Snacks", "emoji": "🍿"},
    ]
    return {"success": True, "data": categories}

@router.get("/foods/browse")
async def browse_foods(category: Optional[str] = None, limit: int = 20):
    """Browse foods by category"""
    db = get_db()
    
    filters = {}
    if category:
        filters["category"] = category
    
    results = []
    cursor = db.food_database.find(filters).limit(limit)
    foods_list = await cursor.to_list(None)
    for food in foods_list:
        results.append({
            "id": str(food["_id"]),
            "name": food["name"],
            "category": food.get("category", "other"),
            "calories": food["calories"],
            "protein": food.get("protein", 0),
            "carbs": food.get("carbs", 0),
            "fats": food.get("fats", 0),
            "fiber": food.get("fiber", 0),
        })
    
    return {
        "success": True,
        "data": results
    }

@router.get("/foods/{food_id}")
async def get_food_details(food_id: str):
    """Get detailed nutrition info for a food"""
    try:
        db = get_db()
        food = await db.food_database.find_one({"_id": ObjectId(food_id)})
        
        if not food:
            raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Food not found"})
        
        return {
            "success": True,
            "data": {
                "id": str(food["_id"]),
                "name": food["name"],
                "category": food.get("category", "other"),
                "calories": food["calories"],
                "protein": food.get("protein", 0),
                "carbs": food.get("carbs", 0),
                "fats": food.get("fats", 0),
                "fiber": food.get("fiber", 0),
                "per": "100g",
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "INVALID_ID", "message": str(e)})

@router.post("/foods/favorite")
async def add_favorite_food(request: Request, food_id: str):
    """Add a food to user's favorites"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    try:
        # Add to user's favorite foods
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorite_foods": food_id}}
        )
        
        return {
            "success": True,
            "data": {"added": result.modified_count > 0}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "ERROR", "message": str(e)})

@router.get("/foods/favorites")
async def get_favorite_foods(request: Request):
    """Get user's favorite foods for quick access"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
    favorite_ids = user_doc.get("favorite_foods", []) if user_doc else []
    
    results = []
    if favorite_ids:
        for fid in favorite_ids[:10]:  # Limit to 10 favorites
            try:
                food = await db.food_database.find_one({"_id": ObjectId(fid)})
                if food:
                    results.append({
                        "id": str(food["_id"]),
                        "name": food["name"],
                        "category": food.get("category", "other"),
                        "calories": food["calories"],
                        "protein": food.get("protein", 0),
                        "carbs": food.get("carbs", 0),
                        "fats": food.get("fats", 0),
                        "fiber": food.get("fiber", 0),
                    })
            except:
                pass
    
    return {
        "success": True,
        "data": results
    }
