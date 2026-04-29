"""
Voice input routes for meal logging
Handles transcription-to-meal conversion using NLP parsing
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from app.routes.auth_routes import get_current_user
from app.database import db
import re
from typing import Dict, List, Optional

router = APIRouter()

# Pydantic models
class VoiceMealLog(BaseModel):
    mealDescription: str
    timestamp: Optional[str] = None
    confidence: float = 1.0

class MealLogResponse(BaseModel):
    id: str
    foodName: str
    calories: int
    protein: float
    carbs: float
    fat: float
    timestamp: str
    source: str
    confidence: float

# Food database with nutritional values
FOOD_DATABASE = {
    # Proteins
    "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "unit": "100g"},
    "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "unit": "100g"},
    "fish": {"calories": 100, "protein": 20, "carbs": 0, "fat": 1, "unit": "100g"},
    "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "unit": "100g"},
    "turkey": {"calories": 135, "protein": 30, "carbs": 0, "fat": 0.7, "unit": "100g"},
    "pork": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14, "unit": "100g"},
    "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "unit": "1 large"},
    "tofu": {"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "unit": "100g"},
    
    # Carbs
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "unit": "100g cooked"},
    "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "unit": "100g cooked"},
    "bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.3, "unit": "1 slice"},
    "potato": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "unit": "100g"},
    "sweet potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "unit": "100g"},
    "oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7, "unit": "100g"},
    
    # Vegetables
    "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "unit": "100g"},
    "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "unit": "100g"},
    "spinach": {"calories": 23, "protein": 2.9, "carbs": 4, "fat": 0.4, "unit": "100g"},
    "kale": {"calories": 49, "protein": 4.3, "carbs": 9, "fat": 0.9, "unit": "100g"},
    "lettuce": {"calories": 15, "protein": 1.4, "carbs": 2.9, "fat": 0.2, "unit": "100g"},
    "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "unit": "100g"},
    
    # Fruits
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "unit": "100g"},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "unit": "100g"},
    "orange": {"calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.3, "unit": "100g"},
    "strawberry": {"calories": 32, "protein": 0.8, "carbs": 8, "fat": 0.3, "unit": "100g"},
    "blueberry": {"calories": 57, "protein": 0.7, "carbs": 14, "fat": 0.3, "unit": "100g"},
    
    # Meals/Combinations
    "sandwich": {"calories": 450, "protein": 20, "carbs": 45, "fat": 15, "unit": "1"},
    "burger": {"calories": 540, "protein": 28, "carbs": 41, "fat": 28, "unit": "1"},
    "pizza": {"calories": 285, "protein": 12, "carbs": 36, "fat": 10, "unit": "1 slice"},
    "salad": {"calories": 150, "protein": 8, "carbs": 12, "fat": 8, "unit": "1"},
    "fries": {"calories": 365, "protein": 4, "carbs": 48, "fat": 17, "unit": "100g"},
    "soup": {"calories": 100, "protein": 5, "carbs": 15, "fat": 3, "unit": "1 cup"},
    "pasta": {"calories": 221, "protein": 8, "carbs": 43, "fat": 1.4, "unit": "100g cooked"},
}

# Quantity multipliers
QUANTITY_MULTIPLIERS = {
    "small": 0.7,
    "medium": 1.0,
    "large": 1.3,
    "extra large": 1.6,
    "huge": 2.0,
    "tiny": 0.5,
    "double": 2.0,
}

@router.post("/log-meal")
async def log_meal_with_voice(
    voice_data: VoiceMealLog,
    current_user: dict = Depends(get_current_user)
):
    """
    Log meal from voice description.
    Uses NLP parsing to extract food, quantity, and estimates calories.
    
    Example input: "I had a grilled chicken with rice and broccoli"
    """
    try:
        description = voice_data.mealDescription.lower().strip()
        
        # Parse the meal description
        parsed_meal = parse_meal_description(description)
        
        # Create meal log document
        meal_log = {
            "userId": str(current_user.get("_id")),
            "foodName": parsed_meal["foodName"],
            "quantity": parsed_meal["quantity"],
            "calories": round(parsed_meal["calories"]),
            "carbs": round(parsed_meal["carbs"], 1),
            "protein": round(parsed_meal["protein"], 1),
            "fat": round(parsed_meal["fat"], 1),
            "timestamp": voice_data.timestamp or datetime.now().isoformat(),
            "source": "voice",
            "confidence": voice_data.confidence,
            "originalTranscript": description,
            "createdAt": datetime.now().isoformat()
        }
        
        # Insert into database
        result = await db.meals.insert_one(meal_log)
        meal_log["_id"] = str(result.inserted_id)
        
        return meal_log
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log meal: {str(e)}")


def parse_meal_description(description: str) -> Dict:
    """
    Parse meal description to extract nutrients using simple NLP.
    
    Args:
        description: User's spoken meal description (e.g., "I had grilled chicken with rice")
    
    Returns:
        Dictionary with:
        - foodName: Human-readable meal name
        - quantity: Estimated quantity
        - calories: Total estimated calories
        - protein, carbs, fat: Macronutrient breakdown
    
    Examples:
        "chicken and rice" → {calories: 280, protein: 35, ...}
        "large pizza with extra cheese" → {calories: 570, ...}
        "apple and banana" → {calories: 141, ...}
    """
    
    # Clean up description
    description = re.sub(r'\bi |a |an ', ' ', description)  # Remove articles
    description = re.sub(r'(very|really|so) ', '', description)  # Remove intensifiers
    
    # Extract quantity modifier if present
    quantity_modifier = 1.0
    for size_word, multiplier in QUANTITY_MULTIPLIERS.items():
        if size_word in description:
            quantity_modifier = multiplier
            break
    
    # Find all food items mentioned
    found_foods = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for food_name, nutrients in FOOD_DATABASE.items():
        # Check if food is mentioned in description
        if food_name in description or f"{food_name}s" in description:
            found_foods.append(food_name)
            
            # Apply quantity modifier only to single items, not combinations
            multiplier = quantity_modifier if len(found_foods) == 1 else 1.0
            
            total_calories += nutrients["calories"] * multiplier
            total_protein += nutrients["protein"] * multiplier
            total_carbs += nutrients["carbs"] * multiplier
            total_fat += nutrients["fat"] * multiplier
    
    # Generate food name
    if found_foods:
        food_name = " with ".join(found_foods)
        # Capitalize
        food_name = " ".join(word.capitalize() for word in food_name.split())
    else:
        # No recognized foods, use generic description
        food_name = description.capitalize()
        # Provide average meal estimate
        total_calories = 300
        total_protein = 15
        total_carbs = 35
        total_fat = 10
    
    # Add size description if applicable
    if quantity_modifier != 1.0:
        size_word = [k for k, v in QUANTITY_MULTIPLIERS.items() if v == quantity_modifier][0]
        food_name = f"{size_word.capitalize()} {food_name}"
    
    return {
        "foodName": food_name,
        "quantity": quantity_modifier,
        "calories": max(int(total_calories), 1),  # Minimum 1 calorie
        "protein": max(total_protein, 0.1),
        "carbs": max(total_carbs, 0.1),
        "fat": max(total_fat, 0.1),
        "identifiedFoods": found_foods
    }


@router.get("/food-suggestions")
async def get_food_suggestions(query: str = ""):
    """
    Get food suggestions from database for autocomplete.
    Useful for showing users what foods are recognized.
    """
    query = query.lower().strip()
    
    if not query:
        # Return most common foods
        common_foods = ["chicken", "beef", "rice", "salad", "pizza", "burger", "apple", "egg"]
        return {"suggestions": common_foods}
    
    # Find matching foods
    suggestions = [
        food for food in FOOD_DATABASE.keys()
        if food.startswith(query) or query in food
    ]
    
    return {"suggestions": suggestions[:10]}


@router.get("/food-info")
async def get_food_info(food_name: str):
    """
    Get detailed nutritional information for a specific food.
    """
    food_name = food_name.lower().strip()
    
    if food_name not in FOOD_DATABASE:
        raise HTTPException(status_code=404, detail=f"Food '{food_name}' not found in database")
    
    food_info = FOOD_DATABASE[food_name]
    return {
        "foodName": food_name.capitalize(),
        "servingSize": food_info.get("unit", "per 100g"),
        "calories": food_info["calories"],
        "protein": food_info["protein"],
        "carbs": food_info["carbs"],
        "fat": food_info["fat"]
    }


@router.get("/examples")
async def get_voice_examples():
    """
    Get example voice commands for the user.
    """
    return [
        "Log dal rice for lunch",
        "How much protein do I have today?",
        "Add 2 glasses of water",
        "What foods help with my health goals?",
        "Show my weekly progress",
    ]
