export type VADEvent = 'SPEECH_START' | 'SPEECH_PAUSE' | 'SPEECH_END' | 'INTERRUPTION';

export interface VADCallbacks {
  onSpeechStart: () => void;
  onSpeechPause: () => void;
  onSpeechEnd: (finalTranscript: string) => void;
  onInterruption: () => void;
  onTranscriptUpdate: (text: string) => void;
}

export class VADEngine {
  private recognition: any = null;
  private silenceTimer: any = null;
  private isSpeaking: boolean = false;
  private currentTranscript: string = '';
  private callbacks: VADCallbacks;
  private isListening: boolean = false;

  constructor(callbacks: VADCallbacks) {
    this.callbacks = callbacks;
    this.initSpeechRecognition();
  }

  private initSpeechRecognition() {
    if (typeof window === 'undefined') return;
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const rec = new SpeechRecognition();
    rec.continuous = true;
    rec.interimResults = true;

    // Prioritize English / Multi-lingual Indian locale
    rec.lang = 'en-IN';

    rec.onresult = (event: any) => {
      let accumulated = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        accumulated += event.results[i][0].transcript;
      }

      const text = accumulated.trim();
      if (!text) return;

      this.currentTranscript = text;
      this.callbacks.onTranscriptUpdate(text);

      if (!this.isSpeaking) {
        this.isSpeaking = true;
        this.callbacks.onSpeechStart();
      }

      // Reset adaptive silence timer on each interim result (handling candidate thinking pauses)
      this.resetSilenceTimer();
    };

    rec.onerror = (err: any) => {
      console.warn("[VADEngine] SpeechRecognition warning:", err);
    };

    rec.onend = () => {
      if (this.isListening) {
        try {
          rec.start();
        } catch (e) {}
      }
    };

    this.recognition = rec;
  }

  private resetSilenceTimer() {
    if (this.silenceTimer) clearTimeout(this.silenceTimer);

    // 2.5 seconds adaptive silence threshold for completed answer
    this.silenceTimer = setTimeout(() => {
      if (this.isSpeaking && this.currentTranscript.trim().length > 2) {
        this.isSpeaking = false;
        const finalAns = this.currentTranscript;
        this.currentTranscript = '';
        this.callbacks.onSpeechEnd(finalAns);
      }
    }, 2500);
  }

  public startListening() {
    this.isListening = true;
    this.isSpeaking = false;
    this.currentTranscript = '';
    if (this.recognition) {
      try {
        this.recognition.start();
      } catch (e) {}
    }
  }

  public stopListening() {
    this.isListening = false;
    this.isSpeaking = false;
    if (this.silenceTimer) clearTimeout(this.silenceTimer);
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }

  public notifyInterruption() {
    this.callbacks.onInterruption();
  }
}
