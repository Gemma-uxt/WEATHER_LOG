import json
import urllib.request
from pathlib import Path

# 수집할 도시: 이름 → (위도, 경도)
CITIES = {
    "seoul": (37.5665, 126.9780),
    "busan": (35.1796, 129.0756),
}

def fetch_today(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"
        "&timezone=Asia%2FSeoul&forecast_days=1"
    )
    with urllib.request.urlopen(url, timeout=30) as res:
        daily = json.load(res)["daily"]
    return {
        "date": daily["time"][0],
        "max": daily["temperature_2m_max"][0],
        "min": daily["temperature_2m_min"][0],
        "avg": daily["temperature_2m_mean"][0],
        "rain": daily["precipitation_sum"][0],
    }

for name, (lat, lon) in CITIES.items():
    record = fetch_today(lat, lon)
    path = Path(f"data-{name}.json")

    # 기존 기록 불러와서 오늘 것 추가 (같은 날짜는 덮어쓰기)
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    data = [d for d in data if d["date"] != record["date"]]
    data.append(record)
    data.sort(key=lambda d: d["date"])

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(name, "저장 완료:", record)

# 마지막 자동 업데이트 시각 기록 (한국 시간)
from datetime import datetime, timezone, timedelta
now = datetime.now(timezone(timedelta(hours=9)))
Path("updated.json").write_text(
    json.dumps({"updated_at": now.strftime("%Y-%m-%d %H:%M")}),
    encoding="utf-8",
)
