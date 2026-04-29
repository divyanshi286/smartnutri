from fastapi import APIRouter, HTTPException, Depends, Request
from datetime import datetime
from typing import Optional
import os
from bson import ObjectId
import json

from app.models import ChatMessageRequest, ChatMessageResponse
from app.database import get_db
from app.security import verify_token

router = APIRouter()

def get_current_user(request: Request):
    """Extract user from JWT token in cookie"""
    token = request.cookies.get("sn_token")
    if not token:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "No token provided"})
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Invalid token"})
    
    return payload

async def get_ai_response(user_message: str, user_context: dict, conversation_history: list) -> dict:
    """
    Get response from LLM (OpenAI).
    Falls back to simple responses if API key not configured.
    """
    
    # Try to use OpenAI API
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Build system prompt with user context
            system_prompt = f"""You are NutriAI, a personalized nutrition coach for {user_context.get('segment', 'general users')}.

User Profile:
- Name: {user_context.get('name', 'User')}
- Segment: {user_context.get('segment', 'adult')}
- Primary Goal: {user_context.get('primaryGoal', 'general health')}
- Conditions: {', '.join(user_context.get('conditions', []))}
- Diet Preferences: {', '.join(user_context.get('dietPreferences', []))}
- Allergies: {user_context.get('allergies', 'none')}
- Activity Level: {user_context.get('activityLevel', 'moderate')}

Nutrition Targets:
- Daily Calories: {user_context.get('calorieTarget', 2000)} kcal
- Protein: {user_context.get('proteinTarget', 50)}g
- Carbs: {user_context.get('carbsTarget', 250)}g
- Fats: {user_context.get('fatsTarget', 65)}g

Instructions:
1. Be supportive and encouraging
2. Provide practical, actionable nutrition advice
3. Consider the user's specific conditions and goals
4. Recommend {user_context.get('segment', 'adult')}-appropriate foods
5. Keep responses conversational and friendly
6. If the user asks about harmful content or illegal activities, politely decline and offer health alternatives
7. Use emoji sparingly for engagement
8. For food recommendations, include calorie/macro estimates when relevant"""

            # Prepare conversation history for API
            messages = []
            for msg in conversation_history[-10:]:  # Use last 10 messages for context
                messages.append({
                    "role": "user" if msg.get("role") == "user" else "assistant",
                    "content": msg.get("content", "")
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}] + messages,
                temperature=0.7,
                max_tokens=500,
            )
            
            ai_content = response.choices[0].message.content
            
            # Extract suggested chips (follow-up questions) if applicable
            chips = []
            if any(word in user_message.lower() for word in ["what", "how", "when", "why", "can i"]):
                chips = ["Tell me more", "Any other options?", "How much should I eat?"]
            
            return {
                "role": "ai",
                "content": ai_content,
                "safe": True,
                "chips": chips
            }
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fall through to fallback
    
    # Fallback: Basic response generation
    return generate_fallback_response(user_message, user_context)

