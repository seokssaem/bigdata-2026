def make_coffee(menu):
    print(f"☕{menu} 제조를 시작합니다!")


# ↓ 여기서부터 작성하세요

def check_menu(menu):
    if menu == '아메리카노' or '카페라떼' or '카푸치노':
        print(f'[메뉴확인] 주문 가능한 메뉴입니다.')
        return True
    else:
        print(f'[메뉴확인] 주문 불가능한 메뉴입니다.')
        return False


if __name__ == "__main__":
    menu = input('주문할 메뉴를 입력하세요 : ')
    if check_menu(menu):
        make_coffee(menu)