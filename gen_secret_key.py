import secrets

secret_key = secrets.token_hex(16)  # Generate a 32-character (16 bytes) hex secret key
print(secret_key)
