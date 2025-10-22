import pandas as pd
NUM_GAMES = 200
POINTS = {
    (0, 0): (3, 3),    
    (0, 1): (0, 5),   
    (1, 0): (5, 0),    
    (1, 1): (1, 1)     
}
def strat_alex(history_a, history_b):
    return 1

def strat_bob(history_a, history_b):
    return 0

def strat_clara(history_a, history_b):
    if len(history_a) == 0:
        return 0
    return history_b[-1]

def strat_denis(history_a, history_b):
    if len(history_a) == 0:
        return 0
    return 1 - history_b[-1]

def strat_emma(history_a, history_b):
    if len(history_a) % 20 == 19:  
        return 1
    return 0

def strat_frida(history_a, history_b):
    if len(history_b) == 0:
        return 0
    if 1 in history_b: 
        return 1
    return 0

def strat_george(history_a, history_b):
    if len(history_b) == 0:
        return 0
    total_games = len(history_b)
    pred_count = sum(history_b)
    if total_games >= 10:
        if pred_count / total_games > 0.8:
            return 1
        if (total_games - pred_count) / total_games > 0.8:
            if total_games % 3 == 0:
                return 1
            return 0
    game_progress = total_games / NUM_GAMES
    if game_progress > 0.8:
        return 1
    if len(history_b) >= 3:
        recent_predal_sequence = sum(history_b[-3:])
        if recent_predal_sequence >= 2:
            return 1
    return history_b[-1]

strats = {
    'Alex': strat_alex,
    'Bob': strat_bob,
    'Clara': strat_clara,
    'Denis': strat_denis,
    'Emma': strat_emma,
    'Frida': strat_frida,
    'George': strat_george
}

def play_game(strat_a, strat_b, num_games=NUM_GAMES):
    history_a = []
    history_b = []
    scores_a = []
    scores_b = []
    for _ in range(num_games):
        move_a = strat_a(history_a, history_b)
        move_b = strat_b(history_b, history_a)
        
        history_a.append(move_a)
        history_b.append(move_b)
        
        score_a, score_b = POINTS[(move_a, move_b)]
        scores_a.append(score_a)
        scores_b.append(score_b)
    return history_a, history_b, scores_a, scores_b

def calculate_dominant_series(scores_a, scores_b):
    max_series = 0
    c_series = 0
    for score_a, score_b in zip(scores_a, scores_b):
        if score_a == 5 and score_b == 0:
            c_series += 1
            max_series = max(max_series, c_series)
        else:
            c_series = 0
    
    return max_series

def main():
    total_scores = {}
    dominant_series = {}
    
    strats_list = list(strats.keys())
    for strat_name in strats_list:
        total_scores[strat_name] = {}
        dominant_series[strat_name] = {}

    for i, name_a in enumerate(strats_list):
        for j, name_b in enumerate(strats_list):
            if i == j:
                continue
                
            strat_a = strats[name_a]
            strat_b = strats[name_b]
            
            _, _, scores_a, scores_b = play_game(strat_a, strat_b)
            
            total_scores[name_a][name_b] = sum(scores_a)
            dominant_series[name_a][name_b] = calculate_dominant_series(scores_a, scores_b)

    df_scores = pd.DataFrame(total_scores).T
    df_series = pd.DataFrame(dominant_series).T

    df_scores = df_scores.astype(object)
    df_series = df_series.astype(object)

    for strat in strats_list:
        df_scores.loc[strat, strat] = '-'
        df_series.loc[strat, strat] = '-'

    print("ОБЩЕЕ ЧИСЛО ОЧКОВ")
    print("(строки - стратегия, столбцы - противник):")
    print(df_scores.to_string())
    
    print("\nДЛИНА НАИБОЛЬШЕЙ ДОМИНИРУЮЩЕЙ СЕРИИ")
    print("(когда стратегия получает +5, а противник 0):")
    print("(строки - стратегия, столбцы - противник):")
    print(df_series.to_string())

    print("\nСУММАРНЫЕ РЕЗУЛЬТАТЫ:")

    df_scores = df_scores.replace('-', 0).astype(int)
    
    total_scores_per_strat = {}
    for strat in strats_list:
        total_score = 0
        for opponent in strats_list:
            if opponent != strat:
                total_score += df_scores.loc[strat, opponent]
        total_scores_per_strat[strat] = total_score
    
    total_scores_series = pd.Series(total_scores_per_strat)
    
    print("\nСуммарные очки против всех оппонентов:")
    for strat, total in total_scores_series.items():
        print(f"{strat}: {total} очков")
    
    df_series_numeric = df_series.replace('-', 0).astype(int)
    
    avg_series_per_strat = {}
    for strat in strats_list:
        series_values = []
        for opponent in strats_list:
            if opponent != strat:
                series_values.append(df_series_numeric.loc[strat, opponent])
        avg_series_per_strat[strat] = sum(series_values) / len(series_values) if series_values else 0
    
    avg_series_series = pd.Series(avg_series_per_strat)
    
    print("\nСредняя длина доминирующей серии против всех оппонентов:")
    for strat, avg in avg_series_series.items():
        print(f"{strat}: {avg:.2f}")

    print("\nДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА:")
    
    best_by_score = total_scores_series.idxmax()
    print(f"\nЛучшая стратегия по общему количеству очков: {best_by_score} ({total_scores_series[best_by_score]} очков)")
    
    best_by_series = avg_series_series.idxmax()
    print(f"Лучшая стратегия по средней длине доминирующих серий: {best_by_series} ({avg_series_series[best_by_series]:.2f})")

    print("\nМатрица побед (по очкам):")
    win_matrix = pd.DataFrame(index=strats_list, columns=strats_list, dtype=object)
    
    for i, name_a in enumerate(strats_list):
        for j, name_b in enumerate(strats_list):
            if i == j:
                win_matrix.loc[name_a, name_b] = '-'
            else:
                score_a = df_scores.loc[name_a, name_b]
                score_b = df_scores.loc[name_b, name_a]
                if score_a > score_b:
                    win_matrix.loc[name_a, name_b] = 'WIN'
                elif score_a < score_b:
                    win_matrix.loc[name_a, name_b] = 'LOSE'
                else:
                    win_matrix.loc[name_a, name_b] = 'DRAW'
    print(win_matrix.to_string())

if __name__ == "__main__":
    main()