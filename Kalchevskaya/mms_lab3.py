import random
import math
from typing import List, Tuple, Callable, Dict

# Таблица выигрышей
W = [
    [3, 0],  # i=0 (сотрудничать)
    [5, 1]   # i=1 (предать)
]

class Strategy:
    def __init__(self, name: str, function: Callable, stochastic: bool = False):
        self.name = name
        self.function = function
        self.stochastic = stochastic
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
    
    def reset(self):
        self.history = []
        self.opponent_history = []
        self.score = 0

# Детерминированные стратегии (из предыдущей работы)
def alex_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return 1

def bob_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return 0

def clara_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    return opponent_history[-1]

def denis_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    return 1 - opponent_history[-1]

def emma_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    turn_number = len(my_history) + 1
    if turn_number % 20 == 0:
        return 1
    return 0

def frida_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    if all(x == 0 for x in opponent_history):
        return 0
    return 1

def george_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    
    total_rounds = len(opponent_history)
    
    # Против Emma
    if total_rounds >= 20:
        for i in range(max(0, total_rounds-20), total_rounds):
            if (i + 1) % 20 == 0:
                if opponent_history[i] != 1:
                    break
            else:
                if opponent_history[i] != 0:
                    break
        else:
            return 1
    
    # Против Bob
    if total_rounds >= 3 and all(x == 0 for x in opponent_history):
        return 1
    
    # Против Alex
    if all(x == 1 for x in opponent_history):
        if total_rounds % 5 == 0:
            return 0
        return 1
    
    # Активное создание доминирующих серий
    if total_rounds >= 3:
        recent_3 = opponent_history[-3:]
        recent_coop = recent_3.count(0)
        if recent_coop >= 2:
            return 1
    
    # Против Tit-for-Tat
    if total_rounds >= 5:
        tit_for_tat = True
        for i in range(1, min(6, len(opponent_history))):
            if i < len(my_history) and opponent_history[i] != my_history[i-1]:
                tit_for_tat = False
                break
        if tit_for_tat:
            return 1 if (total_rounds - 1) % 3 == 2 else 0
    
    # Против Frida
    if total_rounds >= 2:
        if all(x == 0 for x in opponent_history):
            return 1
        return 1
    
    # Против Denis
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
    
    # Адаптивная агрессия
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
    
    if opponent_history[-1] == 0:
        return 1
    
    return 1

# Стохастические стратегии
def hank_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return random.randint(0, 1)

def ivan_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    return 0 if random.random() < 0.9 else 1

def jack_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    if opponent_history[-1] == 0:
        return 0
    else:
        return 0 if random.random() < 0.25 else 1

def kevin_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    if random.random() < 0.25:
        return 1 - opponent_history[-1]  # противоположное
    else:
        return opponent_history[-1]  # повторяет

def lucas_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    # Для совместимости с текущим кодом - эмуляция "до начала игры"
    if not my_history:  # Если это первый ход
        lucas_strategy.cycle_length = random.randint(1, 50)#создаю атрибут
    
    turn_number = len(my_history) + 1
    
    # Каждые cycle_length ходов выдает 1, остальные - 0
    if turn_number % lucas_strategy.cycle_length == 0:
        return 1
    return 0

# Добавляем reset функцию
def reset_lucas():
    if hasattr(lucas_strategy, 'cycle_length'):#проверка на наличие атрибута
        delattr(lucas_strategy, 'cycle_length')#удаляем атрибут

def max_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not hasattr(max_strategy, 'current_mode'):
        max_strategy.current_mode = 0
        max_strategy.moves_left = random.randint(0, 20)
    
    # Сначала возвращаем текущий ход
    current_decision = max_strategy.current_mode
    
    # Затем обновляем счетчик
    max_strategy.moves_left -= 1
    
    # Если ходы закончились, переключаем режим для СЛЕДУЮЩЕГО хода
    if max_strategy.moves_left == 0:
        max_strategy.current_mode = 1 - max_strategy.current_mode
        max_strategy.moves_left = random.randint(0, 20)
    
    return current_decision
