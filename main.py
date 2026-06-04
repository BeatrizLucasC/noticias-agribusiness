from __future__ import annotations

import calendar
import datetime
import json
import os
import urllib.parse
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parent
HISTORY_FILE = ROOT / "history.json"
OUTPUT_FILE = ROOT / "index.html"
MAX_NEWS = 10

NEWS_SOURCES = [
    ("Público", "https://www.publico.pt/rss"),
    ("Jornal de Notícias", "https://www.jn.pt/rss/"),
    ("Expresso", "https://expresso.pt/rss"),
    ("ECO", "https://eco.sapo.pt/rss/"),
    ("Euractiv", "https://www.euractiv.com/section/agriculture-food/feed/"),
    ("Politico Europe", "https://www.politico.eu/feed/"),
    ("Reuters Europe", "https://www.reuters.com/world/europe/rss.xml"),
    ("Guardian UK", "https://www.theguardian.com/world/uk-news/rss"),
    ("Reuters UK", "https://www.reuters.com/world/uk/rss.xml"),
    ("BBC UK", "https://feeds.bbci.co.uk/news/uk/rss.xml"),
    ("Reuters US", "https://www.reuters.com/world/us/rss.xml"),
    ("New York Times Business", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"),
]

KEYWORDS = [
    "agribusiness",
    "agriculture",
    "agro",
    "food",
    "agroalimentar",
    "agricultura",
    "agricole",
    "agrifood",
    "farm",
    "pecuária",
    "silvicultura",
    "agroindústria",
    "agrotech",
]


def parse_datetime(entry) -> datetime.datetime:
    parsed = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if parsed:
        return datetime.datetime.fromtimestamp(calendar.timegm(parsed), tz=datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)


def load_history() -> dict:
    if HISTORY_FILE.exists():
        with HISTORY_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"seen_urls": [], "last_generated": None}


def save_history(history: dict) -> None:
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def match_keywords(text: str) -> bool:
    normalized = text.lower()
    return any(keyword in normalized for keyword in KEYWORDS)


def load_articles() -> list[dict]:
    articles = []
    seen = set()

    for source_name, feed_url in NEWS_SOURCES:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            url = entry.get("link") or entry.get("id")
            if not url or url in seen:
                continue
            seen.add(url)
            published = parse_datetime(entry)
            title = entry.get("title", "Sem título").strip()
            summary = entry.get("summary", "").strip()
            text = f"{title} {summary}" if summary else title
            articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "published": published,
                    "text": text,
                    "is_keyword": match_keywords(text),
                }
            )

    return articles


def build_html(news: list[dict], generated_at: datetime.datetime) -> str:
    rows = []
    for item in news:
        email_body = urllib.parse.quote(f"{item['title']}\n{item['url']}")
        whatsapp_text = urllib.parse.quote(f"{item['title']} {item['url']}")
        rows.append(
            f"""
            <li>
              <article>
                <h2><a href=\"{item['url']}\" target=\"_blank\" rel=\"noopener noreferrer\">{item['title']}</a></h2>
                <div class=\"meta\">{item['source']} · {item['published'].strftime('%d/%m/%Y %H:%M UTC')}</div>
                <div class=\"article-share\">
                  <a class=\"share-link\" href=\"mailto:?subject=Notícia agribusiness&body={email_body}\">Partilhar por email</a>
                  <a class=\"share-link\" href=\"https://api.whatsapp.com/send?text={whatsapp_text}\" target=\"_blank\">Partilhar no WhatsApp</a>
                </div>
              </article>
            </li>
            """
        )

    page_url = "index.html"
    share_text = urllib.parse.quote(
        "Seleção semanal de notícias agribusiness. Aqui tens as 10 notícias mais recentes: " + page_url
    )

    return f"""
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Notícias Agribusiness - Seleção Semanal</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f8f8f8; color: #1a1a1a; }}
    .page {{ max-width: 960px; margin: 0 auto; padding: 24px; }}
    header {{ margin-bottom: 24px; }}
    h1 {{ font-size: 2.4rem; margin: 0 0 8px; }}
    p.subtitle {{ margin: 0; color: #555; }}
    .share-group {{ margin: 18px 0; }}
    .button {{ display: inline-block; margin: 0 8px 8px 0; padding: 10px 18px; border: none; border-radius: 6px; background: #0b6cf3; color: white; text-decoration: none; font-weight: 600; }}
    .button.secondary {{ background: #444; }}
    ol {{ padding-left: 18px; }}
    li {{ margin-bottom: 22px; background: white; padding: 18px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    h2 {{ font-size: 1.1rem; margin: 0 0 8px; }}
    h2 a {{ color: #0b6cf3; text-decoration: none; }}
    .meta {{ font-size: 0.93rem; color: #666; margin-bottom: 12px; }}
    .article-share {{ margin-top: 10px; }}
    .share-link {{ margin-right: 12px; color: #0b6cf3; text-decoration: none; font-size: 0.95rem; }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <h1>Seleção semanal de notícias agribusiness</h1>
      <p class="subtitle">Última atualização: {generated_at.strftime('%d/%m/%Y %H:%M UTC')}</p>
    </header>

    <div class="share-group">
      <a class="button" href="mailto:?subject=Seleção semanal de notícias agribusiness&body={share_text}">Partilhar por email</a>
      <a class="button secondary" href="https://api.whatsapp.com/send?text={share_text}" target="_blank">Partilhar no WhatsApp</a>
    </div>

    <p>Esta página apresenta uma seleção de notícias sobre agribusiness de Portugal, países da UE, Reino Unido e Estados Unidos, ordenadas pela data de publicação.</p>
    <ol>
      {''.join(rows)}
    </ol>
  </div>
</body>
</html>
"""


def build_news_page(articles: list[dict]) -> None:
    generated_at = datetime.datetime.now(datetime.timezone.utc)
    html = build_html(articles, generated_at)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write(html)


def main() -> None:
    history = load_history()
    articles = load_articles()
    articles = [article for article in articles if article["url"] not in history["seen_urls"]]
    articles.sort(key=lambda item: item["published"], reverse=True)

    relevant = [article for article in articles if article["is_keyword"]]
    if len(relevant) < MAX_NEWS:
        remaining = [item for item in articles if item not in relevant]
        relevant.extend(remaining)

    selection = relevant[:MAX_NEWS]
    if not selection:
        print("Nenhuma notícia disponível no momento. Tenta executar de novo mais tarde.")
        return

    build_news_page(selection)

    history["seen_urls"].extend(item["url"] for item in selection)
    history["seen_urls"] = history["seen_urls"][-1000:]
    history["last_generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_history(history)

    print(f"Geradas {len(selection)} notícias em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
