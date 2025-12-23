import sounddevice as sd
import numpy as np
import time

# --- Constants ---
RATE = 16000
CHANNELS = 1
DTYPE = "float32"

def rms_energy(audio: np.ndarray) -> float:
    """Calculates RMS energy with DC offset removal."""
    if audio.size == 0:
        return 0.0
    audio = np.nan_to_num(audio)
    # Remove DC offset to ensure zero-level silence
    audio = audio - np.mean(audio)
    return float(np.sqrt(np.mean(np.square(audio))))

def voice_available():
    """
    Checks for a quick burst of sound. 
    Reduced duration to 0.3s for faster 'interruption' feel.
    """
    DURATION = 0.3 
    THRESHOLD = 0.0035
    
    samples = int(DURATION * RATE)
    audio = sd.rec(samples, samplerate=RATE, channels=CHANNELS, dtype=DTYPE)
    sd.wait()
    
    return rms_energy(audio) > THRESHOLD

def record_until_silence():
    """
    Continuous stream recording. 
    Starts saving data immediately when speech is detected 
    and stops after a period of silence.
    """
    THRESHOLD = 0.004
    SILENCE_LIMIT = 1.5  # Slightly shorter for snappier conversation
    MAX_SECONDS = 20
    BLOCK_SIZE = 1024 

    frames = []
    speech_started = False
    silence_start_time = None
    start_time = time.time()

    print("🎤 Listening... (Speak now)")

    try:
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=DTYPE) as stream:
            while True:
                # Read chunk from buffer
                data, overflow = stream.read(BLOCK_SIZE)
                volume = rms_energy(data)
                now = time.time()

                # If we hear sound, start/continue recording
                if volume > THRESHOLD:
                    if not speech_started:
                        print("-> Recording started...")
                    speech_started = True
                    silence_start_time = None
                    frames.append(data.copy())
                
                # If it's quiet
                else:
                    if speech_started:
                        frames.append(data.copy()) # Keep some 'tail' silence
                        if silence_start_time is None:
                            silence_start_time = now
                        
                        # Stop if silence exceeds limit
                        if now - silence_start_time > SILENCE_LIMIT:
                            print("-> Finished (Silence detected).")
                            break
                    else:
                        # Optional: Keep a small rolling buffer of pre-speech audio 
                        # so the start of words isn't cut off.
                        pass

                # Global timeout
                if now - start_time > MAX_SECONDS:
                    print("-> Finished (Max time reached).")
                    break
                    
    except Exception as e:
        print(f"🎤 Mic error: {e}")
        return None

    if not frames:
        return np.array([], dtype=DTYPE)
        
    return np.concatenate(frames).flatten()