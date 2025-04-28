# fsk_demod.py
import numpy as np
from numpy.typing import NDArray

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
