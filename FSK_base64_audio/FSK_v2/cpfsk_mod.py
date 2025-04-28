import numpy as np
from numpy.typing import NDArray
import io
import wave
import base64

#region CPFSK Modulation Function
def cpfsk_modulation(
    bit_sequence: NDArray[np.int_],
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> tuple[NDArray[np.float_], NDArray[np.float_]]:
    """
    Perform Continuous Phase Frequency Shift Keying (CPFSK) modulation on a given bit sequence.
    
    Parameters:
        bit_sequence: NDArray of bits (0s and 1s) representing the digital data.
        freq0: The carrier frequency (in Hz) representing a binary 0.
        freq1: The carrier frequency (in Hz) representing a binary 1.
        sampling_rate: Number of samples per second (Hz) used in the modulation.
        baud_rate: Number of symbols per second (baud rate).
        
    Returns:
        signal: The CPFSK modulated signal as an NDArray of floats.
        t: Corresponding time axis for the signal as an NDArray of floats.
    """
    # Calculate the number of samples per transmitted bit
    samples_per_bit: int = int(sampling_rate / baud_rate)
    
    # Map each bit to its corresponding frequency: bits=0 -> freq0, bits=1 -> freq1.
    mapped_freqs: NDArray[np.float_] = np.where(bit_sequence == 0, freq0, freq1)
    
    # Create a frequency sequence where each frequency is repeated for one bit duration
    symbol_freqs: NDArray[np.float_] = np.repeat(mapped_freqs, samples_per_bit)
    
    # Generate time array corresponding to the total signal duration
    total_samples: int = symbol_freqs.size
    t: NDArray[np.float_] = np.arange(total_samples) / sampling_rate
    
    # Compute phase increment per sample and integrate for continuous phase
    delta_phi: NDArray[np.float_] = symbol_freqs * (2 * np.pi) / sampling_rate
    phi: NDArray[np.float_] = np.cumsum(delta_phi)
    
    # Generate the CPFSK modulated signal
    signal: NDArray[np.float_] = np.sin(phi)
    
    return signal, t
#endregion

#region CPFSK Modulation To Base64 Audio Wrapper
def cpfsk_modulation_to_base64(
    bit_sequence: NDArray[np.int_],
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> str:
    """
    Perform CPFSK modulation on the input bit sequence and convert the resulting audio signal
    to a base64-encoded WAV file.
    
    Parameters:
        bit_sequence: NDArray of bits (0s and 1s) representing the digital data.
        freq0: Carrier frequency for bit 0.
        freq1: Carrier frequency for bit 1.
        sampling_rate: Number of audio samples per second.
        baud_rate: Symbol rate (symbols per second).
        
    Returns:
        A base64 encoded string representing the WAV audio file.
    """
    # Generate the modulated signal and its time axis using CPFSK modulation
    signal, _ = cpfsk_modulation(bit_sequence, freq0, freq1, sampling_rate, baud_rate)
    
    # Convert the floating-point signal (assumed in range [-1, 1]) to 16-bit PCM format
    pcm_signal = (signal * 32767).astype(np.int16)
    
    # Write the PCM audio data to an in-memory WAV file
    with io.BytesIO() as buffer:
        with wave.open(buffer, 'wb') as wav_file:
            channels = 1          # Mono audio
            sampwidth = 2         # 16-bit PCM (2 bytes per sample)
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(int(sampling_rate))
            wav_file.writeframes(pcm_signal.tobytes())
        wav_bytes = buffer.getvalue()
    
    # Encode the WAV bytes as a base64 encoded string
    audio_base64 = base64.b64encode(wav_bytes).decode('ascii')
    return audio_base64
#endregion
