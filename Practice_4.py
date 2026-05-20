"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_membership(grade)` 함수를 작성하세요.**

- `"정회원"` 또는 `"우수회원"` 이면 `"[회원확인] 예약 권한 확인 완료"` 출력 후 `True` 반환
- 그 외이면 `"[회원확인] 예약 권한 없음"` 출력 후 `False` 반환

**② `check_seat(seat_number)` 함수를 작성하세요.**

- 좌석 번호가 **1 이상 50 이하** 범위를 벗어나면 `"[좌석확인] 유효하지 않은 좌석 번호입니다"` 출력 후 `False` 반환
- 좌석 번호가 **이미 예약된 좌석**이면 `"[좌석확인] 이미 예약된 좌석입니다"` 출력 후 `False` 반환
- 두 조건을 모두 통과하면 `"[좌석확인] 유효한 좌석 번호입니다"` 출력 후 `True` 반환
- ※ 예약 목록은 전역변수 `reserved_seats` 리스트를 사용하세요.

**③ main 코드를 작성하세요.**

- `while` 루프로 아래 메뉴를 반복 실행합니다.
    - `1` 입력 시: 회원 등급과 좌석 번호를 입력받아 두 미들웨어가 모두 `True` 일 때만 `reserve_seat()` 실행
    - `2` 입력 시: `show_reserved()` 실행
    - `3` 입력 시: 종료 메시지 출력 후 루프 종료
- ※ 좌석 번호는 `int()` 로 변환하여 사용하세요.
"""

reserved_seats = []  # 예약된 좌석 번호 목록


def reserve_seat(grade, seat_number):
    reserved_seats.append(seat_number)
    print(f"🪑 [{grade}]{seat_number}번 좌석 예약 완료!")


def show_reserved():
    if not reserved_seats:
        print("[현황] 예약된 좌석이 없습니다")
    else:
        print(f"[현황] 예약된 좌석:{sorted(reserved_seats)}")


# ↓ 여기서부터 작성하세요

def check_membership(grade):
    if grade == "정회원" or grade == "우수회원" or grade == "우수 회원":
        print("[회원 확인] 예약 권한 확인 완료")
        return True
    else:
        print("[회원 확인] 예약 권한 없음")
        return False

def check_seat(seat_number):
    if seat_number < 1 or seat_number > 50:
        print("[좌석 확인] 유효하지 않은 좌석 번호입니다.")
        return False
    elif seat_number in reserved_seats:
        print("[좌석 확인] 이미 예약된 좌석 번호입니다")
        return False
    else:
        print("[좌석 확인] 유효한 좌석 번호입니다")
        return True
        

if __name__ == "__main__":
    while True:
        print()
        print("--- 도서관 좌석 예약 시스템 ---","", "1. 좌석 예약", "2. 예약 현황 보기", "3. 종료", sep = "\n")
        print()

        menu = int(input("메뉴를 선택하세요 : "))
        print()
        if menu == 1:
            grade = input("회원 등급을 입력해주세요 : ")
            if check_membership(grade):
                print()
                seat_number = int(input("좌석 번호를 입력해주세요 : "))
                if check_seat(seat_number):
                    print()
                    reserve_seat(grade, seat_number)
            
        elif menu == 2:
            show_reserved()

        elif menu == 3:
            print("시스템을 종료합니다.")
            break

        else:
            print("잘못 입력하셨습니다.")
