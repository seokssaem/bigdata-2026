# 도서관 좌석 예약 시스템
# 1. 회원등급 - 정회원, 우수회원 --> 예약 권한
#               나머지 등급 --> 예약 권한 없음
# 2. 좌석 예약 - 00번 좌석이 예약이 완료되었습니다.
# 3. main - 회원등급 입력 -> 좌석 번호를 입력 -> 1,2번에 따라서 결과

def reserve_seat(seat_number):
    """
    매개변수(파라미터)
    seat_number : 좌석 번호

    입력된 좌석 번호를 화면에 보여주는 함수
    """
    print(f'{seat_number}번 좌석 예약이 완료되었습니다.')

def check_membership(grade):
    """
    매개변수(파라미터)
    grade : 회원 등급 (준회원/정회원/우수회원)

    반환값(return)
    True / False : bool형으로 반환

    정회원, 우수회원 --> 좌석 예약 권한 준다.
    """
    if grade == '정회원' or grade == '우수회원':
        print('좌석 예약 권한 확인 완료')
        return True
    else :
        print('좌석 예약 권한 없음')
        return False
    
if __name__ == '__main__':
    grade = input('회원 등급을 입력하세요(준회원/정회원/우수회원) : ')
    if check_membership(grade): # 함수 호출
        seat_number = int(input('좌석 번호를 입력하세요 : '))
        reserve_seat(seat_number) # 함수 호출

print(__name__)