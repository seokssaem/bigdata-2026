# 카페 주문 시스템 (기본)

def make_coffee(menu):
    print(f"☕{menu} 제조를 시작합니다!")


# ↓ 여기서부터 작성하세요

def check_menu(menu):
    if menu == '아메리카노' or menu == '카페라떼' or menu == '카푸치노':
        print("[메뉴확인] 주문 가능한 메뉴입니다.")
        return True
    else:
        print("[메뉴확인] 주문 불가능한 메뉴입니다.")
        return False


if __name__ == "__main__":
    menu = input("주문할 메뉴를 입력하세요 : ")
    if check_menu(menu):
        make_coffee(menu)


#----------------------------------------------------------------
def book_movie(title):
    print(f"🎬{title} 예매가 완료되었습니다!")


# ↓ 여기서부터 작성하세요

def check_age(age):
    if age >= 15:
        print("[나이확인] 관람 가능합니다")
        return True
    else:
        print("[나이확인] 15세 미만은 관람 불가합니다")
        return False


if __name__ == "__main__":
    age = int(input('나이를 입력하세요'))
    if check_age(age):
        title = input("예매할 영화 제목을 입력하세요 : ")
        book_movie(title)



#------------------------------------------------------------------
def enter_gym(name):
    print(f"💪{name}님, 입장을 환영합니다!")


# ↓ 여기서부터 작성하세요

def check_membership(membership):
    if membership == '유효':
        print('[회원권확인] 입장 가능합니다')
        return True
    else:
        print('[회원권확인] 유효한 회원권이 없습니다')
        return False        


if __name__ == "__main__":
    membership = input('회원권 상태를 입력하세요 (유효/만료) : ')
    if check_membership(membership):
        name = input('이름을 입력하세요: : ')
        enter_gym(name)