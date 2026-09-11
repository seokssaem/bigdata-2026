import csv
FILENAME = 'students.csv'
students = [
    {'name' : '홍길동', 'score' : 85},
    {'name' : '이순신', 'score' : 92},
    {'name' : '강감찬', 'score' : 78},
]

def save_csv(data):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'score'] )
        writer.writeheader()
        writer.writerows(data)
    print(f'{FILENAME} 저장 완료')

def load_csv():
    with open(FILENAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
    

save_csv(students)
loaded = load_csv()
print('\n 불러온 데이터 : ')
for row in loaded:
    print(row)