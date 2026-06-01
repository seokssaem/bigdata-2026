class WordManger:
    def __init__(self):
        self.word_list = [] # 빈 리스트로 초기화
    
    def add(self):
        word = input('단어 입력: ')
        self.word_list.append(word) # word_list에 word 추가
        print(f'{word} 추가!')
    
    def show(self):
        if not self.word_list:
            print('단어가 없습니다.'); return
        for i, w in enumerate(self.word_list): # 인덱스와 값을 함께 순회
            print(f' {i+1}. {w}')
    
    def sort_desc(self):
        self.word_list.sort(reverse=True) # 내림차순 정렬

# 메뉴 실행--------
wm = WordManger()
while True:
    print('\n 1:추가 2:목록 3:내림차순정렬 4:종료')
    sel = input('선택 >>')
    if sel == '1': wm.add()
    elif sel == '2': wm.show()
    elif sel == '3': wm.sort_desc(); wm.show()
    elif sel == '4': print('종료'); break