def generate_fallback_response(user_message: str, user_context: dict) -> dict:
    """Generate a helpful response without API key"""
    
    user_msg_lower = user_message.lower()
    name = user_context.get('name', 'user')
    segment = user_context.get('segment', 'adult')
    
    # Safety check for harmful content (only actual crisis keywords)
    harmful_keywords = ['suicide', 'kill myself', 'self harm', 'want to die', 'hurt myself']
    if any(keyword in user_msg_lower for keyword in harmful_keywords):
        return {
            "role": "ai",
            "content": "I'm concerned about your well-being. Please reach out to a mental health professional or crisis helpline:\n\n📞 National Suicide Prevention: 988\n💬 Crisis Text Line: Text HOME to 741741",
            "safe": False,
        }
    
    # Enhanced response mapping with multiple keywords per response
    response_map = {
        ('protein', 'amino', 'muscle'): f"Great question about protein, {name}! For a {segment}, aim for about 0.8-1g per pound of body weight. Good sources: chicken, fish, eggs, legumes, Greek yogurt.",
        ('calories', 'kcal', 'energy'): "Calorie needs vary by activity level and goals. Your daily target is in your nutrition summary. Stay consistent rather than perfect!",
        ('carbs', 'carbohydrate', 'glucose'): "Carbs are fuel! Choose whole grains, fruits, and vegetables. Time them around your workouts for best results.",
        ('workout', 'exercise', 'gym', 'training', 'sport'): "Exercise timing with meals matters! Eat light carbs 1-2 hours before, and protein+carbs within 30-60min after.",
        ('pcos', 'polycystic', 'period'): "PCOS management: Focus on low-glycemic foods, balanced meals with protein & fat, regular movement, and stress management.",
        ('period', 'menstrual', 'cycle', 'hormonal'): "Cycle syncing nutrition is powerful! Eat more carbs in follicular phase, more protein/fat in luteal phase.",
        ('water', 'hydration', 'drink', 'hydrate'): "Hydration is #1! Aim for 8-10 glasses daily. Drink more if exercising or in hot weather.",
        ('snack', 'hungry', 'between meals'): f"Healthy snacks for {segment}: nuts, fruit, yogurt, cheese, hard-boiled eggs, trail mix. Include protein!",
        ('sleep', 'rest', 'recovery'): "Sleep is crucial for nutrition! Aim for 7-9 hours. Poor sleep affects hormones and hunger cues.",
        ('digestion', 'gut', 'stomach', 'bloating'): "Digestive health: Eat slowly, chew well, include fiber gradually, and drink water. Probiotics from yogurt help too.",
        ('diet', 'eating', 'food', 'meal'): f"The best diet is one you can stick with! Focus on whole foods, {segment}-appropriate portions, and balance.",
        ('weight', 'lose', 'gain', 'fat', 'slim'): "Weight management is 80% nutrition, 20% exercise. Focus on sustainable habits, not quick fixes.",
        ('sugar', 'sweet', 'dessert'): "Balance is key! Enjoying sweets occasionally is fine. The problem is frequency and hidden sugars. Choose nutrient-dense options.",
        ('fat', 'healthy', 'omega'): "Healthy fats are essential! Include olive oil, nuts, fish, avocado. They support brain and heart health.",
        ('breakfast', 'lunch', 'dinner'): "Meal timing matters! Start your day with protein+carbs, balance midday meals, eat lighter at night.",
    }
    
    # Find best matching response
    for keywords, response in response_map.items():
        if any(keyword in user_msg_lower for keyword in keywords):
            # Generate contextual follow-up suggestions
            if 'water' in keywords:
                chips = ["Any other hydration questions?", "Tell me about nutrition targets", "What else?"]
            elif 'protein' in keywords:
                chips = ["Good protein sources?", "How much protein daily?", "Next question?"]
            elif 'workout' in keywords:
                chips = ["Pre or post-workout meals?", "Recovery nutrition?", "More tips?"]
            else:
                chips = ["Got it!", "Any other questions?", "Tell me more"]
            
            return {
                "role": "ai",
                "content": response,
                "safe": True,
                "chips": chips
            }
    
    # Smart default response that acknowledges their question
    question_types = {
        ('how', 'should', 'can', 'what'): f"That's a great {segment}-focused question! I don't have a specific answer in my database, but I can help with: Foods for your goals, Nutrition targets, Meal timing, Hydration tips, and {segment.title()}-specific advice. What would you like to know?",
        ('best', 'good', 'bad'): "Nutrition is about balance and sustainability! Rather than labeling foods as 'good' or 'bad,' focus on how they fit your goals and make you feel.",
        ('why', 'explain'): "Great question! Understanding the 'why' helps you make better choices. Feel free to ask me about any nutrition topic!",
    }
    
    default_msg = f"That's a great question, {name}! I'm here to help with personalized nutrition advice for {segment}s. Feel free to ask me about:\n\n✓ Foods for your goals\n✓ Nutrition targets\n✓ Meal timing\n✓ Hydration\n✓ {segment.title()}-specific nutrition\n\nWhat would you like to know?"
    
    # Try to match question type
    for keywords, custom_response in question_types.items():
        if any(keyword in user_msg_lower for keyword in keywords):
            default_msg = custom_response
            break
    
    return {
        "role": "ai",
        "content": default_msg,
        "safe": True,
        "chips": ["Tell me about my nutrition targets", "What should I eat today?", "Hydration tips?"]
    }

