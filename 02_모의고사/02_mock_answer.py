# [모의고사 정답] 도서관 좌석 예약 시스템 - 기본

def reserve_seat(seat_number):
    print(f"🪑 {seat_number}번 좌석 예약이 완료되었습니다!")


def check_membership(grade):
    if grade == "정회원" or grade == "우수회원":
        print("예약 권한 확인 완료")
        return True
    else:
        print("예약 권한 없음")
        return False


if __name__ == "__main__":
    grade = input("회원 등급을 입력하세요: ")
    if check_membership(grade):
        seat_number = int(input("좌석 번호를 입력하세요: "))
        reserve_seat(seat_number)
