"""
2. 당신은 놀이공원 입장 시스템을 만들고 있습니다. 이 시스템에는 두 가지 핵심 부분이 있습니다.

메인 시스템 (ride_roller_coaster): 롤러코스터를 태워주는 기능

미들웨어 (check_safety): 탑승 전, 키를 확인하여 안전한지 검사하는 기능

[수행 과제]

아래의 조건에 맞게 파이썬 코드를 완성하세요.

check_safety 함수를 만드세요. 
이 함수는 키(height)를 입력받아 140cm 이상이면 "안전 확인 완료"를 출력하고 True를 반환합니다. 
140cm 미만이면 "탑승 불가"를 출력하고 False를 반환합니다.
main 코드 영역에서 미들웨어(check_safety)의 결과가 True일 때만 메인기능(ride_roller_coaster) 함수가 실행되도록 작성하세요.
"""

def ride_roller_coaster(ride):
    if ride == True:
        print("🎢롤러코스터가 출발합니다! 즐거운 시간 되세요.")


def check_safety(height):
    if height >= 140:
        print("[미들웨어] 안전 확인 완료: 키가 140cm 이상입니다.")
        return True
    else:
        print("[미들웨어] 탑승 불가: 키가 너무 작습니다.")
        return False
    
if __name__=="__main__":
    height = int(input("키를 입력하세요: "))
    ride = check_safety(height)
    if ride:
        ride_roller_coaster(ride)
