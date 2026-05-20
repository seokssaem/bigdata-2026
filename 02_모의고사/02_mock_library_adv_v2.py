# [모의고사 정답] 도서관 좌석 예약 시스템 - 심화 v2
# 추가 기능: 중복 예약 방지, 예약 현황 조회

reserved_seats = []  # 예약된 좌석 번호 목록


def reserve_seat(grade, seat_number):
    reserved_seats.append(seat_number)
    print(f"🪑 [{grade}] {seat_number}번 좌석 예약 완료!")


def check_membership(grade):
    if grade == "정회원" or grade == "우수회원":
        print("[회원확인] 예약 권한 확인 완료")
        return True
    else:
        print("[회원확인] 예약 권한 없음")
        return False


def check_seat(seat_number):
    if not (1 <= seat_number <= 50):
        print("[좌석확인] 유효하지 않은 좌석 번호입니다")
        return False
    if seat_number in reserved_seats:
        print("[좌석확인] 이미 예약된 좌석입니다")
        return False
    print("[좌석확인] 유효한 좌석 번호입니다")
    return True


def show_reserved():
    if not reserved_seats:
        print("[현황] 예약된 좌석이 없습니다")
    else:
        print(f"[현황] 예약된 좌석: {sorted(reserved_seats)}")


if __name__ == "__main__":
    while True:
        print("\n--- 도서관 좌석 예약 시스템 ---")
        print("1. 좌석 예약")
        print("2. 예약 현황 보기")
        print("3. 종료")
        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            grade = input("회원 등급: ")
            seat_number = int(input("좌석 번호: "))
            if check_membership(grade) and check_seat(seat_number):
                reserve_seat(grade, seat_number)

        elif choice == "2":
            show_reserved()

        elif choice == "3":
            print("시스템을 종료합니다.")
            break

        else:
            print("올바른 메뉴 번호를 입력하세요.")