def reset_max():
    if hasattr(max_strategy, 'current_mode'):
        delattr(max_strategy, 'current_mode')
    if hasattr(max_strategy, 'moves_left'):
        delattr(max_strategy, 'moves_left')

def natan_strategy(my_history: List[int], opponent_history: List[int]) -> int:
    if not opponent_history:
        return 0
    
    total_rounds = len(opponent_history)
    
    # Адаптивная стохастическая стратегия
    coop_rate = opponent_history.count(0) / total_rounds
    
    if total_rounds < 10:
        # Начальная фаза - более сотрудничающая
        prob_cooperate = 0.8
    else:
        # Адаптируемся к поведению оппонента
        if coop_rate > 0.7:
            # Оппонент очень сотрудничающий - иногда предаем
            prob_cooperate = 0.6
        elif coop_rate > 0.4:
            # Баланс - отвечаем взаимностью
            prob_cooperate = 0.5
        else:
            # Оппонент агрессивный - защищаемся
            prob_cooperate = 0.3
    
    # Учитываем последние ходы
    if len(opponent_history) >= 3:
        recent = opponent_history[-3:]
        if all(x == 0 for x in recent):
            prob_cooperate += 0.2
        elif all(x == 1 for x in recent):
            prob_cooperate -= 0.2
    
    # Ограничиваем вероятность
    prob_cooperate = max(0.1, min(0.9, prob_cooperate))
    
    return 0 if random.random() < prob_cooperate else 1

def simulate_game(strategy1: Strategy, strategy2: Strategy, rounds: int = 200) -> Tuple[int, int, List[Tuple[int, int]]]:
    """Симулирует одну игру между двумя стратегиями"""
    for round_num in range(rounds):
        s1_decision = strategy1.decide(strategy2.history)
        s2_decision = strategy2.decide(strategy1.history)
        
        s1_score = W[s1_decision][s2_decision]
        s2_score = W[s2_decision][s1_decision]
        
        strategy1.add_result(s1_decision, s2_decision, s1_score)
        strategy2.add_result(s2_decision, s1_decision, s2_score)
    
    return strategy1.score, strategy2.score, list(zip(strategy1.history, strategy2.history))

