import numpy as np
from numpy.typing import NDArray
import base64
import io
import wave

#region Core FSK Demodulation Function
def fsk_demodulation(
    modulated_signal: NDArray[np.float_],
    sampling_rate: float,
    baud_rate: float,
    freq0: float,
    freq1: float
) -> NDArray[np.uint8]:
    """
    Demodulate an FSK (or CPFSK) modulated signal and recover the transmitted bit sequence.
    
    Parameters:
        modulated_signal: NDArray of floats representing the received signal.
        sampling_rate: Number of samples per second (Hz) used in modulation.
        baud_rate: Symbol rate (symbols per second).
        freq0: Carrier frequency representing bit 0.
        freq1: Carrier frequency representing bit 1.
        
    Returns:
        bits: NDArray of type uint8 representing the recovered bit sequence.
    """
    # Calculate number of samples per symbol
    samples_per_bit = int(sampling_rate / baud_rate)
    num_symbols = len(modulated_signal) // samples_per_bit
    bits = np.empty(num_symbols, dtype=np.uint8)
    
    # Time vector for one symbol duration
    t_symbol = np.arange(samples_per_bit) / sampling_rate

    for i in range(num_symbols):
        # Extract the current symbol from the signal
        chunk = modulated_signal[i * samples_per_bit : (i + 1) * samples_per_bit]
        
        # Compute the correlation using quadrature demodulation for freq0.
        I0 = np.dot(chunk, np.cos(2 * np.pi * freq0 * t_symbol))
        Q0 = np.dot(chunk, np.sin(2 * np.pi * freq0 * t_symbol))
        mag0 = np.sqrt(I0**2 + Q0**2)
        
        # Compute the correlation for freq1.
        I1 = np.dot(chunk, np.cos(2 * np.pi * freq1 * t_symbol))
        Q1 = np.dot(chunk, np.sin(2 * np.pi * freq1 * t_symbol))
        mag1 = np.sqrt(I1**2 + Q1**2)
        
        # Decide the bit based on which frequency has higher correlation.
        bits[i] = 0 if mag0 > mag1 else 1
        
    return bits
#endregion

#region Base64 Audio Demodulation Wrapper
def fsk_demodulation_from_base64(
    audio_base64: str,
    sampling_rate: float,
    baud_rate: float,
    freq0: float,
    freq1: float
) -> bytes:
    """
    Demodulate an FSK (or CPFSK) modulated audio provided as a base64-encoded WAV file and recover the transmitted data.
    
    Parameters:
        audio_base64: Base64-encoded string representing a WAV audio file.
        sampling_rate: Number of samples per second (Hz) used during modulation.
        baud_rate: Symbol rate (symbols per second).
        freq0: Carrier frequency representing bit 0.
        freq1: Carrier frequency representing bit 1.
        
    Returns:
        recovered_bytes: A byte array (as bytes) containing the recovered data.
    """
    # Decode the base64 string into WAV file bytes
    wav_data = base64.b64decode(audio_base64)
    
    # Open the WAV file from an in-memory bytes buffer
    with io.BytesIO(wav_data) as buffer:
        with wave.open(buffer, 'rb') as wav_file:
            # Retrieve audio parameters (assumes mono and 16-bit PCM)
            n_channels = wav_file.getnchannels()
            sampwidth = wav_file.getsampwidth()  # Expected to be 2 (16-bit)
            framerate = wav_file.getframerate()  # Should match sampling_rate
            n_frames = wav_file.getnframes()
            audio_frames = wav_file.readframes(n_frames)
    
    # Convert the frames to a NumPy array (using int16 for 16-bit PCM)
    audio_int16 = np.frombuffer(audio_frames, dtype=np.int16)
    
    # Normalize the signal to floating-point, assuming range [-1, 1]
    modulated_signal = audio_int16.astype(np.float32) / 32767.0
    
    # Use the core demodulation function to recover the bit sequence
    bits = fsk_demodulation(modulated_signal, sampling_rate, baud_rate, freq0, freq1)
    
    # Pack the recovered bits into a byte array and return as bytes
    recovered_bytes = np.packbits(bits)
    return recovered_bytes.tobytes()
#endregion
