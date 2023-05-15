import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryption:

    iterations = 100000

    def _derive_key(self, password: bytes, salt: bytes, iterations: int = iterations) -> bytes:

        backend = default_backend()

        """Derive a secret key from a given password and salt"""

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=iterations, backend=backend)

        return b64e(kdf.derive(password))

    def password_encrypt(self, message: bytes, password: str, iterations: int = iterations) -> bytes:

        salt = secrets.token_bytes(16)
        key = self._derive_key(password.encode(), salt, iterations)

        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )

    def password_decrypt(self, token: bytes, password: str) -> bytes:

        decoded = b64d(token)
        salt, iterazione, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iterazione, 'big')

        key = self._derive_key(password.encode(), salt, iterations)

        return Fernet(key).decrypt(token)
