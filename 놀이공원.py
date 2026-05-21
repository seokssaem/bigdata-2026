def check_safety(height):
    if height>=140:
        print("[미들웨어] 안전 확인 완료")
        return True
    else:
        print("[미들웨어] 탑승 불가")
        return False
    
def ride_roller_coaster():
    print("롤러코스터가 출발합니다! 즐거운 시간 되세요.")

if __name__ == "__main__":
    height = int(input("키를 입력하세요: "))
    if check_safety(height):
        ride_roller_coaster()