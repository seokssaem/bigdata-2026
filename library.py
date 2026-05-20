# 도서관
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
    """
    매개변수(파라미터)
    grade : 회원 등급 (준회원/정회원/우수회원)

    반환값(return) : True / False   

    정회원, 우수회원 --> 좌석 예약 권한 부여
    """
    if grade == '정회원' or grade == '우수회원':
        print('예약 권한 확인 완료')
        return True
    else:
        print('예약 권한이 없습니다.')
        return False


def check_seat(seat_number):
    if 1<=seat_number<=50:
        if seat_number not in reserved_seats:
            return True
        else:
            print("이미 예약된 좌석입니다.")
            show_reserved()
            return False
    else:
        print("유효하지 않은 좌석입니다.")
        return False


if __name__ == "__main__":
    while True:
        print('\n--- 도서관 좌석 예약 시스템 ---\n1. 좌석 예약\n2. 예약 현황 보기\n3. 종료')
        menu = int(input('메뉴 선택: '))

        if menu == 3:
            break
        elif menu == 2:
            show_reserved()
        else:
            grade = input('회원등급 입력하세요: ')
            if check_membership(grade):
                seat_num = int(input('원하는 좌석 번호: '))
                if check_seat(seat_num):
                    reserve_seat(grade, seat_num)

