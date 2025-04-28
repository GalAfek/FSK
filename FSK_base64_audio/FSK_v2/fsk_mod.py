# fsk_mod.py
import numpy as np
from numpy.typing import NDArray
import io
import wave
import base64

#region Basic FSK Modulation Function
def fsk_modulation(
    bit_sequence: NDArray[np.int_],
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> tuple[NDArray[np.float_], NDArray[np.float_]]:
    """
    Perform Frequency Shift Keying (FSK) modulation on a given bit sequence.
    
    Parameters:
        bit_sequence: An NDArray of bits (0s and 1s) representing your digital data.
        freq0: The carrier frequency (in Hz) to represent a binary 0.
        freq1: The carrier frequency (in Hz) to represent a binary 1.
        sampling_rate: The number of samples per second (Hz) for the modulation.
        baud_rate: The symbol rate in symbols per second.
        
    Returns:
        signal: The FSK modulated signal as an NDArray of floats.
        t: A corresponding time axis for the signal.
    """
    # Calculate the number of samples per transmitted bit
    samples_per_bit: int = int(sampling_rate / baud_rate)
    
    # Map each bit to its corresponding frequency:
    # Bits with value 0 become freq0, and bits with value 1 become freq1.
    mapped_freqs: NDArray[np.float_] = np.where(bit_sequence == 0, freq0, freq1)
    
    # Create a frequency sequence where each bit’s frequency is repeated for its duration
    symbol_freqs: NDArray[np.float_] = np.repeat(mapped_freqs, samples_per_bit)
    
    # Generate time array corresponding to the length of the modulated signal
    total_samples: int = symbol_freqs.size
    t: NDArray[np.float_] = np.arange(total_samples) / sampling_rate
    
    # Generate the FSK signal using sine waves. Note that we use the instantaneous frequency
    # from the symbol_freqs for each sample point.
    signal: NDArray[np.float_] = np.sin(2.0 * np.pi * symbol_freqs * t)
    
    return signal, t
#endregion

#region FSK Modulation to Base64 Audio Wrapper
def fsk_modulation_to_base64(
    bit_sequence: NDArray[np.int_],
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> str:
    """
    Perform FSK modulation on the input bit sequence and convert the resulting audio signal
    into a Base64-encoded WAV file.
    
    Parameters:
        bit_sequence: NDArray of bits (0s and 1s) representing your digital data.
        freq0: Carrier frequency for bit 0.
        freq1: Carrier frequency for bit 1.
        sampling_rate: The number of audio samples per second.
        baud_rate: The symbol rate (symbols per second).
        
    Returns:
        A Base64-encoded string representing the generated WAV audio file.
    """
    # Generate the FSK-modulated signal and corresponding time axis using the basic FSK modulation function
    signal, _ = fsk_modulation(bit_sequence, freq0, freq1, sampling_rate, baud_rate)
    
    # Convert the floating-point signal (assumed in range [-1, 1]) to 16-bit PCM values
    pcm_signal = (signal * 32767).astype(np.int16)
    
    # Write the PCM data to an in-memory WAV file
    with io.BytesIO() as buffer:
        with wave.open(buffer, 'wb') as wav_file:
            channels = 1           # Mono audio
            sampwidth = 2          # 16-bit PCM (2 bytes per sample)
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(int(sampling_rate))
            wav_file.writeframes(pcm_signal.tobytes())
        wav_bytes = buffer.getvalue()
    
    # Encode the WAV file bytes as a Base64 string
    audio_base64 = base64.b64encode(wav_bytes).decode('ascii')
    return audio_base64
#endregion
