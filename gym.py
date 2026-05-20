# 헬스장

def enter_gym(name, locker):
    print(f"💪{name}님,{locker}번 락커를 사용하세요. 입장을 환영합니다!")


# ↓ 여기서부터 작성하세요

def check_membership(membership):
    if membership == '유효':
        print("[회원권확인] 입장 가능합니다")
        return True
    else:
        print("[회원권확인] 유효한 회원권이 없습니다" )
        return False


def check_locker(locker):
    if 1<=locker<=50:
        print("[락커확인] 사용 가능한 락커 번호입니다")
        return True
    else:
        print("[락커확인] 락커 번호는 1번에서 50번 사이여야 합니다")
        return False


if __name__ == "__main__":
    membership = input('회원권 상태를 입력하세요 (유효/만료): ')
    locker = int(input('락커 번호를 입력하세요: '))
    if check_membership(membership) and check_locker(locker):
        name = input('이름을 입력하세요: ')
        enter_gym(name, locker)