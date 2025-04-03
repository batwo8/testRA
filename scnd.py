import pandas as pd
from datetime import datetime, timedelta

# Функция для округления времени до ближайших 10 минут
def round_to_nearest_10_minutes(dt):
    minutes = (dt.minute // 10) * 10
    return dt.replace(minute=minutes, second=0, microsecond=0)

# Загрузка данных
df = pd.read_csv("flights.csv")

# Преобразуем timestamp в datetime (если это еще не сделано)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Преобразуем departure_time в datetime (чтобы извлечь время в формате H:M)
df['departure_time'] = pd.to_datetime(df['departure_time'], format='%H:%M', errors='coerce').dt.time

# Время запроса
current_time = datetime.now()

# Округляем время запроса до ближайших 10 минут
rounded_current_time = round_to_nearest_10_minutes(current_time)

# Начало и конец интервала (от округленного времени до плюс 1 час)
# Извлекаем только время из rounded_current_time и комбинируем его с сегодняшней датой
interval_start = datetime.combine(datetime.today(), rounded_current_time.time())  # Используем только .time() для времени
interval_end = interval_start + timedelta(hours=1)

# Фильтрация рейсов по departure_time в интервале (interval_start, interval_end)
filtered_flights = df[
    (df['departure_time'] >= interval_start.time()) & (df['departure_time'] < interval_end.time())
]

# Группировка по аэропорту, модели, авиакомпании и времени отправления
hourly_report = (
    filtered_flights.groupby(['airport', 'departure_time', 'model', 'airline'])
    .size()
    .reset_index(name='count')
)

# Фильтрация по текущему дню + группировка по departure_time
start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
daily_report = (
    df[df['timestamp'] >= start_of_day]
    .groupby(['airport', 'departure_time', 'model', 'airline'])
    .size()
    .reset_index(name='count')
)

# Сохранение отчётов
hourly_report.to_csv("flights_report_hourly.csv", index=False)
daily_report.to_csv("flights_report_daily.csv", index=False)

print("Отчёты сохранены:")
print(f"- flights_report_hourly.csv (за текущий час: {rounded_current_time.strftime('%Y-%m-%d %H:%M')})")
print(f"- flights_report_daily.csv (за весь день: {start_of_day.strftime('%Y-%m-%d')})")

