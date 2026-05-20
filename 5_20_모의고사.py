# # 도서관 좌석 예약 시스템
# # 1. 회원등급이 - 정회원, 우수회원 --> 예약 권한
# #           나머지 등급 --> 예약 권한 없음
# # 2. 좌석 예약 - 00번 좌석이 예약이 완료되었습니다!
# # 3. main - 회원등급 입력 -> 좌석 번호를 입력 -> 1, 2번에 따라서 결과

# def reserve_seat(seat_number):
#     """
#     매개변수(파라미터)
#     seat_number : 좌석 번호

#     입력된 좌석 번호를 화면에 보여주는 함수
#     """
#     print(f'{seat_number}번 좌석 예약이 완료되었습니다!')

# def check_membership(grade):
#     """
#     매개변수(파라미터)
#     grade : 회원 등급 (준회원/정회원/우수회원)

#     반환값(return)
#     True / False : bool형으로 반환
#     정회원, 우수회원 --> 좌석 예약 권한 준다!
#     """

#     if grade == '정회원' or grade == '우수회원':
#         print('좌석 예약 권한 확인 완료!')
#         return True
#     else:
#         print('좌석 예약 권한 없음!')
#         return False

# if __name__ == '__main__':
#     grade = input('회원 등급을 입력하세요(준회원/정회원/우수회원) : ')
#     if check_membership(grade): # 함수 호출
#         seat_number = int(input('좌석 번호를 입력하세요 : '))
#         reserve_seat(seat_number) # 함수 호출

# ------------------------------------------------------------------------------

def make_coffee(menu):
    print(f"☕{menu} 제조를 시작합니다!")


# ↓ 여기서부터 작성하세요

def check_menu(menu):
    if menu == '아메리카노' or menu == '카페라떼' or menu == '카푸치노':
        print(f'{menu} 주문 가능한 메뉴입니다.')
        return True
    else:
        print(f'{menu} 주문 불가능한 메뉴입니다.')
        return False



if __name__ == "__main__":
    menu = input('주문 메뉴 (아메리카노 / 카페라떼 / 카푸치노) : ')
    if check_menu(menu):
        make_coffee(menu)

# ------------------------------------------------------------------------------

# def book_movie(title):
#     print(f"🎬{title} 예매가 완료되었습니다!")


# # ↓ 여기서부터 작성하세요

# def check_age(age):
#     if age >= 15:
#         print(f'{age} 관람 가능합니다')
#         return True
#     else:
#         print(f'{age} 15세 미만은 관람 불가합니다')
#         return False


# if __name__ == "__main__":
#     age = int(input('나이를 입력하세요 : '))
#     if check_age(age):
#         title = input('영화 제목을 입력하세요 : ')
#         book_movie(title)

# ------------------------------------------------------------------------------

# def enter_gym(name):
#     print(f"💪{name}님, 입장을 환영합니다!")


# # ↓ 여기서부터 작성하세요

# def check_membership(membership):
#     if membership == '유효':
#         print(f'{membership} 입장 가능합니다.')
#         return True
#     else:
#         print(f'{membership} 유효한 회원권이 없습니다.')
#         return False


# if __name__ == "__main__":
#     membership = input('회원권 상태를 입력하세요 (유효 / 만료) : ')
#     if check_membership(membership):
#         name = input('이름을 입력하세요 : ')
#         enter_gym(name)