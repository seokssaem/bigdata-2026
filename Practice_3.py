"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_membership(membership)` 함수를 작성하세요.**

- 회원권 상태(`membership`)를 문자열로 입력받습니다.
- `"유효"` 이면 `"[회원권확인] 입장 가능합니다"` 를 출력하고 `True` 를 반환합니다.
- 그 외이면 `"[회원권확인] 유효한 회원권이 없습니다"` 를 출력하고 `False` 를 반환합니다.

**② main 코드를 작성하세요.**

- 회원권 상태를 `input()` 으로 입력받습니다.
- 미들웨어(`check_membership`)의 결과가 `True` 일 때만 이름을 입력받고 `enter_gym()` 이 실행됩니다.
"""

def enter_gym(name):
    print(f"💪{name}님, 입장을 환영합니다!")


# ↓ 여기서부터 작성하세요

def check_membership(membership):
    if membership == "유효":
        print("[회원권 확인] 입장 가능합니다.")
        return True
    else:
        print("[회원권 확인] 유효한 회원권이 없습니다.")
        return False

if __name__ == "__main__":
    membership = input("회원권 상태를 입력하세요 (유효/만료) : ")
    status = check_membership(membership)
    if status:
        name = input("이름을 입력해주세요 : ")
        enter_gym(name)
