from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
import json

from app.models import (
    RegisterRequest, LoginRequest, OnboardingRequest,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.security import (
    hash_password, verify_password, create_access_token,
    verify_token, encrypt_data, decrypt_data
)
from app.utils import (
    calculate_nutrition_targets, get_theme_for_segment,
    get_welcome_greeting, SEGMENT_THEME_MAP
)
from app.database import get_db

router = APIRouter()

def get_current_user(request):
    """Extract user from JWT token in cookie"""
    token = request.cookies.get("sn_token")
    if not token:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "No token provided"})
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Invalid token"})
    
    return payload

@router.post("/register")
async def register(req: RegisterRequest, response: Response):
    """Register new user"""
    db = get_db()
    
    # Check email uniqueness
    existing = await db.users.find_one({"email": req.email})
    if existing:
        raise HTTPException(
            status_code=409,
            detail={"code": "EMAIL_EXISTS", "message": "Email already registered"}
        )
    
    # Auto-detect segment
    segment = "teen-girl-h" if req.age < 18 else "adult"
    
    # Create user
    user_doc = {
        "email": req.email,
        "password_hash": hash_password(req.password),
        "name": req.name,
        "age": req.age,
        "is_parent": req.isParent,
        "segment": segment,
        "created_at": datetime.utcnow(),
        "last_login_at": None,
    }
    
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create profile record
    await db.profiles.insert_one({
        "user_id": user_id,
        "segment": segment,
        "onboarding_complete": False,
        "onboarding_step": 0,
        "created_at": datetime.utcnow(),
    })
    
    # Create JWT token
    token = create_access_token({"userId": user_id, "email": req.email})
    
    # Set httpOnly, Secure, SameSite cookie
    response.set_cookie(
        key="sn_token",
        value=token,
        httponly=True,
        secure=True,  # Set to True in production (HTTPS)
        samesite="strict",
        max_age=30 * 24 * 60 * 60,  # 30 days
    )
    
    return {
        "success": True,
        "data": {
            "userId": user_id,
            "email": req.email,
            "name": req.name,
            "segment": segment,
            "onboardingComplete": False,
        }
    }

@router.post("/login")
async def login(req: LoginRequest, response: Response):
    """Login user"""
    db = get_db()
    
    # Find user by email
    user = await db.users.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password_hash"]):
        # Generic 401 — don't reveal if email exists
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )
    
    user_id = str(user["_id"])
    
    # Get profile
    profile = await db.profiles.find_one({"user_id": user_id})
    
    # Update last_login_at
    await db.users.update_one({"_id": user["_id"]}, {"$set": {"last_login_at": datetime.utcnow()}})
    
    # Create token
    token = create_access_token(
        {"userId": user_id, "email": req.email},
        remember_me=req.rememberMe
    )
    
    # Set cookie
    max_age = 7 * 24 * 60 * 60 if req.rememberMe else None
    is_production = False  # Set to True in production
    response.set_cookie(
        key="sn_token",
        value=token,
        httponly=True,
        secure=is_production,  # Only secure in production
        samesite="lax",  # Use 'lax' for better localhost compatibility
        max_age=max_age,
    )
    
    return {
        "success": True,
        "data": {
            "userId": user_id,
            "email": user["email"],
            "name": user["name"],
            "segment": profile.get("segment", "adult") if profile else "adult",
            "onboardingComplete": profile.get("onboarding_complete", False) if profile else False,
            "onboardingStep": profile.get("onboarding_step", 0) if profile else 0,
            "theme": get_theme_for_segment(profile.get("segment", "adult") if profile else "adult"),
        }
    }

