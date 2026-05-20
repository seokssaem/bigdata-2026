reserved_seats = []

def reserve_seat(grade, seat_number):
    reserved_seats.append(seat_number)
    print(f"🪑 [{grade}]{seat_number}번 좌석 예약 완료!")


def check_membership(grade):
    if grade == '정회원' or grade == '우수회원':
        return True
    else :
        print("예약 권한이 없음")
        return False
    

def check_seat(seat_number):
    if 1 > seat_number or seat_number > 50 :
        print('유효하지 않은 좌석 번호입니다')
        return  False
    elif seat_number in reserved_seats:
        print('이미 예약된 좌석입니다')
        return False
    else:
        print('유효한 좌석입니다')
        return True


if __name__ == '__main__':
    grade = input('회원 등급을 입력하세요(준회원/정회원/우수회원) : ')
    check_membership(grade)
    if check_membership(grade):  
        seat_number = int(input('좌석 번호를 입력하세요 : '))
        check_seat(seat_number) 
        if check_seat(seat_number):
                print(f'{seat_number}번 좌석 예약 완료!')
