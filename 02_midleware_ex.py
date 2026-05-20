# 카페 주문 시스템

def check_menu(menu) :
    if menu == '아메리카노' or menu == '카페라떼' or menu == '카푸치노' :
        print('[메뉴확인] 주문 가능한 메뉴입니다')
        return True
    else :
        print('[메뉴확인] 주문 불가능한 메뉴입니다')
        return False
    
def check_quantity(quantity) :
    if 1 <= quantity <= 10 :
        print('[수량확인] 주문 수량이 유효합니다')
        return True
    else :
        print('[수량확인] 수량은 1잔 이상 10잔 이하만 가능합니다')
        return False
    
def make_coffee(menu, quantity) :
    print(f'{menu} {quantity}잔 제조를 시작합니다')

if __name__ == '__main__' :
    menu = input('주문할 메뉴를 입력하세요 : ')
    quantity = int(input('수량을 입력하세요 : '))

    if check_menu(menu) and check_quantity(quantity) :
        make_coffee(menu, quantity)