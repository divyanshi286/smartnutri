"""
Seed database with initial data
Run with: python seed_db.py
"""
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "smartnutri")
USE_MONGOMOCK = os.getenv("USE_MONGOMOCK", "true").lower() == "true"

# For mongomock - synchronous wrapper
if USE_MONGOMOCK:
    import mongomock
    client = mongomock.MongoClient()
    db = client[DB_NAME]
else:
    from motor.motor_asyncio import AsyncIOMotorClient
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    # This won't work without proper setup, so we'll focus on mongomock

from app.security import hash_password
from app.utils import calculate_nutrition_targets

# Sample food database entries - Comprehensive food list
FOOD_DATABASE = [
    # Grains
    {"name": "Rice (cooked)", "category": "grains", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4, "iron_mg": 0.2, "magnesium_mg": 12, "omega3_mg": 0},
    {"name": "Wheat bread", "category": "grains", "calories": 269, "protein": 9, "carbs": 49, "fats": 3.3, "fiber": 7, "iron_mg": 2.7, "magnesium_mg": 38, "omega3_mg": 0},
    {"name": "Roti (wheat)", "category": "grains", "calories": 265, "protein": 9.2, "carbs": 48, "fats": 3.7, "fiber": 7.3, "iron_mg": 2.6, "magnesium_mg": 36, "omega3_mg": 0},
    {"name": "Oatmeal", "category": "grains", "calories": 389, "protein": 17, "carbs": 66, "fats": 7, "fiber": 10.6, "iron_mg": 4.3, "magnesium_mg": 177, "omega3_mg": 0},
    {"name": "Basmati rice", "category": "grains", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4, "iron_mg": 0.2, "magnesium_mg": 12, "omega3_mg": 0},
    
    # Proteins
    {"name": "Chicken breast", "category": "protein", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "fiber": 0, "iron_mg": 0.9, "magnesium_mg": 29, "omega3_mg": 0.1},
    {"name": "Egg", "category": "protein", "calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "fiber": 0, "iron_mg": 1.8, "magnesium_mg": 12, "omega3_mg": 0.2},
    {"name": "Lentils (cooked)", "category": "protein", "calories": 116, "protein": 9, "carbs": 20, "fats": 0.4, "fiber": 8, "iron_mg": 3.3, "magnesium_mg": 36, "omega3_mg": 0},
    {"name": "Chickpeas (cooked)", "category": "protein", "calories": 134, "protein": 8.9, "carbs": 22, "fats": 2.4, "fiber": 6.4, "iron_mg": 2.4, "magnesium_mg": 48, "omega3_mg": 0},
    {"name": "Paneer cheese", "category": "protein", "calories": 265, "protein": 26, "carbs": 3.6, "fats": 17, "fiber": 0, "iron_mg": 0.6, "magnesium_mg": 18, "omega3_mg": 0},
    {"name": "Fish (salmon)", "category": "protein", "calories": 206, "protein": 22, "carbs": 0, "fats": 13, "fiber": 0, "iron_mg": 0.8, "magnesium_mg": 29, "omega3_mg": 2260},
    {"name": "Tofu", "category": "protein", "calories": 76, "protein": 8, "carbs": 2, "fats": 4.8, "fiber": 1.2, "iron_mg": 2.7, "magnesium_mg": 31, "omega3_mg": 0},
    {"name": "Moong dal (cooked)", "category": "protein", "calories": 106, "protein": 7.7, "carbs": 19, "fats": 0.4, "fiber": 2.4, "iron_mg": 2.5, "magnesium_mg": 28, "omega3_mg": 0},
    {"name": "Yogurt (plain)", "category": "protein", "calories": 59, "protein": 10, "carbs": 3.3, "fats": 0.4, "fiber": 0, "iron_mg": 0.1, "magnesium_mg": 12, "omega3_mg": 0},
    
    # Vegetables
    {"name": "Spinach", "category": "vegetables", "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "fiber": 2.2, "iron_mg": 2.7, "magnesium_mg": 79, "omega3_mg": 0.1},
    {"name": "Broccoli", "category": "vegetables", "calories": 34, "protein": 2.8, "carbs": 7, "fats": 0.4, "fiber": 2.4, "iron_mg": 1, "magnesium_mg": 64, "omega3_mg": 0.2},
    {"name": "Tomato", "category": "vegetables", "calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2, "iron_mg": 0.3, "magnesium_mg": 11, "omega3_mg": 0},
    {"name": "Carrot", "category": "vegetables", "calories": 41, "protein": 0.9, "carbs": 10, "fats": 0.2, "fiber": 2.8, "iron_mg": 0.3, "magnesium_mg": 12, "omega3_mg": 0},
    {"name": "Bell pepper", "category": "vegetables", "calories": 31, "protein": 1, "carbs": 6, "fats": 0.3, "fiber": 2.2, "iron_mg": 0.3, "magnesium_mg": 12, "omega3_mg": 0.1},
    {"name": "Cucumber", "category": "vegetables", "calories": 16, "protein": 0.7, "carbs": 3.6, "fats": 0.1, "fiber": 0.5, "iron_mg": 0.3, "magnesium_mg": 13, "omega3_mg": 0},
    {"name": "Potato", "category": "vegetables", "calories": 77, "protein": 2, "carbs": 17, "fats": 0.1, "fiber": 2.1, "iron_mg": 0.8, "magnesium_mg": 23, "omega3_mg": 0},
    
    # Fruits
    {"name": "Banana", "category": "fruits", "calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3, "fiber": 2.6, "iron_mg": 0.3, "magnesium_mg": 31, "omega3_mg": 0},
    {"name": "Apple", "category": "fruits", "calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "fiber": 2.4, "iron_mg": 0.1, "magnesium_mg": 5, "omega3_mg": 0},
    {"name": "Orange", "category": "fruits", "calories": 47, "protein": 0.9, "carbs": 12, "fats": 0.1, "fiber": 2.4, "iron_mg": 0.1, "magnesium_mg": 10, "omega3_mg": 0},
    {"name": "Mango", "category": "fruits", "calories": 60, "protein": 0.8, "carbs": 15, "fats": 0.4, "fiber": 1.6, "iron_mg": 0.2, "magnesium_mg": 11, "omega3_mg": 0},
    {"name": "Grape", "category": "fruits", "calories": 67, "protein": 0.6, "carbs": 17, "fats": 0.2, "fiber": 0.9, "iron_mg": 0.4, "magnesium_mg": 7, "omega3_mg": 0},
    {"name": "Berry (mixed)", "category": "fruits", "calories": 45, "protein": 0.7, "carbs": 10, "fats": 0.3, "fiber": 2.4, "iron_mg": 0.3, "magnesium_mg": 6, "omega3_mg": 0},
    
    # Nuts & Seeds
    {"name": "Almonds", "category": "nuts", "calories": 579, "protein": 21, "carbs": 22, "fats": 50, "fiber": 12.5, "iron_mg": 3.7, "magnesium_mg": 270, "omega3_mg": 0},
    {"name": "Peanut butter", "category": "nuts", "calories": 588, "protein": 25, "carbs": 20, "fats": 50, "fiber": 6, "iron_mg": 1.7, "magnesium_mg": 168, "omega3_mg": 0},
    {"name": "Sunflower seeds", "category": "nuts", "calories": 584, "protein": 23, "carbs": 20, "fats": 51, "fiber": 8.6, "iron_mg": 5.48, "magnesium_mg": 325, "omega3_mg": 0},
    
    # Dairy
    {"name": "Milk (full fat)", "category": "dairy", "calories": 61, "protein": 3.2, "carbs": 4.8, "fats": 3.3, "fiber": 0, "iron_mg": 0.1, "magnesium_mg": 10, "omega3_mg": 0},
    {"name": "Milk (skimmed)", "category": "dairy", "calories": 35, "protein": 3.4, "carbs": 4.7, "fats": 0.1, "fiber": 0, "iron_mg": 0.1, "magnesium_mg": 10, "omega3_mg": 0},
    {"name": "Cheese", "category": "dairy", "calories": 402, "protein": 25, "carbs": 1.3, "fats": 33, "fiber": 0, "iron_mg": 0.7, "magnesium_mg": 28, "omega3_mg": 0},
    
    # Oils & Condiments
    {"name": "Olive oil", "category": "oils", "calories": 884, "protein": 0, "carbs": 0, "fats": 100, "fiber": 0, "iron_mg": 0, "magnesium_mg": 0, "omega3_mg": 1},
    {"name": "Coconut oil", "category": "oils", "calories": 884, "protein": 0, "carbs": 0, "fats": 100, "fiber": 0, "iron_mg": 0, "magnesium_mg": 0, "omega3_mg": 0},
    
    # Prepared dishes (popular)
    {"name": "Dal makhani", "category": "prepared", "calories": 180, "protein": 12, "carbs": 15, "fats": 8, "fiber": 5, "iron_mg": 2.4, "magnesium_mg": 36, "omega3_mg": 0},
    {"name": "Dal rice", "category": "prepared", "calories": 250, "protein": 11, "carbs": 42, "fats": 2, "fiber": 5, "iron_mg": 2.6, "magnesium_mg": 48, "omega3_mg": 0},
    {"name": "Chicken curry", "category": "prepared", "calories": 150, "protein": 20, "carbs": 5, "fats": 6, "fiber": 1, "iron_mg": 1.2, "magnesium_mg": 31, "omega3_mg": 0},
    {"name": "Butter chicken", "category": "prepared", "calories": 210, "protein": 18, "carbs": 8, "fats": 11, "fiber": 1, "iron_mg": 1.5, "magnesium_mg": 25, "omega3_mg": 0},
    {"name": "Biryani", "category": "prepared", "calories": 280, "protein": 14, "carbs": 35, "fats": 9, "fiber": 2, "iron_mg": 1.8, "magnesium_mg": 42, "omega3_mg": 0},
    {"name": "Samosa", "category": "snacks", "calories": 262, "protein": 3.4, "carbs": 32, "fats": 13, "fiber": 1.9, "iron_mg": 0.8, "magnesium_mg": 18, "omega3_mg": 0},
    {"name": "Chikhalwali", "category": "snacks", "calories": 380, "protein": 12, "carbs": 45, "fats": 16, "fiber": 3, "iron_mg": 1.5, "magnesium_mg": 28, "omega3_mg": 0},
]

# Sample meal templates with categories
MEAL_EMOJIS = {
    "breakfast": "🍳",
    "lunch": "🥗",
    "dinner": "🍽",
    "snack": "🍌"
}

MEAL_COLORS = {
    "breakfast": "#FFD700",
    "lunch": "#FF6347",
    "dinner": "#4169E1",
    "snack": "#90EE90"
}

# Achievement/Badge templates
BADGE_TEMPLATES = [
    {"name": "First Log", "description": "Logged your first meal", "icon": "🎯", "threshold": 1},
    {"name": "Week Warrior", "description": "Logged meals for 7 days straight", "icon": "⚔️", "threshold": 7},
    {"name": "Protein Master", "description": "Hit protein goal 5 times", "icon": "💪", "threshold": 5},
    {"name": "Hydration Hero", "description": "Drank 2.5L water 3 times", "icon": "💧", "threshold": 3},
    {"name": "Calorie Counter", "description": "Logged 20 meals", "icon": "🔢", "threshold": 20},
    {"name": "Consistency King", "description": "30-day streak", "icon": "👑", "threshold": 30},
]

def seed_database(db):
    """Seed the database with initial data"""
    try:
        print("🌱 Starting database seeding...")
        
        # Check if already seeded
        existing_user = db.users.find_one({"email": "test@example.com"})
        if existing_user:
            print("⚠️  Database already has test user. Skipping seeding.")
            return
        
        # 1. Seed food database
        print("\n📚 Seeding food database...")
        food_result = db.food_database.insert_many(FOOD_DATABASE)
        print(f"[OK] Inserted {len(FOOD_DATABASE)} food items")
        
        # 2. Seed test user
        print("\n👤 Seeding test user...")
        test_user = {
            "email": "test@example.com",
            "password_hash": hash_password("password123"),
            "name": "Test User",
            "age": 25,
            "is_parent": False,
            "segment": "adult",
            "created_at": datetime.utcnow(),
            "last_login_at": None,
        }
        user_result = db.users.insert_one(test_user)
        user_id = str(user_result.inserted_id)
        print(f"[OK] Created user: {user_id}")
        
        # 3. Create profile
        print("\n📋 Creating user profile...")
        profile = {
            "user_id": user_id,
            "segment": "adult",
            "display_name": "Test User",
            "weight_kg": 70,
            "height_cm": 175,
            "age": 25,
            "gender": "F",
            "activity_level": "moderate",
            "primary_goal": "maintain",
            "conditions": [],
            "cycle_data": None,
            "diet_preferences": ["vegetarian"],
            "allergies": None,
            "indian_cuisine": True,
            "onboarding_complete": True,
            "onboarding_step": 5,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        db.profiles.insert_one(profile)
        print("[OK] Profile created")
        
        # 4. Calculate and create nutrition targets
        print("\n🎯 Calculating nutrition targets...")
        targets = calculate_nutrition_targets(
            weight_kg=70,
            height_cm=175,
            age=25,
            segment="adult",
            activity_level="moderate",
            primary_goal="maintain",
            conditions=[]
        )
        nutrition_targets = {
            "user_id": user_id,
            "segment": "adult",
            "calories": targets["calories"],
            "protein_g": targets["protein_g"],
            "carbs_g": targets["carbs_g"],
            "fats_g": targets["fats_g"],
            "water_glasses": targets["water_glasses"],
            "iron_mg": targets["iron_mg"],
            "magnesium_mg": targets["magnesium_mg"],
            "omega3_mg": targets["omega3_mg"],
            "fiber_g": targets["fiber_g"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        db.nutrition_targets.insert_one(nutrition_targets)
        print(f"[OK] Targets: {targets['calories']} kcal, {targets['protein_g']}g protein")
        
        # 5. Seed sample meals for the last 7 days
        print("\n🍽️  Seeding sample meals...")
        meals_inserted = 0
        for days_ago in range(7):
            meal_date = (datetime.utcnow() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            # Add 3-4 meals per day
            for meal_type in ["breakfast", "lunch", "dinner"]:
                foods = FOOD_DATABASE[days_ago::3][:2]  # 2 foods per meal
                
                total_calories = sum(f["calories"] for f in foods)
                total_protein = sum(f.get("protein", f.get("protein_g", 0)) for f in foods)
                total_carbs = sum(f.get("carbs", f.get("carbs_g", 0)) for f in foods)
                total_fats = sum(f.get("fats", f.get("fats_g", 0)) for f in foods)
                
                meal_log = {
                    "user_id": user_id,
                    "meal_type": meal_type,
                    "date": meal_date,
                    "foods": foods,
                    "total_calories": total_calories,
                    "total_protein_g": total_protein,
                    "total_carbs_g": total_carbs,
                    "total_fats_g": total_fats,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
                db.meal_logs.insert_one(meal_log)
                meals_inserted += 1
        
        print(f"[OK] Inserted {meals_inserted} meal logs")
        
        # 6. Seed progress logs
        print("\n📈 Seeding progress logs...")
        progress_inserted = 0
        for days_ago in range(7):
            log_date = (datetime.utcnow() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            progress_log = {
                "user_id": user_id,
                "date": log_date,
                "weight_kg": 70 - (days_ago * 0.1),  # Slight decrease
                "mood": ["great", "good", "ok", "tired"][days_ago % 4],
                "energy_level": 7 + (days_ago % 3) - 1,
                "water_glasses": 2.5,
                "exercise_minutes": [30, 45, 0, 60, 30, 0, 45][days_ago % 7],
                "notes": f"Day {days_ago + 1} of tracking",
                "created_at": datetime.utcnow(),
            }
            db.progress_logs.insert_one(progress_log)
            progress_inserted += 1
        
        print(f"[OK] Inserted {progress_inserted} progress logs")
        
        # 7. Seed achievements
        print("\n🏆 Seeding achievements...")
        achievements = []
        for i, badge_template in enumerate(BADGE_TEMPLATES):
            achievement = {
                "user_id": user_id,
                "badge_id": f"badge-{i}",
                "name": badge_template["name"],
                "description": badge_template["description"],
                "icon": badge_template["icon"],
                "unlocked": i < 3,  # First 3 badges unlocked
                "earned_at": (datetime.utcnow() - timedelta(days=7-i)) if i < 3 else None,
                "created_at": datetime.utcnow(),
            }
            achievements.append(achievement)
        
        db.achievements.insert_many(achievements)
        print(f"[OK] Inserted {len(achievements)} achievements")
        
        print("\n[SUCCESS] Database seeding completed successfully!")
        print(f"\nTest credentials:")
        print(f"  Email: test@example.com")
        print(f"  Password: password123")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    seed_database(db)
