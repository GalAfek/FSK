# wrapper.py
import numpy as np
from .fsk_mod import fsk_modulation_to_base64
from .cpfsk_mod import cpfsk_modulation_to_base64
from .fsk_demod import fsk_demodulation_from_base64

#region FSK Wrappers
def byte_array_to_fsk(
    data: bytes,
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> str:
    """
    Convert a byte array into a Base64-encoded FSK modulated WAV audio.
    
    Parameters:
        data: Input byte array.
        freq0: Carrier frequency for binary 0.
        freq1: Carrier frequency for binary 1.
        sampling_rate: Sampling rate in Hz.
        baud_rate: Symbol rate (symbols per second).
        
    Returns:
        A Base64 encoded WAV audio string representing the FSK modulated signal.
    """
    # Convert the byte array into a bit sequence.
    bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    return fsk_modulation_to_base64(bits, freq0, freq1, sampling_rate, baud_rate)

def fsk_to_byte_array(
    audio_base64: str,
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> bytes:
    """
    Convert a Base64-encoded FSK modulated WAV audio back to its original byte array.
    
    Parameters:
        audio_base64: Base64 encoded WAV audio.
        freq0: Carrier frequency for binary 0.
        freq1: Carrier frequency for binary 1.
        sampling_rate: Sampling rate in Hz.
        baud_rate: Symbol rate (symbols per second).
        
    Returns:
        The recovered byte array.
    """
    return fsk_demodulation_from_base64(audio_base64, sampling_rate, baud_rate, freq0, freq1)
#endregion

#region CPFSK Wrappers
def byte_array_to_cpfsk(
    data: bytes,
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> str:
    """
    Convert a byte array into a Base64-encoded CPFSK modulated WAV audio.
    
    Parameters:
        data: Input byte array.
        freq0: Carrier frequency for binary 0.
        freq1: Carrier frequency for binary 1.
        sampling_rate: Sampling rate in Hz.
        baud_rate: Symbol rate (symbols per second).
        
    Returns:
        A Base64 encoded WAV audio string representing the CPFSK modulated signal.
    """
    # Convert the byte array into a bit sequence.
    bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    return cpfsk_modulation_to_base64(bits, freq0, freq1, sampling_rate, baud_rate)

def cpfsk_to_byte_array(
    audio_base64: str,
    freq0: float,
    freq1: float,
    sampling_rate: float,
    baud_rate: float
) -> bytes:
    """
    Convert a Base64-encoded CPFSK modulated WAV audio back to its original byte array.
    
    Parameters:
        audio_base64: Base64 encoded WAV audio.
        freq0: Carrier frequency for binary 0.
        freq1: Carrier frequency for binary 1.
        sampling_rate: Sampling rate in Hz.
        baud_rate: Symbol rate (symbols per second).
        
    Returns:
        The recovered byte array.
    """
    # In this implementation we use the same demodulation function since the receiver treats both modulations similarly.
    return fsk_demodulation_from_base64(audio_base64, sampling_rate, baud_rate, freq0, freq1)
#endregion
