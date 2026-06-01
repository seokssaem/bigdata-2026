"""
[스마트 카페 메뉴 목록]
에스프레소 아메리카노 카푸치노 카페라떼 모카라떼 바닐라라떼 소이라떼 피넛라떼 토피넛라떼 화이트모카 카라멜마끼야또 프라푸치노 핫초코 레몬에이드 청포도에이드 자몽에이드 스무디 망고스무디 딸기스무디 초코쿠키 화이트쿠키 피넛쿠키 당근케이크 초코케이크 치즈케이크
1.가격별 메뉴 조회 2.종류별 메뉴 조회 3.주문 0.종료: 1
최저가격, 최고가격 입력(예:1000,2000) 2000,2500
< 입력조건의 메뉴 목록 >
[['에스프레소', 2000], ['아메리카노', 2500], ['초코쿠키', 2000], ['화이트쿠키', 2000], ['피넛쿠키', 2000]]
1.가격별 메뉴 조회 2.종류별 메뉴 조회 3.주문 0.종료: 2
종류별 메뉴 입력(예:커피,음료,디저트) 디저트
< 입력조건의 메뉴 목록 >
[['초코쿠키', 2000], ['화이트쿠키', 2000], ['피넛쿠키', 2000], ['당근케이크', 5000], ['초코케이크', 5000], ['치즈케이크', 5000]]
1.가격별 메뉴 조회 2.종류별 메뉴 조회 3.주문 0.종료: 3
원하는 메뉴 입력 : 초코케이크
< 입력조건의 메뉴 목록 >
[['초코케이크', 5000, '디저트']]
1.가격별 메뉴 조회 2.종류별 메뉴 조회 3.주문 0.종료: 0
스마트 카페 메뉴조회 시스템 종료!
"""

menu = {
    "커피":{"에스프레소":2000,
    "아메리카노":2500,
    "카푸치노":2500,
    "카페라떼":3500,
    "모카라떼":3500,
    "바닐라라떼":4000,
    "소이라떼":4000,
    "피넛라떼":4000,
    "토피넛라떼":4000,
    "화이트모카":5000,
    "카라멜마끼야또":4500},
    "음료":{"프라푸치노":3500,
    "핫초코":3500,
    "레몬에이드":4000,
    "청포도에이드":4000,
    "자몽에이드":4000,
    "스무디":3000,
    "망고스무디":3500,
    "딸기스무디":3500},
    "디저트":{"초코쿠키":2000,
    "화이트쿠키":2000,
    "피넛쿠키":2000,
    "당근케이크":5000,
    "초코케이크":5000,
    "치즈케이크":5000}
}

all_menu = {}

for group, items in menu.items():
    for name, price in items.items():
        all_menu[name] = price

def reset():
    
    return choice

print()
print("스마트 카페에 오신 것을 환영합니다.")
print()
print("-- 스마트 카페 메뉴 목록 --")

for name, price in all_menu.items():
    print(name, end=" ")
print()

loop = False

# 메뉴 조회 후 메인 화면으로 가려면 아래 두 줄을 비활성화하세요.
# 메뉴 조회 후 주문 화면으로 가려면 아래 두 줄을 활성화하세요.
# 104번, 120번

# 주문 종료 후 기능으로 돌아가려면 아래 줄을 비활성화 하세요.
# 168번

while True:
    if not loop:
        print()
        print("-----  기능  -----")
        choice = input("1.가격별 메뉴 조회\n2.종류별 메뉴 조회\n3.주문\n0.종료\n\n기능을 선택하세요. : ")
    else:
        choice = "3"

    if choice == "1" or choice == "2" or choice == "3" or choice == "0":
            choice = int(choice)
            print()
    else:
        print("잘못 입력하셨습니다. 처음부터 다시 진행해주세요.")
        
    if choice == 0:
        print("감사합니다. 안녕히 가세요.")
        break

    elif choice == 1:
        min_price = int(input("최소 금액을 입력해주세요.(예: 1000): "))
        max_price = int(input("최대 금액을 입력해주세요.(예: 5000): "))
        print()
        if min_price <= max_price:
            check = False
            for name, price in all_menu.items():
                if min_price <= price <= max_price:
                    print(f"{name} : {price:,}원")
                    check = True
                    loop = True # 메뉴 조회 후 메인 화면으로 가려면 비활성화하세요. 메뉴 조회 후 주문 화면으로 가려면 활성화하세요.
            if not check:
                print("조회된 메뉴가 없습니다. 처음부터 다시 진행해주세요.")
                
        else:
            print("잘못 입력하셨습니다. 처음부터 다시 진행해주세요.")

    elif choice == 2:
        category = input("조회하실 메뉴 분류를 입력해주세요.(예: 커피, 음료, 디저트): ")
        print()
        check = False
        for group, items in menu.items():
            if category == group:
                for name, price in items.items():
                    print(f"{name} : {price:,}원")
                check = True
                loop = True # 메뉴 조회 후 메인 화면으로 가려면 비활성화하세요. 메뉴 조회 후 주문 화면으로 가려면 활성화하세요.
        if not check:
            print("잘못 입력하셨습니다. 처음부터 다시 진행해주세요.")
            print()
            continue
        
    elif choice ==3:
        total_price = 0
        order_list = {}
        while True:
            order = input("무슨 메뉴를 주문하시겠습니까?(예: 에스프레소)(주문 종료: 0): ")
            print()
            if order == "0":
                if order_list == {}:
                    print("다음에 다시 찾아주세요. 감사합니다.")
                    break
                else:
                    first = True
                    for name, count in order_list.items():
                        if first:
                            print(f"{name} {count}잔", end="")
                            first = False
                        else:
                            print(f", {name} {count}잔", end=" ")
                    print(f"총 금액은 {total_price:,}원입니다.")
                    gold = int(input("얼마를 지불 하시겠습니까? : "))
                    print()
                    print(f"{gold:,}원 받았습니다. 거스름 돈 {gold - total_price:,}원 입니다. 감사합니다.") 
                    print()
                break

            elif order not in all_menu:
                print("잘못 입력하셨습니다. 주문을 진행해주세요.")
                print()

            elif order in all_menu:
                order_count = int(input("수량을 입력해주세요.(예: 3): "))
                print(f"{order} {order_count}잔")
                print()
                total_price += all_menu[order] * order_count
                if order in order_list:
                    order_list[order] += order_count
                    
                else:
                    order_list[order] = order_count

            else:
                break
        break # 주문 종료 후 기능으로 돌아가려면 비활성화 하세요.