@router.patch("/onboarding")
async def save_onboarding(req: OnboardingRequest, request: Request, response: Response):
    """Save complete onboarding data and calculate nutrition targets"""
    user_payload = get_current_user(request)
    user_id = user_payload["userId"]
    
    db = get_db()
    
    # Calculate nutrition targets
    nutrition = calculate_nutrition_targets(
        weight_kg=req.weight,
        height_cm=req.height,
        age=0,  # Get age from user
        segment=req.segment,
        activity_level=req.activityLevel,
        primary_goal=req.primaryGoal,
        conditions=req.conditions or []
    )
    
    # Get user age
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        nutrition = calculate_nutrition_targets(
            weight_kg=req.weight,
            height_cm=req.height,
            age=user["age"],
            segment=req.segment,
            activity_level=req.activityLevel,
            primary_goal=req.primaryGoal,
            conditions=req.conditions or []
        )
    
    # Prepare profile update
    profile_update = {
        "segment": req.segment,
        "display_name": req.displayName,
        "weight_kg": req.weight,
        "height_cm": req.height,
        "activity_level": req.activityLevel,
        "primary_goal": req.primaryGoal,
        "conditions": req.conditions or [],
        "diet_preferences": req.dietPreferences or [],
        "allergies": req.allergies,
        "indian_cuisine": req.indianCuisine,
        "sport_type": req.sportType,
        "training_frequency": req.trainingFrequency,
        "onboarding_complete": True,
        "onboarding_step": 5,
        "updated_at": datetime.utcnow(),
    }
    
    # Update profile
    await db.profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_update}
    )
    
    # Save nutrition targets
    await db.nutrition_targets.update_one(
        {"user_id": user_id},
        {"$set": {**nutrition, "updated_at": datetime.utcnow()}},
        upsert=True
    )
    
    # Save cycle data if present and encrypt sensitive fields
    if req.cycleData:
        cycle_doc = {
            "user_id": user_id,
            "cycle_length": req.cycleData.cycleLength,
            "created_at": datetime.utcnow(),
        }
        
        # Encrypt sensitive fields
        if req.cycleData.lastPeriodDate:
            cycle_doc["last_period_date"] = encrypt_data(req.cycleData.lastPeriodDate)
        if req.cycleData.symptoms:
            cycle_doc["symptoms_enc"] = encrypt_data(json.dumps(req.cycleData.symptoms))
        
        await db.cycle_records.insert_one(cycle_doc)
    
    theme = get_theme_for_segment(req.segment)
    greeting = get_welcome_greeting(req.displayName, req.primaryGoal, req.segment)
    
    return {
        "success": True,
        "data": {
            "profile": profile_update,
            "nutritionTargets": nutrition,
            "theme": theme,
            "greeting": greeting,
        }
    }

@router.post("/logout")
async def logout(response: Response):
    """Logout user — clear cookie"""
    response.delete_cookie("sn_token", secure=True, samesite="strict")
    return {"success": True, "data": {}}

@router.get("/me")
async def get_current_user_profile(request: Request, response: Response):
    """Get current user profile — called on app startup"""
    user_payload = get_current_user(request)
    user_id = user_payload["userId"]
    
    db = get_db()
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User not found"})
    
    profile = await db.profiles.find_one({"user_id": user_id})
    nutrition = await db.nutrition_targets.find_one({"user_id": user_id})
    
    return {
        "success": True,
        "data": {
            "userId": user_id,
            "email": user["email"],
            "name": user["name"],
            "segment": profile.get("segment", "adult") if profile else "adult",
            "theme": get_theme_for_segment(profile.get("segment", "adult") if profile else "adult"),
            "onboardingComplete": profile.get("onboarding_complete", False) if profile else False,
            "profile": profile if profile else {},
            "nutritionTargets": nutrition if nutrition else {},
        }
    }

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    """Request password reset — always return 200"""
    # TODO: Implement email sending
    # For now, just return success
    return {"success": True, "data": {}}

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    """Reset password with token"""
    token_payload = verify_token(req.token)
    if not token_payload or "userId" not in token_payload:
        raise HTTPException(status_code=400, detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"})
    
    user_id = token_payload["userId"]
    db = get_db()
    
    # Update password
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password_hash": hash_password(req.newPassword)}}
    )
    
    return {"success": True, "data": {}}
