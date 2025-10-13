class p0 :
    def __init__(self):
        self.last = 0 #хранение последнего хода
    def next (self, i):  #сделать ход
        return 0
    def name(self):
        return "NULL"
    def reload(self):
        self.last = 0
class p1 :
    def __init__(self):
        self.last = 1;
    def next (self, i):
        return 1;
    def name(self):
        return "ONE"
    def reload(self):
        self.last=1
class pRepeat :
    def __init__(self):
        self.num = 0
        self.last = 0
    def next (self, i):
        self.num += 1
        if self.num == 1:
            return 0;
        return i;
    def name(self):
        return "Repeater"
    def reload(self):
        self.last=0
        self.num = 0
class pOposite:
    def __init__(self):
        self.num = 0
        self.last = 0
    def next(self, i):
        self.num += 1
        if self.num == 1:
            return 0;
        return 1 if i==0 else 0;
    def name(self):
        return "Opositer"
    def reload(self):
        self.last=0
        self.num = 0
class p20_1:
    def __init__(self):
        self.num = 0
        self.last = 0
    def next(self, i):
        self.num += 1
        if self.num == 1:
            return 0;
        return not (self.num % 20)
    def name(self):
        return "20Lover"
    def reload(self):
        self.last=0
        self.num = 0
class pHurt :
    def __init__(self):
        self.num  = 0
        self.trigger = 0
        self.last = 0
    def next(self, i):
        self.num += 1
        if self.num == 1:
            return 0;
        if i == 1:
            self.trigger = 1
        return self.trigger
    def name(self):
        return "Hurter"
    def reload(self):
        self.last=0
        self.num = 0
        self.trigger = 0

class me:
    def __init__(self):
        self.num = 0
        self.last = 0
        self.coop = 0
        self.dis = 0
    def next(self, i):
        self.num += 1
        if i == 0:
            self.coop += 1
        else:
            self.dis += 1
        if self.num <= 5:
            return 0;
        rate = self.coop / self.num
        if rate > 0.99:
            return 0
        elif rate < 0.99:
            return 1
        else:
            return i
    def name(self):
        return "me"
    def reload(self):
        self.last=0
        self.num = 0
        self.coop = 0
        self.dis = 0

# [p0(), p1(), pRepeat(), pOposite(), p20_1(), pHurt()]
playerX = [p0(), p1(), pRepeat(), pOposite(), p20_1(), pHurt(), me()]
playerY = [p0(), p1(), pRepeat(), pOposite(), p20_1(), pHurt(), me()]
result = [[0 for _ in range(len(playerY))] for _ in range(len(playerX))]
series = [[0 for _ in range(len(playerY))] for _ in range(len(playerX))]
company = [0 for _ in range(len(playerX))]


for i in range(len(playerX)):
    for j in range(len(playerY)):
        s = 0
        for _ in range(200):
            a = playerX[i].next(playerY[j].last)  #1 играк сыграл в зависимости от прошлого хода 2 игрока
            b = playerY[j].next(playerX[i].last)  #2 играк сыграл
            if a:
                if b:
                    result[i][j] += 1
                    if s > series[i][j]:
                        series[i][j] = s
                    s=0
                else:
                    result[i][j] += 5
                    s += 1
            else:
                if s > series[i][j]:
                    series[i][j] = s
                s = 0
                if b == 0:
                    result[i][j] += 3
            if s > series[i][j]:
                series[i][j] = s
            playerX[i].last = a #запоминание своего последнего хода
            playerY[j].last = b
            # print(f"{k}: {result[i][j]} ({a}, {b})")
        playerX[i].reload()
        playerY[j].reload()


print("Сколько очков получит игрок слева, играя с игроком сверху")
print(f"        ", end=" ")
for i in range(len(playerY)):
    print(f"{playerY[i].name():>8}", end=" ")
print()
for i in range(len(playerX)):
    print(f"{playerX[i].name():>8}", end="|")
    for j in range(len(playerY)):
        print(f"{result[i][j]:>8}", end=" ")
    print()

print("Результат, если баллы набирают только 1-е игроки, но не 2-е(не компания)")
for i in range(len(playerX)):
    sum = 0
    for j in range(len(playerY)):
        sum += result[i][j]
    print(f"{playerX[i].name():>8} have {sum} points")

print("Результат, если играет компания")
for i in range(len(playerX)):
    sum = 0
    for j in range(len(playerY)):
        sum += result[i][j]
    print(f"{playerX[i].name():>8} have {sum - result[i][i]} points")

print("Максимальная серия игрока слева, играя с игроком сверху")
print(f"        ", end=" ")
for i in range(len(playerY)):
    print(f"{playerY[i].name():>8}", end=" ")
print()
for i in range(len(playerX)):
    print(f"{playerX[i].name():>8}", end="|")
    for j in range(len(playerY)):
        print(f"{series[i][j]:>8}", end=" ")
    print()

print("Максимальная серия для игроков слева(не компания)")
for i in range(len(playerX)):
    mx = 0
    for j in range(len(playerY)):
        if series[i][j] > mx:
            mx = series[i][j]
    print(f"Max sery of {playerX[i].name():>8}: {mx}")
