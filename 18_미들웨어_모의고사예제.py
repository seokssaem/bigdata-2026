# 도서관 좌석 예약 시스템

# 1. 회원등급- 정회원, 우수회원 --> 예약 권한
#             나머지 등급 --> 예약 권한 없음
# 2. 좌석 예약- 00번 좌석이 예약 완료되었습니다!
# 3. main- 회원등급 입력 -> 좌석 번호를 입력 ->1,2번에 따라서 결과 도출

# def reserve_seat(seat_number):
#     """
#     매개변수(파라미터)
#     seat_number : 좌석번호

#     입력된 좌석 번호를 화면에 보여주는 함수
#     """
#     print(f'{seat_number}번 좌석 예약이 완료되었습니다!')

# def check_membership(grade):
#     """
#     매개변수(파라미터)
#     grade : 회원등급 (준회원/정회원/우수회원)

#     반환값(return)
#     True / False : bool형으로 반환

#     정회원,우수회원 --> 좌석 예약 권한 준다!
#     """

#     if grade == '정회원' or grade =='우수회원':
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


# 2. 카페 주문 시스템

# 1. 판매가능한 메뉴는 아메리카노, 카페라떼, 카푸치노
#    해당 메뉴이면 "[메뉴확인] 주문 가능한 메뉴 입니다" True 를 반환합니다.
# 그 외의 메뉴이면 "[메뉴확인] 주문 불가능한 메뉴입니다" 를 출력하고 False 를 반환합니다.


# def make_coffee(menu):
#     print(f"☕ {menu} 제조를 시작합니다!")

# def check_menu(menu):

#     available_menus = ["아메리카노", "카페라떼", "카푸치노"]
    
#     if menu in available_menus:
#         print("[메뉴확인] 주문 가능한 메뉴입니다")
#         return True
#     else:
#         print("[메뉴확인] 주문 불가능한 메뉴입니다")
#         return False


# if __name__ == "__main__":
#     # 주문할 메뉴를 input()으로 입력받음
#     order_menu = input("주문할 메뉴를 입력하세요: ")
    
   
#     if check_menu(order_menu):
#         make_coffee(order_menu)

# **`check_age(age)` 함수를 작성하세요.**

# - 나이(`age`)를 정수로 입력받습니다.
# - **15세 이상**이면 `"[나이확인] 관람 가능합니다"` 를 출력하고 `True` 를 반환합니다.
# - 15세 미만이면 `"[나이확인] 15세 미만은 관람 불가합니다"` 를 출력하고 `False` 를 반환합니다.

# **② main 코드를 작성하세요.**

# - 나이를 `input()` 으로 입력받습니다. ※ `int()` 로 변환하여 사용하세요.
# - 미들웨어(`check_age`)의 결과가 `True` 일 때만 영화 제목을 입력받고 `book_movie()` 가 실행됩니다.



def book_movie(title):
    print(f"🎬{title} 예매가 완료되었습니다!")


def check_age(age):
    if age >= 15:
        print('[나이확인]관람 가능합니다')
        return True
    else:
        print('[나이확인]15세 미만은 관람 불가합니다')
        return False

if __name__ == "__main__":  
    age = int(input('나이를 입력하세요? : '))
    if check_age(age):
        title = input ('예매할 영화 제목을 입력하세요? : ')
        book_movie(title)
  

#    아래 조건에 맞게 파이썬 코드를 완성하세요.

# **① `check_membership(membership)` 함수를 작성하세요.**

# - 회원권 상태(`membership`)를 문자열로 입력받습니다.
# - `"유효"` 이면 `"[회원권확인] 입장 가능합니다"` 를 출력하고 `True` 를 반환합니다.
# - 그 외이면 `"[회원권확인] 유효한 회원권이 없습니다"` 를 출력하고 `False` 를 반환합니다.

# **② main 코드를 작성하세요.**

# - 회원권 상태를 `input()` 으로 입력받습니다.
# - 미들웨어(`check_membership`)의 결과가 `True` 일 때만 이름을 입력받고 `enter_gym()` 이 실행됩니다.


# def enter_gym(name):
#     print(f"💪{name}님, 입장을 환영합니다!")


# # ↓ 여기서부터 작성하세요

# def check_membership(membership):
#     if membership == '유효':
#         print('[회원권확인]입장가능')
#         return True
#     else:
#         print('[회원권확인]유효한 회원권 없음')
#         return False


# if __name__ == "__main__":
#     membership = input('회원권 상태(유효/만료) : ')
#     if check_membership(membership):
#         name = input('이름을 입력하세요 : ')
#         enter_gym(name)