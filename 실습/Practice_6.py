"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_age(age)` 함수를 작성하세요.**

- **15세 이상**이면 `"[나이확인] 관람 가능합니다"` 출력 후 `True` 반환
- 15세 미만이면 `"[나이확인] 15세 미만은 관람 불가합니다"` 출력 후 `False` 반환

**② `check_seat(seat)` 함수를 작성하세요.**

- 좌석 번호는 **1번 이상 100번 이하**만 유효합니다.
- 유효하면 `"[좌석확인] 유효한 좌석 번호입니다"` 출력 후 `True` 반환
- 유효하지 않으면 `"[좌석확인] 좌석 번호는 1번에서 100번 사이여야 합니다"` 출력 후 `False` 반환

**③ main 코드를 작성하세요.**

- 나이와 좌석 번호를 각각 `input()` 으로 입력받습니다.
- **두 미들웨어가 모두 `True` 일 때만** 영화 제목을 입력받고 `book_movie()` 가 실행됩니다.
- ※ 나이와 좌석 번호는 `int()` 로 변환하여 사용하세요.
"""

def book_movie(title, seat):
    print(f"🎬{title} {seat}번 좌석 예매가 완료되었습니다!")


# ↓ 여기서부터 작성하세요

def check_age(age):
    if 15 <= age <= 150:
        print("[나이 확인] 영화 관람 가능합니다.")
        print()
        return True
    elif 0 <= age < 15:
        print("[나이 확인] 15세 미만은 관람할 수 없습니다.")
        print()
        return False
    else:
        print("잘못 입력하셨습니다.")
        print()
        return False

def check_seat(seat):
    if 1 <= seat <= 100:
        print("[좌석 확인] 유효한 좌석 번호입니다")
        print()
        return True
    else:
        print("[좌석 확인] 좌석 번호는 1번에서 100번 사이여야 합니다")
        print()
        return False

if __name__ == "__main__":
    age = int(input("나이를 입력하세요 : "))
    if check_age(age):
        seat = int(input("좌석 번호를 입력하세요 : "))
        if check_seat(seat):
            title = input("예매할 영화 제목을 입력하세요 : ")
            print()
            book_movie(title, seat)
