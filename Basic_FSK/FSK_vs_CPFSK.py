# fsk_vs_cpfsk_demod.py
import numpy as np
import matplotlib.pyplot as plt
from FSK import fsk_demodulation, fsk_modulation, cpfsk_modulation

#region Define modulation and simulation parameters
# -----------------------
sampling_rate: float = 44100.0  # Typical audio sampling rate (Hz)
baud_rate: float = 300.0         # Symbols per second
freq0: float = 1200.0            # Carrier frequency for bit 0
freq1: float = 2200.0            # Carrier frequency for bit 1
#endregion

#region Simulate the received data (byte array) and convert to bits
# For demonstration, we use a predefined byte array.
received_data: bytes = b"Hello FSK!"

# Convert the received byte array into a bit sequence:
bit_sequence: np.ndarray = np.unpackbits(
    np.frombuffer(received_data, dtype=np.uint8)
)
# print("Original bit sequence:", bit_sequence)
#endregion

#region Perform modulation using FSK and CPFSK methods
# Standard FSK modulation (phase discontinuities)
fsk_signal, t_fsk = fsk_modulation(bit_sequence, freq0, freq1, sampling_rate, baud_rate)
# Continuous Phase FSK (CPFSK) modulation (continuous phase)
cpfsk_signal, t_cpfsk = cpfsk_modulation(bit_sequence, freq0, freq1, sampling_rate, baud_rate)
#endregion

#region Perform demodulation of the modulated signals
# Demodulate the FSK modulated signal
demodulated_bits_fsk = fsk_demodulation(fsk_signal, sampling_rate, baud_rate, freq0, freq1)
recovered_bytes_fsk = np.packbits(demodulated_bits_fsk)

# Demodulate the CPFSK modulated signal
demodulated_bits_cpfsk = fsk_demodulation(cpfsk_signal, sampling_rate, baud_rate, freq0, freq1)
recovered_bytes_cpfsk = np.packbits(demodulated_bits_cpfsk)
#endregion

#region Compare recovered messages to the received message
# Convert recovered bytes to byte arrays (messages)
recovered_message_fsk = recovered_bytes_fsk.tobytes()
recovered_message_cpfsk = recovered_bytes_cpfsk.tobytes()
# Print the recovered messages
print("Recovered message from FSK:  ", recovered_message_fsk)
print("Recovered message from CPFSK:", recovered_message_cpfsk)
#endregion

#region Compare the recovered messages to the original received data
if recovered_message_fsk == received_data:
    print("FSK recovered data matches the received data!")
else:
    print("FSK recovered data does NOT match the received data!")

if recovered_message_cpfsk == received_data:
    print("CPFSK recovered data matches the received data!")
else:
    print("CPFSK recovered data does NOT match the received data!")
#endregion

#region Plotting (optional)
plt.figure(figsize=(12, 6))
# Vertically offset the signals for clarity
plt.plot(t_fsk, fsk_signal + 1.0, label="FSK Signal", alpha=0.8)
plt.plot(t_cpfsk, cpfsk_signal - 1.0, label="CPFSK Signal", alpha=0.8)
plt.title("Modulated Signals and Their Demodulation")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()
#endregion
