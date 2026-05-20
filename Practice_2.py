"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_age(age)` 함수를 작성하세요.**

- 나이(`age`)를 정수로 입력받습니다.
- **15세 이상**이면 `"[나이확인] 관람 가능합니다"` 를 출력하고 `True` 를 반환합니다.
- 15세 미만이면 `"[나이확인] 15세 미만은 관람 불가합니다"` 를 출력하고 `False` 를 반환합니다.

**② main 코드를 작성하세요.**

- 나이를 `input()` 으로 입력받습니다. ※ `int()` 로 변환하여 사용하세요.
- 미들웨어(`check_age`)의 결과가 `True` 일 때만 영화 제목을 입력받고 `book_movie()` 가 실행됩니다.
"""

def book_movie(title):
    print(f"🎬{title} 예매가 완료되었습니다!")


# ↓ 여기서부터 작성하세요

def check_age(age):
    if age >= 15:
        print("[나이 확인] 관람 가능합니다.")
        return True
    else:
        print("[나이 확인] 15세 미만은 관람 불가합니다.")
        return False

if __name__ == "__main__":
    age = int(input("나이를 확인합니다 : "))
    check = check_age(age)
    if check:
        title = input("관람하실 영화 제목을 입력해주세요 : ")
        book_movie(title)