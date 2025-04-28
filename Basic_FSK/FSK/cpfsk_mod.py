# cpfsk_mod.py
import numpy as np
from numpy.typing import NDArray

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
    
    How It Works:
      1. Calculate the number of samples per bit based on the sampling rate and baud rate.
      2. Map each bit to its corresponding frequency: 0 becomes freq0 and 1 becomes freq1.
      3. Repeat each frequency for the duration of one symbol, forming the instantaneous frequency vector.
      4. Create a time axis that corresponds to the total number of samples.
      5. Compute the phase increment for each sample using:
             delta_phi = 2π * instantaneous_frequency / sampling_rate.
      6. Integrate these increments with np.cumsum() to ensure continuous phase over the entire signal.
      7. Generate the CPFSK signal by taking the sine of the cumulative phase.
    """
    # Calculate the number of samples per transmitted bit
    samples_per_bit: int = int(sampling_rate / baud_rate)
    
    # Map each bit to its corresponding frequency
    # Bits with value 0 become freq0, and bits with value 1 become freq1.
    mapped_freqs: NDArray[np.float_] = np.where(bit_sequence == 0, freq0, freq1)
    
    # Create a frequency sequence where each bit's mapped frequency is repeated for the entire bit duration
    symbol_freqs: NDArray[np.float_] = np.repeat(mapped_freqs, samples_per_bit)
    
    # Generate time array corresponding to the total signal duration
    total_samples: int = symbol_freqs.size
    t: NDArray[np.float_] = np.arange(total_samples) / sampling_rate
    
    # Compute phase increment for each sample:
    # delta_phi = 2π * frequency / sampling_rate, ensures phase increment per sample.
    delta_phi: NDArray[np.float_] = symbol_freqs * (2 * np.pi) / sampling_rate
    
    # Integrate the phase increments to obtain the instantaneous phase
    phi: NDArray[np.float_] = np.cumsum(delta_phi)
    
    # Generate the CPFSK signal with continuous phase modulation
    signal: NDArray[np.float_] = np.sin(phi)
    
    return signal, t
