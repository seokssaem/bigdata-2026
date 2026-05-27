import json

with open("260527/cafe_menu.json", "r", encoding="utf-8") as f:
    cafe_menu = json.load(f)

while True:
    print("1.가격별 메뉴 조회 2.종류별 메뉴 조회 3.주문 0.종료 : ", end="")
    num = input()
    
    if num == '0':
        print("스마트 카페 메뉴조회 시스템 종료!")
        break
        
    elif num == '1':
        price_input = (input("최저가격, 최고가격 입력(예:1000,2000) "))
        
        min_price, max_price = map(int, price_input.split(','))
        
        result = []
        for name, info in cafe_menu.items():
            if min_price <= info[0] <= max_price:
                result.append([name, info[0]])
        
        print("\n< 입력조건의 메뉴 목록 >")
        print(result)

    elif num == '2':
        category_input = input("종류별 메뉴 입력(예:커피,음료,디저트) ")

        result = []
        for name, info in cafe_menu.items():
            if info[1] == category_input:
                result.append([name, info[0]])

        print("\n< 입력조건의 메뉴 목록 >")
        print(result)

    elif num == '3':
        order_list = []
        total = 0

        while True:
            order_input = input("주문 메뉴 입력(0:종료) ")
            if order_input == '0':
                break
            else :
                count = int(input("수량 입력: "))

                order_list.append([order_input, cafe_menu[order_input][0], count])
                total += (cafe_menu[order_input][0] *  count)

        print("주문 내역 확인 : ", order_list)
        print(f'지불 총금액: {total}원')
