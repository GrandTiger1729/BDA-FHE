from concrete import fhe
import numpy as np

from constants import *
from utils import generate_random_string, encode_string_to_array

class Service:
    """
    Service class to manage queries for users to check if they are in a blacklist.
    This class provides methods to update the blacklist and check if a user ID is in the blacklist.
    """
    
    def __init__(self, server: fhe.Server, encrypted_and_encoded_captcha: fhe.Value, captcha_length: int = CAPTCHA_LENGTH):
        self.server = server
        self._captcha_length = captcha_length
        
        # To simplify the example, we assume the service only needs to handle one user at a time.
        self.encrypted_and_encoded_captcha = encrypted_and_encoded_captcha

    @property
    def captcha_length(self) -> int:
        """
        Returns the length of the captcha string.
        This is used to determine how many characters the captcha will have.
        """
        return self._captcha_length

    # def request_client(self) -> fhe.Client:
    #     """
    #     Requests the client to perform operations on the encrypted blacklist.
    #     Returns a Client object that can be used to interact with the server.
    #     """
    #     serialized_client_specs: bytes = self.server.client_specs.serialize()
    #     client_specs = fhe.ClientSpecs.deserialize(serialized_client_specs)
    #     client = fhe.Client(client_specs)
    #     return client

    def _captcha_match(self, encrypted_and_encoded_user_input: np.ndarray, evaluation_keys: fhe.EvaluationKeys) -> fhe.Value:
        """
        Matches the encrypted and encoded user input against the generated captcha string.
        """
        assert self.encrypted_and_encoded_captcha is not None, "Captcha string must be generated before matching."

        return self.server.run(encrypted_and_encoded_user_input, self.encrypted_and_encoded_captcha, evaluation_keys=evaluation_keys)

    def verify_captcha(self, serialized_encrypted_and_encoded_user_input: bytes, serialized_evaluation_keys: bytes) -> bytes:
        """
        Verifies the user input against the generated captcha.
        """
        assert self.encrypted_and_encoded_captcha is not None, "Captcha string must be generated before matching."

        deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(serialized_evaluation_keys)
        deserialized_encrypted_and_encoded_user_input = fhe.Value.deserialize(serialized_encrypted_and_encoded_user_input)

        result: fhe.Value = self._captcha_match(deserialized_encrypted_and_encoded_user_input, deserialized_evaluation_keys)
        serialized_result: bytes = result.serialize()
        return serialized_result