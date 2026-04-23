import { useState, useCallback, useRef } from 'react';

/**
 * Hook for Web Speech API integration
 * Handles voice recording, transcription, and confidence scoring
 */
export const useVoiceInput = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [error, setError] = useState(null);
  const [isSupported, setIsSupported] = useState(
    typeof window !== 'undefined' && 
    (window.SpeechRecognition || window.webkitSpeechRecognition)
  );
  const recognitionRef = useRef(null);
  const interimTranscriptRef = useRef('');

  // Initialize speech recognition
  const initializeRecognition = useCallback(() => {
    if (!isSupported) {
      setError('Speech Recognition is not supported in your browser');
      return null;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    // Configuration
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    recognition.maxAlternatives = 1;

    // Event handlers
    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
      interimTranscriptRef.current = '';
    };

    recognition.onresult = (event) => {
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptSegment = event.results[i][0].transcript;
        const isFinal = event.results[i].isFinal;
        const segmentConfidence = event.results[i][0].confidence;

        if (isFinal) {
          // Update final transcript
          setTranscript((prev) => prev + transcriptSegment + ' ');
          setConfidence(segmentConfidence);
        } else {
          // Build interim transcript (not final yet)
          interimTranscript += transcriptSegment;
        }
      }

      interimTranscriptRef.current = interimTranscript;
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      
      // User-friendly error messages
      const errorMessages = {
        'no-speech': 'No speech detected. Please speak clearly.',
        'audio-capture': 'No microphone found. Please check your device.',
        'network': 'Network error. Please check your connection.',
        'permission-denied': 'Microphone access denied.',
        'aborted': 'Speech recognition was aborted.',
      };

      const errorMsg = errorMessages[event.error] || `Error: ${event.error}`;
      setError(errorMsg);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    return recognition;
  }, [isSupported]);

  // Start listening
  const startListening = useCallback(() => {
    if (!recognitionRef.current) {
      recognitionRef.current = initializeRecognition();
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
      } catch (err) {
        // Already listening
        console.warn('Already listening');
      }
    }
  }, [initializeRecognition]);

  // Stop listening
  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, []);

  // Abort listening
  const abortListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.abort();
      setIsListening(false);
    }
  }, []);

  // Reset transcript
  const resetTranscript = useCallback(() => {
    setTranscript('');
    setConfidence(0);
    setError(null);
    interimTranscriptRef.current = '';
  }, []);

  return {
    transcript,
    isListening,
    error,
    confidence,
    isSupported,
    interimTranscript: interimTranscriptRef.current,
    startListening,
    stopListening,
    abortListening,
    resetTranscript,
  };
};
