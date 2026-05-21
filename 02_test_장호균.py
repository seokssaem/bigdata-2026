# 미들웨어의 개념을 설명하시오
# 서로다른 시스템이나 애플리케이션을 연결해주는 
# 중간 역할의 소프트웨어

# 미들웨어가 필요한 이유 2가지
# 프로그램의 안정성과 유지보수를 높이기 위해
# 미들웨어가 필요하다

# 조건기능검사를 재사용하여 코드의 중복을 
# 줄이기 위해 사용 하는 장점이 있다.

def ride_attraction():
    print("롤러코스터 출발합니다! 즐거운 시간 되세요.")


def check_height(height):

    if height >= 140:
        print("[미들웨어] 안전 확인 완료: 키가 140cm 이상입니다.")
        return True

    else:
        print("[미들웨어] 탑승 불가: 키가 너무 작습니다.")
        return False


if __name__ == "__main__":

    height = int(input("키를 입력하세요 : "))

    if check_height(height):
        ride_attraction()