@router.post("/message")
async def send_chat_message(req: ChatMessageRequest, request: Request):
    """Send a chat message and get AI response"""
    try:
        print(f"[CHAT] Received message: {req.text}")
        
        # Get current user
        user_payload = get_current_user(request)
        user_id = user_payload.get("userId")  # Token uses camelCase
        print(f"[CHAT] User ID: {user_id}")
        
        db = get_db()
        print(f"[CHAT] Database: {db}")
        
        # Fetch user profile for context
        user_profile = await db.profiles.find_one({"user_id": user_id})
        print(f"[CHAT] Profile: {user_profile}")
        if not user_profile:
            user_profile = {}
        
        # Store user message
        user_msg_doc = {
            "user_id": user_id,
            "role": "user",
            "content": req.text,
            "created_at": datetime.utcnow().isoformat()
        }
        result = await db.chat_messages.insert_one(user_msg_doc)
        
        # Get conversation history (last 20 messages)
        history = []
        cursor = db.chat_messages.find({"user_id": user_id}).sort("created_at", -1).limit(20)
        messages_list = await cursor.to_list(None)
        messages_list.reverse()  # Reverse to chronological order
        for msg in messages_list:
            history.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })
        
        # Get AI response
        ai_response_data = await get_ai_response(
            req.text,
            {
                "name": user_profile.get("displayName", "User"),
                "segment": user_profile.get("segment", "adult"),
                "conditions": user_profile.get("conditions", []),
                "primaryGoal": user_profile.get("primaryGoal", "general health"),
                "dietPreferences": user_profile.get("dietPreferences", []),
                "allergies": user_profile.get("allergies", ""),
                "activityLevel": user_profile.get("activityLevel", "moderate"),
                "calorieTarget": user_profile.get("nutrition", {}).get("calories", 2000),
                "proteinTarget": user_profile.get("nutrition", {}).get("protein_g", 50),
                "carbsTarget": user_profile.get("nutrition", {}).get("carbs_g", 250),
                "fatsTarget": user_profile.get("nutrition", {}).get("fats_g", 65),
            },
            history
        )
        
        # Store AI response
        ai_msg_doc = {
            "user_id": user_id,
            "role": "ai",
            "content": ai_response_data.get("content"),
            "safe": ai_response_data.get("safe", True),
            "chips": ai_response_data.get("chips", []),
            "created_at": datetime.utcnow().isoformat()
        }
        ai_result = await db.chat_messages.insert_one(ai_msg_doc)
        
        # Return AI response
        return {
            "data": {
                "id": str(ai_result.inserted_id),
                "role": "ai",
                "content": ai_response_data.get("content"),
                "safe": ai_response_data.get("safe", True),
                "chips": ai_response_data.get("chips", [])
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Chat error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={"code": "CHAT_ERROR", "message": "Failed to process chat message"}
        )

@router.get("/suggestions")
async def get_chat_suggestions(request: Request):
    """Get personalized chat suggestions based on user profile"""
    try:
        user_payload = get_current_user(request)
        user_id = user_payload.get("userId")  # Token uses camelCase
        
        db = get_db()
        profile = await db.profiles.find_one({"user_id": user_id})
        
        # Base suggestions for all users
        base = [
            "What should I eat for breakfast?",
            "How many calories should I eat?",
            "What foods help with energy?"
        ]
        
        # Add segment and condition-specific suggestions
        if profile:
            segment = profile.get("segment", "")
            conditions = profile.get("conditions", [])
            goals = profile.get("goals", [])
            
            if "teen-girl-h" in segment or "teen-girl-a" in segment or "pcos" in [c.lower() for c in conditions]:
                base.append("What foods help with PCOS?")
            
            if "athlete" in segment or "athletic" in [g.lower() for g in goals]:
                base.append("Best foods for muscle recovery?")
        
        return {"success": True, "data": base}
    
    except Exception as e:
        print(f"Suggestions error: {e}")
        return {"success": True, "data": [
            "What should I eat for breakfast?",
            "How many calories should I eat?",
            "What foods help with energy?"
        ]}

@router.get("/history")
async def get_chat_history(request: Request, limit: int = 50):
    """Get chat history for current user"""
    try:
        user_payload = get_current_user(request)
        user_id = user_payload.get("userId")  # Token uses camelCase
        
        db = get_db()
        
        messages = []
        cursor = db.chat_messages.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        msgs_list = await cursor.to_list(None)
        msgs_list.reverse()  # Reverse to chronological order
        for msg in msgs_list:
            messages.append({
                "id": str(msg.get("_id", "")),
                "role": msg.get("role"),
                "content": msg.get("content"),
                "safe": msg.get("safe", True),
                "chips": msg.get("chips", []),
                "createdAt": msg.get("created_at")
            })
        
        return {"data": messages}
    
    except Exception as e:
        import traceback
        print(f"History error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={"code": "HISTORY_ERROR", "message": "Failed to fetch chat history"}
        )
