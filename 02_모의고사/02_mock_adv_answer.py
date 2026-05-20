# [모의고사 정답] 도서관 좌석 예약 시스템 - 심화

def reserve_seat(grade, seat_number):
    print(f"🪑 [{grade}] {seat_number}번 좌석 예약 완료!")


def check_membership(grade):
    if grade == "정회원" or grade == "우수회원":
        print("[회원확인] 예약 권한 확인 완료")
        return True
    else:
        print("[회원확인] 예약 권한 없음")
        return False


def check_seat(seat_number):
    if 1 <= seat_number <= 50:
        print("[좌석확인] 유효한 좌석 번호입니다")
        return True
    else:
        print("[좌석확인] 유효하지 않은 좌석 번호입니다")
        return False


if __name__ == "__main__":
    grade = input("회원 등급: ")
    seat_number = int(input("좌석 번호: "))
    if check_membership(grade) and check_seat(seat_number):
        reserve_seat(grade, seat_number)
