from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    ph = PasswordHasher()
    return ph.verify(hashed_password, plain_password)
