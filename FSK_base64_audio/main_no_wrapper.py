# main.py
import numpy as np
from FSK_v2 import fsk_modulation_to_base64, cpfsk_modulation_to_base64, fsk_demodulation_from_base64

#region Define modulation parameters
sampling_rate: float = 44100.0  # Samples per second (Hz)
baud_rate: float = 300.0         # Symbols per second (baud rate)
freq0: float = 1200.0            # Carrier frequency representing bit 0
freq1: float = 2200.0            # Carrier frequency representing bit 1
#endregion

#region Convert input byte array to bit sequence
# Our input data as a byte array
received_data: bytes = b"Hello FSK!"
# Unpack the bits: each byte becomes 8 bits, yielding an array of 0s and 1s.
bit_sequence = np.unpackbits(np.frombuffer(received_data, dtype=np.uint8))
#endregion

#region Modulation to Base64 Audio
# Perform FSK modulation, returning a Base64-encoded WAV file.
audio_base64_fsk = fsk_modulation_to_base64(bit_sequence, freq0, freq1, sampling_rate, baud_rate)

# Perform CPFSK modulation, returning a Base64-encoded WAV file.
audio_base64_cpfsk = cpfsk_modulation_to_base64(bit_sequence, freq0, freq1, sampling_rate, baud_rate)
#endregion

#region Demodulation from Base64 Audio
# Demodulate the FSK Base64 audio to recover the transmitted byte data.
recovered_bytes_fsk = fsk_demodulation_from_base64(audio_base64_fsk, sampling_rate, baud_rate, freq0, freq1)

# Demodulate the CPFSK Base64 audio to recover the transmitted byte data.
recovered_bytes_cpfsk = fsk_demodulation_from_base64(audio_base64_cpfsk, sampling_rate, baud_rate, freq0, freq1)
#endregion

#region Output and Comparison
print("Original message:         ", received_data)
print("FSK Recovered message:    ", recovered_bytes_fsk)
print("CPFSK Recovered message:  ", recovered_bytes_cpfsk)

if recovered_bytes_fsk == received_data:
    print("FSK recovered data matches the original.")
else:
    print("FSK recovered data DOES NOT match the original.")

if recovered_bytes_cpfsk == received_data:
    print("CPFSK recovered data matches the original.")
else:
    print("CPFSK recovered data DOES NOT match the original.")
#endregion
