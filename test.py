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
    print(f" Сканируем аэропорт: {airport.upper()} ({url})")

    driver.get(url)
    time.sleep(5)

    flights = driver.find_elements(By.CSS_SELECTOR, "tr")
    for flight in flights[1:]:
        columns = flight.find_elements(By.TAG_NAME, "td")
        if len(columns) < 5:
            continue

        callsign = columns[0].text.strip() or "N/A"
        icao = columns[1].text.strip() or "N/A"
        model = columns[2].text.strip() or "N/A"
        airline = columns[3].text.strip() or "N/A"
        route = columns[4].text.strip() or "N/A"

        if "N/A" in route or "Cancelled" in route:
            continue

        flights_data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "callsign": callsign,
            "icao": icao,
            "model": model,
            "airline": airline,
            "route": route,
            "airport": airport.upper()
        })

driver.quit()

# Сохранение в CSV
with open("flights.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["timestamp", "callsign", "icao", "model", "airline", "route", "airport"])
    writer.writeheader()
    writer.writerows(flights_data)

print(" Данные сохранены в flights.csv")