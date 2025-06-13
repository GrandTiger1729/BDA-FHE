from concrete import fhe
import numpy as np

from constants import *
from utils import generate_random_string, encode_string_to_array


def _captcha_match_impl(encoded_user_input: np.ndarray, encoded_captcha: np.ndarray) -> bool:
    """
    Implementation of the function to check if a user input matches the captcha.
    Returns True if the user input matches the captcha, otherwise False.
    """
    not_matches = np.sum(encoded_user_input != encoded_captcha)
    return not_matches == 0

compiler = fhe.Compiler(
    _captcha_match_impl, {"encoded_user_input": "encrypted", "encoded_captcha": "encrypted"}
)
input_set = [
    (encode_string_to_array(
        generate_random_string(CAPTCHA_LENGTH), CAPTCHA_LENGTH
    ), encode_string_to_array(
        generate_random_string(CAPTCHA_LENGTH), CAPTCHA_LENGTH
    )) for _ in range(10)
]

circuit: fhe.Circuit = compiler.compile(input_set)
circuit.keygen()

captcha_string = generate_random_string(CAPTCHA_LENGTH)
encoded_captcha = encode_string_to_array(captcha_string, CAPTCHA_LENGTH)

print(circuit.encrypt_run_decrypt(*input_set[0]))
print(_captcha_match_impl(encoded_captcha, encoded_captcha))