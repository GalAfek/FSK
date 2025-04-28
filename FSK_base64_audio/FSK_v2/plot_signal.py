# plot_signal.py
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
import wave

def decode_wav_from_base64(audio_base64: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Decode a Base64-encoded WAV file into a PCM waveform and its corresponding time vector.
    
    Parameters:
        audio_base64: Base64-encoded string representing the WAV audio.
        
    Returns:
        waveform: NumPy array of floats (normalized to roughly [-1, 1]).
        t: NumPy array representing the time (seconds) for each sample.
    """
    # Decode the Base64 string into WAV bytes.
    wav_bytes = base64.b64decode(audio_base64)
    with io.BytesIO(wav_bytes) as buffer:
        with wave.open(buffer, 'rb') as wav_file:
            sr = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            frames = wav_file.readframes(n_frames)
    # Convert the PCM bytes into a normalized float array (assuming 16-bit PCM).
    waveform = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32767.0
    t = np.arange(len(waveform)) / sr
    return waveform, t

def plot_modulated_signal(audio_base64: str, title: str = "Modulated Signal", show_plot: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """
    Decode a Base64-encoded WAV file and plot its waveform.
    
    This function is intended to help you verify that the modulation works correctly by providing
    a visual plot of the output signal.
    
    Parameters:
        audio_base64: Base64-encoded string representing the modulated WAV audio.
        title: Title for the plot (e.g., "FSK Modulated Signal" or "CPFSK Modulated Signal").
        show_plot: If True, the plot is displayed immediately (set to False if you just want to get the data).
        
    Returns:
        A tuple (waveform, t) where:
            waveform: NDArray of floats (the audio signal).
            t: NDArray of times corresponding to samples in the signal.
    
    Usage Example:
        waveform, t = plot_modulated_signal(my_audio_base64, "FSK Modulated Signal")
    """
    waveform, t = decode_wav_from_base64(audio_base64)
    
    plt.figure(figsize=(10, 4))
    plt.plot(t, waveform, label="Signal")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    
    if show_plot:
        plt.show()
    
    return waveform, t

# Optional: If you run this file directly, the following block can be used for quick testing.
if __name__ == "__main__":
    # Sample usage for testing:
    # (You can generate a sample Base64 audio string via your modulator functions and paste it here.)
    sample_audio_base64 = ""  # e.g., set this to a string returned by byte_array_to_fsk or byte_array_to_cpfsk
    if sample_audio_base64:
        plot_modulated_signal(sample_audio_base64, "Test Modulated Signal")
    else:
        print("No sample Base64 audio provided. Please set 'sample_audio_base64' for testing.")
