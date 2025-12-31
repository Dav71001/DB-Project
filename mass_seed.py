import requests
import random
from datetime import datetime

URL = "http://127.0.0.1:8000"

def run_seed():
    streets = ["Abovyan", "Tumanyan", "Mashtots", "Sayat-Nova"]
    print("Начинаю массовое заполнение...")
    for i in range(50):
        apt_res = requests.post(f"{URL}/apartments/", json={
            "street": random.choice(streets),
            "house_number": str(random.randint(1, 100)),
            "apartment_number": str(i+1),
            "owner": f"Resident {i+1}"
        })
        if apt_res.status_code == 200:
            apt_id = apt_res.json()["id"]
            requests.post(f"{URL}/payments/", json={
                "apartment_id": apt_id,
                "service_id": random.randint(1, 3),
                "amount": float(random.randint(500, 4500)),
                "payment_date": datetime.now().isoformat()
            })
    print("Готово! Проверьте данные в Swagger.")

if __name__ == "__main__":
    run_seed()