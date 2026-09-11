<<<<<<< HEAD
def ride_roller_coaster():
    print("롤러코스터가 출발합니다! 즐거운 시간 되세요.")


def check_safety(height):
    if height >= 140:
        print("[미들웨어] 안전 확인 완료 : 키가 140cm 이상입니다.")
        return True
    else:
        print("[미들웨어] 탑승 불가 : 키가 너무 작습니다.")
        return False
    

if __name__ == "__main__":
    height = int(input(print("키를 입력하세요 : ")))
    if check_safety(height):
#=======
def ride_roller_coaster():
    print("롤러코스터가 출발합니다! 즐거운 시간 되세요.")


def check_safety(height):
    if height >= 140:
        print("[미들웨어] 안전 확인 완료 : 키가 140cm 이상입니다.")
        return True
    else:
        print("[미들웨어] 탑승 불가 : 키가 너무 작습니다.")
        return False
    

if __name__ == "__main__":
    height = int(input(print("키를 입력하세요 : ")))
    if check_safety(height):
>>>>>>> ca169814e2a3d8aa6199e3815d1ef75b5dab2cea
        ride_roller_coaster()