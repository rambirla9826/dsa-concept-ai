export class VoiceSynthService {
  private static selectedVoice: SpeechSynthesisVoice | null = null;

  private static initVoices(): SpeechSynthesisVoice | null {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      return null;
    }

    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return null;

    // Prioritize Female Indian English voices
    const indianFemale = voices.find(v => 
      v.lang.toLowerCase().includes('en-in') || 
      (v.lang.toLowerCase().includes('in') && v.name.toLowerCase().includes('female')) ||
      v.name.toLowerCase().includes('heera') ||
      v.name.toLowerCase().includes('veena') ||
      v.name.toLowerCase().includes('google हिन्दी')
    );

    if (indianFemale) {
      cls.selectedVoice = indianFemale;
      return indianFemale;
    }

    // Fallback to any en-IN voice
    const indianAny = voices.find(v => v.lang.toLowerCase().includes('en-in'));
    if (indianAny) {
      cls.selectedVoice = indianAny;
      return indianAny;
    }

    // Fallback to UK/US Female voice
    const femaleFallback = voices.find(v => 
      v.name.toLowerCase().includes('female') || 
      v.name.toLowerCase().includes('zira') || 
      v.name.toLowerCase().includes('samantha')
    );

    cls.selectedVoice = femaleFallback || voices[0];
    return cls.selectedVoice;
  }

  public static speak(text: string, onStart?: () => void, onEnd?: () => void) {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      if (onEnd) onEnd();
      return;
    }

    window.speechSynthesis.cancel(); // Stop any previous speech immediately

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    const voice = this.initVoices();
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
    }

    utterance.onstart = () => {
      if (onStart) onStart();
    };

    utterance.onend = () => {
      if (onEnd) onEnd();
    };

    utterance.onerror = () => {
      if (onEnd) onEnd();
    };

    window.speechSynthesis.speak(utterance);
  }

  public static stop() {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }
}
const cls = VoiceSynthService;
