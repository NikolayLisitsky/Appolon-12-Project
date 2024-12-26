import krpc
import time
import json

# Подключаемся к серверу kRPC
conn = krpc.connect(name='Rocket Logger')
vessel = conn.space_center.active_vessel

# Имя выходного файла
output_file = 'data.json'

# Инициализируем список для хранения данных
flight_data = []

print("Сбор данных начался. Нажмите Ctrl+C для завершения и сохранения данных.")

try:
    while True:
        # Получаем референтный кадр
        surface_frame = vessel.orbit.body.reference_frame
        flight = vessel.flight(surface_frame)

        # Получаем текущие данные
        altitude = flight.mean_altitude
        speed = flight.speed
        mass = vessel.mass
        mission_time = vessel.met

        # Добавляем данные в список
        flight_data.append({
            'time': round(mission_time, 2),
            'altitude': round(altitude, 2),
            'speed': round(speed, 2),
            'mass': round(mass, 2)
        })

        # Печатаем данные в консоль (опционально)
        print(f"Time: {mission_time:.2f} s, Altitude: {altitude:.2f} m, "
              f"Speed: {speed:.2f} m/s, Mass: {mass:.2f} kg")

        # Ждем 1 секунду перед следующим измерением
        time.sleep(1)

except KeyboardInterrupt:
    print("\nПрерывание записи данных...")
    print("Сохранение данных в JSON-файл...")

    # Сохраняем данные в JSON-файл
    with open(output_file, 'w') as file:
        json.dump(flight_data, file, indent=4)

    print(f"Данные успешно сохранены в файл: {output_file}")

