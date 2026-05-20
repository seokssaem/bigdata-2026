def make_coffee(menu):
    print(f'{menu} 제조를 시작합니다!')

def check_menu(menu):
    if menu == '아메리카노' or menu == '카페라떼' or menu == '카푸치노':
        print('[메뉴 확인] 주문 가능한 메뉴입니다')
        return True
    else:
        print('[메뉴 확인] 주문 불가능한 메뉴입니다')
        return False 

if __name__ == '__main__':
    menu = input('주문할 메뉴를 입력하세요 : ')
    if check_menu(menu):
        make_coffee(menu)  
    

