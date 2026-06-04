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
    ("Agroportal", "https://agroportal.pt/feed/"),
    ("ECO", "https://eco.sapo.pt/rss/"),
    ("Público", "https://www.publico.pt/rss"),
    ("Jornal de Notícias", "https://www.jn.pt/rss/"),
    ("Expresso", "https://expresso.pt/rss"),
    ("Euractiv Agriculture & Food", "https://www.euractiv.com/section/agriculture-food/feed/"),
    ("Politico Europe", "https://www.politico.eu/feed/"),
    ("Reuters Europe", "https://www.reuters.com/world/europe/rss.xml"),
    ("Farmers Weekly", "https://www.fwi.co.uk/rss"),
    ("AgWeb", "https://www.agweb.com/feed/"),
    ("Farm Progress", "https://www.farmprogress.com/rss"),
    ("Agriculture.com", "https://www.agriculture.com/rss"),
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
    "farmers",
    "pecuária",
    "silvicultura",
    "agroindústria",
    "agrotech",
    "agronegócio",
    "agronegocio",
    "agropecuária",
    "agropecuaria",
    "horticultura",
    "agrifoodtech",
    "foodtech",
    "commodities",
    "commoditie",
    "fertilizer",
    "fertilizante",
    "irrigation",
    "irrigação",
    "supply chain",
    "bioeconomy",
    "bioeconomia",
    "food security",
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

            categories = []
            for tag in getattr(entry, "tags", []) or []:
                if isinstance(tag, dict):
                    categories.append(tag.get("term", ""))
                else:
                    categories.append(getattr(tag, "term", ""))
            categories_text = " ".join([cat for cat in categories if cat])

            articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "published": published,
                    "text": text,
                    "is_keyword": match_keywords(text) or match_keywords(categories_text),
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
            <article class=\"card\">
              <div>
                <h2><a href=\"{item['url']}\" target=\"_blank\" rel=\"noopener noreferrer\">{item['title']}</a></h2>
                <div class=\"meta\">{item['source']} · {item['published'].strftime('%d/%m/%Y %H:%M UTC')}</div>
              </div>
              <div class=\"article-share\">
                <a class=\"share-link\" href=\"mailto:?subject=Notícia agribusiness&body={email_body}\">Partilhar por email</a>
                <a class=\"share-link\" href=\"https://api.whatsapp.com/send?text={whatsapp_text}\" target=\"_blank\">Partilhar no WhatsApp</a>
              </div>
            </article>
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
    :root {{
      color-scheme: light;
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f7fb;
      color: #111827;
    }}

    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 0; background: linear-gradient(180deg, #f5f7fb 0%, #ffffff 100%); }}
    a {{ color: inherit; text-decoration: none; }}
    img {{ max-width: 100%; display: block; }}

    .site-shell {{ max-width: 1180px; margin: 0 auto; padding: 24px 20px 40px; }}
    .site-header {{ display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 18px 0; }}
    .brand {{ font-size: 1rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f3d68; }}
    .nav-links {{ display: flex; gap: 16px; font-size: 0.95rem; color: #475569; }}
    .nav-links a {{ color: #475569; transition: color 0.2s ease; }}
    .nav-links a:hover {{ color: #0b6cf3; }}

    .hero {{ background: linear-gradient(135deg, #0b6cf3 0%, #264c8f 100%); border-radius: 32px; color: white; padding: 56px 40px; position: relative; overflow: hidden; }}
    .hero::before {{ content: ""; position: absolute; inset: 0; background: radial-gradient(circle at top right, rgba(255,255,255,0.15), transparent 28%); pointer-events: none; }}
    .hero::after {{ content: ""; position: absolute; inset: 0; background: radial-gradient(circle at bottom left, rgba(255,255,255,0.08), transparent 26%); pointer-events: none; }}
    .hero-content {{ position: relative; z-index: 1; max-width: 760px; }}
    .eyebrow {{ text-transform: uppercase; letter-spacing: 0.2em; font-size: 0.75rem; margin-bottom: 18px; color: rgba(255,255,255,0.85); }}
    .hero h1 {{ font-size: clamp(2.4rem, 4vw, 4rem); line-height: 1.02; margin: 0 0 20px; }}
    .hero p {{ font-size: 1.05rem; line-height: 1.8; max-width: 680px; color: rgba(255,255,255,0.92); margin: 0 0 28px; }}

    .hero-actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; }}
    .button {{ display: inline-flex; align-items: center; justify-content: center; min-height: 50px; padding: 0 22px; border-radius: 999px; border: none; cursor: pointer; font-weight: 700; transition: transform 0.2s ease, background 0.2s ease; }}
    .button.primary {{ background: #ffffff; color: #0b6cf3; }}
    .button.primary:hover {{ transform: translateY(-1px); background: #eff6ff; }}
    .button.secondary {{ background: rgba(255,255,255,0.18); color: white; }}
    .button.secondary:hover {{ transform: translateY(-1px); background: rgba(255,255,255,0.28); }}

    .hero-meta {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: 14px; margin-top: 32px; }}
    .hero-card {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.14); border-radius: 18px; padding: 18px 20px; }}
    .hero-card strong {{ display: block; font-size: 1.15rem; margin-bottom: 8px; }}
    .hero-card span {{ color: rgba(255,255,255,0.8); font-size: 0.92rem; }}

    .section-title {{ margin: 56px 0 20px; font-size: 1.75rem; line-height: 1.1; color: #0f172a; }}
    .description {{ max-width: 760px; margin: 0 0 28px; color: #475569; font-size: 1rem; line-height: 1.8; }}

    .news-grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(280px,1fr)); gap: 20px; }}
    .card {{ background: white; border-radius: 24px; padding: 24px; box-shadow: 0 24px 80px rgba(15, 23, 42, 0.08); border: 1px solid rgba(15,23,42,0.06); display: flex; flex-direction: column; gap: 16px; }}
    .card h2 {{ font-size: 1.1rem; margin: 0; line-height: 1.4; }}
    .card h2 a {{ color: #0f3d68; }}
    .card h2 a:hover {{ color: #0b6cf3; }}
    .card .meta {{ font-size: 0.9rem; color: #64748b; margin: 0; }}
    .card .article-share {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: auto; }}
    .share-link {{ display: inline-flex; align-items: center; gap: 8px; color: #0b6cf3; text-decoration: none; font-size: 0.95rem; }}
    .share-link:hover {{ text-decoration: underline; }}

    .footer {{ margin-top: 48px; padding-top: 32px; border-top: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; color: #64748b; font-size: 0.95rem; }}
    .footer a {{ color: #0b6cf3; }}
    .footer .small {{ max-width: 720px; }}

    @media (max-width: 640px) {{
      .site-header {{ flex-direction: column; align-items: flex-start; gap: 12px; }}
      .hero {{ padding: 36px 22px; }}
      .hero-meta {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="site-shell">
    <header class="site-header">
      <div class="brand">Agribusiness News</div>
      <nav class="nav-links">
        <a href="#noticias">Notícias</a>
        <a href="#partilhar">Partilhar</a>
      </nav>
    </header>

    <section class="hero">
      <div class="hero-content">
        <div class="eyebrow">Seleção semanal</div>
        <h1>Notícias relevantes do agribusiness em Portugal, UE, Reino Unido e EUA</h1>
        <p>Os 10 artigos mais recentes sobre agricultura, inovação agrícola, cadeia de valor e economia agroalimentar, selecionados de fontes credíveis.</p>

        <div class="hero-actions">
          <a class="button primary" href="mailto:?subject=Seleção semanal de notícias agribusiness&body={share_text}">Partilhar por email</a>
          <a class="button secondary" href="https://api.whatsapp.com/send?text={share_text}" target="_blank">Partilhar no WhatsApp</a>
        </div>

        <div class="hero-meta">
          <div class="hero-card">
            <strong>Última atualização</strong>
            <span>{generated_at.strftime('%d/%m/%Y %H:%M UTC')}</span>
          </div>
          <div class="hero-card">
            <strong>Total de notícias</strong>
            <span>{len(news)}</span>
          </div>
          <div class="hero-card">
            <strong>Fonte</strong>
            <span>Portugal · UE · UK · EUA</span>
          </div>
        </div>
      </div>
    </section>

    <main>
      <h2 id="noticias" class="section-title">Últimas notícias</h2>
      <p class="description">A seleção abaixo apresenta as notícias mais recentes e relevantes do setor agribusiness, ordenadas por data.</p>

      <div class="news-grid">
        {''.join(rows)}
      </div>
    </main>

    <footer class="footer">
      <div class="small">Fonte: notícias públicas de jornais credíveis de Portugal, União Europeia, Reino Unido e Estados Unidos.</div>
      <div>© {generated_at.year} Notícias Agribusiness</div>
    </footer>
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

    history["last_generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_history(history)

    print(f"Geradas {len(selection)} notícias em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
