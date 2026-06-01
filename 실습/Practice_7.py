"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_membership(membership)` 함수를 작성하세요.**

- `"유효"` 이면 `"[회원권확인] 입장 가능합니다"` 출력 후 `True` 반환
- 그 외이면 `"[회원권확인] 유효한 회원권이 없습니다"` 출력 후 `False` 반환

**② `check_locker(locker)` 함수를 작성하세요.**

- 락커 번호는 **1번 이상 50번 이하**만 유효합니다.
- 유효하면 `"[락커확인] 사용 가능한 락커 번호입니다"` 출력 후 `True` 반환
- 유효하지 않으면 `"[락커확인] 락커 번호는 1번에서 50번 사이여야 합니다"` 출력 후 `False` 반환

**③ main 코드를 작성하세요.**

- 회원권 상태와 락커 번호를 각각 `input()` 으로 입력받습니다.
- **두 미들웨어가 모두 `True` 일 때만** 이름을 입력받고 `enter_gym()` 이 실행됩니다.
- ※ 락커 번호는 `int()` 로 변환하여 사용하세요.
"""

def enter_gym(name, locker):
    print(f"💪{name}님,{locker}번 락커를 사용하세요. 입장을 환영합니다!")


# ↓ 여기서부터 작성하세요
"""회원권 상태를 입력하세요 (유효/만료): 유효
락커 번호를 입력하세요: 23
[회원권확인] 입장 가능합니다
[락커확인] 사용 가능한 락커 번호입니다
이름을 입력하세요: 홍길동
💪 홍길동님, 23번 락커를 사용하세요. 입장을 환영합니다!"""


def check_membership(membership):
    if membership == "유효":
        print("[회원권 확인] 입장 가능합니다")
        print()
        return True
    else:
        print("[회원권 확인] 유효한 회원권이 없습니다")
        print()
        return False

def check_locker(locker):
    if 1 <= locker <= 50:
        print("[락커 확인] 사용 가능한 락커 번호입니다")
        print()
        return True
    else:
        print("[락커 확인] 락커 번호는 1번에서 50번 사이여야 합니다")
        print()
        return False

if __name__ == "__main__":
    membership = input("회원권 상태를 입력하세요 (유효/만료): ")
    if check_membership(membership):
        locker = int(input("락커 번호를 입력하세요 : "))
        if check_locker(locker):
            name = input("이름을 입력하세요 : ")
            print()
            enter_gym(name, locker)
