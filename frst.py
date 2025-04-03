from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

airports = ["ist", "aer", "ods", "cnd", "var", "doj", "aaq", "bus"]
flights_data = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for airport in airports:
    url = f"https://www.flightradar24.com/data/airports/{airport}"
    print(f"Сканируем аэропорт: {airport.upper()} ({url})")  # Выводим только сканируемый аэропорт с ссылкой

    driver.get(url)
    time.sleep(5)

    flights = driver.find_elements(By.CSS_SELECTOR, "tr")
    for flight in flights[1:]:
        columns = flight.find_elements(By.TAG_NAME, "td")

        # Игнорируем строки с пустыми данными или с лишней информацией
        if len(columns) < 6 or "* All times are in local timezone" in columns[0].text:
            continue

        departure_time = columns[0].text.strip() or "N/A"  # Теперь первый элемент - это departure_time
        callsign = columns[1].text.strip() or "N/A"  # Второй элемент - это callsign
        route = columns[2].text.strip() or "N/A"  # Третий элемент - это route
        airline = columns[3].text.strip() or "N/A"  # Четвёртый элемент - это airline
        model = columns[4].text.strip() or "N/A"  # Пятый элемент - это model

        if "N/A" in route or "Cancelled" in route:
            continue

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        flights_data.append({
            "timestamp": timestamp,
            "departure_time": departure_time,
            "callsign": callsign,
            "icao": "N/A",  # В вашем примере нет данных об ICAO, можно оставить "N/A"
            "model": model,
            "airline": airline,
            "route": route,
            "airport": airport.upper()
        })

driver.quit()

# Сохранение в CSV
with open("flights.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file,
                            fieldnames=["timestamp", "departure_time", "callsign", "icao", "model", "airline", "route",
                                        "airport"])
    writer.writeheader()
    writer.writerows(flights_data)

print("Данные сохранены в flights.csv")  # Выводим сообщение о сохранении данных
