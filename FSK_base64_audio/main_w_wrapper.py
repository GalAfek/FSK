# main.py
from FSK_v2 import (
    byte_array_to_fsk,
    fsk_to_byte_array,
    byte_array_to_cpfsk,
    cpfsk_to_byte_array,
)

#region Define Parameters
sampling_rate = 44100.0  # Samples per second (Hz)
baud_rate = 300.0        # Symbols per second (baud rate)
freq0 = 1200.0           # Carrier frequency for bit 0
freq1 = 2200.0           # Carrier frequency for bit 1
#endregion

def main():
    # Original data to be modulated
    data = b"Hello FSK!"
    print("Original Data:", data)
    
    # ----- FSK Modulation & Demodulation -----
    print("\n--- FSK Round-Trip ---")
    # Convert the byte array to a Base64-encoded FSK modulated audio string
    encoded_audio_fsk = byte_array_to_fsk(data, freq0, freq1, sampling_rate, baud_rate)
    # Print a truncated preview of the Base64 string for sanity checks
    print("Encoded FSK Audio (Base64, truncated):", encoded_audio_fsk[:100] + "...")
    
    # Convert the Base64 audio back into a byte array via FSK demodulation
    recovered_fsk = fsk_to_byte_array(encoded_audio_fsk, freq0, freq1, sampling_rate, baud_rate)
    print("Recovered FSK Data:", recovered_fsk)
    
    if recovered_fsk == data:
        print("✅ FSK round-trip successful!")
    else:
        print("❌ FSK round-trip error!")
    
    # ----- CPFSK Modulation & Demodulation -----
    print("\n--- CPFSK Round-Trip ---")
    # Convert the byte array to a Base64-encoded CPFSK modulated audio string
    encoded_audio_cpfsk = byte_array_to_cpfsk(data, freq0, freq1, sampling_rate, baud_rate)
    print("Encoded CPFSK Audio (Base64, truncated):", encoded_audio_cpfsk[:100] + "...")
    
    # Convert the Base64 audio back into a byte array via CPFSK demodulation
    recovered_cpfsk = cpfsk_to_byte_array(encoded_audio_cpfsk, freq0, freq1, sampling_rate, baud_rate)
    print("Recovered CPFSK Data:", recovered_cpfsk)
    
    if recovered_cpfsk == data:
        print("✅ CPFSK round-trip successful!")
    else:
        print("❌ CPFSK round-trip error!")

if __name__ == "__main__":
    main()
