import json
import matplotlib.pyplot as plt

# Имя файла с данными
input_file = 'data.json'

# Чтение данных из JSON-файла
with open(input_file, 'r', encoding="UTF-8") as file:
    flight_data = json.load(file)

# Извлечение данных
time = [entry['time'] for entry in flight_data]
altitude = [entry['altitude'] for entry in flight_data]
speed = [entry['speed'] for entry in flight_data]
mass = [entry['mass'] for entry in flight_data]

# Создание фигуры для нескольких графиков
plt.figure(figsize=(14, 10))

# График высоты
plt.subplot(3, 1, 1)  # 3 строки, 1 столбец, 1-й график
plt.plot(time, altitude, label='Высота', color='blue', marker='o', linewidth=0.8, markersize=2)
plt.title('Высота от времени')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.grid(True)
plt.legend()

# График скорости
plt.subplot(3, 1, 2)  # 3 строки, 1 столбец, 2-й график
plt.plot(time, speed, label='Скорость', color='green', marker='o', linewidth=0.8, markersize=2)
plt.title('Скорость от времени')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.grid(True)
plt.legend()

# График массы
plt.subplot(3, 1, 3)  # 3 строки, 1 столбец, 3-й график
plt.plot(time, mass, label='Масса', color='red', marker='o', linewidth=0.8, markersize=2)
plt.title('Масса от времени')
plt.xlabel('Время (с)')
plt.ylabel('Масса (кг)')
plt.grid(True)
plt.legend()

# Настройка общего пространства между графиками
plt.tight_layout()

# Отображение графиков
plt.show()

