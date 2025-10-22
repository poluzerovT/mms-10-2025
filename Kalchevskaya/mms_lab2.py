from typing import List, Tuple, Callable

# Таблица выигрышей
W = [
    [3, 0],  # i=0 (сотрудничать)
    [5, 1]   # i=1 (предать)
]

class Strategy:
    def __init__(self, name: str, function: Callable):
        self.name = name
        self.function = function
        self.history = []
        self.opponent_history = []
        self.score = 0
    
    def decide(self, opponent_history: List[int]) -> int:
        decision = self.function(self.history, opponent_history)
        self.history.append(decision)
        return decision
    
    def add_result(self, my_decision: int, opponent_decision: int, score: int):
        self.opponent_history.append(opponent_decision)
        self.score += score

# Стратегии
def alex_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return 1

def bob_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return 0

def clara_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:  # первый ход
        return 0
    return opponent_history[-1]  # последний ход оппонента

def denis_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:  # первый ход
        return 0
    return 1 - opponent_history[-1]  # обратное к последнему ходу оппонента

def emma_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    turn_number = len(my_history) + 1
    if turn_number % 20 == 0:  # каждая 20-я партия
        return 1
    return 0

def frida_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:  # первый ход
        return 0
    # 0 до тех пор, пока у опонента 0, затем 1
    if all(x == 0 for x in opponent_history):
        return 0
    return 1
def george_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    
    total_rounds = len(opponent_history)
    
    # 1. ПРОТИВ Emma - МАКСИМАЛЬНАЯ ЭКСПЛУАТАЦИЯ (ПЕРВЫМ!)
    if total_rounds >= 20:
        # Определяем цикл Emma
        for i in range(max(0, total_rounds-20), total_rounds):
            if (i + 1) % 20 == 0:
                if opponent_history[i] != 1:
                    break
            else:
                if opponent_history[i] != 0:
                    break
        else:
            # Emma идентифицирована - всегда предаем!
            return 1
    
    # 2. ПОЛНОЕ ДОМИНИРОВАНИЕ НАД BOB И ДОВЕРЧИВЫМИ
    if total_rounds >= 3 and all(x == 0 for x in opponent_history):
        return 1
    
    # 3. ПРОТИВ ALEX - ЗАЩИТА
    if all(x == 1 for x in opponent_history):
        if total_rounds % 5 == 0:
            return 0
        return 1
    
    # 4. АКТИВНОЕ СОЗДАНИЕ ДОМИНИРУЮЩИХ СЕРИЙ
    if total_rounds >= 3:
        recent_3 = opponent_history[-3:]
        recent_coop = recent_3.count(0)
        if recent_coop >= 2:
            return 1
    
    # 5. ПРОТИВ TIT-FOR-TAT
    if total_rounds >= 5:
        tit_for_tat = True
        for i in range(1, min(6, len(opponent_history))):
            if i < len(my_history) and opponent_history[i] != my_history[i-1]:
                tit_for_tat = False
                break
        if tit_for_tat:#0 0 1 0 0 1 
            return 1 if (total_rounds - 1) % 3 == 2 else 0
    
    # 6. ПРОТИВ Frida - ПРОСТАЯ ЛОГИКА
    if total_rounds >= 2:
        if all(x == 0 for x in opponent_history):
            return 1
        return 1
    
    # 7. ПРОТИВ Denis
    if total_rounds >= 4:
        denis_pattern = True
        for i in range(1, min(5, len(opponent_history))):
            if i >= len(my_history): 
                break
            expected = 1 - my_history[i-1]
            if opponent_history[i] != expected:
                denis_pattern = False
                break
        if denis_pattern:
            return total_rounds % 2
    
    # 8. АДАПТИВНАЯ АГРЕССИЯ
    if total_rounds >= 8:
        overall_coop_rate = opponent_history.count(0) / total_rounds
        if overall_coop_rate >= 0.6:
            cycle_pos = (total_rounds - 1) % 5
            return 0 if cycle_pos < 2 else 1
        if overall_coop_rate >= 0.3:
            if opponent_history[-1] == 0:
                if len(my_history) >= 1 and my_history[-1] == 0:
                    return 1
                return 0
            else:
                return 1
    
    # 9. УЛЬТИМАТИВНОЕ ПРАВИЛО
    if opponent_history[-1] == 0:
        return 1
    
    return 1

def simulate_game(strategy1: Strategy, strategy2: Strategy, rounds: int = 200) -> Tuple[int, int, List[Tuple[int, int]]]:
    """Симулирует игру между двумя стратегиями"""
    for round_num in range(rounds):
        # Получаем решения
        s1_decision = strategy1.decide(strategy2.history)
        s2_decision = strategy2.decide(strategy1.history)
        
        # Вычисляем выигрыши
        s1_score = W[s1_decision][s2_decision]
        s2_score = W[s2_decision][s1_decision]
        
        # Обновляем историю и счет
        strategy1.add_result(s1_decision, s2_decision, s1_score)
        strategy2.add_result(s2_decision, s1_decision, s2_score)
    
    return strategy1.score, strategy2.score, list(zip(strategy1.history, strategy2.history))

