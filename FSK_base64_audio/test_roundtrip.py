# test_roundtrip.py
from FSK_v2 import byte_array_to_fsk, fsk_to_byte_array, byte_array_to_cpfsk, cpfsk_to_byte_array

def test_fsk_roundtrip():
    # Original data
    data = b"Hello FSK!"
    
    # Define modulation parameters
    sampling_rate = 44100.0
    baud_rate = 300.0
    freq0 = 1200.0
    freq1 = 2200.0
    
    # Modulate the data into Base64 FSK audio
    audio = byte_array_to_fsk(data, freq0, freq1, sampling_rate, baud_rate)
    # Demodulate the Base64 audio back into a byte array
    recovered = fsk_to_byte_array(audio, freq0, freq1, sampling_rate, baud_rate)
    
    # The recovered data should match the original data exactly.
    assert recovered == data
    
def test_cpfsk_roundtrip():
    # Original data
    data = b"Hello FSK!"
    
    # Define modulation parameters
    sampling_rate = 44100.0
    baud_rate = 300.0
    freq0 = 1200.0
    freq1 = 2200.0
    
    # Modulate the data into Base64 CPFSK audio
    audio = byte_array_to_cpfsk(data, freq0, freq1, sampling_rate, baud_rate)
    # Demodulate the Base64 audio back into a byte array
    recovered = cpfsk_to_byte_array(audio, freq0, freq1, sampling_rate, baud_rate)
    
    # The recovered data should match the original data.
    assert recovered == data

if __name__ == "__main__":
    # If you run this file directly, the assertions should pass without errors.
    test_fsk_roundtrip()
    test_cpfsk_roundtrip()
    print("Both FSK and CPFSK round-trip tests passed!")
