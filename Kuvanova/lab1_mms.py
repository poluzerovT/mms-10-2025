import numpy as np
import matplotlib.pyplot as plt

def coin_experiment(p=0.5, n_tosses=100, n_experiments=10000):
   
    results = []# количество орлов в каждом эксперименте
    max_series_lengths = []#максимальная длина серий орлов
    has_5_series = []#наличие серий из 5 орлов подряд
    
    #повторние эксп-та
    for _ in range(n_experiments):
        # Генерация 0-решка 1-орел
        tosses = np.random.choice([0, 1], size=n_tosses, p=[1-p, p])
        
        # Считаем количество орлов
        heads_count = np.sum(tosses)#cуммирование элементов массива
        results.append(heads_count)
        
        # Анализ серии орлов
        current_series = 0
        max_series = 0 # максимальная длина серии в эксп-те
        found_5_series = False
        
        for toss in tosses:
            if toss == 1:  # Орел
                current_series += 1
                max_series = max(max_series, current_series)

                if current_series >= 5:
                    found_5_series = True
            else:  # Решка
                current_series = 0
                
        max_series_lengths.append(max_series)
        has_5_series.append(found_5_series)
    
    return np.array(results), np.array(max_series_lengths), np.array(has_5_series)

def simple_visualization():
    
    # Генерируем данные один раз
    results, max_series, has_5_series = coin_experiment(p=0.5, n_tosses=100, n_experiments=10000)
    
   
    plt.figure(figsize=(10, 8))

     # 1. среднее кол-во орлов
    plt.subplot(2, 2, 1) # позиця 1 в сетке 2 на 2
    plt.hist(results, bins=20, alpha=0.7, color='pink', edgecolor='black')
   
    #верт линия по средним результатам
    plt.axvline(np.mean(results), color='red', linestyle='--', linewidth=2, label=f'Среднее: {np.mean(results):.1f}')
    plt.xlabel('Количество орлов')
    plt.ylabel('Частота')
    plt.title('1. Среднее число орлов')
    plt.legend()
    plt.grid(True, alpha=0.3)#cетка
    
    # 2. График вероятности >60 орлов
    plt.subplot(2, 2, 2)
    values = [55, 60, 65, 70]
    probs = [np.mean(results > x) for x in values]

    #cтолбчатая диаграмма 
    plt.bar(values, probs, color=['orange', 'red', 'darkred', 'maroon'], alpha=0.7)
    plt.xlabel('Орлов')
    plt.ylabel('Вероятность')
    plt.title('2. Вероятность чсла орлов больше 60')
    for i, v in enumerate(probs):
        plt.text(values[i], v + 0.01, f'{v:.3f}', ha='center')
    plt.grid(True, alpha=0.3)
    
    # 3. График вероятностей по интервалам
    plt.subplot(2, 2, 3)
    intervals = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), 
                (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
    interval_probs = []
    interval_labels = []
    
    for start, end in intervals:
        if end == 100:
            prob = np.mean((results >= start) & (results <= end))
        else:
            prob = np.mean((results >= start) & (results < end))
        interval_probs.append(prob)
        interval_labels.append(f'{start}-{end}')
    
    plt.bar(interval_labels, interval_probs, alpha=0.7, color='green')
    plt.xlabel('Интервалы')
    plt.ylabel('Вероятность')
    plt.title('3. Вероятность выпадения числа орлов по интервалам')
    plt.xticks(rotation=90)
    plt.grid(True, alpha=0.3)
    
    # 4. График 95% интервала
    plt.subplot(2, 2, 4)
    lower = np.percentile(results, 2.5)
    upper = np.percentile(results, 97.5)
    

    plt.axvspan(lower, upper, alpha=0.3, color='yellow', label='95% интервал')
    plt.axvline(lower, color='orange', linestyle='--', label=f'Нижняя: {lower:.1f}')
    plt.axvline(upper, color='orange', linestyle='--', label=f'Верхняя: {upper:.1f}')
    plt.axvline(np.mean(results), color='red', linewidth=2, label='Среднее')
    plt.xlabel('Количество орлов')
    plt.title('4. С вероятность 0.95 стоит ожидать значение числа орлов в интервале..')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 5. График серий из 5 орлов
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    prob_5 = np.mean(has_5_series)
    plt.bar(['Есть серия из 5+ орлов', 'Нет серии из 5+ орлов'], 
            [prob_5, 1-prob_5], color=['purple', 'gray'], alpha=0.7)
    plt.ylabel('Вероятность')
    plt.title('5. Вероятность серии из 5+ орлов подряд')
    for i, v in enumerate([prob_5, 1-prob_5]):
        plt.text(i, v + 0.01, f'{v:.3f}', ha='center')
    plt.grid(True, alpha=0.3)
    
   
    
    # Графики зависимости от p 
    print("Строим графики зависимости от p...")
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    metrics = {'числа орлов': [], 'ширины интервала': [], 'вероятности серии из 5 орлов': [], 'длины макс. серия': []}
    
    for p in p_values:
        res, max_s, has_5 = coin_experiment(p=p, n_experiments=2000)
        metrics['числа орлов'].append(np.mean(res))
        metrics['ширины интервала'].append(np.percentile(res, 97.5) - np.percentile(res, 2.5))
        metrics['вероятности серии из 5 орлов'].append(np.mean(has_5))
        metrics['длины макс. серия'].append(np.mean(max_s))
    
    plt.figure(figsize=(15, 10))
    
    for i, (title, values) in enumerate(metrics.items(), 1):
        plt.subplot(2, 2, i)
        plt.plot(p_values, values, 'o-', linewidth=2, markersize=8)
        plt.xlabel('Вероятность орла (p)')
        plt.ylabel(title)
        plt.title(f'Зависимость {title.lower()} от p')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Запускаем визуализацию
simple_visualization()