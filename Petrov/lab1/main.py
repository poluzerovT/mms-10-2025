import matplotlib.pyplot as plt
import numpy as np
import random

def throw(p):
    return (p != 0) and (random.random() <= p)
#==============
def experiment(p):
    k = m0 = m = 0
    for _ in range (100):
        if throw(p) :
            k += 1
            m += 1
        else :
            m0 = max(m0, m)
            m = 0
    m0 = max(m0, m)
    return k, m0
#==============
def sum_arr(arr, l, r):
    sum = 0
    for i in range(l, r):
        sum += arr[i]
    return sum
#====================

n = 10000
k60 = k5 = sum = 0
arr = [0] * (101)
data = []
for i in range (n):
    x, s = experiment(0.5)
    arr[x] += 1
    data.append(x)
    sum += x
    if x > 60:
        k60 += 1
    if s > 4 :
        k5 += 1
print(f"Среднее количество орлов: {sum/n:.2f}")
print(f"Количество орлов > 60: {k60/n:.6f}")

l = 0
r = 100
sum = n
while sum > 0.95 * n:
    if arr[l] < arr[r]:
        sum -=arr[l]
        l+=1
    else:
        sum -= arr[r]
        r -= 1
print(f"95% орлов содержится в интервале от {l} до {r} выпаданий включительно")
print(f"Вероятность серии из 5 орлов: {k5 / n:.4f}")

#=======1histogram===================
plt.figure(1, figsize=(8, 4))
plt.hist(data, bins=101, range=(0, 101), color = 'red')
plt.title('Вероятность выпадения')
plt.xlabel('Выпадение орлов в эксперименте')
plt.ylabel('Количество экспериментов')
plt.grid(alpha=0.3)
plt.xticks(np.arange(0, 101, 5))
# =====================================

# # ========2bar==========================
bottom = [i for i in range(1, 11)]
tens_label = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']
tens_sum = []
for i in range(10):
    tens_sum.append(sum_arr(arr, i*10, i*10 + 10 + (i == 9)) / n)
plt.figure(2, figsize=(8, 5))
bars = plt.bar(bottom, tens_sum, tick_label = tens_label, width = 1, color = 'cyan')
plt.title('Вероятность по десяткам')
plt.xlabel('Орлы в эксперименте')
plt.ylabel('Количество экспериментов')
plt.grid(axis='y', alpha=0.3)
for bar, value in zip(bars, tens_sum):
     if (value != 0):
         plt.text(bar.get_x() + bar.get_width()/2, value + 0.001,
                 f'{value:.4f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
# # ================================

# =======p-experiment=============
p = 0.0
x_data = []
mid_data = []
inter_data = []
or5_data = []
max_s_data = []
while p <= 1.0:
    x_data.append(p)
    arr = [0] * (101)
    sum_or = max_s = k5 = 0
    for i in range(n):
        x, s = experiment(p)
        arr[x] += 1
        sum_or += x
        if s > 4:
            k5 += 1
        max_s = max(max_s, s)
    mid_data.append(sum_or/n)
    max_s_data.append(max_s)
    or5_data.append(k5 / n)
    l = 0
    r = 100
    sum = n
    while sum > 0.95 * n:
        if arr[l] < arr[r]:
            sum -= arr[l]
            l += 1
        else:
            sum -= arr[r]
            r -= 1
    inter_data.append(r - l + 1)
    p += 0.01

# ========3-plot===================
plt.figure(3, figsize=(7, 4))
plt.plot(x_data, mid_data, label = 'Среднее число  орлов в эксперементе')
plt.xlabel('P')
plt.ylabel('Число орлов')
plt.grid(alpha=0.3)
plt.xticks(np.arange(0, 1, 0.1))
# =================================

# ========4-plot====================
plt.figure(4, figsize=(7, 4))
plt.plot(x_data, inter_data, label = 'Ширина интервала 95% орлов')
plt.title('Ширина интервала 95% орлов')
plt.xlabel('P')
plt.ylabel('Длина')
plt.grid(alpha=0.3)
plt.xticks(np.arange(0, 1, 0.1))
# =================================

# ========5-plot========================
plt.figure(5, figsize=(7, 4))
plt.plot(x_data, or5_data, label = 'Вероятность наличия серии из 5 орлов')
plt.title('Вероятность наличия серии из 5 орлов')
plt.xlabel('P')
plt.ylabel('Вероятность')
plt.grid(alpha=0.3)
plt.xticks(np.arange(0, 1, 0.1))
# ====================================

# =========6-plot=====================
plt.figure(6, figsize=(7, 4))
plt.plot(x_data, max_s_data, label = 'Длина максимальной серии')
plt.title('Длина максимальной серии')
plt.xlabel('P')
plt.ylabel('Длина серии')
plt.grid(alpha=0.3)
plt.xticks(np.arange(0, 1, 0.1))
# ======================================

plt.show()


