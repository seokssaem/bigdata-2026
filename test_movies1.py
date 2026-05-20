def book_movie(title):
    print(f"☕{title} 예매가 완료되었습니다.!")


# ↓ 여기서부터 작성하세요

def check_age(age):
    if age >= 15:
        print('관람가능합니다.')
        return True
    else :
        print("15세 미만은 관람 불가입니다.")
        return False

if __name__ == "__main__" :
    age = int(input('나이를 입력하세요 : '))

    if check_age(age):
        title = input('예매할 영화 제목을 입력하세요 : ')
        book_movie(title)