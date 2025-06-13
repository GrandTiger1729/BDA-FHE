import numpy as np
import string

def generate_random_string(length: int) -> str:
    """
    Generates a random string of the specified length using uppercase letters, lowercase letters, and digits.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(np.random.choice(list(characters), size=length))

def encode_string_to_array(s: str, length: int) -> np.ndarray:
    """
    Encodes a string into a fixed-length numpy array of int8.
    Pads with zeros if the string is shorter than the specified length.
    """
    if len(s) > length:
        raise ValueError(f"String length exceeds the specified length of {length}.")
    
    encoded = np.zeros(length, dtype=np.int8)
    for i, char in enumerate(s):
        encoded[i] = ord(char)
    return encoded