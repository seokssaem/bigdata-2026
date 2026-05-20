"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_menu(menu)` 함수를 작성하세요.**

- 판매 가능한 메뉴는 `"아메리카노"`, `"카페라떼"`, `"카푸치노"` 입니다.
- 해당 메뉴이면 `"[메뉴확인] 주문 가능한 메뉴입니다"` 를 출력하고 `True` 를 반환합니다.
- 그 외의 메뉴이면 `"[메뉴확인] 주문 불가능한 메뉴입니다"` 를 출력하고 `False` 를 반환합니다.

**② main 코드를 작성하세요.**

- 주문할 메뉴를 `input()` 으로 입력받습니다.
- 미들웨어(`check_menu`)의 결과가 `True` 일 때만 `make_coffee()` 가 실행됩니다.
"""


def make_coffee(menu):
    print(f"☕{menu} 제조를 시작합니다!")


# ↓ 여기서부터 작성하세요
coffee = {"아메리카노", "카페라떼", "카푸치노"}
def check_menu(menu):
    if menu in coffee:
        print("[메뉴 확인] 주문 가능한 메뉴입니다.")
        return True
    else:
        print("[메뉴 확인]는 주문 불가능한 메뉴입니다.")
        return False

if __name__ == "__main__":
    order = input("무엇을 주문하시겠습니까? : ")
    menu = check_menu(order)
    if menu:
        make_coffee(order)