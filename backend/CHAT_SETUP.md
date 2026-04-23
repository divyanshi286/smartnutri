# 🤖 AI Chat Implementation Guide - SmartNutri

## ✅ What's Been Implemented

The complete AI chatbot system is now built into SmartNutri! Here's what was added:

### Backend Implementation
- ✅ **Chat Message Storage** — All conversations stored in MongoDB
- ✅ **Chat Routes** — 3 new endpoints:
  - `POST /api/chat/message` — Send message & get AI response
  - `GET /api/chat/suggestions` — Get personalized chat suggestions
  - `GET /api/chat/history` — Retrieve conversation history
- ✅ **LLM Integration** — OpenAI ChatGPT support (optional, with fallback)
- ✅ **Context-Aware Responses** — AI knows user's segment, goals, conditions
- ✅ **Safety Checks** — Filters harmful content with crisis resources
- ✅ **Quick Reply Chips** — Suggested follow-up questions

### Frontend Integration
- ✅ **Chat.jsx** — Already configured to call backend
- ✅ **useChatSuggestions()** — Hook for personalized suggestions
- ✅ **useSendChat()** — Hook for sending messages
- ✅ **Message History** — Persisted in Zustand store

---

## 🚀 Quick Start (No API Key Required)

The chat works **immediately** without an OpenAI API key! It uses a fallback system with helpful responses.

### 1. Start the Backend
```bash
cd smartnutri-backend
python main.py
# Backend runs on http://localhost:3001
```

### 2. Start the Frontend
```bash
cd smartnutri-vite
npm run dev
# Frontend runs on http://localhost:5173
```

### 3. Test the Chat
1. Register → Complete onboarding
2. Go to Dashboard → Click "Chat" tab
3. Try asking questions like:
   - "Best protein foods for my goal?"
   - "What should I eat today?"
   - "PCOS-friendly foods?"
   - "Meal ideas for athletic performance?"

✅ **Chat works immediately without setup!**

---

## 🌟 Upgrade to ChatGPT (Optional - For Better Responses)

To get **personalized AI coaching** with ChatGPT, get an OpenAI API key:

### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (keep it secret!)

### Step 2: Add to Backend
Edit `smartnutri-backend/.env`:
```env
OPENAI_API_KEY=sk-proj-your-key-here
```

### Step 3: Restart Backend
```bash
python main.py
```

Now the chat will use ChatGPT for personalized responses!

### Cost
- Free trial: $5 credit (good for testing)
- Production: ~$0.001 per message
- Budget friendly for small apps

---

## 📋 API Reference

### POST /api/chat/message
Send a message and get AI response.

**Request:**
```json
{
  "text": "Best foods for energy?"
}
```

**Response:**
```json
{
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "role": "ai",
    "content": "Great question! For sustained energy...",
    "safe": true,
    "chips": ["Tell me more", "Any other options?"]
  }
}
```

### GET /api/chat/suggestions
Get personalized suggestions for the current user.

**Response:**
```json
{
  "data": [
    {
      "label": "💪 Best foods for my goal?",
      "msg": "What are the best foods for my goal?"
    },
    ...
  ]
}
```

### GET /api/chat/history?limit=50
Get conversation history.

**Response:**
```json
{
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "role": "user",
      "content": "Best protein sources?",
      "createdAt": "2024-01-15T10:30:00"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "role": "ai",
      "content": "Great question!...",
      "safe": true,
      "chips": ["Tell me more"]
    }
  ]
}
```

---

## 🎯 Fallback Responses (No API Key)

The app has smart fallback responses for common topics:

| User Asks | Response Type | Example |
|-----------|---|---|
| `protein` | Nutrition advice | "Aim for 0.8-1g per pound..." |
| `calories` | Calorie targets | "Your daily target is in nutrition..." |
| `carbs` | Carb advice | "Choose whole grains..." |
| `workout` | Exercise timing | "Eat light carbs 1-2 hrs before..." |
| `pcos` | PCOS tips | "Focus on low-glycemic foods..." |
| `period` | Cycle syncing | "Eat more carbs in follicular phase..." |
| `water` | Hydration | "Aim for 8-10 glasses daily..." |
| `snack` | Snack ideas | "Nuts, fruit, yogurt..." |

