import math
import matplotlib.pyplot as plt

class PopulationModels:#Класс для исследования моделей роста популяции
    @staticmethod
    def exponential_growth(x0, r, n_steps=100):#Модель экспоненциального роста
        x = [0.0] * n_steps
        x[0] = x0
        
        for t in range(n_steps-1):
            x[t+1] = r * x[t]
            
        return x
    
    @staticmethod
    def logistic_model(x0, r, n_steps=100):#Логистическая модель
        x = [0.0] * n_steps
        x[0] = x0
        
        for t in range(n_steps-1):
            x[t+1] = r * x[t] * (1 - x[t])
            
        return x
    
    @staticmethod
    def moran_model(x0, r, n_steps=100):#Модель Морана
       
        x = [0.0] * n_steps
        x[0] = x0
        
        for t in range(n_steps-1):
            x[t+1] = x[t] * math.exp(r * (1 - x[t]))
            
        return x
    
    @staticmethod
    def host_parasite_model(x0, y0, a, b, c, n_steps=100):#Модель хозяин-паразит
        x = [0.0] * n_steps
        y = [0.0] * n_steps
        x[0] = x0
        y[0] = y0
        
        for t in range(n_steps-1):
            exp_term = math.exp(-a * y[t])
            x[t+1] = b * x[t] * exp_term
            y[t+1] = c * x[t] * (1 - exp_term)
            
        return x, y

def analyze_models():#Анализ моделей с простой визуализацией

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    r_values = [ 3.8, ]
    x0 = 0.1
    n_steps = 50
    
    for r in r_values:
        trajectory = PopulationModels.logistic_model(x0, r, n_steps)
        plt.plot(trajectory, label=f'r={r}')
    
    plt.title('Логистическая модель')
    plt.xlabel('Время')
    plt.ylabel('Популяция')
    plt.legend()
    plt.grid(True)
    
    ##########################################
    plt.subplot(2, 2, 2)
    r_values = [0.5, 1.0, 2.0, 3.0]
    
    for r in r_values:
        trajectory = PopulationModels.moran_model(x0, r, n_steps)
        plt.plot(trajectory, label=f'r={r}')
    
    plt.title('Модель Морана')
    plt.xlabel('Время')
    plt.ylabel('Популяция')
    plt.legend()
    plt.grid(True)
    
    ##############################################
    plt.subplot(2, 2, 3)
    a, b, c = 0.1, 2.0, 0.8
    x, y = PopulationModels.host_parasite_model(0.5, 0.1, a, b, c, n_steps)
    plt.plot(x, label='Хозяева')
    plt.plot(y, label='Паразиты')
    plt.title('Модель хозяин-паразит')
    plt.xlabel('Время')
    plt.ylabel('Популяция')
    plt.legend()
    plt.grid(True)
    
    #######################
    plt.subplot(2, 2, 4)
    r_values = [0.5, 1.0, 2.0, 3.0]
    
    for r in r_values:
        trajectory = PopulationModels.exponential_growth(x0, r, n_steps)
        plt.plot(trajectory, label=f'r={r}')
    
    plt.title('Экспоненциальный рост')
    plt.xlabel('Время')
    plt.ylabel('Популяция')
    plt.legend()
    plt.grid(True)
    plt.ylim(-0.1, 2.0)  # сделала более детальный масштаб
    
    plt.tight_layout()
    plt.show() 

def analyze_all_models():
    x0 = 0.1
    n_steps = 50
    print("\n" + "="*60)
    print("АНАЛИЗ ВСЕХ МОДЕЛЕЙ ПОПУЛЯЦИЙ")
    print("="*60)
 
    print("\n ЭКСПОНЕНЦИАЛЬНАЯ МОДЕЛЬ:")
    print("-" * 40)
    r_values = [0.5, 1.0, 2.0, 3.0]
    for r in r_values:
        trajectory = PopulationModels.exponential_growth(x0, r, n_steps)
        final_values = [round(x, 6) for x in trajectory[-10:]]
        unique_values = len(set(final_values))
        print(f"r = {r:.1f}: {unique_values} уникальных значений")
        if unique_values == 1:
            print(f"  Неподвижная точка: {final_values[0]}")
        else:
            print(f"  Изменение популяции")

  
    print("\n ЛОГИСТИЧЕСКАЯ МОДЕЛЬ :")
    print("-" * 40)
    r_values = [0.5, 1.0, 2.0, 3.0]
    for r in r_values:
        #  200 шагов
        x_temp = 0.5
        for _ in range(200):
            x_temp = r * x_temp * (1 - x_temp)
        

        final_values = []
        for _ in range(50):
            x_temp = r * x_temp * (1 - x_temp)
            final_values.append(round(x_temp, 6))
        
        unique_values = len(set(final_values))
        print(f"r = {r:.1f}: {unique_values} уникальных значений")
        if unique_values == 1:
            print(f"  Неподвижная точка: {final_values[0]}")
        elif unique_values == 2:
            print(f"  2-цикл: {list(set(final_values))}")
        else:
            print(f"  Сложное поведение ({unique_values} уникальных значений)")

    print("\n МОДЕЛЬ МОРАНА :")
    print("-" * 40)
    r_values = [0.5, 1.0, 2.0, 3.0]
    for r in r_values:
       
        x_temp = x0
        for _ in range(200):
            x_temp = x_temp * math.exp(r * (1 - x_temp))
        
   
        final_values = []
        for _ in range(50):
            x_temp = x_temp * math.exp(r * (1 - x_temp))
            final_values.append(round(x_temp, 6))
        
        unique_values = len(set(final_values))
        print(f"r = {r:.1f}: {unique_values} уникальных значений")
        if unique_values == 1:
            print(f"  Неподвижная точка: {final_values[0]}")
        elif unique_values == 2:
            print(f"  2-цикл: {list(set(final_values))}")
        else:
            print(f"  Сложное поведение ({unique_values} уникальных значений)")

   
    print("\n МОДЕЛЬ ХОЗЯИН-ПАРАЗИТ:")
    print("-" * 40)
    a, b, c = 0.1, 2.0, 0.8
    x, y = PopulationModels.host_parasite_model(0.5, 0.1, a, b, c, n_steps)
    
    final_x = [round(val, 6) for val in x[-10:]]
    unique_x = len(set(final_x))
    print(f"Хозяева: {unique_x} уникальных значений")
    if unique_x == 1:
        print(f"  Неподвижная точка: {final_x[0]}")
    elif unique_x == 2:
        print(f"  2-цикл: {list(set(final_x))}")
    else:
        print(f"  Сложное поведение ({unique_x} уникальных значений)")
    
    final_y = [round(val, 6) for val in y[-10:]]
    unique_y = len(set(final_y))
    print(f"Паразиты: {unique_y} уникальных значений")
    if unique_y == 1:
        print(f"  Неподвижная точка: {final_y[0]}")
    elif unique_y == 2:
        print(f"  2-цикл: {list(set(final_y))}")
    else:
        print(f"  Сложное поведение ({unique_y} уникальных значений)")

if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        print("Matplotlib доступен")
    except ImportError:
        print("Установите matplotlib: pip install matplotlib")
        exit()
    
   
    analyze_all_models()
    print("\n" + "="*60)
    analyze_models()