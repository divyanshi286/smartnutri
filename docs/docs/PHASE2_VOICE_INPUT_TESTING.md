# Phase 2.1: Voice Input - Testing & Verification Guide

**Date:** April 7, 2026  
**Status:** Implementation Complete - Ready for Testing  
**Components Implemented:**
- ✅ `useVoiceInput.js` - React hook for Web Speech API
- ✅ `VoiceInput.jsx` - UI component with visual feedback
- ✅ `VoiceInput.module.css` - Responsive styling
- ✅ `voice_routes.py` - Backend meal parsing API
- ✅ `voice.js` - API client functions
- ✅ Integration with `main.py`

---

## 🧪 Phase 1: Setup & Verification

### Step 1: Verify Backend Route Registration

Check that voice routes are properly integrated:

```bash
# Start backend
cd smartnutri-backend
python main.py

# In another terminal, test voice endpoint
curl http://localhost:3001/api/voice/food-suggestions?query=chicken
```

**Expected Response:**
```json
{
  "suggestions": ["chicken", "chicken sandwich"]
}
```

### Step 2: Test Food Database

Test that food parsing works:

```bash
curl http://localhost:3001/api/voice/food-info?food_name=chicken
```

**Expected Response:**
```json
{
  "foodName": "Chicken",
  "servingSize": "100g",
  "calories": 165,
  "protein": 31,
  "carbs": 0,
  "fat": 3.6
}
```

---

## 🧪 Phase 2: Frontend Testing

### Step 1: Start Frontend Dev Server

```bash
cd smartnutri-vite
npm run dev
```

### Step 2: Test VoiceInput Component

Create a test file to verify the component:

```bash
# Create test file
cat > smartnutri-vite/src/components/features/VoiceInput.test.jsx << 'EOF'
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { VoiceInput } from './VoiceInput';

// Mock Web Speech API
global.SpeechRecognition = jest.fn(() => ({
  start: jest.fn(),
  stop: jest.fn(),
  abort: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  continuous: false,
  interimResults: false,
  lang: 'en-US',
}));

describe('VoiceInput Component', () => {
  it('renders voice input button', () => {
    render(<VoiceInput />);
    const button = screen.getByRole('button', { name: /start recording/i });
    expect(button).toBeInTheDocument();
  });

  it('shows microphone icon', () => {
    render(<VoiceInput />);
    expect(screen.getByText(/tap to speak/i)).toBeInTheDocument();
  });

  it('handles unsupported browser gracefully', () => {
    // Temporarily disable SpeechRecognition
    global.SpeechRecognition = undefined;
    global.webkitSpeechRecognition = undefined;
    
    render(<VoiceInput />);
    expect(screen.getByText(/voice input not supported/i)).toBeInTheDocument();
  });
});
EOF
```

### Step 3: Manual Browser Testing

#### Test 1: Basic Voice Recording
```
1. Open browser to http://localhost:5173/
2. Navigate to Meals section
3. Click "Voice" input tab
4. Click "Start Recording" button
5. Say: "I had chicken and rice"
6. Click "Stop & Log" button
```

**Expected Output:**
- Microphone permission prompt (first time)
- Pulsing microphone icon while recording
- Transcript appearing in real-time
- Confidence score displayed (95%+)
- Success message: "✅ Chicken with rice logged! ~280 cal"

#### Test 2: Confidence Scoring
```
1. Say clearly: "Grilled salmon with vegetables"
   Expected: 95%+ confidence
   
2. Say quietly/unclear: "something something"
   Expected: 30-50% confidence
   
3. Say nothing
   Expected: "No speech detected" message
```

#### Test 3: Multiple Foods
```
Utterances to test:
- "Chicken and rice" → Should log both foods
- "Large pizza with fries" → Should apply size multiplier
- "Small salad" → Should reduce calories proportionally
- "I had two apples" → Should recognize quantity
```

#### Test 4: Unknown Foods
```
- "I had some mystery food" → Falls back to generic meal estimate
- Random gibberish → Uses description as food name
- Mumbling → Shows error, asks to try again
```

---

## 📊 Manual Test Cases

### Test Case 1: Happy Path
```
Scenario: User logs a common meal
Input: "Chicken sandwich with fries"
Expected:
  - Transcript shows exact wording
  - Confidence: 90%+
  - Meal logged with:
    * foodName: "Chicken sandwich with Fries"
    * calories: ~815
    * protein: ~24g
    * carbs: ~93g
    * fat: ~32g
```

### Test Case 2: Size Modifiers
```
Scenario: User mentions size of meal
Inputs:
  - "Small salad" → calories reduced to 70% of normal
  - "Large burger" → calories increased to 130% of normal
  - "Double pizza" → calories doubled
  
Verify: Multipliers apply to first item only (most common pattern)
```

### Test Case 3: Error Handling
```
Scenarios:
1. No microphone permission
   Expected: "Microphone access denied"
   
2. Network error during submission
   Expected: "Error: Failed to log meal"
   
3. Browser crashes during recording
   Expected: Component gracefully recovers
```

### Test Case 4: Compatibility Testing
```
Test on these browsers:
- Chrome/Brave ✓
- Firefox (works differently)
- Safari iOS ✓
- Edge ✓
- Firefox on phone
- Safari on Android (limited)

Note: Results vary by browser
```

---

## 🔧 Browser Developer Tools Testing

### Test Web Speech API

Open browser console and test:

