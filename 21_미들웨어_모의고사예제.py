def enter_gym(name):
    print(f"💪{name}님, 입장을 환영합니다!")



def check_membership(membership):
    if membership == '유효':
        print(f'[회원권확인] 입장 가능합니다.')
        return True
    else:
        print(f'[회원권확인] 유효한 회원권이 없습니다.')
        return False


if __name__ == "__main__":
    membership = input('회원권 상태를 입력하세요 (유효/만료): ')
    if check_membership(membership):
        name = input('이름을 입력하세요: ')
        enter_gym(name)
