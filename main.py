def conv_hm_to_m(hm: str) -> int:  # Конвертирование из час:минута в минуты
    tmp = hm.split(':')
    return int(tmp[0]) * 60 + int(tmp[1])


def conv_m_to_hm(lst: list) -> list:  # Конвертирование из минут в час:минута
    for index in range(len(lst)):
        for i in range(2):
            if lst[index][i] // 60 < 10:
                h = f'0{lst[index][i] // 60}'
            else:
                h = f'{lst[index][i] // 60}'
            if lst[index][i] % 60 < 10:
                m = f'0{lst[index][i] % 60}'
            else:
                m = f'{lst[index][i] % 60}'
            lst[index][i] = f'{h}:{m}'
    return lst


busy = [  # список занятых окон
    {
        'start': '10:30',
        'stop': '10:50'
    },
    {
        'start': '18:40',
        'stop': '18:50'
    },
    {
        'start': '14:40',
        'stop': '15:50'
    },
    {
        'start': '16:40',
        'stop': '17:20'
    },
    {
        'start': '20:05',
        'stop': '20:20'
    }
]

busy_m_intervals = []  # Список занятых окон в минутах
start = 9 * 60  # Начало рабочего дня в минутах
end = 21 * 60  # Конец рабочего дня в минутах
free_m_intervals = [[start, end]]  # Свободные окна в минутах

for x in busy:  # Цикл для заполнения занятых окон в минутах
    busy_m_intervals.append([conv_hm_to_m(x['start']), conv_hm_to_m(x['stop'])])

for b_m_interval in busy_m_intervals:  # Цикл для заполнения свободных окон в минутах
    for i, f_m_interval in enumerate(free_m_intervals):
        if b_m_interval[0] >= f_m_interval[0] and b_m_interval[1] <= f_m_interval[1]:
            free_m_intervals.insert(i + 1, [b_m_interval[1], f_m_interval[1]])
            free_m_intervals[i][1] = b_m_interval[0]

for index, interval in enumerate(free_m_intervals):  # Цикл для создания свободных окошек в 30 минут
    for num in range(interval[0], interval[1] - 29, 30):
        if num + 30 > interval[1]:
            break
        free_m_intervals.insert(index + 1, [num + 30, interval[1]])
        free_m_intervals[index][1] = num + 30

for interval in free_m_intervals:  # Цикл для удаления окон, длина которых меньше 30 минут
    if interval[1] - interval[0] != 30:
        free_m_intervals.remove(interval)

free_hm_intervals = conv_m_to_hm(free_m_intervals)  # Свободные окна в формате час:минута
new_free_intervals = []  # Список свободных окон по 30 минут

for i in range(len(free_m_intervals)):  # Заполнение списка свободных окон по 30 минут
    new_free_intervals.append({'start': f'{free_hm_intervals[i][0]}',
                               'stop': f'{free_hm_intervals[i][1]}'})

print(new_free_intervals)  # Вывод информации о свободных окнах по 30 минут в консоль
