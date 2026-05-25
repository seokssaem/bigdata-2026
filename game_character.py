class Character:
    def __init__(self, name, hp, attack, job = "모험가"):
        self.name = name
        self.hp = max(0, hp)
        self.attack = attack
        self.job = job
        if job == "전사":
            self.shield = 3
        else:
            self.shield = 0

    def show_info(self):
        print(f"이름 : {self.name} | HP : {self.hp}, 공격력 : {self.attack}, 방어 : {self.shield}")

    def attack_enemy(self, target):
        if target.shield_block():
            target.hp -= self.attack//2
            print(f"{self.name}가(이) {target.name}을(를) 공격! {self.attack//2} 피해!")
        else:
            target.hp -= self.attack
            print(f"{self.name}가(이) {target.name}을(를) 공격! {self.attack} 피해!")

        if not target.is_alive():
            print(f"{target.name}가(이) 쓰러졌다.")
            target.hp = 0

    def shield_block(self):
        if self.shield > 0:
            choice = input(f"{self.name}의 방패를 사용하시겠습니까?(y/n) : ")
            if choice == "y":
                self.shield -= 1
                return True
            else:
                print(f"{self.name}의 방패를 사용하지 않습니다.")
                return False
        else:
            print(f"{self.name}는(은) 방패가 없습니다.")
            return False

    def is_alive(self):
        if self.hp > 0:
            return True
        else:
            return False
    
    def __str__(self):
        return f"이름 : {self.name} | HP : {self.hp}, 공격력 : {self.attack}, 방어 : {self.shield}"


if __name__ == "__main__":
    hero = Character("아서", 100, 30)
    boss = Character("드래곤", 150, 50)
    minion = Character("고블린", 20, 5)

    hero.show_info()

    minion.show_info()
    hero.attack_enemy(minion)

    player = Character("가웨인", 120, 35, "전사")
    player.show_info()

    boss.show_info()
    hero.attack_enemy(boss)
    player.attack_enemy(boss)
    boss.attack_enemy(hero)
    boss.attack_enemy(player)

    hero.show_info()
    minion.show_info()
    player.show_info()
    boss.show_info()