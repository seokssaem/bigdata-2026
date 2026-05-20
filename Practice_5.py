"""
## 🎯 수행 과제

아래 조건에 맞게 파이썬 코드를 완성하세요.

**① `check_menu(menu)` 함수를 작성하세요.**

- 판매 가능한 메뉴는 `"아메리카노"`, `"카페라떼"`, `"카푸치노"` 입니다.
- 해당 메뉴이면 `"[메뉴확인] 주문 가능한 메뉴입니다"` 출력 후 `True` 반환
- 그 외이면 `"[메뉴확인] 주문 불가능한 메뉴입니다"` 출력 후 `False` 반환

**② `check_quantity(quantity)` 함수를 작성하세요.**

- 주문 수량은 **1잔 이상 10잔 이하**만 유효합니다.
- 유효하면 `"[수량확인] 주문 수량이 유효합니다"` 출력 후 `True` 반환
- 유효하지 않으면 `"[수량확인] 수량은 1잔 이상 10잔 이하만 가능합니다"` 출력 후 `False` 반환

**③ main 코드를 작성하세요.**

- 메뉴와 수량을 각각 `input()` 으로 입력받습니다.
- **두 미들웨어가 모두 `True` 일 때만** `make_coffee()` 가 실행됩니다.
- ※ 수량은 `int()` 로 변환하여 사용하세요.
"""

def make_coffee(menu, quantity):
    print(f"☕{menu} {quantity}잔 제조를 시작합니다!")


# ↓ 여기서부터 작성하세요
coffee = {"아메리카노", "카페라떼", "카푸치노"}

def check_menu(menu):
    if menu in coffee:
        print("[메뉴 확인] 주문 가능한 메뉴입니다.")
        print()
        return True
    else:
        print("[메뉴 확인]는 주문 불가능한 메뉴입니다.")
        print()
        return False

def check_quantity(quantity):
    if 1 <= quantity <= 10:
        print("[수량 확인] 주문 수량이 유효합니다.")
        print()
        return True
    else:
        print("[수량 확인] 주문 수량은 1잔 이상 10잔 이하만 가능합니다")
        print()
        return False

if __name__ == "__main__":
    menu = input("주문할 메뉴를 입력하세요 : ")
    if check_menu(menu):
        quantity = int(input("수량을 입력하세요 : "))
        if check_quantity(quantity):
            make_coffee(menu, quantity)