```javascript
// Check if browser supports Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
console.log('Speech Recognition supported:', !!SpeechRecognition);

// Test microphone permission
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    console.log('Audio devices:', devices.filter(d => d.kind === 'audioinput'));
  });

// Manually test Speech Recognition
const recognition = new SpeechRecognition();
recognition.onresult = (e) => console.log('Heard:', e.results[0][0].transcript);
recognition.start();
// Speak now...
```

---

## 📱 Mobile Testing

### iOS (Safari)
```
✓ Microphone access: Works
✓ Web Speech API: Works
✓ Performance: Good
⚠️ Issues:
  - Requires permission prompt
  - May stop after 60 seconds of silence
```

### Android (Chrome)
```
✓ Microphone access: Works
✓ Web Speech API: Works
✓ Performance: Good
✓ Multilingual: Works
```

---

## 🚀 Performance Testing

### Load Test
```
Measure:
- Time to start recording: < 500ms
- Time to first transcript: < 2 seconds
- Meal logging latency: < 1 second
- API response time: < 500ms
```

### Memory Test
```
Monitoring:
- Memory increase after 1 min recording: < 10MB
- Memory increase during processing: < 20MB
- No memory leaks after multiple recordings
```

### Accuracy Test
```
Test with various inputs:
- 50 clear meal descriptions
- 50 unclear/mumbled inputs
- Expected accuracy: 85%+
```

---

## ✅ Verification Checklist

### Functionality
- [ ] Web Speech API initialized correctly
- [ ] Microphone prompts user for permission
- [ ] Starts listening on button click
- [ ] Stops listening on button click
- [ ] Shows real-time transcript
- [ ] Displays confidence score
- [ ] Sends to backend on stop
- [ ] Displays success message
- [ ] Clears transcript on reset
- [ ] Shows errors gracefully

### UI/UX
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Pulse animation shows while listening
- [ ] Button states clear (disabled/enabled)
- [ ] Timer shows recording duration
- [ ] Colors match design system
- [ ] Accessible (ARIA labels)
- [ ] Tooltips helpful and clear

### Backend
- [ ] Voice endpoint registered
- [ ] Meal parsing works correctly
- [ ] Food database accessible
- [ ] Nutritional calculations accurate
- [ ] Database persistence working
- [ ] Error handling robust
- [ ] Duplicate checking prevents same meal twice

### Cross-Browser
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (iOS/macOS)
- [ ] Edge
- [ ] Mobile Chrome
- [ ] Mobile Safari

---

## 🐛 Debugging Guide

### Issue: Microphone Permission Denied

```
Cause: Browser permission not granted
Solution:
1. Check browser settings
2. Reset permissions: Settings → Privacy → Microphone
3. Reload page
4. Grant permission when prompted

Chrome console:
```javascript
// Check permission status
navigator.permissions.query({ name: 'microphone' })
  .then(result => console.log(result.state));
```

### Issue: No Speech Detected

```
Cause: Microphone not working or too quiet
Solution:
1. Check system mic privacy settings
2. Test microphone in another app
3. Speak louder/closer to microphone
4. Try different browser

Firefox specific:
- Go to about:config
- Set media.navigator.streams.fake = true (for testing)
```

### Issue: Transcript Not Appearing

```
Cause: Interim results not showing
Solution:
View the VoiceInput component's internal state:

In React DevTools:
- Find VoiceInput component
- Check 'transcript' prop value
- Check 'interimTranscript' in hook
```

### Issue: Meal Not Logging

```
Cause: Backend endpoint not responding
Solution:
1. Verify backend is running
2. Check console for network errors
3. Verify route is registered
4. Call API manually:

```bash
curl -X POST http://localhost:3001/api/voice/log-meal \
  -H "Content-Type: application/json" \
  -d '{"mealDescription":"chicken and rice","confidence":0.9}'
```

### Issue: Performance Slow

```
Causes: 
- Backend processing slow
- Network latency
- Microphone lag

Solution:
1. Profile with Chrome DevTools
2. Check Network tab for API latency
3. Optimize food parsing algorithm
```

---

## 📈 Success Metrics

After implementation, measure:

```
Feature Adoption:
- % of users trying voice feature: Target 30%+
- % successful meal logs via voice: Target 80%+
- Time to log meal: Target < 30 seconds

Quality:
- Accuracy of meal recognition: Target 85%+
- Confidence score average: Target 80%+
- Error rate: Target < 5%

Performance:
- API response time: < 500ms (95th percentile)
- Recording latency: < 100ms
- Meal log latency: < 1 second
```

---

## 📋 Testing Checklist Template

Use this when running tests:

```
Date: ___________
Tester: _________
Browser: ________
OS: _____________

Component: VoiceInput
Test Type: (Manual / Automated)

Test Cases:
☐ Test 1: ______________
   Status: (PASS / FAIL)
   Notes: _______________

☐ Test 2: ______________
   Status: (PASS / FAIL)
   Notes: _______________

[etc...]

Overall Status: (PASS / FAIL / PARTIAL)
Issues Found: ___________
```

---

## 🚀 Next Steps

1. **Run all tests** - Use checklist above
2. **Fix any issues** - Debug using the guide
3. **Optimize performance** - Profile and tune
4. **Document findings** - Create bug reports if needed
5. **Move to Phase 2.2** - Camera input (when voice is stable)

---

## 📞 Support

If you encounter issues:

1. Check the debugging guide above
2. Review error messages in console
3. Check browser compatibility
4. Try a different browser
5. Verify backend is running
6. Clear browser cache

**Status: READY FOR TESTING** ✅
