from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """비밀번호를 해싱해서 반환한다."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """입력한 비밀번호와 저장된 해시값을 비교한다."""
    return password_hash.verify(
        plain_password,
        hashed_password
    )