import React, { useEffect, useState, useRef } from 'react';
import { api } from '../../services/api';
import { InterviewQuestionData } from '../../types';
import { Mic, MicOff, Volume2, VolumeX, Square, Send, Sparkles, Brain, CheckCircle2, AlertCircle } from 'lucide-react';

interface VoiceInterviewViewProps {
  interviewId: string;
  onFinish: () => void;
}

type InterviewState = 'GENERATING' | 'AI_SPEAKING' | 'LISTENING' | 'EVALUATING' | 'IDLE';

export const VoiceInterviewView: React.FC<VoiceInterviewViewProps> = ({ interviewId, onFinish }) => {
  const [currentQuestion, setCurrentQuestion] = useState<InterviewQuestionData | null>(null);
  const [state, setState] = useState<InterviewState>('GENERATING');
  const [transcript, setTranscript] = useState<string>('');
  const [manualText, setManualText] = useState<string>('');
  const [useTextInput, setUseTextInput] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [questionsCount, setQuestionsCount] = useState<number>(1);
  
  // Speech Recognition reference
  const recognitionRef = useRef<any>(null);

  // 1. Fetch Next Question
  const loadNextQuestion = async () => {
    setState('GENERATING');
    setTranscript('');
    setManualText('');
    setError(null);

    try {
      const q = await api.getNextQuestion(interviewId);
      setCurrentQuestion(q);
      setQuestionsCount(q.question_number);
      
      // Auto speak question using Browser Web Speech API
      speakQuestion(q.question_text);
    } catch (e: any) {
      if (e.message.includes('completed')) {
        handleFinishInterview();
      } else {
        console.error("Error loading question", e);
        setError(e.message || "Failed generating next question.");
        setState('IDLE');
      }
    }
  };

  useEffect(() => {
    loadNextQuestion();

    // Initialize Web SpeechRecognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: any) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recognition.onerror = (err: any) => {
        console.warn("Speech recognition error:", err);
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
      if (recognitionRef.current) recognitionRef.current.stop();
    };
  }, [interviewId]);

  // 2. Play AI Voice Question
  const speakQuestion = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      utterance.onstart = () => setState('AI_SPEAKING');
      utterance.onend = () => startListening();
      utterance.onerror = () => startListening();

      window.speechSynthesis.speak(utterance);
    } else {
      startListening();
    }
  };

  // 3. Start Listening to Student Voice
  const startListening = () => {
    setState('LISTENING');
    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
      } catch (e) {
        // Recognition already started
      }
    }
  };

  // 4. Stop Listening & Submit Answer
  const stopListeningAndSubmit = async (finalAnswerText?: string) => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
    }

    const answerToSubmit = finalAnswerText || transcript || manualText;
    if (!answerToSubmit || answerToSubmit.trim().length < 2) {
      setError("No voice answer detected. Please speak your answer or use text input.");
      return;
    }

    setState('EVALUATING');
    setError(null);

    try {
      await api.submitInterviewAnswer(interviewId, answerToSubmit);
      if (questionsCount >= 5) {
        handleFinishInterview();
      } else {
        loadNextQuestion();
      }
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Evaluation failed. Please try again.");
      setState('IDLE');
    }
  };

  const handleFinishInterview = async () => {
    try {
      await api.finishInterview(interviewId);
      onFinish();
    } catch (e) {
      console.error(e);
      onFinish();
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Header Card */}
      <div className="glass-panel p-6 rounded-2xl flex flex-wrap items-center justify-between gap-4 border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30 flex items-center justify-center font-bold">
            Q{questionsCount}
          </div>
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Technical Voice Interview</span>
            <h2 className="text-xl font-bold text-white">Question {questionsCount} of 5</h2>
          </div>
        </div>

        <button
          onClick={handleFinishInterview}
          className="px-4 py-2 bg-rose-600/20 text-rose-300 border border-rose-500/30 hover:bg-rose-600/30 text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5"
        >
          <Square className="w-3.5 h-3.5 fill-rose-400" /> End Interview Early
        </button>
      </div>

      {/* Main Interactive Screen */}
      <div className="glass-panel p-8 rounded-3xl border border-slate-800 text-center relative overflow-hidden space-y-8">
        
        {/* Visual State Badges */}
        <div className="flex justify-center">
          {state === 'GENERATING' && (
            <div className="px-4 py-1.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-bold flex items-center gap-2 animate-pulse">
              <Sparkles className="w-4 h-4" /> Generating Adaptive Question...
            </div>
          )}

          {state === 'AI_SPEAKING' && (
            <div className="px-4 py-1.5 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-bold flex items-center gap-2 glow-active">
              <Volume2 className="w-4 h-4 animate-bounce" /> AI SPEAKING
            </div>
          )}

          {state === 'LISTENING' && (
            <div className="px-4 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-bold flex items-center gap-2 glow-active">
              <Mic className="w-4 h-4 animate-pulse" /> LISTENING TO YOUR VOICE...
            </div>
          )}

          {state === 'EVALUATING' && (
            <div className="px-4 py-1.5 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-bold flex items-center gap-2 animate-pulse">
              <Brain className="w-4 h-4" /> Evaluating Technical Dimensions...
            </div>
          )}
        </div>

        {/* AI Question Statement */}
        {currentQuestion && (
          <div className="space-y-3 max-w-2xl mx-auto">
            <div className="flex items-center justify-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 px-2.5 py-0.5 rounded-full border border-blue-500/20">
                {currentQuestion.topic}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-purple-500/10 text-purple-400 px-2.5 py-0.5 rounded-full border border-purple-500/20">
                {currentQuestion.question_type}
              </span>
            </div>

            <h3 className="text-xl sm:text-2xl font-extrabold text-white leading-relaxed">
              "{currentQuestion.question_text}"
            </h3>
          </div>
        )}

        {/* Animated Mic Wave Area */}
        <div className="py-6 flex flex-col items-center justify-center">
          <div
            onClick={() => {
              if (state === 'LISTENING') stopListeningAndSubmit();
              else startListening();
            }}
            className={`w-28 h-28 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 ${
              state === 'LISTENING'
                ? 'bg-gradient-to-tr from-emerald-600 to-teal-500 shadow-xl shadow-emerald-500/40 scale-105'
                : 'bg-slate-900 border border-slate-800 hover:border-slate-700'
            }`}
          >
            <Mic className={`w-12 h-12 ${state === 'LISTENING' ? 'text-white animate-bounce' : 'text-slate-500'}`} />
          </div>

          <p className="text-xs text-slate-400 font-medium mt-4">
            {state === 'LISTENING' ? 'Click mic or finish speaking to evaluate answer' : 'Click mic to record voice answer'}
          </p>
        </div>

        {/* Real-time Speech Transcript Display */}
        {transcript && (
          <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 text-left max-w-2xl mx-auto">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Live Transcribed Answer:</p>
            <p className="text-sm text-slate-200 font-mono italic">"{transcript}"</p>
          </div>
        )}

        {/* Text Input Fallback Toggle */}
        <div className="max-w-xl mx-auto pt-2">
          {!useTextInput ? (
            <button
              type="button"
              onClick={() => setUseTextInput(true)}
              className="text-xs font-semibold text-slate-400 hover:text-blue-400 underline"
            >
              Having microphone issues? Use text input fallback
            </button>
          ) : (
            <div className="space-y-3 text-left">
              <textarea
                rows={3}
                value={manualText}
                onChange={(e) => setManualText(e.target.value)}
                placeholder="Type your technical answer here..."
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
              />
              <button
                type="button"
                onClick={() => stopListeningAndSubmit(manualText)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl flex items-center gap-1.5"
              >
                <Send className="w-3.5 h-3.5" /> Submit Written Answer
              </button>
            </div>
          )}
        </div>

        {error && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs font-semibold flex items-center justify-center gap-2 max-w-md mx-auto">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

      </div>

    </div>
  );
};
