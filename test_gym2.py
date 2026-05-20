def enter_gym(name):
    print(f"💪{name}님, 입장을 환영합니다!")


# ↓ 여기서부터 작성하세요

def check_membership(membership):
    if membership == '유효':
        print('입장 가능합니다')
        return True
    else :
        print('유효한 회원권이 없습니다')
        return False
    
def check_locker(locker):
    if 1<= locker <= 50:
        print('사용 가능한 락커 번호입니다.')
        return True
    else:
        print('락커 번호가 유효하지 않습니다.')
        return False
    
if __name__ == "__main__":
    membership = input('회원권 상태를 입력하세요 (유효/만료):')
    if check_membership(membership):
        locker = int(input('락커 번호를 입력하세요'))
        if check_locker(locker):
            name = input('이름을 입력하세요 : ')
            enter_gym(name)
