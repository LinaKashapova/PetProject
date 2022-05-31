from math import log, atanh
import matplotlib.pyplot as plt

#Физические величины
g_Earth = 9.81
g_Moon = 1.622
u = 3000

m0_fluel = 100 #Начальный запас топлива



def high(M, h0, v0, dm, dt, u):#расчет высоты
    r = log(1- dm/M)
    h = h0+-g_Moon * dt**2/2 + v0 * dt + ((1 - r + M * r/dm) if dm!=0 else 0) * u * dt
    return h
def velocity(M, v0, dm, dt, u):#расчет скорости
    v = v0 - g_Moon * dt - (2 * u * atanh(dm/(dm - 2 * M)) if dm!= 0 else 0)
    return v
def overheight(M, dm, dt, u):
    return dm/dt * u/M/g_Earth


def main (m0_fluel, u):
    h = 1000 #начальная высота
    M0 = 1000 #сухая масса лунолёта
    M = M0 + m0_fluel #масса с топливом
    v = 0
    arr_h = [h] #хранение высоты
    arr_v = [v] #ждя скорости
    arr_t = [0]
    print("Необходимо посадить лунолёт с высоты", h, "метров. С запасом топлива", m0_fluel, "кг.")
    print("Вводите данные в формате 'dm dt' или 'dm,dt', разделив запятой или пробелом")
    while(True):
        print("\n")
        string = (input("Введите массу (кг) и время выброса топлива (с):")).replace(","," ").split() #введём два числа через , или пробел
        dm = min(float(string[0]), m0_fluel) #выбрасываемая масса, если пытаемся выбросить больше остатка - выбрасываем всё, что осталось
        dt = max(1, float(string[1])) #промежуток времени не меньше единицы
        u_cur = abs(u)*(-1 if dm < 0 else 1)
        if m0_fluel!=0:#если есть топливо
            if abs(overheight(M, dm, dt, u_cur)) <= 5: #проверяем на перегрузку
                h = high(M, h, v, dm, dt, u_cur)
                v = velocity(M, v, dm, dt, u_cur) #пересчитываем высоту и скорость
                m0_fluel -= abs(dm)
                M -= abs(dm)
                arr_t.append(arr_t[-1] + dt) #В "нормальном" режиме мы можем сразу добавить время
            else:
                print("Перегрузка! Корабль неуправляем")
                h = high(M, h, v, 1, 10, 0) #избегаем деления на 0
                v = velocity(M, v, 1, 10, 0) #топливо не выбрасывается в течении 10 секунд
                arr_t.append(arr_t[-1] + 10) #добавляем 10 к времени
            arr_h.append(max(h,0)) #независимо от перегрузки выводим
            arr_v.append(v)
            print("Текущая высота", max(h, 0))
            print("Текущая скорость", v)
            print("Запас топлива", m0_fluel)
        else:
            print("Закончилось топливо")
            while h > 0: #пока лунолёт не упал смотрим за его полётом посекундно
                h = high(M, h, v,1, 1, 0)
                v = velocity(M, v, 1, 1, 0)
                arr_h.append(max(h,0))# чтобы не уйти ниже поверхности
                arr_v.append(v)
                arr_t.append(arr_t[-1]+1)
        if arr_h[-1]==0: #достигли Луны
            if abs(v)<=5: print("ПОБЕДА!!!")
            else: print("Поражение:((((")
        fig = plt.figure()
        fig.suptitle("График снижения")
        ax = fig.add_subplot(111)
        l = ax.plot(arr_t, arr_h, 'k--')
        plt.show()

        fig = plt.figure() #второй график
        fig.suptitle("График изменения скорости")
        ax = fig.add_subplot(111)
        l = ax.plot(arr_t, arr_v, 'k--')
        plt.show()
        return 0
    return 0
if __name__ == '__main__':
    main(m0_fluel, u)
