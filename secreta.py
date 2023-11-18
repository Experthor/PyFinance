import secrets

# Genera una clave secreta segura de 32 bytes
clave_secreta = secrets.token_hex(32)

print(clave_secreta)