from concrete import fhe
import numpy as np

from constants import *
from utils import generate_random_string, encode_string_to_array
from service import Service


def _captcha_match_impl(encoded_user_input: np.ndarray, encoded_captcha: np.ndarray) -> bool:
    """
    Implementation of the function to check if a user input matches the captcha.
    Returns True if the user input matches the captcha, otherwise False.
    """
    # matches = fhe.zero()
    # for i in range(CAPTCHA_LENGTH):
    #     matches += (encoded_user_input[i] == encoded_captcha[i])
    # return matches == CAPTCHA_LENGTH
    
    not_matches = np.sum(encoded_user_input != encoded_captcha)
    return not_matches == 0

class Server:

    def __init__(self, captcha_length: int = CAPTCHA_LENGTH):
        """
        Initializes the server with a given captcha length.
        The captcha length determines the length of the generated captcha strings.
        """
        self.captcha_length = captcha_length

        compiler = fhe.Compiler(
            _captcha_match_impl, {"encoded_user_input": "encrypted", "encoded_captcha": "encrypted"}
        )
        input_set = [
            (encode_string_to_array(
                generate_random_string(captcha_length), captcha_length
            ), encode_string_to_array(
                generate_random_string(captcha_length), captcha_length
            )) for _ in range(10)
        ]
        self.circuit: fhe.Circuit = compiler.compile(input_set)
        self.circuit.keygen()
        
        self.generate_captcha()
        encoded_captcha = encode_string_to_array(self.captcha_string, captcha_length)
        _, circuit_encrypted_and_encoded_captcha = self.circuit.encrypt(encoded_captcha, encoded_captcha)
        self.service = Service(self.circuit.server, circuit_encrypted_and_encoded_captcha, self.captcha_length)

    def generate_captcha(self) -> str:
        """
        Generates a random captcha string of the specified length.
        Returns the generated captcha string.
        """
        self.captcha_string = generate_random_string(self.captcha_length)
        return self.captcha_string
    
    def regenerate_captcha(self) -> str:
        """
        Regenerates the captcha string and updates the service with the new captcha.
        Returns the new captcha string.
        """
        self.generate_captcha()
        encoded_captcha = encode_string_to_array(self.captcha_string, self.captcha_length)
        _, encrypted_and_encoded_captcha = self.circuit.encrypt(encoded_captcha, encoded_captcha)
        self.service.encrypted_and_encoded_captcha = encrypted_and_encoded_captcha
        return self.captcha_string