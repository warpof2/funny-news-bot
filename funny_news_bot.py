import feedparser
import openai
import telegram
import time

# === НАСТРОЙКИ ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # например: @funnydailynews

NEWS_FEED_URL = "http://feeds.bbci.co.uk/news/rss.xml"

openai.api_key = OPENAI_API_KEY
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def get_news():
    feed = feedparser.parse(NEWS_FEED_URL)
    return feed.entries[:3]

def generate_funny_post(title, summary):
    prompt = f"""
You're a witty AI news commentator. Read the news and respond with a short, funny comment and a light-hearted piece of advice.

News title: {title}
Summary: {summary}

Respond in this format:
"Funny Comment"
Advice: "Short advice"
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message["content"]

def post_to_telegram(text):
    bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    posted_titles = set()

    while True:
        news_items = get_news()
        for item in news_items:
            if item.title in posted_titles:
                continue
            funny_text = generate_funny_post(item.title, item.summary)
            post_text = f"*{item.title}*

{funny_text}"
            post_to_telegram(post_text)
            posted_titles.add(item.title)
            time.sleep(5)
        time.sleep(1800)

if __name__ == "__main__":
    main()