def calculate_statistics(scores: List[int]) -> Dict[str, float]:
    """Вычисляет статистические характеристики выборки"""
    if not scores:
        return {}
    
    n = len(scores)
    mean = sum(scores) / n
    
    # Дисперсия
    variance = sum((x - mean) ** 2 for x in scores) / (n - 1) if n > 1 else 0
    
    # Медиана
    sorted_scores = sorted(scores)# по возрастанию
    if n % 2 == 0:
        median = (sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2# четное берем среднее из двух центральных
    else:
        median = sorted_scores[n//2]#берем серединку
    
    # Мода (гистограммный метод)
    k = int(math.log2(1 + n))  # число интервалов
    if k < 1:
        k = 1
    
    min_score, max_score = min(scores), max(scores)
    if min_score == max_score:
        mode = min_score
    else:
        bin_width = (max_score - min_score) / k
        bins = [0] * k
        for score in scores:
            bin_index = min(int((score - min_score) / bin_width), k - 1)
            bins[bin_index] += 1
        
        max_bin_index = bins.index(max(bins))
        mode_lower = min_score + max_bin_index * bin_width
        mode_upper = min_score + (max_bin_index + 1) * bin_width
        mode = (mode_lower + mode_upper) / 2
    
    return {
        'mean': mean,
        'variance': variance,
        'median': median,
        'mode': mode,
        'min': min_score,
        'max': max_score,
        'std': math.sqrt(variance) if variance > 0 else 0
    }

def simulate_multiple_games(strategy1: Strategy, strategy2: Strategy, 
                          num_simulations: int = 1000, rounds: int = 200) -> Dict:
    """Проводит множественные симуляции и возвращает статистику"""
    s1_scores = []
    s2_scores = []
    
    for _ in range(num_simulations):
        # Сбрасываем стратегии
        strategy1.reset()
        strategy2.reset()
        
        # Симулируем игру
        s1_score, s2_score, _ = simulate_game(strategy1, strategy2, rounds)
        s1_scores.append(s1_score)
        s2_scores.append(s2_score)
    
    # Статистика по очкам
    s1_stats = calculate_statistics(s1_scores)
    s2_stats = calculate_statistics(s2_scores)
    
    return {
        'strategy1_scores': s1_stats,
        'strategy2_scores': s2_stats,
        'raw_scores': (s1_scores, s2_scores)
    }

def print_table(headers, data):
    """Печатает таблицу с выравниванием"""
    col_widths = []
    for i in range(len(headers)):
        max_width = len(headers[i])
        for row in data:
            max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)
    
    header_line = ""
    for i, header in enumerate(headers):
        header_line += header.ljust(col_widths[i])
    print(header_line)
    print("-" * len(header_line))
    
    for row in data:
        row_line = ""
        for i, cell in enumerate(row):
            row_line += str(cell).ljust(col_widths[i])
        print(row_line)

def print_statistics_table(strategy_pairs_stats):
    """Печатает таблицу статистических характеристик"""
    print("\n" + "="*100)
    print("СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ СТРАТЕГИЙ")
    print("="*100)
    
    headers = ["Пара стратегий", "Стратегия", "Среднее", "Медиана", "Мода", "Дисперсия", "Станд. откл.", "Мин", "Макс"]
    data = []
    
    for pair, stats in strategy_pairs_stats.items():
        s1, s2 = pair.split(" vs ")
        
        # Статистика для первой стратегии
        s1_stats = stats['strategy1_scores']
        data.append([
            f"{s1} vs {s2}",
            s1,
            f"{s1_stats['mean']:.1f}",
            f"{s1_stats['median']:.1f}",
            f"{s1_stats['mode']:.1f}",
            f"{s1_stats['variance']:.1f}",
            f"{s1_stats['std']:.1f}",
            s1_stats['min'],
            s1_stats['max']
        ])
        
        # Статистика для второй стратегии
        s2_stats = stats['strategy2_scores']
        data.append([
            f"{s1} vs {s2}",
            s2,
            f"{s2_stats['mean']:.1f}",
            f"{s2_stats['median']:.1f}",
            f"{s2_stats['mode']:.1f}",
            f"{s2_stats['variance']:.1f}",
            f"{s2_stats['std']:.1f}",
            s2_stats['min'],
            s2_stats['max']
        ])
    
    print_table(headers, data)

def calculate_overall_rankings(strategy_pairs_stats, all_strategies):
    """Вычисляет общие рейтинги стратегий"""
    total_scores = {name: 0 for name in all_strategies}
    total_games = {name: 0 for name in all_strategies}
    
    for pair, stats in strategy_pairs_stats.items():
        s1, s2 = pair.split(" vs ")
        total_scores[s1] += stats['strategy1_scores']['mean']
        total_scores[s2] += stats['strategy2_scores']['mean']
        total_games[s1] += 1
        total_games[s2] += 1
    
    # Вычисляем средний счет за игру
    avg_scores = {}
    for strategy in all_strategies:
        if total_games[strategy] > 0:
            avg_scores[strategy] = total_scores[strategy] / total_games[strategy]
        else:
            avg_scores[strategy] = 0
    
    return avg_scores

def main():
    # Инициализация случайного seed для воспроизводимости
    random.seed(42)
    
    # Создаем стратегии
    deterministic_strategies = [
        Strategy("Alex", alex_strategy),
        Strategy("Bob", bob_strategy),
        Strategy("Clara", clara_strategy),
        Strategy("Denis", denis_strategy),
        Strategy("Emma", emma_strategy),
        Strategy("Frida", frida_strategy),
        Strategy("George", george_strategy)
    ]
    
    stochastic_strategies = [
        Strategy("Hank", hank_strategy, stochastic=True),
        Strategy("Ivan", ivan_strategy, stochastic=True),
        Strategy("Jack", jack_strategy, stochastic=True),
        Strategy("Kevin", kevin_strategy, stochastic=True),
        Strategy("Lucas", lucas_strategy, stochastic=True),
        Strategy("Max", max_strategy, stochastic=True),
        Strategy("Natan", natan_strategy, stochastic=True)
    ]
    
    all_strategies = deterministic_strategies + stochastic_strategies
    all_strategy_names = [s.name for s in all_strategies]
    
    print("ЗАПУСК MMC СИМУЛЯЦИЙ...")
    print(f"Всего стратегий: {len(all_strategies)}")
    print(f"Детерминированных: {len(deterministic_strategies)}")
    print(f"Стохастических: {len(stochastic_strategies)}")
    print(f"Число симуляций на пару: 1000")
    print(f"Число раундов в игре: 200")
    
    strategy_pairs_stats = {}
    total_pairs = len(all_strategies) * (len(all_strategies) - 1) // 2
    current_pair = 0
    
    # Симулируем все пары стратегий
    for i, s1 in enumerate(all_strategies):
        for j, s2 in enumerate(all_strategies):
            if i < j:  # Избегаем дублирования
                current_pair += 1
                print(f"Прогресс: {current_pair}/{total_pairs} - {s1.name} vs {s2.name}")
                
                # Для пар с хотя бы одной стохастической стратегией используем MMC
                if s1.stochastic or s2.stochastic:
                    stats = simulate_multiple_games(s1, s2, num_simulations=1000)
                else:
                    # Для детерминированных пар достаточно одной симуляции
                    s1.reset()
                    s2.reset()
                    s1_score, s2_score, _ = simulate_game(s1, s2)
                    
                    stats = {
                        'strategy1_scores': calculate_statistics([s1_score]),
                        'strategy2_scores': calculate_statistics([s2_score]),
                        'raw_scores': ([s1_score], [s2_score])
                    }
                
                strategy_pairs_stats[f"{s1.name} vs {s2.name}"] = stats
    
    # Печатаем результаты
    print_statistics_table(strategy_pairs_stats)
    
    # Общие рейтинги
    avg_scores = calculate_overall_rankings(strategy_pairs_stats, all_strategy_names)
    
    print("\n" + "="*60)
    print("ОБЩИЙ РЕЙТИНГ СТРАТЕГИЙ (по среднему количеству очков)")
    print("="*60)
    
    sorted_scores = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (strategy, score) in enumerate(sorted_scores, 1):
        print(f"{i:2d}. {strategy:10s}: {score:.1f} очков в среднем")
    
    # Анализ лучших стратегий
    print("\n" + "="*60)
    print("АНАЛИЗ ЛУЧШИХ СТРАТЕГИЙ")
    print("="*60)
    
    top_3 = sorted_scores[:3]
    for i, (strategy, score) in enumerate(top_3, 1):
        strategy_type = "Стохастическая" if any(s.name == strategy and s.stochastic for s in all_strategies) else "Детерминированная"
        print(f"{i}. {strategy} ({strategy_type}): {score:.1f} очков")
    
    # Сравнение детерминированных и стохастических стратегий
    det_scores = [score for strat, score in sorted_scores 
                 if any(s.name == strat and not s.stochastic for s in all_strategies)]
    stoch_scores = [score for strat, score in sorted_scores 
                   if any(s.name == strat and s.stochastic for s in all_strategies)]
    
    if det_scores and stoch_scores:
        avg_det = sum(det_scores) / len(det_scores)
        avg_stoch = sum(stoch_scores) / len(stoch_scores)
        print(f"\nСредний результат детерминированных стратегий: {avg_det:.1f}")
        print(f"Средний результат стохастических стратегий: {avg_stoch:.1f}")
        
        if avg_det > avg_stoch:
            print("Детерминированные стратегии в среднем эффективнее")
        else:
            print("Стохастические стратегии в среднем эффективнее")

if __name__ == "__main__":
    main()