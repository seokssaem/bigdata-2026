# [모의고사 정답] 카페 주문 시스템 - 기본

def make_coffee(menu):
    print(f"☕ {menu} 제조를 시작합니다!")


def check_menu(menu):
    available = ["아메리카노", "카페라떼", "카푸치노"]
    if menu in available:
        print("[메뉴확인] 주문 가능한 메뉴입니다")
        return True
    else:
        print("[메뉴확인] 주문 불가능한 메뉴입니다")
        return False


if __name__ == "__main__":
    menu = input("주문할 메뉴를 입력하세요: ")
    if check_menu(menu):
        make_coffee(menu)
