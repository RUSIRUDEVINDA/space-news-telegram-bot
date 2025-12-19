# 🚀 Space News Telegram Bot

An automated Telegram bot that delivers the latest **NASA Astronomy Picture of the Day (APOD)**, **SpaceX launches**, **NASA breaking news**, **ESA updates**, and more — complete with beautiful images — directly to your Telegram channel.

Runs 24/7 for **free** using **GitHub Actions**. No server needed!

## ✨ Features

- Daily stunning NASA APOD with high-quality image and explanation
- Latest SpaceX mission details with patch image
- Real-time NASA, ESA, and Astronomy.com news via RSS
- Automatic duplicate prevention (only sends new items)
- Posts with images, captions, and links
- Fully automated — runs every few hours on GitHub

## 📸 Preview (Example Posts)

Your channel will get posts like this:

> 🌌 **NASA Astronomy Picture of the Day**  
> _The Orion Bulge_  
> A stunning view of the central bulge of the Orion Nebula...  
> 🔗 [Full HD Image]

> 🚀 **NASA Breaking News**  
> _NASA’s Hubble Finds Evidence of Distant Planet Collision_  
> ...  
> 🔗 Read more

> 🚀 **Latest SpaceX Launch**  
> _Starlink Group 10-9_  
> 📅 Dec 20, 2025  
> 🔗 Watch Live

## 🛠️ How to Set Up Your Own (Step-by-Step)

### 1. Create a Telegram Bot

1. Open Telegram → Search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g., "Space News Bot") and username (e.g., "my_space_news_bot")
4. Copy the **API token** (looks like `123456789:ABCdef...`)

### 2. Create a Telegram Channel

1. In Telegram → New Channel
2. Name it (e.g., "Space News Daily")
3. Make it public or private
4. Add your bot as **Administrator** (with "Post Messages" permission)

### 3. Get Channel Chat ID

1. Post any message in your channel
2. Open in browser: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   (Replace `<YOUR_TOKEN>` with your bot token)
3. Look for `"chat":{"id":-1001234567890` → Copy the number (starts with `-100...`)

### 4. Fork This Repository

Click the **Fork** button at the top right of this repo → Create your own copy.

### 5. Add Secrets to Your Forked Repo

1. Go to your forked repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these:

| Name           | Value                                    |
| -------------- | ---------------------------------------- |
| `BOT_TOKEN`    | Your bot token from BotFather            |
| `CHAT_ID`      | Your channel ID (e.g., -100123...)       |
| `NASA_API_KEY` | Your NASA key (optional but recommended) |

> Get free NASA API key: https://api.nasa.gov/ (instant)

### 6. (Optional) Customize Schedule

Edit `.github/workflows/run.yml`:

```yaml
- cron: "0 */2 * * *" # Change to your preferred frequency Examples:(Every hour: 0 * * * *,      Every 4 hours: 0 */4 * * *, Once daily: 0 0 * * *

```
