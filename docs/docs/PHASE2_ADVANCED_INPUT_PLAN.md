# Phase 2: Advanced Input Methods Implementation Guide

**Start Date:** April 7, 2026  
**Scope:** Voice input + Camera/photo recognition for meal logging  
**Estimated Duration:** 4-6 weeks  
**Effort Level:** Medium-High

---

## 🎯 Phase 2 Goals

```
✅ Voice Input for Meals
   └─ Users can log meals by speaking instead of typing

✅ Camera/Photo Input
   └─ Users can take photos of meals and upload

✅ AI Meal Recognition
   └─ System automatically identifies food from photos
   └─ Extracts nutritional information
   └─ Populates meal log form

✅ Enhanced UX
   └─ Quick meal logging (< 30 seconds)
   └─ Mobile-friendly interface
   └─ Offline support for recording
```

---

## 📊 Phase 2 Tech Stack

| Component | Technology | Cost | Reasoning |
|-----------|-----------|------|-----------|
| **Voice Recognition** | Web Speech API (Built-in) | $0 | Free, works in browser, good accuracy |
| **Recording** | MediaRecorder API | $0 | Native browser, no dependencies |
| **Camera Access** | getUserMedia API | $0 | Native browser, works on mobile |
| **Image Recognition** | OpenAI Vision API | $0.01-0.03 per image | Fast, accurate, reasonable cost |
| **File Storage** | MongoDB GridFS | $0 | Use existing database |
| **Optional: CDN** | Cloudflare (free tier) | $0 | Image optimization & caching |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
├─────────────────────────────────────────────────────────────┤
│  VoiceInput Component  │  CameraInput Component            │
│  - Recording UI        │  - Camera stream                  │
│  - Transcript display  │  - Photo capture                  │
│  - Confidence score    │  - Preview                        │
└────────────┬───────────────────────────────┬────────────────┘
             │                               │
             └───────────────────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  API Client (Axios)    │
                    │  - Voice transcription │
                    │  - Image upload        │
                    │  - Meal recognition    │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┴──────────────────┐
             │                                      │
    ┌────────▼──────────┐              ┌──────────▼────────┐
    │  Node.js Backend  │              │  OpenAI Vision    │
    │  /api/voice       │              │  API              │
    │  /api/upload      │              │  (Image analysis) │
    │  /api/recognize   │              └───────────────────┘
    └────────┬──────────┘
             │
    ┌────────▼──────────────┐
    │  MongoDB             │
    │  - Meal logs         │
    │  - Images (GridFS)   │
    │  - Voice recordings  │
    └──────────────────────┘
```

---

## 🔧 Implementation Phases

### Phase 2.1: Voice Input (Week 1-2)
```
Dependencies:
  ✓ Web Speech API (browser native)
  ✓ React hooks for recording
  ✓ Backend endpoint for logging

Files to create:
  - src/components/features/VoiceInput.jsx
  - src/hooks/useVoiceInput.js
  - src/api/voice.js
  - smartnutri-backend/app/routes/voice_routes.py
```

### Phase 2.2: Camera/Photo Upload (Week 2-3)
```
Dependencies:
  ✓ getUserMedia API (browser native)
  ✓ File upload handling
  ✓ MongoDB GridFS for storage

Files to create:
  - src/components/features/CameraInput.jsx
  - src/hooks/useCameraCapture.js
  - smartnutri-backend/app/routes/upload_routes.py
```

### Phase 2.3: Image Recognition (Week 3-4)
```
Dependencies:
  ✓ OpenAI Vision API key
  ✓ Image processing pipeline
  ✓ Calorie/nutrition extraction

Files to create:
  - smartnutri-backend/app/services/vision.py
  - smartnutri-backend/app/routes/recognition_routes.py
```

### Phase 2.4: Integration & Testing (Week 4-5)
```
- Connect voice to meal logging
- Connect photos to meal recognition
- UI/UX polish
- Mobile testing
- Performance optimization
```

---

## 📝 Step 1: Voice Input Implementation

### 1.1 Create Voice Hook

**File:** `smartnutri-vite/src/hooks/useVoiceInput.js`

```javascript
import { useState, useCallback, useRef } from 'react';

