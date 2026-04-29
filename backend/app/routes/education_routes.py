"""
Education and learning modules endpoints
Endpoints for nutrition education content, quizzes, and learning progress
"""
from fastapi import APIRouter, HTTPException, Request, Path
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()

# Education modules content
EDUCATION_MODULES = [
    {
        "id": "macronutrients",
        "title": "Understanding Macronutrients",
        "icon": "🥗",
        "description": "Learn about proteins, carbohydrates, and fats - the building blocks of nutrition",
        "videoUrl": "https://example.com/videos/macros.mp4",
        "duration": 12,
        "quiz": [
            {
                "question": "Which macronutrient provides the most calories per gram?",
                "options": ["Protein (4 cal/g)", "Carbohydrates (4 cal/g)", "Fats (9 cal/g)", "Water (0 cal/g)"],
                "correct": 2
            },
            {
                "question": "What is the recommended daily protein intake for an average adult?",
                "options": ["10g", "0.8g per kg of body weight", "100g", "As much as possible"],
                "correct": 1
            },
            {
                "question": "Which of these is a complex carbohydrate?",
                "options": ["Sugar", "Oatmeal", "Candy", "Fruit juice"],
                "correct": 1
            }
        ]
    },
    {
        "id": "hydration",
        "title": "Hydration & Water Intake",
        "icon": "💧",
        "description": "Master the science of proper hydration and its impact on your body and performance",
        "videoUrl": "https://example.com/videos/hydration.mp4",
        "duration": 8,
        "quiz": [
            {
                "question": "How much water should an average person drink daily?",
                "options": ["1 liter", "2-3 liters", "5-6 liters", "As much as possible"],
                "correct": 1
            },
            {
                "question": "What is the first sign of dehydration?",
                "options": ["Thirst", "Dry lips", "Dark urine", "Headache"],
                "correct": 2
            },
            {
                "question": "Does drinking water with meals affect digestion?",
                "options": ["Yes, it dilutes stomach acid", "No, it aids digestion", "Only if it's cold", "Depends on the meal"],
                "correct": 1
            }
        ]
    },
    {
        "id": "meal-timing",
        "title": "Meal Timing & Frequency",
        "icon": "⏰",
        "description": "Discover the optimal timing for meals and how meal frequency affects your metabolism",
        "videoUrl": "https://example.com/videos/meal-timing.mp4",
        "duration": 10,
        "quiz": [
            {
                "question": "What is intermittent fasting?",
                "options": ["Skipping breakfast", "Eating within a specific time window", "Eating every 2 hours", "Never eating after 6pm"],
                "correct": 1
            },
            {
                "question": "When is the best time to eat after a workout?",
                "options": ["Immediately", "Within 30-60 minutes", "After 2 hours", "Before the next day"],
                "correct": 1
            },
            {
                "question": "How many meals per day is optimal?",
                "options": ["1 large meal", "2 meals", "3-5 balanced meals", "As many as you want"],
                "correct": 2
            }
        ]
    },
    {
        "id": "micronutrients",
        "title": "Micronutrients: Vitamins & Minerals",
        "icon": "✨",
        "description": "Understand the role of vitamins and minerals in maintaining optimal health",
        "videoUrl": "https://example.com/videos/micronutrients.mp4",
        "duration": 14,
        "quiz": [
            {
                "question": "Which vitamin is produced by your skin when exposed to sunlight?",
                "options": ["Vitamin A", "Vitamin B12", "Vitamin D", "Vitamin K"],
                "correct": 2
            },
            {
                "question": "Iron is essential for which body function?",
                "options": ["Building bones", "Oxygen transport in blood", "Muscle contraction", "Vision"],
                "correct": 1
            },
            {
                "question": "Which mineral is most important for bone health?",
                "options": ["Sodium", "Potassium", "Calcium", "Iron"],
                "correct": 2
            }
        ]
    },
    {
        "id": "cycle-nutrition",
        "title": "Cycle Syncing Nutrition",
        "icon": "🌸",
        "description": "Learn how to adjust your nutrition based on your menstrual cycle phases",
        "videoUrl": "https://example.com/videos/cycle-nutrition.mp4",
        "duration": 11,
        "quiz": [
            {
                "question": "How long is an average menstrual cycle?",
                "options": ["21 days", "28 days", "35 days", "It varies, typically 21-35 days"],
                "correct": 3
            },
            {
                "question": "What nutrient is especially important during the luteal phase?",
                "options": ["Carbohydrates", "Magnesium", "Calcium", "Sodium"],
                "correct": 1
            },
            {
                "question": "When is your energy typically highest in the cycle?",
                "options": ["Menstruation", "Follicular phase", "Ovulation", "Luteal phase"],
                "correct": 2
            }
        ]
    },
    {
        "id": "nutrition-goals",
        "title": "Setting & Achieving Nutrition Goals",
        "icon": "🎯",
        "description": "Create a personalized nutrition plan and track your progress toward your health goals",
        "videoUrl": "https://example.com/videos/nutrition-goals.mp4",
        "duration": 9,
        "quiz": [
            {
                "question": "What makes a nutrition goal SMART?",
                "options": ["Simple", "Specific, Measurable, Achievable, Relevant, Time-bound", "Smart and good", "Speed-focused"],
                "correct": 1
            },
            {
                "question": "How often should you reassess your nutrition goals?",
                "options": ["Never", "Every 6 months", "Every 1-3 months", "Daily"],
                "correct": 2
            },
            {
                "question": "What is a realistic weight loss rate per week?",
                "options": ["1-2 lbs", "3-4 lbs", "5+ lbs", "As much as possible"],
                "correct": 0
            }
        ]
    }
]


