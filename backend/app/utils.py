import math
from typing import Dict

# Segment to theme mapping
SEGMENT_THEME_MAP = {
    "adult": "th-adult",
    "teen-girl-h": "th-girl-h",
    "teen-girl-a": "th-girl-a",
    "teen-boy": "th-boy",
}

# Activity level multipliers (TDEE = BMR × activity_multiplier)
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

# Goal-based calorie modifiers (multiplier on TDEE)
CALORIE_MODIFIERS = {
    # Adult
    "weight-loss": 0.85,
    "weight-gain": 1.15,
    "manage-condition": 1.0,
    "maintain": 1.0,
    # Teen Girl - Hormonal
    "hormone-balance": 1.0,
    "manage-pcos": 1.0,
    "weight-management": 1.0,
    "energy": 1.0,
    # Teen Girl - Athletic
    "performance": 1.05,
    "lean-muscle": 1.0,
    "endurance": 1.05,
    "recover": 1.0,
    # Teen Boy
    "build-muscle": 1.1,
    "performance": 1.05,
    "lean-bulk": 1.05,
    "energy": 1.0,
}

# Condition-based micronutrient modifiers
CONDITION_MODIFIERS = {
    "PCOS": {"iron": 18, "magnesium": 310, "omega3": 1600},
    "Type 2 Diabetes": {"fiber": 30, "magnesium": 400},
    "Hypothyroid": {"iron": 18, "magnesium": 310},
    "Anemia": {"iron": 27, "magnesium": 310},
}

def calculate_bmr(weight_kg: float, height_cm: int, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Harris-Benedict formula.
    gender: 'M' or 'F'
    """
    weight_lb = weight_kg * 2.20462
    height_in = height_cm / 2.54
    
    if gender == 'M':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    return bmr

def calculate_tdee(
    weight_kg: float,
    height_cm: int,
    age: int,
    gender: str,
    activity_level: str
) -> float:
    """Calculate Total Daily Energy Expenditure"""
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
    return bmr * multiplier

def infer_gender_from_segment(segment: str) -> str:
    """Infer gender from segment"""
    if "girl" in segment:
        return "F"
    elif "boy" in segment:
        return "M"
    else:
        # Default for adult — assume diverse, use neutral adjustment
        return "F"  # Default female for adult (can be customized in onboarding)

def calculate_nutrition_targets(
    weight_kg: float,
    height_cm: int,
    age: int,
    segment: str,
    activity_level: str,
    primary_goal: str,
    conditions: list = None
) -> Dict:
    """Calculate personalized nutrition targets"""
    
    if conditions is None:
        conditions = []
    
    gender = infer_gender_from_segment(segment)
    is_teen = age < 18
    
    # Base TDEE
    base_tdee = calculate_tdee(weight_kg, height_cm, age, gender, activity_level)
    
    # Apply goal modifier
    goal_modifier = CALORIE_MODIFIERS.get(primary_goal, 1.0)
    
    # Teens never get deficit
    if is_teen and goal_modifier < 1.0:
        goal_modifier = 1.0
    
    calories = int(base_tdee * goal_modifier)
    
    # Macros
    if segment == "teen-boy" or (segment == "teen-girl-a" and "performance" in primary_goal):
        # Athletic: higher protein (1.6g/kg for teens, 1.8g/kg for adults)
        protein_multiplier = 1.6 if is_teen else 1.8
    elif is_teen:
        # General teen: 1.2g/kg minimum
        protein_multiplier = 1.2
    else:
        # Adult: standard 1.6g/kg
        protein_multiplier = 1.6
    
    protein_g = int(weight_kg * protein_multiplier)
    
    # Carbs: remaining calories after protein and fat
    fats_g = int(weight_kg * 0.8)  # ~0.8g/kg baseline
    carbs_g = max(100, int((calories - (protein_g * 4) - (fats_g * 9)) / 4))
    
    # Water: rough estimate 8-10 glasses/day
    water_glasses = 8 if weight_kg < 60 else (9 if weight_kg < 80 else 10)
    
    # Micros: base values
    iron_mg = 18.0 if gender == "F" else 8.0
    magnesium_mg = 310 if gender == "F" else 400
    omega3_mg = 1600
    fiber_g = 25
    
    # Apply condition modifiers
    for condition in conditions:
        if condition in CONDITION_MODIFIERS:
            mods = CONDITION_MODIFIERS[condition]
            iron_mg = max(iron_mg, mods.get("iron", iron_mg))
            magnesium_mg = max(magnesium_mg, mods.get("magnesium", magnesium_mg))
            omega3_mg = max(omega3_mg, mods.get("omega3", omega3_mg))
            fiber_g = max(fiber_g, mods.get("fiber", fiber_g))
    
    return {
        "calories": calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fats_g": fats_g,
        "water_glasses": water_glasses,
        "iron_mg": iron_mg,
        "magnesium_mg": magnesium_mg,
        "omega3_mg": omega3_mg,
        "fiber_g": fiber_g,
    }

def get_theme_for_segment(segment: str) -> str:
    """Get CSS theme string for segment"""
    return SEGMENT_THEME_MAP.get(segment, "th-adult")

def get_welcome_greeting(name: str, goal: str, segment: str) -> str:
    """Generate personalized welcome message"""
    goal_map = {
        "weight-loss": "weight loss journey",
        "weight-gain": "muscle gain plan",
        "manage-condition": "health management plan",
        "hormone-balance": "hormone-balanced nutrition",
        "manage-pcos": "PCOS-friendly nutrition",
        "performance": "athletic performance plan",
        "build-muscle": "muscle-building program",
    }
    goal_text = goal_map.get(goal, "personalized nutrition plan")
    
    return f"Welcome, {name}! Your {goal_text} is ready. Let's make today count! 🌿"
