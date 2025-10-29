import random
import matplotlib.pyplot as plt
import numpy as np

def coin_flip(p=0.5):
    return 1 if random.random() < p else 0

def simulate_experiment(n_flips=100, p=0.5):
    return [coin_flip(p) for _ in range(n_flips)]

def has_series_of_n(sequence, n=5):
    count = 0
    for outcome in sequence:
        if outcome == 1:
            count += 1
            if count == n:
                return True
        else:
            count = 0
    return False

def calculate_percentile(data, percentile):
    if not data:
        return 0
    sorted_data = sorted(data)
    index = (len(sorted_data) - 1) * percentile / 100
    lower_index = int(index)
    if lower_index == index:
        return sorted_data[lower_index]
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[lower_index + 1]
    return lower_value + (upper_value - lower_value) * (index - lower_index)

def main():
    # Параметры эксперимента
    n_experiments = 50000
    n_flips = 100
    p = 0.5
    
    random.seed(42)
    
    # Проводим эксперименты
    all_heads_counts = []
    all_series_results = []
    
    for i in range(n_experiments):
        experiment = simulate_experiment(n_flips, p)
        heads_count = sum(experiment)
        has_series = has_series_of_n(experiment, 5)
        all_heads_counts.append(heads_count)
        all_series_results.append(has_series)

    # Вычисляем необходимые значения
    average_heads = np.mean(all_heads_counts)
    prob_more_than_60 = np.mean(np.array(all_heads_counts) > 60)
    prob_series = np.mean(all_series_results)
    lower_bound = calculate_percentile(all_heads_counts, 2.5)
    upper_bound = calculate_percentile(all_heads_counts, 97.5)

    # 1. ПЯТЬ ДИАГРАММ ПО УСЛОВИЮ
    plt.figure(figsize=(15, 10))
    
    # Диаграмма 1: Среднее число орлов
    plt.subplot(2, 3, 1)
    plt.bar(['Среднее'], [average_heads], color='skyblue', alpha=0.7)
    plt.ylabel('Количество орлов')
    plt.title('Среднее число орлов')
    plt.grid(True, alpha=0.3)
    plt.text(0, average_heads + 1, f'{average_heads:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Диаграмма 2: Вероятность >60 орлов
    plt.subplot(2, 3, 2)
    sizes = [prob_more_than_60, 1 - prob_more_than_60]
    labels = [f'>60 орлов\n{prob_more_than_60:.4f}', f'≤60 орлов\n{1-prob_more_than_60:.4f}']
    colors = ['lightcoral', 'lightblue']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Вероятность >60 орлов')
    
    # Диаграмма 3: Распределение по интервалам
    plt.subplot(2, 3, 3)
    bins = list(range(0, 101, 10))
    bins.append(101)
    hist, _ = np.histogram(all_heads_counts, bins=bins)
    probabilities = hist / len(all_heads_counts)
    
    x_labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins)-1)]
    x_pos = np.arange(len(x_labels))
    
    bars = plt.bar(x_pos, probabilities, color='lightgreen', alpha=0.7, edgecolor='black')
    plt.xlabel('Интервалы количества орлов')
    plt.ylabel('Вероятность')
    plt.title('Вероятность по интервалам')
    plt.xticks(x_pos, x_labels, rotation=45)
    plt.grid(True, alpha=0.3)
    
    for bar, prob in zip(bars, probabilities):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
                f'{prob:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Диаграмма 4: 95% доверительный интервал
    plt.subplot(2, 3, 4)
    plt.errorbar(1, average_heads, yerr=[[average_heads - lower_bound], [upper_bound - average_heads]], 
                fmt='o', capsize=10, capthick=2, markersize=10, color='red', linewidth=2)
    plt.xlim(0.5, 1.5)
    plt.ylim(lower_bound - 2, upper_bound + 2)
    plt.xticks([])
    plt.ylabel('Количество орлов')
    plt.title(f'95% доверительный интервал\n[{lower_bound:.1f}, {upper_bound:.1f}]')
    plt.grid(True, alpha=0.3)
    
    # Диаграмма 5: Вероятность серии из 5 орлов
    plt.subplot(2, 3, 5)
    series_data = [prob_series, 1 - prob_series]
    colors_series = ['gold', 'lightgray']
    bars = plt.bar(['Есть серия', 'Нет серии'], series_data, color=colors_series, alpha=0.7, edgecolor='black')
    plt.ylabel('Вероятность')
    plt.title('Вероятность серии из 5 орлов')
    plt.grid(True, alpha=0.3)
    
    for bar, prob in zip(bars, series_data):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{prob:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Оставляем 6-ю ячейку пустой для лучшего расположения
    plt.subplot(2, 3, 6)
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

    # 2. ЧЕТЫРЕ ДИАГРАММЫ ЗАВИСИМОСТИ ОТ P
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    n_simulations = 1000
    
    results = {
        'average_heads': [],
        'prob_more_than_60': [],
        'interval_width': [],
        'series_prob': []
    }
    
    for p_val in p_values:
        heads_counts = []
        series_results = []
        
        for _ in range(n_simulations):
            experiment = simulate_experiment(n_flips, p_val)
            heads_count = sum(experiment)
            has_series = has_series_of_n(experiment, 5)
            heads_counts.append(heads_count)
            series_results.append(has_series)
        
        # Вычисляем все метрики для текущего p
        results['average_heads'].append(np.mean(heads_counts))
        results['prob_more_than_60'].append(np.mean(np.array(heads_counts) > 60))
        results['series_prob'].append(np.mean(series_results))
        
        # Ширина доверительного интервала
        lower = calculate_percentile(heads_counts, 2.5)
        upper = calculate_percentile(heads_counts, 97.5)
        results['interval_width'].append(upper - lower)
    
    # Графики зависимости от p
    plt.figure(figsize=(15, 10))
    
    # График 1: Среднее число орлов от p
    plt.subplot(2, 2, 1)
    plt.plot(p_values, results['average_heads'], 'o-', linewidth=2, markersize=6)
    plt.xlabel('Вероятность орла (p)')
    plt.ylabel('Среднее число орлов')
    plt.title('Среднее число орлов от p')
    plt.grid(True, alpha=0.3)
    
    # График 2: Вероятность >60 орлов от p
    plt.subplot(2, 2, 2)
    plt.plot(p_values, results['prob_more_than_60'], 's-', linewidth=2, markersize=6, color='orange')
    plt.xlabel('Вероятность орла (p)')
    plt.ylabel('Вероятность >60 орлов')
    plt.title('Вероятность >60 орлов от p')
    plt.grid(True, alpha=0.3)
    
    # График 3: Ширина доверительного интервала от p
    plt.subplot(2, 2, 3)
    plt.plot(p_values, results['interval_width'], '^-', linewidth=2, markersize=6, color='green')
    plt.xlabel('Вероятность орла (p)')
    plt.ylabel('Ширина 95% интервала')
    plt.title('Ширина доверительного интервала от p')
    plt.grid(True, alpha=0.3)
    
    # График 4: Вероятность серии от p
    plt.subplot(2, 2, 4)
    plt.plot(p_values, results['series_prob'], 'd-', linewidth=2, markersize=6, color='red')
    plt.xlabel('Вероятность орла (p)')
    plt.ylabel('Вероятность серии')
    plt.title('Вероятность серии из 5 орлов от p')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()