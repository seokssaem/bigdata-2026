Class = [["수학", 113, "A+"], ["영어", 3, "B+"], ["국어", 4, "A"], ["체육", 2, "F"]]
have_credit = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]
score_credit = {"A+":4.5, "A":4.0, "B+":3.5, "B":3.0, "C+":2.5, "C":2.0, "D+":1.5, "D":1.0, "F":0.0}

def 평균평점():
    plus = 0
    count = 0
    for name, credit, have in Class:
        if score_credit[have]: # F학점을 평점 평균 계산에 포함 시키고 싶다면 주석처리하고 아래 두 줄의 들여쓰기를 한 칸 없애세요.
            plus += score_credit[have]
            count += 1
    ave = plus / count
    return ave

def 이수학점():
    이수 = 0
    for name, credit, have in Class:
        이수 += credit
    return 이수



while True:
    print("\n------메뉴------")
    print("\n1. 수강 강좌 정보 입력\n2. 평균 평점 확인\n3. 졸업 여건 확인\n0. 종료\n")

    choice = input("메뉴를 선택하세요. : ")
    print()

    if choice == "0" or choice == "1" or choice == "2" or choice == "3":
        choice = int(choice)
        
        if choice == 0:
            break

        elif choice == 1:
            while True:
                name = input("과목 명(0: 종료) : ")
                if name == "0":
                    break
                else:
                    credit = int(input("학점 수 : "))
                    have = input("취득학점(A+, A, B+, B, C+, C, D+, D, F) : ")
                    if have not in have_credit:
                        print("\n잘못 입력하셨습니다.\n")
                        continue
                    Class.append([name, credit, have])
                    print(f"\n{name} 수강 강좌가 등록되었습니다.\n")
        
        elif choice == 2:
            print(평균평점())
            if 평균평점() >= 4.0:
                print("장학 대상자입니다. 축하드립니다.")

        elif choice == 3:
            등록학기 = int(input("총 등록 학기 수 입력 : "))
            A = False
            B = False
            C = False

            if 등록학기 >= 8:
                print("졸업 학기 충족")
                A = True
            else:
                print(f"{8 - 등록학기}학기 부족")
                continue
            
            print()
            print(f"이수 학점 : {이수학점()}")
            if 이수학점() >= 120:
            
                print("졸업 학점 충족")
            
                B = True
            else:
                print(f"{120 - 이수학점()}학점 부족")
                break

            print()
            print(f"평균평점 : {평균평점()}")

            if 평균평점() >= 2.5:
                print("졸업 평균평점 충족")
                C = True
            else:
                print(f"{2.5 - 평균평점()} 평균평점 낮음")
            
            print()

            if A and B and C:
                if 평균평점() >= 4.0:
                    print("모든 졸업 여건을 충족하셨습니다.\n축하드립니다. 장학 졸업 대상자 입니다.")
                else:
                    print("모든 졸업 여건을 충족하셨습니다.\n졸업 대상자 입니다.")

            else:
                print("졸업 여건을 충족하지 못했습니다.")
