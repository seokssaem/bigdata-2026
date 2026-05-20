# [모의고사 정답] 영화관 예매 시스템 - 기본

def book_movie(title):
    print(f"🎬 {title} 예매가 완료되었습니다!")


def check_age(age):
    if age >= 15:
        print("[나이확인] 관람 가능합니다")
        return True
    else:
        print("[나이확인] 15세 미만은 관람 불가합니다")
        return False


if __name__ == "__main__":
    age = int(input("나이를 입력하세요: "))
    if check_age(age):
        title = input("예매할 영화 제목을 입력하세요: ")
        book_movie(title)
