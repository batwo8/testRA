import pandas as pd
from datetime import datetime

# Загрузка данных
df = pd.read_csv("flights.csv")

# Преобразуем timestamp в datetime и извлекаем час
df['timestamp'] = pd.to_datetime(df['timestamp'])
current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

# Фильтрация по текущему часу + группировка
hourly_report = (
    df[df['timestamp'] >= current_hour]
    .groupby(['airport', 'model', 'airline'])
    .size()
    .reset_index(name='count')
)

# Группировка за весь день
daily_report = (
    df.groupby(['airport', 'model', 'airline'])
    .size()
    .reset_index(name='count')
)

# Сохранение отчётов
hourly_report.to_csv("flights_report_hourly.csv", index=False)
daily_report.to_csv("flights_report_daily.csv", index=False)

print(" Отчёты сохранены:")
print(f"- flights_report_hourly.csv (за текущий час: {current_hour})")
print("- flights_report_daily.csv (за весь день)")