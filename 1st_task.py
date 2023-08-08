import math

g = 9.81

v = float(input("Введите начальную скорость (в м/с): "))
alpha = float(input("Введите угол броска (в градусах): "))

# Переводим угол в радианы
alpha_rad = math.radians(alpha)

# Рассчитываем дальность полета
x = (v ** 2 * math.sin(2 * alpha_rad)) / g

# Создаем список координат точек траектории
trajectory = []
for i in range(101):
    t = i / 100 * x
    y = t * math.tan(alpha_rad) - (g * t ** 2) / (2 * v ** 2 * math.cos(alpha_rad) ** 2)
    trajectory.append((t, y))

# Выводим результаты
print("Дальность полета: {:.2f} м".format(x))
print("Точки траектории:")
for point in trajectory:
    print("x = {:.2f} м, y = {:.2f} м".format(point[0], point[1]))