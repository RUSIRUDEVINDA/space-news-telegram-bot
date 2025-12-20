import feedparser
import requests
import json
import os

# Secrets from GitHub
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")  

LAST_FILE = "last_seen.json"

RSS_SOURCES = {
    "NASA Breaking News": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "ESA News": "https://www.esa.int/rssfeed/Our_Activities",
    "Astronomy.com": "https://astronomy.com/rss"
}

APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
SPACEX_URL = "https://api.spacexdata.com/v4/launches/latest"

def load_seen():
    if os.path.exists(LAST_FILE):
        try:
            with open(LAST_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_seen(data):
    with open(LAST_FILE, "w") as f:
        json.dump(data, f)

def send_message(text, photo=None):
    try:
        if photo:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                json={
                    "chat_id": CHAT_ID,
                    "photo": photo,
                    "caption": text,
                    "parse_mode": "Markdown"
                }
            )
        else:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": text,
                    "parse_mode": "Markdown"
                }
            )
        print(f"Sent: {text[:60]}...")
    except Exception as e:
        print(f"Telegram send error: {e}")

def process_rss(name, url, seen):
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            return
        for entry in feed.entries[:5]:
            uid = entry.link
            if uid in seen:
                continue

            image = None
            if hasattr(entry, "media_content") and entry.media_content:
                for media in entry.media_content:
                    if media.get("medium") == "image":
                        image = media["url"]
                        break

            title = entry.title
            summary = getattr(entry, "summary", "")
            link = entry.link

            msg = f"🚀 *{name}*\n\n*{title}*\n\n{summary[:400]}...\n\n🔗 [Read more]({link})"
            send_message(msg, image)
            seen[uid] = True
    except Exception as e:
        print(f"RSS error ({name}): {e}")

def check_apod(seen):
    try:
        data = requests.get(APOD_URL).json()  # ← FIXED: was NASA_APOD
        uid = data["date"]
        if uid in seen:
            return

        title = data["title"]
        explanation = data["explanation"]
        url = data["url"]
        hdurl = data.get("hdurl", url)

        msg = f"🌌 *NASA Astronomy Picture of the Day*\n\n*{title}*\n\n{explanation[:500]}...\n\n🔗 [Full Image]({hdurl})"

        if data["media_type"] == "image":
            send_message(msg, url)
        else:
            send_message(msg + f"\n\n🎥 [Watch Video]({url})")

        seen[uid] = True
    except Exception as e:
        print(f"APOD error: {e}")

def check_spacex(seen):
    try:
        data = requests.get(SPACEX_URL).json()
        uid = data["id"]
        if uid in seen:
            return

        name = data["name"]
        date = data["date_utc"][:10]
        webcast = data["links"].get("webcast", "No link")
        patch = data["links"]["patch"].get("small") or data["links"]["patch"].get("large")

        msg = f"🚀 *Latest SpaceX Mission*\n\n*{name}*\n\n📅 {date}\n🔗 [Watch]({webcast})"
        send_message(msg, patch)

        seen[uid] = True
    except Exception as e:
        print(f"SpaceX error: {e}")

# === MAIN ===
if __name__ == "__main__":
    print("Starting space news update...")
    seen = load_seen()

    for name, url in RSS_SOURCES.items():
        process_rss(name, url, seen)

    check_apod(seen)
    check_spacex(seen)

    save_seen(seen)
    print("Update complete!")