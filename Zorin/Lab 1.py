import random
from time import time
from random import random as rnd
import matplotlib.pyplot as plt
#SEED = int(time() * 100)
SEED = 1
random.seed(SEED)


def flipCoin(odds=0.5):
    return rnd() <= odds


def flipCoin100(odds=0.5):
    total = 0
    curStreak = 0
    maxStreak = 0
    for i in range(100):
        result = flipCoin(odds)
        total += result
        if result:
            curStreak += 1
        else:
            curStreak = 0
        if curStreak > maxStreak:
            maxStreak = curStreak
    return total, maxStreak


def partOne():
    TOTAL_RUNS = int(1e5)
    summary = 0
    streakCnt = 0
    decades = [0] * 10
    countByCount = [0] * 101
    over60 = 0
    for run in range(TOTAL_RUNS):
        eagles, streak = flipCoin100()
        summary += eagles
        decades[eagles // 10 - eagles // 100] += 1
        countByCount[eagles] += 1
        if streak >= 5:
            streakCnt += 1
        if eagles > 60:
            over60 +=1
    over60 /= TOTAL_RUNS
    average = summary / TOTAL_RUNS
    streakprob = streakCnt / TOTAL_RUNS
    decadesprobs = [0] * 10
    for i in range(10):
        decadesprobs[i] = decades[i] / TOTAL_RUNS

    lBest = -1
    rBest = -1
    l = 0
    r = 0
    curSum = countByCount[0]
    lookingForprob = .95
    while l <= r <= 101:
        prob = curSum / TOTAL_RUNS
        if prob >= lookingForprob:
            if lBest == -1 or r - l < rBest - lBest:
                lBest = l
                rBest = r
            curSum -= countByCount[l]
            l += 1
        else:
            r += 1
            if r <= 100:
                curSum += countByCount[r]

    print(f"больше 60 с шансом {over60}")
    for i in range(10):
        print(f"for probs to get in [{i*10}, {(i+1)*10}) are {decadesprobs[i]} and total appear {decades[i]}")
    print(f"prob {lookingForprob} may appear on [{lBest},{rBest}]")

    print(f"Average is {average}, streak of 5 has prob {streakprob}")


def partTwo():

    stepCnt = 101

    averages = [0] * stepCnt
    widths = [0] * stepCnt
    streakprobs = [0] * stepCnt
    longestStreaks = [0] * stepCnt
    probs = [0] * stepCnt
    i = 0
    lookingForprob = .95

    for prob in range(0, 101, 100//(stepCnt-1)):
      #  print(prob, i)
        probF = prob / 100
        probs[i] = probF
        TOTAL_RUNS = int(1e3)
        summary = 0
        countByCount = [0] * 101
        for run in range(TOTAL_RUNS):
            eagles, streak = flipCoin100(probF)
            summary += eagles
            countByCount[eagles] += 1
            longestStreaks[i] += streak
            if streak >= 5:
                streakprobs[i] += 1

        averages[i] = summary / TOTAL_RUNS
        longestStreaks[i] /= TOTAL_RUNS
        streakprobs[i] /= TOTAL_RUNS

        lBest = -1
        rBest = -1
        l = 0
        r = 1
        curSum = countByCount[0]
        while l < r <= 101:
            prob = curSum / TOTAL_RUNS
            if prob >= lookingForprob:
                if lBest == -1 or r - l < rBest - lBest:
                    lBest = l
                    rBest = r
                curSum -= countByCount[l]
                l += 1
            else:
                if r <= 100:
                    curSum += countByCount[r]
                r += 1
        widths[i] = rBest-lBest
        i += 1

    labelAverage = "Среднее значение"
    labelWidth = f"Ширина интервала, где будет {lookingForprob} всех бросков"
    labelStreak = "Вероятность серии из 5 орлов"
    labelLongest = "Ожидаемая максимальная серия"

    plt.figure(labelAverage)
    plt.plot(probs, averages, label='Среднеее значение')
    plt.grid()
    plt.legend()
    plt.title("Зависимости от вероятности выпадения орла")
    plt.xlabel('Вероятность выпадения орла, [%]')
    plt.ylabel('Число орлов на 100 бросков')

    plt.figure(labelWidth)
    plt.plot(probs, widths, label='Ширина предсказанного интервала')
    plt.grid()
    plt.legend()
    plt.title("Зависимости от вероятности выпадения орла")
    plt.xlabel('Вероятность выпадения орла, [%]')
    plt.ylabel('Ширина предсказанного интервала')

    plt.figure(labelStreak)
    plt.plot(probs, streakprobs, label='Вероятность серии из 5 орлов')
    plt.grid()
    plt.legend()
    plt.title("Зависимости от вероятности выпадения орла")
    plt.xlabel('Вероятность выпадения орла, [%]')
    plt.ylabel('Вероятность серии из 5 орлов')

    plt.figure(labelLongest)
    plt.plot(probs, longestStreaks, label='Длина максимальной серии')
    plt.grid()
    plt.legend()
    plt.title("Зависимости от вероятности выпадения орла")
    plt.xlabel('Вероятность выпадения орла, [%]')
    plt.ylabel('Длина макс. серии')

    plt.show()

print(f"current seed is {SEED}")
partOne()
partTwo()