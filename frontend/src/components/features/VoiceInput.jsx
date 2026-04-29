import React, { useState, useEffect } from 'react';
import { useVoiceInput } from '../../hooks/useVoiceInput';
import { useLogMeal } from '../../hooks/useQueries';
import { logMealWithVoice } from '../../api/voice';
import styles from './VoiceInput.module.css';

/**
 * VoiceInput Component
 * Allows users to log meals using voice commands
 * Features:
 * - Real-time transcription
 * - Confidence scoring
 * - Multi-language support (optional)
 * - Fallback UI for unsupported browsers
 */
export const VoiceInput = ({ onMealLogged, mealDate = null, onTranscriptChange = null }) => {
  const {
    transcript,
    isListening,
    error,
    confidence,
    isSupported,
    interimTranscript,
    startListening,
    stopListening,
    resetTranscript,
  } = useVoiceInput();

  const [isProcessing, setIsProcessing] = useState(false);
  const [systemMessage, setSystemMessage] = useState('');
  const [recordingTime, setRecordingTime] = useState(0);
  const { mutate: logMeal } = useLogMeal();

  // Track recording time
  useEffect(() => {
    if (!isListening) {
      setRecordingTime(0);
      return;
    }

    const interval = setInterval(() => {
      setRecordingTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [isListening]);

  // Notify parent of transcript changes
  useEffect(() => {
    if (onTranscriptChange) {
      onTranscriptChange({
        transcript,
        interimTranscript,
        isListening,
      });
    }
  }, [transcript, interimTranscript, isListening, onTranscriptChange]);

  const handleStartRecording = () => {
    resetTranscript();
    setSystemMessage('');
    startListening();
  };

  const handleVoiceSubmit = async (voiceTranscript) => {
    try {
      const result = await logMealWithVoice(
        voiceTranscript,
        mealDate || new Date().toISOString(),
        confidence
      );

      // Use React Query mutation for cache invalidation
      logMeal(
        { mealType: 'voice', food: result },
        {
          onSuccess: () => {
            setSystemMessage(`✅ Added: ${result.foodName || result.name} (~${result.calories} cal)`);
            resetTranscript();
            if (onMealLogged) {
              onMealLogged(result);
            }
          },
          onError: (error) => {
            setSystemMessage(`❌ Error: ${error.message}`);
          }
        }
      );
    } catch (err) {
      setSystemMessage(`❌ Error: ${err.message}`);
    }
  };

  const handleStopRecording = async () => {
    stopListening();

    const fullTranscript = (transcript + interimTranscript).trim();

    if (!fullTranscript) {
      setSystemMessage('😅 No speech detected. Please try again.');
      return;
    }

    setIsProcessing(true);
    setSystemMessage('🔄 Processing your meal description...');

    try {
      await handleVoiceSubmit(fullTranscript);
    } finally {
      setIsProcessing(false);
    }
  };

  // Browser not supported
  if (!isSupported) {
    return (
      <div className={styles.voiceInputContainer}>
        <div className={styles.notSupported}>
          <p>🔇 Voice Input Not Supported</p>
          <p className={styles.helpText}>
            Your browser doesn't support voice input. Please use:
          </p>
          <ul>
            <li>Chrome/Chromium</li>
            <li>Safari (iOS/macOS)</li>
            <li>Edge</li>
          </ul>
          <p className={styles.helpText}>Try using the text input or camera instead.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.voiceInputContainer}>
      {/* Recording Status */}
      <div className={styles.recordingIndicator}>
        {isListening && (
          <div className={styles.pulseAnimation}>
            <div className={styles.dot} />
          </div>
        )}
        <h3 className={styles.status}>
          {isListening ? '🎤 Listening...' : '🎤 Tap to speak'}
        </h3>
        {isListening && (
          <p className={styles.timer}>{recordingTime.toFixed(0)}s</p>
        )}
      </div>

      {/* Transcript Display */}
      <div className={styles.transcriptSection}>
        {transcript && (
          <div className={styles.transcript}>
            <p className={styles.label}>What you said:</p>
            <p className={styles.transcriptText}>{transcript}</p>
            {confidence > 0 && (
              <p className={styles.confidence}>
                Confidence: {(confidence * 100).toFixed(0)}% 
                <span className={styles.confidenceBar}>
                  <span 
                    className={styles.confidenceFill}
                    style={{ width: `${confidence * 100}%` }}
                  />
                </span>
              </p>
            )}
          </div>
        )}

        {interimTranscript && !transcript && (
          <div className={styles.interim}>
            <p className={styles.label}>Interim:</p>
            <p className={styles.transcriptText}>{interimTranscript}</p>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className={styles.errorBox}>
          <p className={styles.error}>⚠️ {error}</p>
        </div>
      )}

      {/* System Message */}
      {systemMessage && (
        <div className={styles.messageBox}>
          <p className={styles.message}>{systemMessage}</p>
        </div>
      )}

      {/* Control Buttons */}
      <div className={styles.buttonGroup}>
        {!isListening ? (
          <button
            onClick={handleStartRecording}
            disabled={isProcessing}
            className={styles.primaryBtn}
            title="Start recording your meal description"
          >
            {isProcessing ? '⏳ Processing...' : '🎙️ Start Recording'}
          </button>
        ) : (
          <button
            onClick={handleStopRecording}
            disabled={isProcessing}
            className={styles.stopBtn}
            title="Stop recording"
          >
            ⏹️ Stop & Log
          </button>
        )}

        {transcript && (
          <button
            onClick={resetTranscript}
            disabled={isProcessing || isListening}
            className={styles.secondaryBtn}
            title="Clear the transcript"
          >
            🗑️ Clear
          </button>
        )}
      </div>

      {/* Help Text */}
      <div className={styles.helpSection}>
        <p className={styles.helpText}>
          💡 Tip: Describe what you ate, like "grilled chicken with rice and vegetables"
        </p>
      </div>
    </div>
  );
};
