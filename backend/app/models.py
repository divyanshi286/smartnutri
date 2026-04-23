from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Auth Request/Response Models
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    age: int = Field(..., ge=10, le=100)
    isParent: bool = False

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    rememberMe: Optional[bool] = False

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str = Field(..., min_length=8, max_length=100)

# Onboarding Models
class CycleDataSchema(BaseModel):
    lastPeriodDate: Optional[str] = None
    cycleLength: Optional[int] = None
    symptoms: Optional[List[str]] = []

class OnboardingRequest(BaseModel):
    segment: str = Field(..., pattern="^(adult|teen-girl-h|teen-girl-a|teen-boy)$")
    displayName: str = Field(..., min_length=1, max_length=100)
    weight: float = Field(..., gt=0, le=200)
    height: int = Field(..., gt=0, le=300)
    activityLevel: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    primaryGoal: str
    conditions: Optional[List[str]] = []
    cycleData: Optional[CycleDataSchema] = None
    sportType: Optional[str] = None
    trainingFrequency: Optional[str] = None
    dietPreferences: Optional[List[str]] = []
    allergies: Optional[str] = None
    indianCuisine: bool = True

# Response Models
class UserResponse(BaseModel):
    userId: str = Field(alias="_id")
    email: str
    name: str
    segment: Optional[str] = None
    onboardingComplete: bool = False
    onboardingStep: int = 0
    theme: Optional[str] = None

    class Config:
        populate_by_name = True

class NutritionTargetsResponse(BaseModel):
    calories: int
    protein_g: int
    carbs_g: int
    fats_g: int
    water_glasses: int
    iron_mg: float
    magnesium_mg: int
    omega3_mg: int
    fiber_g: int

class LoginResponse(BaseModel):
    userId: str
    email: str
    name: str
    segment: str
    onboardingComplete: bool
    onboardingStep: int
    theme: str

class OnboardingResponse(BaseModel):
    profile: dict
    nutritionTargets: NutritionTargetsResponse
    theme: str
    greeting: str

class ApiResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None

# Meal & Food Models
class FoodItemSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    calories: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    fats_g: float = Field(..., ge=0)
    fiber_g: Optional[float] = 0
    iron_mg: Optional[float] = 0
    magnesium_mg: Optional[float] = 0
    omega3_mg: Optional[float] = 0
    quantity: Optional[str] = "1 serving"

class MealLogRequest(BaseModel):
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    foods: List[FoodItemSchema]
    notes: Optional[str] = None
    photo_url: Optional[str] = None

class MealLogResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    meal_type: str
    date: str
    foods: List[dict]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    created_at: str

    class Config:
        populate_by_name = True

class DayNutritionResponse(BaseModel):
    date: str
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    total_water_glasses: float
    meals: List[dict]

class ProgressLogRequest(BaseModel):
    weight: Optional[float] = None
    mood: Optional[str] = None
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    water_glasses: Optional[float] = 0
    exercise_minutes: Optional[int] = 0
    notes: Optional[str] = None

class BadgeSchema(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    earned_at: Optional[str] = None
    unlocked: bool = False

class CycleSummarySchema(BaseModel):
    phase: Optional[str] = None
    label: Optional[str] = None
    daysLeft: Optional[int] = None
    recommendations: Optional[List[str]] = []

class DashboardResponse(BaseModel):
    user: dict
    greeting: str
    date: str
    nutrition: dict
    cycleSummary: Optional[CycleSummarySchema] = None
    aiNudge: dict
    badges: List[BadgeSchema]
    streak: int

# Chat Models
class ChatMessageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

class ChatMessageResponse(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    role: str  # "user" or "ai"
    content: str
    safe: bool = True
    chips: Optional[List[str]] = []  # Quick reply suggestions

    class Config:
        populate_by_name = True
