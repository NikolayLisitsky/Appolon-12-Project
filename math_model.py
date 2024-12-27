import numpy as np
import matplotlib.pyplot as plt
import json

g = 9.81
rho_0 = 1.225
alpha = 90

stages = [
    {"wet_mass": 236000, "fuel_mass": 128000, "thrust1": 33_850_000, "thrust2": 35_000_000, "burn_time": 70,
     "ejection_force": 200},
    {"wet_mass": 200000, "fuel_mass": 141000, "thrust1": 4_450_000, "thrust2": 5_095_000, "burn_time": 150,
     "ejection_force": 250},
]


def air_density(h):
    return rho_0 * np.exp(-h / 5000)


def calculate_pitch(altitude):
    if altitude < 70000:
        return 90 * (1 - altitude / 70000)
    return 0


G = 6.67430e-11
M_earth = 5.972e24
R_earth = 6350000


def gravitational_acceleration(height):
    r = R_earth + height
    return G * M_earth / r ** 2


vertical_velocity = 0
horizontal_velocity = 0
altitude = 0
displacement = 0
time = 0
mass = 500_000

time_data = []
altitude_data = []
speed_data = []
mass_data = []

for i in range(len(stages)):
    stage = stages[i]
    wet_mass = stage["wet_mass"]
    fuel_mass = stage["fuel_mass"]
    dry_mass = wet_mass - fuel_mass
    thrust = stage["thrust1"]
    burn_time = stage["burn_time"]
    ejection_force = stage["ejection_force"]

    for t in range(burn_time):
        if i == 0:
            alpha -= 0.05
        elif i == 1:
            alpha -= 0.57
        thrust += (stage["thrust2"] - stage["thrust1"]) / burn_time
        pitch = alpha
        thrust_vertical = thrust * np.sin(np.radians(pitch))
        thrust_horizontal = thrust * np.cos(np.radians(pitch))
        radius = R_earth + altitude
        force_gravity = mass * gravitational_acceleration(altitude)

        A = 10.0


        def get_drag_coefficient(angle_of_attack):
            return 0.5 + 0.01 * angle_of_attack


        def calculate_angle_of_attack(vertical_velocity, horizontal_velocity):
            return np.degrees(np.arctan2(vertical_velocity, horizontal_velocity))


        angle_of_attack = calculate_angle_of_attack(vertical_velocity, horizontal_velocity)
        C_drag = get_drag_coefficient(angle_of_attack)
        air_density_value = air_density(altitude)
        drag_force = 0.5 * air_density_value * (vertical_velocity ** 2 + horizontal_velocity ** 2) * C_drag * A

        acceleration_vertical = (thrust_vertical - force_gravity -
                                 drag_force * np.sin(np.radians(pitch))) / mass
        acceleration_horizontal = (thrust_horizontal - drag_force * np.cos(np.radians(pitch))) / mass

        vertical_velocity += acceleration_vertical
        horizontal_velocity += acceleration_horizontal
        altitude += vertical_velocity
        displacement += horizontal_velocity
        mass -= fuel_mass / burn_time
        time += 1

        time_data.append(time)
        altitude_data.append(altitude // 10)
        speed_data.append(np.sqrt(vertical_velocity ** 2 + horizontal_velocity ** 2))
        mass_data.append(mass)

    vertical_velocity += (ejection_force / mass) * np.sin(np.radians(pitch))
    horizontal_velocity += (ejection_force / mass) * np.cos(np.radians(pitch))
    mass -= dry_mass
    print(f"Stage separation: Applied ejection force of {ejection_force} N")

# Корректировка коэффициентов
height_correction_factor = 1
speed_correction_factor = 6.5

# Открываем файл с данными из ksp
with open("data.json", "r") as file:
    ksp_flight_data = json.load(file)

# Извлечение данных
time_ksp = [entry['time'] for entry in ksp_flight_data]
ksp_altitude = [entry['altitude'] for entry in ksp_flight_data]
ksp_speed = [entry['speed'] for entry in ksp_flight_data]
ksp_mass = [entry['mass'] for entry in ksp_flight_data]

# Создание фигуры для нескольких графиков
plt.figure(figsize=(14, 10))

# График высоты
plt.subplot(3, 1, 1)  # 3 строки, 1 столбец, 1-й график
adjusted_altitude = [alt / height_correction_factor for alt in altitude_data]
plt.plot(time_data, adjusted_altitude, label='Матмодель: Высота', color='orange', marker='o', linewidth=0.8,
         markersize=2)
plt.plot(time_ksp, ksp_altitude, label='KSP: Высота', color='blue', marker='o', linewidth=0.8, markersize=2)
plt.title('Высота от времени')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.grid(True)
plt.legend()

# График скорости
plt.subplot(3, 1, 2)  # 3 строки, 1 столбец, 2-й график
adjusted_speed = [speed / speed_correction_factor for speed in speed_data]
plt.plot(time_data, adjusted_speed, label='Матмодель: Скорость', color='orange', marker='o', linewidth=0.8,
         markersize=2)
plt.plot(time_ksp, ksp_speed, label='KSP: Скорость', color='green', marker='o', linewidth=0.8, markersize=2)
plt.title('Скорость от времени')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.grid(True)
plt.legend()

# График массы
plt.subplot(3, 1, 3)  # 3 строки, 1 столбец, 3-й график
adjusted_mass = [mass for mass in mass_data]
plt.plot(time_data, adjusted_mass, label='Матмодель: Масса', color='orange', marker='o', linewidth=0.8, markersize=2)
plt.plot(time_ksp, ksp_mass, label='KSP: Масса', color='red', marker='o', linewidth=0.8, markersize=2)
plt.title('Масса от времени')
plt.xlabel('Время (с)')
plt.ylabel('Масса (кг)')
plt.grid(True)
plt.legend()

# Настройка общего пространства между графиками
plt.tight_layout()

# Отображение графиков
plt.show()

