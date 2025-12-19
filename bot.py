import feedparser, requests, json, os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")  

LAST_FILE = "last_seen.json"

RSS_SOURCES = {
    "NASA Breaking": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "ESA": "https://www.esa.int/rssfeed/Our_Activities",
    "Astronomy": "https://astronomy.com/rss"
}

APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
SPACEX = "https://api.spacexdata.com/v4/launches/latest"

def load_seen():
    return json.load(open(LAST_FILE)) if os.path.exists(LAST_FILE) else {}

def save_seen(data):
    json.dump(data, open(LAST_FILE, "w"))

def send(text, image=None):
    if image:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {"chat_id": CHAT_ID, "caption": text, "photo": image, "parse_mode": "Markdown"}
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def process_rss(name, url, seen):
    feed = feedparser.parse(url)
    for item in feed.entries[:3]:
        uid = item.link
        if uid in seen:
            continue

        image = None
        if "media_content" in item:
            image = item.media_content[0]["url"]

        msg = f"🚀 *{name}*\n\n🛰 *{item.title}*\n\n{item.summary[:300]}...\n\n🔗 {item.link}"
        send(msg, image)
        seen[uid] = True

def apod(seen):
    data = requests.get(NASA_APOD).json()
    if data["date"] in seen:
        return
    send(f"🌌 *NASA APOD*\n\n🛰 *{data['title']}*\n\n{data['explanation'][:300]}...\n\n🔗 {data['url']}",
         data["url"] if data["media_type"] == "image" else None)
    seen[data["date"]] = True

def spacex(seen):
    data = requests.get(SPACEX).json()
    if data["id"] in seen:
        return
    send(f"🚀 *SpaceX Launch*\n\n🛰 *{data['name']}*\n\n📅 {data['date_utc']}\n🔗 {data['links']['webcast']}",
         data["links"]["patch"]["large"])
    seen[data["id"]] = True

def main():
    seen = load_seen()
    for name, url in RSS_SOURCES.items():
        process_rss(name, url, seen)
    apod(seen)
    spacex(seen)
    save_seen(seen)

main()

