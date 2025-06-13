from concrete import fhe
import numpy as np

from constants import *
from utils import encode_string_to_array
from service import Service

class Client:
    """
    The Client class is responsible for interacting with the server to check if a user ID is in the blacklist.
    """

    def __init__(self, service: Service, client: fhe.Client):
        """
        Initializes the Client with a reference to the service.
        """
        self.service = service
        self.client = client
        # self.client: fhe.Client = self.service.request_client()
        
    def _generate_serialized_evaluation_keys(self) -> bytes:
        """
        Generates evaluation keys for the client.
        Returns the serialized evaluation keys.
        """
        self.client.keys.generate()
        serialized_evaluation_keys: bytes = self.client.evaluation_keys.serialize()
        return serialized_evaluation_keys

    def verify(self, user_input: str) -> bool:
        """
        Verifies the user input against the generated captcha.
        Returns True if the user input matches the captcha, otherwise False.
        """
        serialized_evaluation_keys: bytes = self._generate_serialized_evaluation_keys()
        encoded_user_input = encode_string_to_array(user_input, self.service.captcha_length)
        args: tuple[fhe.Value] = self.client.encrypt(encoded_user_input, encoded_user_input)
        encrypted_and_encoded_user_input, _ = args
        serialized_encrypted_and_encoded_user_input: bytes = encrypted_and_encoded_user_input.serialize()

        serialized_result: bytes = self.service.verify_captcha(serialized_encrypted_and_encoded_user_input, serialized_evaluation_keys)
        deserialized_result = fhe.Value.deserialize(serialized_result)

        decrypted_result = self.client.decrypt(deserialized_result)
        return bool(decrypted_result)