export const useVoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);

  // Initialize Web Speech API
  const startListening = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Speech Recognition not supported in this browser');
      return;
    }

    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = 'en-US';

    let interimTranscript = '';

    recognitionRef.current.onstart = () => {
      setIsListening(true);
      setError(null);
    };

    recognitionRef.current.onresult = (event) => {
      interimTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        
        if (event.results[i].isFinal) {
          setTranscript(prev => prev + transcript + ' ');
          setConfidence(event.results[i][0].confidence);
        } else {
          interimTranscript += transcript;
        }
      }
    };

    recognitionRef.current.onerror = (event) => {
      setError(`Speech error: ${event.error}`);
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current.start();
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, []);

  const resetTranscript = useCallback(() => {
    setTranscript('');
    setConfidence(0);
    setError(null);
  }, []);

  return {
    transcript,
    isListening,
    error,
    confidence,
    startListening,
    stopListening,
    resetTranscript
  };
};
```

### 1.2 Create Voice Input Component

**File:** `smartnutri-vite/src/components/features/VoiceInput.jsx`

```javascript
import React, { useState } from 'react';
import { useVoiceInput } from '../../hooks/useVoiceInput';
import { logMealWithVoice } from '../../api/voice';
import styles from './VoiceInput.module.css';

export const VoiceInput = ({ onMealLogged, mealDate }) => {
  const {
    transcript,
    isListening,
    error,
    confidence,
    startListening,
    stopListening,
    resetTranscript
  } = useVoiceInput();

  const [isProcessing, setIsProcessing] = useState(false);
  const [systemMessage, setSystemMessage] = useState('');

  const handleStartRecording = () => {
    resetTranscript();
    startListening();
  };

  const handleStopRecording = async () => {
    stopListening();
    
    if (!transcript.trim()) {
      setSystemMessage('No speech detected. Please try again.');
      return;
    }

    setIsProcessing(true);
    setSystemMessage('Processing your meal...');

    try {
      const result = await logMealWithVoice({
        mealDescription: transcript,
        timestamp: mealDate,
        confidence: confidence
      });

      setSystemMessage(`✅ ${result.foodName} logged! Calories: ${result.calories}`);
      resetTranscript();
      
      if (onMealLogged) {
        onMealLogged(result);
      }
    } catch (err) {
      setSystemMessage(`❌ Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className={styles.voiceInputContainer}>
      <div className={styles.recordingIndicator}>
        {isListening && <div className={styles.pulse} />}
        <h3>{isListening ? '🎤 Listening...' : '🎤 Tap to speak'}</h3>
      </div>

      <div className={styles.transcript}>
        {transcript && (
          <>
            <p className={styles.transcriptText}>{transcript}</p>
            <p className={styles.confidence}>
              Confidence: {(confidence * 100).toFixed(0)}%
            </p>
          </>
        )}
      </div>

      {error && <p className={styles.error}>{error}</p>}
      {systemMessage && <p className={styles.message}>{systemMessage}</p>}

      <div className={styles.buttonGroup}>
        {!isListening ? (
          <button
            onClick={handleStartRecording}
            disabled={isProcessing}
            className={styles.primaryBtn}
          >
            {isProcessing ? '⏳ Processing...' : '🎙️ Start Recording'}
          </button>
        ) : (
          <button
            onClick={handleStopRecording}
            disabled={isProcessing}
            className={styles.stopBtn}
          >
            ⏹️ Stop Recording
          </button>
        )}
        
        {transcript && (
          <button
            onClick={resetTranscript}
            className={styles.secondaryBtn}
          >
            Clear
          </button>
        )}
      </div>
    </div>
  );
};
```

### 1.3 Add Voice API

**File:** `smartnutri-vite/src/api/voice.js`

```javascript
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

export const logMealWithVoice = async (voiceData) => {
  try {
    const response = await axios.post(
      `${API_BASE}/voice/log-meal`,
      {
        mealDescription: voiceData.mealDescription,
        timestamp: voiceData.timestamp,
        confidence: voiceData.confidence
      }
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to log meal');
  }
};

export const transcribeVoice = async (audioBlob) => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  try {
    const response = await axios.post(
      `${API_BASE}/voice/transcribe`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to transcribe');
  }
};
```

### 1.4 Backend Voice Endpoint

**File:** `smartnutri-backend/app/routes/voice_routes.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from app.security import get_current_user
from app.database import db
import re

router = APIRouter(prefix="/voice", tags=["voice"])

class VoiceMealLog(BaseModel):
    mealDescription: str
    timestamp: str = None
    confidence: float = 1.0

@router.post("/log-meal")
async def log_meal_with_voice(
    voice_data: VoiceMealLog,
    current_user: dict = Depends(get_current_user)
):
    """
    Log meal from voice description.
    Uses NLP to extract food, quantity, and estimates calories.
    """
    try:
        description = voice_data.mealDescription.lower().strip()
        
        # Simple NLP parsing (can be enhanced with spaCy/NLTK)
        parsed_meal = parse_meal_description(description)
        
        # Log meal to database
        meal_log = {
            "userId": current_user["_id"],
            "foodName": parsed_meal["foodName"],
            "quantity": parsed_meal["quantity"],
            "calories": parsed_meal["calories"],
            "carbs": parsed_meal["carbs"],
            "protein": parsed_meal["protein"],
            "fat": parsed_meal["fat"],
            "timestamp": voice_data.timestamp or datetime.now().isoformat(),
            "source": "voice",
            "confidence": voice_data.confidence,
            "originalTranscript": description
        }
        
        # Insert into database
        result = await db.meals.insert_one(meal_log)
        meal_log["_id"] = str(result.inserted_id)
        
        return meal_log
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_meal_description(description: str) -> dict:
    """
    Parse meal description to extract nutrients.
    This is a simple implementation - can be enhanced.
    
    Example: "I had a chicken sandwich with fries"
    Returns: {
        "foodName": "chicken sandwich with fries",
        "quantity": "1",
        "calories": 650,
        "protein": 25,
        "carbs": 65,
        "fat": 25
    }
    """
    
    # Food database (expand this)
    food_database = {
        "chicken sandwich": {"calories": 450, "protein": 25, "carbs": 45, "fat": 15},
        "fries": {"calories": 365, "protein": 4, "carbs": 48, "fat": 17},
        "burger": {"calories": 540, "protein": 28, "carbs": 41, "fat": 28},
        "salad": {"calories": 150, "protein": 8, "carbs": 12, "fat": 8},
        "pizza": {"calories": 285, "protein": 12, "carbs": 36, "fat": 10},
        "apple": {"calories": 95, "protein": 0, "carbs": 25, "fat": 0},
        "banana": {"calories": 105, "protein": 1, "carbs": 27, "fat": 0},
        "water": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0},
    }
    
    # Extract quantity (numbers like "1", "2", "a", "an")
    quantity_match = re.search(r'(\d+|a|an)', description)
    quantity = quantity_match.group(0) if quantity_match else "1"
    
    # Find food items in description
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    food_items = []
    
    for food_name, nutrients in food_database.items():
        if food_name in description:
            food_items.append(food_name)
            total_calories += nutrients["calories"]
            total_protein += nutrients["protein"]
            total_carbs += nutrients["carbs"]
            total_fat += nutrients["fat"]
    
    return {
        "foodName": " with ".join(food_items) if food_items else description,
        "quantity": quantity,
        "calories": total_calories if total_calories > 0 else 250,
        "protein": total_protein if total_protein > 0 else 15,
        "carbs": total_carbs if total_carbs > 0 else 30,
        "fat": total_fat if total_fat > 0 else 10
    }
```

---

## 📸 Step 2: Camera/Photo Upload Implementation

### 2.1 Create Camera Hook

**File:** `smartnutri-vite/src/hooks/useCameraCapture.js`

```javascript
import { useState, useRef, useCallback } from 'react';

export const useCameraCapture = () => {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [photo, setPhoto] = useState(null);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsCameraActive(true);
        setError(null);
      }
    } catch (err) {
      setError(`Camera access denied: ${err.message}`);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      setIsCameraActive(false);
    }
  }, []);

  const capturePhoto = useCallback(() => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0);
      
      canvasRef.current.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        setPhoto({ blob, url });
      }, 'image/jpeg', 0.9);
    }
  }, []);

  const clearPhoto = useCallback(() => {
    setPhoto(null);
  }, []);

  return {
    isCameraActive,
    photo,
    error,
    videoRef,
    canvasRef,
    startCamera,
    stopCamera,
    capturePhoto,
    clearPhoto
  };
};
```

### 2.2 Camera Input Component

**File:** `smartnutri-vite/src/components/features/CameraInput.jsx`

```javascript
import React, { useState } from 'react';
import { useCameraCapture } from '../../hooks/useCameraCapture';
import { uploadMealPhoto } from '../../api/upload';
import styles from './CameraInput.module.css';

export const CameraInput = ({ onMealLogged, mealDate }) => {
  const {
    isCameraActive,
    photo,
    error,
    videoRef,
    canvasRef,
    startCamera,
    stopCamera,
    capturePhoto,
    clearPhoto
  } = useCameraCapture();

  const [isProcessing, setIsProcessing] = useState(false);
  const [systemMessage, setSystemMessage] = useState('');

  const handleStartCamera = async () => {
    await startCamera();
  };

  const handleCapture = () => {
    capturePhoto();
    setSystemMessage('📸 Photo captured! Review before submitting.');
  };

  const handleUpload = async () => {
    if (!photo) return;

    setIsProcessing(true);
    setSystemMessage('🔍 Analyzing meal...');

    try {
      const result = await uploadMealPhoto(photo.blob, mealDate);
      setSystemMessage(`✅ ${result.foodName} identified! Calories: ${result.calories}`);
      clearPhoto();
      
      if (onMealLogged) {
        onMealLogged(result);
      }
    } catch (err) {
      setSystemMessage(`❌ ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  if (error) {
    return (
      <div className={styles.cameraContainer}>
        <p className={styles.error}>❌ {error}</p>
        <p className={styles.helpText}>
          Make sure you've granted camera permissions in your browser settings.
        </p>
      </div>
    );
  }

  return (
    <div className={styles.cameraContainer}>
      {!isCameraActive && !photo && (
        <div className={styles.placeholder}>
          <p>📷 Take a photo of your meal</p>
          <button onClick={handleStartCamera} className={styles.primaryBtn}>
            📷 Open Camera
          </button>
        </div>
      )}

      {isCameraActive && !photo && (
        <div className={styles.cameraSection}>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className={styles.videoStream}
          />
          <canvas ref={canvasRef} style={{ display: 'none' }} />
          
          <div className={styles.controls}>
            <button onClick={handleCapture} className={styles.captureBtn}>
              📸 Capture Photo
            </button>
            <button onClick={stopCamera} className={styles.secondaryBtn}>
              ✕ Cancel
            </button>
          </div>
        </div>
      )}

      {photo && (
        <div className={styles.previewSection}>
          <img src={photo.url} alt="Meal preview" className={styles.preview} />
          <div className={styles.controls}>
            <button
              onClick={handleUpload}
              disabled={isProcessing}
              className={styles.primaryBtn}
            >
              {isProcessing ? '⏳ Analyzing...' : '✅ Log Meal'}
            </button>
            <button
              onClick={() => {
                clearPhoto();
                handleStartCamera();
              }}
              className={styles.secondaryBtn}
            >
              📸 Retake Photo
            </button>
          </div>
        </div>
      )}

      {systemMessage && <p className={styles.message}>{systemMessage}</p>}
    </div>
  );
};
```

### 2.3 Upload API

**File:** `smartnutri-vite/src/api/upload.js`

```javascript
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

export const uploadMealPhoto = async (imageBlob, mealDate) => {
  const formData = new FormData();
  formData.append('image', imageBlob, 'meal.jpg');
  formData.append('timestamp', mealDate);

  try {
    const response = await axios.post(
      `${API_BASE}/upload/meal-photo`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to upload photo');
  }
};

export const recognizeMeal = async (imageBlob) => {
  const formData = new FormData();
  formData.append('image', imageBlob);

  try {
    const response = await axios.post(
      `${API_BASE}/recognition/analyze-meal`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to recognize meal');
  }
};
```

---

## 🤖 Step 3: Image Recognition with OpenAI Vision

### 3.1 Setup OpenAI API

**Get API Key:**
```bash
1. Go to https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy key to backend .env file
4. Set: OPENAI_API_KEY=sk-....
```

### 3.2 Vision Service

**File:** `smartnutri-backend/app/services/vision.py`

```python
import openai
import base64
from typing import Dict
import os

class VisionService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_meal_image(self, image_data: bytes) -> Dict:
        """
        Analyze a meal image using OpenAI Vision API.
        Returns: {
            "foodName": "Grilled chicken with vegetables",
            "confidence": 0.95,
            "calories": 450,
            "protein": 35,
            "carbs": 20,
            "fat": 15,
            "servingSize": "1 plate",
            "description": "Grilled chicken breast with steamed broccoli and carrots"
        }
        """
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Call OpenAI Vision API
            response = self.client.vision.analyze(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": self._get_analysis_prompt()
                            }
                        ]
                    }
                ]
            )
            
            # Parse response
            result = self._parse_vision_response(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Vision API error: {str(e)}")
    
    def _get_analysis_prompt(self) -> str:
        """Prompt for meal analysis"""
        return """Analyze this food image and provide:
1. Food name/description
2. Estimated calorie count
3. Macronutrients (protein, carbs, fat in grams)
4. Serving size estimate
5. Confidence level (0-1)

Format as JSON:
{
    "foodName": "...",
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
    "servingSize": "...",
    "confidence": 0.0,
    "ingredients": ["...", "..."]
}"""
    
    def _parse_vision_response(self, response_text: str) -> Dict:
        """Parse JSON response from Vision API"""
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback
                return {
                    "foodName": "Unknown meal",
                    "calories": 300,
                    "protein": 15,
                    "carbs": 40,
                    "fat": 10,
                    "servingSize": "1 serving",
                    "confidence": 0.5
                }
        except:
            return {
                "foodName": "Unknown meal",
                "calories": 300,
                "protein": 15,
                "carbs": 40,
                "fat": 10
            }

vision_service = VisionService()
```

### 3.3 Upload Routes with Recognition

**File:** `smartnutri-backend/app/routes/upload_routes.py`

```python
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from softmax.services.vision import vision_service
from app.database import db
from app.security import get_current_user
from datetime import datetime
import io

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/meal-photo")
async def upload_meal_photo(
    image: UploadFile = File(...),
    timestamp: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a meal photo and analyze it with Vision API.
    Automatically fills in nutritional information.
    """
    try:
        # Read image data
        image_data = await image.read()
        
        # Analyze with Vision API
        meal_info = await vision_service.analyze_meal_image(image_data)
        
        # Store image in MongoDB GridFS
        grid_fs = GridFS(db)
        file_id = grid_fs.put(image_data, filename=f"meal_{datetime.now().timestamp()}.jpg")
        
        # Create meal log document
        meal_log = {
            "userId": current_user["_id"],
            "foodName": meal_info.get("foodName", "Unknown"),
            "calories": meal_info.get("calories", 300),
            "protein": meal_info.get("protein", 15),
            "carbs": meal_info.get("carbs", 40),
            "fat": meal_info.get("fat", 10),
            "servingSize": meal_info.get("servingSize", "1 serving"),
            "timestamp": timestamp or datetime.now().isoformat(),
            "source": "camera",
            "confidence": meal_info.get("confidence", 0.8),
            "imageId": str(file_id),
            "ingredients": meal_info.get("ingredients", [])
        }
        
        # Insert into database
        result = await db.meals.insert_one(meal_log)
        meal_log["_id"] = str(result.inserted_id)
        
        return meal_log
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/meal-photo/{file_id}")
async def get_meal_photo(file_id: str):
    """Retrieve stored meal photo"""
    try:
        grid_fs = GridFS(db)
        file_data = grid_fs.get(ObjectId(file_id))
        return StreamingResponse(
            io.BytesIO(file_data.read()),
            media_type="image/jpeg"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Photo not found")
```

---

## 🎨 Step 4: Frontend Integration

### 4.1 Update Meals Component

Integrate voice and camera into existing Meals.jsx:

```javascript
// In smartnutri-vite/src/components/features/meals/Meals.jsx

import { VoiceInput } from '../VoiceInput';
import { CameraInput } from '../CameraInput';

export const Meals = () => {
  const [inputMode, setInputMode] = useState('form'); // 'form' | 'voice' | 'camera'

  return (
    <div className={styles.mealsContainer}>
      <div className={styles.inputModes}>
        <button 
          onClick={() => setInputMode('form')}
          className={inputMode === 'form' ? styles.active : ''}
        >
          ✍️ Type
        </button>
        <button 
          onClick={() => setInputMode('voice')}
          className={inputMode === 'voice' ? styles.active : ''}
        >
          🎤 Voice
        </button>
        <button 
          onClick={() => setInputMode('camera')}
          className={inputMode === 'camera' ? styles.active : ''}
        >
          📷 Photo
        </button>
      </div>

      {inputMode === 'form' && <MealForm onSubmit={handleLogMeal} />}
      {inputMode === 'voice' && <VoiceInput onMealLogged={handleMealLogged} />}
      {inputMode === 'camera' && <CameraInput onMealLogged={handleMealLogged} />}

      {/* Existing meal list... */}
    </div>
  );
};
```

---

## 📊 Cost Analysis

| Feature | Service | Monthly Cost | Notes |
|---------|---------|--------------|-------|
| Voice Input | Web Speech API | $0 | Free, built-in |
| Camera | getUserMedia API | $0 | Free, built-in |
| Image Recognition | OpenAI Vision | ~$15 | ~1000 images at $0.01-0.03 each |
| Image Storage | MongoDB | $0 | Free tier (512MB) |
| **Total** | | **~$15/month** | Scales with usage |

---

## 🧪 Testing Strategy

### Manual Testing
```bash
1. Voice Input
   - Test in Chrome, Firefox, Safari
   - Test with different accents
   - Test confidence scoring

2. Camera
   - Test on mobile devices
   - Test with different lighting
   - Test with different food types

3. Image Recognition
   - Test with clear photos
   - Test with blurry photos
   - Test with multiple food items
```

### Automated Tests
```python
# Backend tests for voice parsing
def test_parse_meal_description():
    result = parse_meal_description("chicken sandwich with fries")
    assert result["foodName"] == "chicken sandwich with fries"
    assert result["calories"] > 0

# Backend tests for vision API
@pytest.mark.asyncio
async def test_analyze_meal_image():
    image_path = "test_images/sandwich.jpg"
    with open(image_path, "rb") as f:
        result = await vision_service.analyze_meal_image(f.read())
    assert "foodName" in result
    assert result["calories"] > 0
```

---

## 📋 Implementation Checklist

### Week 1-2: Voice Input
- [ ] Create `useVoiceInput` hook
- [ ] Build VoiceInput component
- [ ] Create backend voice endpoint
- [ ] Implement meal parsing logic
- [ ] Test across browsers
- [ ] Add error handling

### Week 2-3: Camera/Upload
- [ ] Create `useCameraCapture` hook
- [ ] Build CameraInput component
- [ ] Implement file upload API
- [ ] Setup MongoDB GridFS
- [ ] Test on mobile devices

### Week 3-4: Image Recognition
- [ ] Get OpenAI API key
- [ ] Build VisionService
- [ ] Integrate Vision API
- [ ] Create meal recognition endpoint
- [ ] Test with different foods

### Week 4-5: Integration & Polish
- [ ] Integrate voice into Meals component
- [ ] Integrate camera into Meals component
- [ ] Add loading states
- [ ] Optimize images before upload
- [ ] Add confidence scoring UI
- [ ] Mobile responsiveness

### Week 5-6: Testing & Deployment
- [ ] Manual E2E testing
- [ ] Performance testing
- [ ] Mobile testing
- [ ] Create test data
- [ ] Deploy to staging
- [ ] Beta user testing

---

## 🚀 Next Steps

1. **Start with Voice Input** (easiest, no dependencies)
2. **Add Camera** (requires permission handling)
3. **Integrate OpenAI Vision** (requires API key and cost)
4. **Polish & Test** (ensure quality UX)

Ready to start? Let me know and I'll help with the first implementation!

---

**Estimated Timeline:** 4-6 weeks  
**Estimated Team Size:** 1 full-stack engineer  
**Estimated Cost:** $15/month (image recognition API)
