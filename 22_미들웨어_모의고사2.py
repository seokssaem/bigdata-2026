def book_title(title):
    print(f'{title} 예매가 완료되었습니다!')

def check_age(age):
    if age > 15:
        print('[나이확인]관람이 가능합니다.')
        return True
    else:
        print('[나이확인]15세 미만은 관람 불가합니다.')
        return False

if __name__ == '__main__':
    age = int(input('나이를 입력하세요 : '))
    if check_age(age):
        reserve_movies = input('예매할 영화 제목을 입력하세요 : ')
        book_title(reserve_movies) 

