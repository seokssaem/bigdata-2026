# 도서관 좌석 예약 시스템

reserved_seats = []

def reserve_seat(grade, seat_number) :
    # 좌석 예약
    reserved_seats.append(seat_number)
    print(f'[{grade}] {seat_number}번 좌석 예약 완료')

def check_membership(grade) :
    # 회원등급 확인 
    if grade == '정회원' or grade == '우수회원' :
        print('[회원확인] 예약 권한 확인 완료')
        return True
    else :
        print('[회원확인] 예약 권한 없음')
        return False
    
def check_seat(seat_number) :
    # 좌석 번호 유효성 및 중복 여부 확인
    if seat_number < 1 or seat_number > 50 :
        print('[좌석확인] 유효하지 않은 좌석 번호입니다')
        return False
    elif seat_number in reserved_seats :
        print('[좌석확인] 이미 예약된 좌석입니다')
        return False
    else :
        print('[좌석확인] 유효한 좌석 번호입니다')
        return True
    
def show_reserved() :
    # 예약된 좌석 목록 출력
    print(f'[현황] 예약된 좌석 : {sorted(reserved_seats)}')

if __name__ == '__main__' :
    print('--- 도서관 좌석 예약 시스템 ---')
    print('1. 좌석 예약\n2. 예약 현황 보기\n3. 종료')
    while True :
        num = int(input('\n메뉴를 선택하세요 : '))

        if num == 1 :
            grade = input('회원 등급 입력 : ')
            seat_num = int(input('좌석 번호 입력 : '))

            if check_membership(grade) and check_seat(seat_num) :
                reserve_seat(grade, seat_num)
        elif num == 2 :
            show_reserved()
        else :
            print('시스템을 종료합니다')
            break