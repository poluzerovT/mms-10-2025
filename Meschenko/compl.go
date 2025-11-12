package main

import (
	"fmt"
	"strings"
)

type Strategy func(historySelf, historyOpp []int) int

var W = [2][2]int{
	{3, 0},
	{5, 1},
}

// --- стратегии ---

// Alex - всегда 1
func Alex(_ []int, _ []int) int { return 1 }

// Bob - всегда 0
func Bob(_ []int, _ []int) int { return 0 }

// Clara - сначала 0, потом последнее значение оппонента
func Clara(_ []int, historyOpp []int) int {
	if len(historyOpp) == 0 {
		return 0
	}
	return historyOpp[len(historyOpp)-1]
}

// Denis - сначала 0, потом обратное к последнему выбору оппонента
func Denis(_ []int, historyOpp []int) int {
	if len(historyOpp) == 0 {
		return 0
	}
	last := historyOpp[len(historyOpp)-1]
	if last == 0 {
		return 1
	}
	return 0
}

// Emma - всегда 0, но каждая 20-я партия - 1
func Emma(historySelf []int, _ []int) int {
	// партия нумеруется с 0, поэтому 19,39,... -> индекс %20==19
	if len(historySelf)%20 == 19 {
		return 1
	}
	return 0
}

// Frida - 0 до тех пор, пока у оппонента 0; затем 1
func Frida(_ []int, historyOpp []int) int {
	if len(historyOpp) == 0 {
		return 0
	}
	// если у оппонента когда-либо был 1, то ответ 1
	for _, v := range historyOpp {
		if v == 1 {
			return 1
		}
	}
	return 0
}

// George - первые 50 партий 0, следующие 50 партий 1, затем повторять (на 200 партий достаточно)
func George(historySelf []int, _ []int) int {
	turn := len(historySelf) // 0-based
	// pattern: 50 zeros, 50 ones, 50 zeros, 50 ones, ...
	block := (turn / 50) % 2
	if block == 0 {
		return 0
	}
	return 1
}

// --- симуляция одной встречи ---
// возвращает: scoreA, scoreB, maxDomA, maxDomB
func playMatch(strA, strB Strategy, rounds int) (int, int, int, int) {
	hA := make([]int, 0, rounds)
	hB := make([]int, 0, rounds)
	scoreA, scoreB := 0, 0
	curDomA, curDomB := 0, 0
	maxDomA, maxDomB := 0, 0

	for t := 0; t < rounds; t++ {
		a := strA(hA, hB)
		b := strB(hB, hA)

		// защита: принудительно нормализуем ходы в {0,1}
		if a != 0 {
			a = 1
		}
		if b != 0 {
			b = 1
		}

		hA = append(hA, a)
		hB = append(hB, b)

		gA := W[a][b]
		gB := W[b][a]
		scoreA += gA
		scoreB += gB

		// доминирующая партия: один получает 5, другой 0
		if gA == 5 && gB == 0 {
			curDomA++
			curDomB = 0
		} else if gB == 5 && gA == 0 {
			curDomB++
			curDomA = 0
		} else {
			curDomA = 0
			curDomB = 0
		}
		if curDomA > maxDomA {
			maxDomA = curDomA
		}
		if curDomB > maxDomB {
			maxDomB = curDomB
		}
	}
	return scoreA, scoreB, maxDomA, maxDomB
}

func main() {
	rounds := 200
	strategies := map[string]Strategy{
		"Alex":   Alex,
		"Bob":    Bob,
		"Clara":  Clara,
		"Denis":  Denis,
		"Emma":   Emma,
		"Frida":  Frida,
		"George": George,
	}

	// Список имён для детерминированного обхода
	names := []string{"Alex", "Bob", "Clara", "Denis", "Emma", "Frida", "George"}

	type Result struct {
		A, B             string
		ScoreA, ScoreB   int
		MaxDomA, MaxDomB int
	}

	results := make([]Result, 0, len(names)*len(names))

	// запускаем для всех упорядоченных пар (A vs B). Включаем и самопротивостояния.
	for _, a := range names {
		for _, b := range names {
			scoreA, scoreB, maxDomA, maxDomB := playMatch(strategies[a], strategies[b], rounds)
			results = append(results, Result{
				A: a, B: b,
				ScoreA: scoreA, ScoreB: scoreB,
				MaxDomA: maxDomA, MaxDomB: maxDomB,
			})
		}
	}

	// Вывод таблицы: общие очки
	fmt.Println(strings.Repeat("=", 72))
	fmt.Println("Таблица 1: Общие числа очков (игрок A vs игрок B)")
	fmt.Println(strings.Repeat("-", 72))
	fmt.Printf("%-10s %-10s %10s %10s\n", "Игрок A", "Игрок B", "Очки A", "Очки B")
	fmt.Println(strings.Repeat("-", 72))
	for _, r := range results {
		fmt.Printf("%-10s %-10s %10d %10d\n", r.A, r.B, r.ScoreA, r.ScoreB)
	}
	fmt.Println(strings.Repeat("=", 72))

	// Вывод таблицы: длина наибольшей доминирующей серии
	fmt.Println("Таблица 2: Длина наибольшей доминирующей серии (5 vs 0)")
	fmt.Println(strings.Repeat("-", 72))
	fmt.Printf("%-10s %-10s %12s %12s\n", "Игрок A", "Игрок B", "Серия A", "Серия B")
	fmt.Println(strings.Repeat("-", 72))
	for _, r := range results {
		fmt.Printf("%-10s %-10s %12d %12d\n", r.A, r.B, r.MaxDomA, r.MaxDomB)
	}
	fmt.Println(strings.Repeat("=", 72))
}