For other questions, the bot asks clarifying questions and offers suggestions.

---

## 🛡️ Safety Features

The chat has built-in safety checks:

1. **Harmful Content Detection** — Filters crisis-related keywords
2. **Crisis Resources** — Automatically provides helplines
3. **Response Filtering** — All AI responses marked as safe/unsafe
4. **Age-Appropriate** — Responses tailored to user's segment

Example: If user mentions "suicide" or "self-harm":
```
Response includes:
📞 National Suicide Prevention: 988
💬 Crisis Text Line: Text HOME to 741741
```

---

## 📊 Data Flow Diagram

```
User Types Message
       ↓
Frontend sends to POST /api/chat/message
       ↓
Backend gets user profile + conversation history
       ↓
         ↙ No OpenAI Key      OpenAI Key ↘
    
   Fallback responses         ChatGPT API
   (instant, free)            (personalized, smart)
    
       ↓ Both ↓
       
Store in MongoDB
       ↓
Return message + suggestions
       ↓
Frontend displays + stores in Zustand
       ↓
User sees response immediately
```

---

## 🔧 Troubleshooting

### Chat not responding?
1. Verify backend is running: `http://localhost:3001/health` should return `{"status": "ok"}`
2. Check browser console for errors
3. Verify you're authenticated (logged in)
4. Check backend logs for error messages

### ChatGPT responses failing?
1. Verify API key is correct in `.env`
2. Check OpenAI account has credits
3. Verify no typos in `OPENAI_API_KEY`
4. Restart backend after adding API key

### Responses are generic?
- Without OpenAI API key, fallback responses are used
- Add API key for personalized ChatGPT responses
- Restart backend after adding key

---

## 📝 Next Steps

### Now That Chat Works:
1. ✅ Register & test chat features
2. ✅ Try all suggestions (vary by segment/goals)
3. ✅ Log a meal and ask about it
4. ✅ (Optional) Add OpenAI key for ChatGPT

### What's Next on Phase 1:
- **Food Database** — Real food search/autocomplete
- **Cycle Tracking** — Backend endpoints for cycle management
- **Progress System** — Enhanced analytics & tracking

---

## 💡 Feature Ideas

Future enhancements for chat:

- [ ] Voice input with speech-to-text
- [ ] Meal logging via chat ("Log dal rice lunch")
- [ ] Meal photo analysis ("What's in this?")
- [ ] Personalized meal recommendations
- [ ] Daily nutrition summary
- [ ] Chat export to PDF
- [ ] Chat search & filtering
- [ ] Conversation themes/personas

---

## 🎓 Understanding the Code

### Chat Routes: [chat_routes.py](app/routes/chat_routes.py)
- `POST /api/chat/message` — Main chat handler
- `get_ai_response()` — LLM integration logic
- `generate_fallback_response()` — Fallback responses
- `GET /api/chat/suggestions` — Segment-specific suggestions
- `GET /api/chat/history` — Chat history retrieval

### Models: [models.py](app/models.py)
- `ChatMessageRequest` — Validates user message
- `ChatMessageResponse` — Formats AI response

### Frontend: [Chat.jsx](../smartnutri-vite/src/components/features/chat/Chat.jsx)
- Displays messages in real-time
- Handles user input & voice
- Shows loading states
- Renders quick reply chips

### API Client: [api/index.js](../smartnutri-vite/src/api/index.js)
- `sendChatMessage(text)` — Calls POST /api/chat/message
- `fetchChatSuggestions()` — Calls GET /api/chat/suggestions

---

## 📞 Support

If issues arise:
1. Check backend logs for errors
2. Verify API key format (starts with `sk-proj-`)
3. Check OpenAI account hasn't hit rate limits
4. Restart both frontend & backend
5. Clear browser cache and localStorage

---

**Happy chatting! 🚀**
