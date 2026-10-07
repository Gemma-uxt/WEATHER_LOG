import json
import urllib.request
from pathlib import Path

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665&longitude=126.9780"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=Asia%2FSeoul&forecast_days=1"
)
DATA_FILE = Path("data.json")

# 1. 날씨 데이터 받아오기
with urllib.request.urlopen(URL, timeout=30) as res:
    daily = json.load(res)["daily"]

record = {
    "date": daily["time"][0],
    "max": daily["temperature_2m_max"][0],
    "min": daily["temperature_2m_min"][0],
    "rain": daily["precipitation_sum"][0],
}

# 2. 기존 기록 불러와서 오늘 것 추가 (같은 날짜는 덮어쓰기)
data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else []
data = [d for d in data if d["date"] != record["date"]]
data.append(record)
data.sort(key=lambda d: d["date"])

# 3. 저장
DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("저장 완료:", record)