@router.get("/education/modules")
async def get_education_modules(request: Request):
    """Get list of all available education modules"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get user's completed modules
        completed = await db.achievements.find_one({"user_id": user_id, "type": "education"})
        completed_modules = completed.get("modules", []) if completed else []
        
        # Format modules with completion status
        modules = []
        for module in EDUCATION_MODULES:
            modules.append({
                "id": module["id"],
                "title": module["title"],
                "icon": module["icon"],
                "description": module["description"],
                "videoUrl": module["videoUrl"],
                "duration": module["duration"],
                "quiz": module["quiz"],
                "completed": module["id"] in completed_modules
            })
        
        return {
            "success": True,
            "data": modules
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "MODULES_ERROR", "message": str(e)}
        )


@router.post("/education/modules/{module_id}/complete")
async def complete_education_module(
    module_id: str = Path(..., description="The education module ID"),
    request: Request = None
):
    """Mark an education module as completed"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Verify module exists
        module_exists = any(m["id"] == module_id for m in EDUCATION_MODULES)
        if not module_exists:
            raise HTTPException(
                status_code=404,
                detail={"code": "MODULE_NOT_FOUND", "message": f"Module {module_id} not found"}
            )
        
        # Update achievements with $addToSet to avoid duplicates
        result = await db.achievements.update_one(
            {"user_id": user_id, "type": "education"},
            {
                "$addToSet": {"modules": module_id},
                "$set": {"updated_at": datetime.utcnow()}
            },
            upsert=True
        )
        
        return {
            "success": True,
            "data": {
                "message": f"Module {module_id} marked as completed",
                "moduleId": module_id
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "COMPLETION_ERROR", "message": str(e)}
        )


@router.get("/education/modules/{module_id}")
async def get_module_details(
    module_id: str = Path(..., description="The education module ID"),
    request: Request = None
):
    """Get detailed information about a specific module"""
    try:
        user = get_current_user(request)
        
        # Find module
        module = next((m for m in EDUCATION_MODULES if m["id"] == module_id), None)
        if not module:
            raise HTTPException(
                status_code=404,
                detail={"code": "MODULE_NOT_FOUND", "message": f"Module {module_id} not found"}
            )
        
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Check completion status
        completed = await db.achievements.find_one({"user_id": user_id, "type": "education"})
        is_completed = module_id in (completed.get("modules", []) if completed else [])
        
        return {
            "success": True,
            "data": {
                **module,
                "completed": is_completed
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "MODULE_ERROR", "message": str(e)}
        )
