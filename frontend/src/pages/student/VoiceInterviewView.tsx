import React, { useEffect, useState, useRef } from 'react';
import { api } from '../../services/api';
import { VoiceSynthService } from '../../services/voice_synth';
import { VADEngine } from '../../services/vad_engine';
import { Square, Volume2, Mic, Brain, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';

interface VoiceInterviewViewProps {
  interviewId: string;
  onFinish: () => void;
}

export type InterviewState = 
  | 'IDLE'
  | 'INTRO'
  | 'AI_SPEAKING'
  | 'AI_FINISHED'
  | 'LISTENING'
  | 'USER_SPEAKING'
  | 'USER_PAUSED'
  | 'USER_FINISHED'
  | 'PROCESSING'
  | 'EVALUATING'
  | 'GENERATING_FOLLOWUP'
  | 'GENERATING_NEXT_QUESTION'
  | 'AI_RESPONDING'
  | 'COMPLETED'
  | 'ERROR';

export const VoiceInterviewView: React.FC<VoiceInterviewViewProps> = ({ interviewId, onFinish }) => {
  const [state, setState] = useState<InterviewState>('INTRO');
  const [currentQuestion, setCurrentQuestion] = useState<any>(null);
  const [reactionText, setReactionText] = useState<string>('');
  const [transcript, setTranscript] = useState<string>('');
  const [questionNum, setQuestionNum] = useState<number>(1);
  const [error, setError] = useState<string | null>(null);

  // Timer
  const [secondsElapsed, setSecondsElapsed] = useState<number>(0);
  const timerRef = useRef<any>(null);

  // VAD Engine Reference
  const vadRef = useRef<VADEngine | null>(null);

  // Start Timer
  useEffect(() => {
    timerRef.current = setInterval(() => {
      setSecondsElapsed(prev => prev + 1);
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      VoiceSynthService.stop();
      if (vadRef.current) vadRef.current.stopListening();
    };
  }, []);

  // Initialize VAD Engine & Load First Question
  useEffect(() => {
    vadRef.current = new VADEngine({
      onSpeechStart: () => {
        // If AI is speaking and user interrupts
        if (state === 'AI_SPEAKING') {
          VoiceSynthService.stop();
          setState('USER_SPEAKING');
        } else {
          setState('USER_SPEAKING');
        }
      },
      onSpeechPause: () => {
        setState('USER_PAUSED');
      },
      onSpeechEnd: (finalAns) => {
        handleUserSpeechFinished(finalAns);
      },
      onInterruption: () => {
        VoiceSynthService.stop();
        setState('USER_SPEAKING');
      },
      onTranscriptUpdate: (text) => {
        setTranscript(text);
      }
    });

    playIntroAndLoadFirstQuestion();
  }, [interviewId]);

  // 1. Play Brief AI Greeting Intro
  const playIntroAndLoadFirstQuestion = async () => {
    setState('INTRO');
    const introMsg = "Hi! Welcome to your AI Voice Technical Interview. I've analyzed your resume and skills. Let me start with your first technical question.";
    
    VoiceSynthService.speak(introMsg, 
      () => setState('AI_SPEAKING'),
      () => loadNextQuestion()
    );
  };

  // 2. Fetch Next Question / Adaptive Follow-Up
  const loadNextQuestion = async () => {
    setState('GENERATING_NEXT_QUESTION');
    setTranscript('');
    setError(null);

    try {
      const data = await api.getNextQuestion(interviewId);
      setCurrentQuestion(data);
      setQuestionNum(data.question_number);
      setReactionText(data.reaction || "Got it.");

      // AI speaks Reaction + Spoken Question
      const fullSpoken = `${data.reaction || "Got it."} ${data.question_text}`;
      
      VoiceSynthService.speak(
        fullSpoken,
        () => setState('AI_SPEAKING'),
        () => {
          setState('LISTENING');
          if (vadRef.current) vadRef.current.startListening();
        }
      );
    } catch (e: any) {
      if (e.message.includes('completed')) {
        handleFinishInterview();
      } else {
        console.error("Error generating question", e);
        setError(e.message || "Failed loading question.");
        setState('ERROR');
      }
    }
  };

  // 3. User Finished Answer -> Send for Evaluation
  const handleUserSpeechFinished = async (spokenText: string) => {
    if (vadRef.current) vadRef.current.stopListening();

    // Check for clarification requests (Interruption handling)
    const textLower = spokenText.toLowerCase();
    if (textLower.includes("repeat") || textLower.includes("didn't understand") || textLower.includes("pardon")) {
      const repeatMsg = `Sure, I'll repeat that for you. ${currentQuestion?.question_text || ""}`;
      VoiceSynthService.speak(
        repeatMsg,
        () => setState('AI_SPEAKING'),
        () => {
          setState('LISTENING');
          if (vadRef.current) vadRef.current.startListening();
        }
      );
      return;
    }

    setState('EVALUATING');

    try {
      const result = await api.submitInterviewAnswer(interviewId, spokenText);

      // Low confidence recovery check
      if (result.low_speech_confidence) {
        const recoverMsg = "Sorry, I couldn't catch that clearly. Could you please repeat your answer?";
        VoiceSynthService.speak(
          recoverMsg,
          () => setState('AI_SPEAKING'),
          () => {
            setState('LISTENING');
            if (vadRef.current) vadRef.current.startListening();
          }
        );
        return;
      }

      if (questionNum >= 5) {
        handleFinishInterview();
      } else {
        loadNextQuestion();
      }
    } catch (e: any) {
      console.error("Evaluation error:", e);
      setError(e.message || "Evaluation error.");
      setState('ERROR');
    }
  };

  const handleFinishInterview = async () => {
    VoiceSynthService.stop();
    if (vadRef.current) vadRef.current.stopListening();
    try {
      await api.finishInterview(interviewId);
      onFinish();
    } catch (e) {
      onFinish();
    }
  };

  // Format Timer
  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header Bar */}
      <div className="glass-panel p-6 rounded-2xl flex items-center justify-between border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30 flex items-center justify-center font-bold">
            Q{questionNum}
          </div>
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Real-Time AI Technical Voice Interview</span>
            <h2 className="text-xl font-bold text-white">Question {questionNum} of 5</h2>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-xs font-mono font-bold text-slate-300 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800">
            ⏱ {formatTime(secondsElapsed)}
          </div>
          <button
            onClick={handleFinishInterview}
            className="px-4 py-2 bg-rose-600/20 text-rose-300 border border-rose-500/30 hover:bg-rose-600/30 text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5"
          >
            <Square className="w-3.5 h-3.5 fill-rose-400" /> End Interview
          </button>
        </div>
      </div>

      {/* Main Human-Like Interviewer Card */}
      <div className="glass-panel p-8 sm:p-12 rounded-3xl border border-purple-500/30 text-center relative overflow-hidden space-y-8 bg-gradient-to-b from-slate-900/90 to-purple-950/20 shadow-2xl">
        
        {/* Female AI Technical Interviewer Avatar */}
        <div className="relative inline-block">
          <div className={`w-32 h-32 rounded-full mx-auto flex items-center justify-center border-2 transition-all duration-500 ${
            state === 'AI_SPEAKING'
              ? 'border-purple-500 bg-purple-600/20 shadow-2xl shadow-purple-500/50 scale-105'
              : state === 'USER_SPEAKING' || state === 'LISTENING'
              ? 'border-emerald-500 bg-emerald-600/20 shadow-2xl shadow-emerald-500/50 scale-105'
              : 'border-slate-800 bg-slate-900'
          }`}>
            <Brain className={`w-16 h-16 transition-colors ${
              state === 'AI_SPEAKING' ? 'text-purple-400 animate-pulse' : state === 'USER_SPEAKING' ? 'text-emerald-400 animate-bounce' : 'text-slate-500'
            }`} />
          </div>

          {/* Spoken Pulse Wave Animation */}
          {state === 'AI_SPEAKING' && (
            <div className="absolute inset-0 rounded-full border-4 border-purple-400/40 animate-ping pointer-events-none" />
          )}
          {state === 'USER_SPEAKING' && (
            <div className="absolute inset-0 rounded-full border-4 border-emerald-400/40 animate-ping pointer-events-none" />
          )}
        </div>

        {/* State Badge */}
        <div className="flex justify-center">
          {state === 'INTRO' && (
            <div className="px-4 py-1.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-bold flex items-center gap-2">
              <Sparkles className="w-4 h-4 animate-spin" /> INTRODUCING INTERVIEW
            </div>
          )}

          {state === 'AI_SPEAKING' && (
            <div className="px-4 py-1.5 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-bold flex items-center gap-2 glow-active">
              <Volume2 className="w-4 h-4 animate-bounce" /> AI INTERVIEWER SPEAKING
            </div>
          )}

          {(state === 'LISTENING' || state === 'USER_SPEAKING' || state === 'USER_PAUSED') && (
            <div className="px-4 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-bold flex items-center gap-2 glow-active">
              <Mic className="w-4 h-4 animate-pulse" />
              {state === 'USER_SPEAKING' ? 'SPEAKING... (Automatic Turn Detection Active)' : state === 'USER_PAUSED' ? 'THINKING... (System Waiting)' : 'LISTENING TO YOUR VOICE...'}
            </div>
          )}

          {(state === 'PROCESSING' || state === 'EVALUATING') && (
            <div className="px-4 py-1.5 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-bold flex items-center gap-2 animate-pulse">
              <Brain className="w-4 h-4" /> Evaluating Technical Reasoning...
            </div>
          )}

          {(state === 'GENERATING_NEXT_QUESTION' || state === 'GENERATING_FOLLOWUP') && (
            <div className="px-4 py-1.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-bold flex items-center gap-2 animate-pulse">
              <Sparkles className="w-4 h-4" /> Synthesizing Adaptive Follow-up Question...
            </div>
          )}
        </div>

        {/* Question Subtitle Card */}
        {currentQuestion && (
          <div className="space-y-3 max-w-2xl mx-auto bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
            <div className="flex items-center justify-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-purple-500/10 text-purple-400 px-2.5 py-0.5 rounded-full border border-purple-500/20">
                {currentQuestion.topic}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 px-2.5 py-0.5 rounded-full border border-blue-500/20">
                {currentQuestion.question_type}
              </span>
            </div>

            <h3 className="text-xl sm:text-2xl font-extrabold text-white leading-relaxed">
              "{currentQuestion.question_text}"
            </h3>
          </div>
        )}

        {/* Live Spoken Transcript */}
        {transcript && (
          <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 text-left max-w-2xl mx-auto">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Live Candidate Voice Transcript (Hinglish/English):</p>
            <p className="text-sm text-slate-200 font-mono italic">"{transcript}"</p>
          </div>
        )}

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
