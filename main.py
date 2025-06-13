from concrete import fhe

from server import Server
from service import Service
from client import Client

if __name__ == "__main__":
    # Initialize the server with a default captcha length
    server = Server()
    service = server.service
    client = Client(service, server.circuit.client)
    
    print("Answer: ", server.captcha_string)

    # Client verifies the captcha
    user_input = input("Please enter the captcha: ")
    is_verified = client.verify(user_input)
    if is_verified:
        print("Captcha verification successful!")
    else:
        print("Captcha verification failed.")