def calculate_dominant_series(history: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Вычисляет длину наибольшей доминирующей серии для каждого игрока"""
    max_s1_dominant = 0
    max_s2_dominant = 0
    current_s1_dominant = 0
    current_s2_dominant = 0
    
    for s1_move, s2_move in history:
        s1_score = W[s1_move][s2_move]
        s2_score = W[s2_move][s1_move]
        
        # Проверяем доминирование первого игрока (5 vs 0)
        if s1_score == 5 and s2_score == 0:
            current_s1_dominant += 1
            current_s2_dominant = 0
        # Проверяем доминирование второго игрока (5 vs 0)
        elif s2_score == 5 and s1_score == 0:
            current_s2_dominant += 1
            current_s1_dominant = 0
        else:
            current_s1_dominant = 0
            current_s2_dominant = 0
        
        max_s1_dominant = max(max_s1_dominant, current_s1_dominant)
        max_s2_dominant = max(max_s2_dominant, current_s2_dominant)
    
    return max_s1_dominant, max_s2_dominant

def print_table(headers, data):
    """Печатает таблицу с выравниванием"""
    # Вычисляем ширину колонок
    col_widths = []
    for i in range(len(headers)):
        max_width = len(headers[i])
        for row in data:
            max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)
    
    # Печатаем заголовки
    header_line = ""
    for i, header in enumerate(headers):
        header_line += header.ljust(col_widths[i])
    print(header_line)
    print("-" * len(header_line))
    
    # Печатаем данные
    for row in data:
        row_line = ""
        for i, cell in enumerate(row):
            row_line += str(cell).ljust(col_widths[i])
        print(row_line)

def print_ranking(title, data, reverse=True):
    """Печатает рейтинг стратегий"""
    print(f"\n{title}:")
    print("-" * 50)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=reverse)
    for i, (strategy, value) in enumerate(sorted_data, 1):
        print(f"{i}. {strategy}: {value}")

def main():
    strategies = [
        Strategy("Alex", alex_strategy),
        Strategy("Bob", bob_strategy),
        Strategy("Clara", clara_strategy),
        Strategy("Denis", denis_strategy),
        Strategy("Emma", emma_strategy),
        Strategy("Frida", frida_strategy),
        Strategy("George", george_strategy)
    ]
    
    # Таблицы для результатов
    total_scores_table = []
    dominant_series_table = []
    
    # Словари для рейтингов
    total_scores_ranking = {name: 0 for name in [s.name for s in strategies]}
    dominant_series_ranking = {name: 0 for name in [s.name for s in strategies]}
    
    # Симулируем все пары стратегий
    for i, s1 in enumerate(strategies):
        for j, s2 in enumerate(strategies):
            if i < j:  # Чтобы избежать дублирования
                # Сбрасываем историю и счет
                s1.history = []
                s1.opponent_history = []
                s1.score = 0
                s2.history = []
                s2.opponent_history = []
                s2.score = 0
                
                # Симулируем игру
                s1_score, s2_score, history = simulate_game(s1, s2)
                s1_dominant, s2_dominant = calculate_dominant_series(history)
                
                total_scores_table.append([s1.name, s2.name, s1_score, s2_score, s1_score + s2_score])
                dominant_series_table.append([s1.name, s2.name, s1_dominant, s2_dominant])
                
                # Обновляем рейтинги очков
                total_scores_ranking[s1.name] += s1_score
                total_scores_ranking[s2.name] += s2_score
                
                # Обновляем рейтинги доминирующих серий (сумма максимальных серий)
                dominant_series_ranking[s1.name] += s1_dominant
                dominant_series_ranking[s2.name] += s2_dominant
    
    # Печатаем таблицу общих очков
    print("ТАБЛИЦА ОБЩИХ ОЧКОВ:")
    print("=" * 80)
    headers = ["Стратегия 1", "Стратегия 2", "Очки 1", "Очки 2", "Сумма очков"]
    print_table(headers, total_scores_table)
    
    # Рейтинг стратегий по сумме очков
    print_ranking("РЕЙТИНГ СТРАТЕГИЙ ПО СУММЕ ОЧКОВ (все партии)", total_scores_ranking)
    
    # Печатаем таблицу доминирующих серий
    print("\n\nТАБЛИЦА ДОМИНИРУЮЩИХ СЕРИЙ:")
    print("=" * 80)
    headers = ["Стратегия 1", "Стратегия 2", "Макс. доминирование 1", "Макс. доминирование 2"]
    print_table(headers, dominant_series_table)
    
    # Рейтинг стратегий по сумме доминирующих серий
    print_ranking("РЕЙТИНГ СТРАТЕГИЙ ПО СУММЕ ДОМИНИРУЮЩИХ СЕРИЙ", dominant_series_ranking)
    
    # Итоговый анализ лидеров
    print("\n\n" + "=" * 80)
    print("ИТОГОВЫЙ АНАЛИЗ ЛИДЕРОВ ПО МЕТРИКАМ")
    print("=" * 80)
    
    # Лидер по очкам
    leader_score = max(total_scores_ranking.items(), key=lambda x: x[1])
    print(f" ЛИДЕР ПО ОЧКАМ: {leader_score[0]} ({leader_score[1]} очков)")
    
    # Лидер по доминирующим сериям (сумма)
    leader_dominant_sum = max(dominant_series_ranking.items(), key=lambda x: x[1])
    print(f" ЛИДЕР ПО СУММЕ ДОМИНИРУЮЩИХ СЕРИЙ: {leader_dominant_sum[0]} ({leader_dominant_sum[1]} серий)")

if __name__ == "__main__":
    main()