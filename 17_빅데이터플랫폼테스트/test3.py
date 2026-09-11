def validate_password(pw: str) -> str:
    if len(pw) < 8:
        raise ValueError("비밀번호는 8자 이상이어야 합니다")
    return "가입 성공"

for pw in ["abcdefgh", "abcdefg", ""]:
    try:
        print(pw, "→", validate_password(pw))
    except ValueError as e:
        print(pw, "→", e)