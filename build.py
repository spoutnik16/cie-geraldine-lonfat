#!/usr/bin/env python3
"""
Build script for Compagnie Géraldine Lonfat website.
Reads JSON data + Jinja2 templates → generates static HTML in docs/
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import re

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Jinja2 non installé. Installation...")
    os.system("pip install jinja2")
    from jinja2 import Environment, FileSystemLoader

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = BASE_DIR / "docs"

MONTHS_FR = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "août",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
}


def load_data():
    """Load all JSON data files."""
    data = {}
    for name in ["shows", "events", "bio", "shows_extra"]:
        path = DATA_DIR / f"{name}.json"
        with open(path, "r", encoding="utf-8") as f:
            data[name] = json.load(f)
    return data


def parse_iso(iso_str):
    """Parse ISO datetime string (Python 3.6 compatible)."""
    clean = re.sub(r'[+-]\d{2}:\d{2}$', '', iso_str)
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(clean, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse: {iso_str}")


def format_date_fr(iso_str):
    """Format ISO datetime to French date string."""
    dt = parse_iso(iso_str)
    return "{} {} {}".format(dt.day, MONTHS_FR[dt.month], dt.year)


def clean_html_description(html):
    """Clean up Django HTML description for static site display."""
    if not html:
        return ""
    # Remove <section> and <iframe> tags but keep content
    text = re.sub(r'<section[^>]*>', '', html)
    text = re.sub(r'</section>', '', text)
    # Remove iframes (YouTube embeds — we handle trailers separately)
    text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.DOTALL)
    # Remove div wrappers (leftsmall, rightbig, etc.)
    text = re.sub(r'<div[^>]*>', '', text)
    text = re.sub(r'</div>', '', text)
    # Remove links to old site
    text = re.sub(r'<a[^>]*href="http://compagnieinterface[^"]*"[^>]*>(.*?)</a>', r'\1', text)
    # Remove <strong> links
    text = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', text)
    # Clean up HTML entities
    text = text.replace('&amp;', '&')
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text.strip()


def prepare_shows(data):
    """Add computed fields to shows, merge extra data."""
    shows = data["shows"]
    events = data["events"]
    extras = data["shows_extra"]

    for show in shows:
        # Find first/last year from events
        show_events = [e for e in events if e["show_id"] == show["id"]]
        played_dates = []
        for ev in show_events:
            for d in ev["dates"]:
                if not d["cancelled"]:
                    played_dates.append(d["datetime"])
        if played_dates:
            played_dates.sort()
            show["first_year"] = parse_iso(played_dates[0]).year
            show["last_year"] = parse_iso(played_dates[-1]).year
        else:
            show["first_year"] = "\u2014"
            show["last_year"] = "\u2014"

        # Merge extra data (press quotes, trailer, gallery)
        slug = show["slug"]
        if slug in extras:
            extra = extras[slug]
            show["press_quotes"] = extra.get("press_quotes", [])
            show["trailer_id"] = extra.get("trailer_id")
            show["trailer_type"] = extra.get("trailer_type")
            show["gallery_images"] = extra.get("gallery_images", [])
        else:
            show["press_quotes"] = []
            show["trailer_id"] = None
            show["trailer_type"] = None
            show["gallery_images"] = []

        # Clean HTML description for display
        show["description_clean"] = clean_html_description(show.get("description", ""))

    return shows


def prepare_calendar(data):
    """Prepare chronological event list grouped by year."""
    events_by_year = {}
    total_played = 0
    total_cancelled = 0

    for ev in data["events"]:
        for d in ev["dates"]:
            dt = parse_iso(d["datetime"])
            year = dt.year
            if year not in events_by_year:
                events_by_year[year] = []

            date_display = f"{dt.day} {MONTHS_FR[dt.month]}"
            if dt.hour > 0:
                date_display += f" \u00b7 {dt.hour}h{dt.minute:02d}"

            events_by_year[year].append({
                "datetime": dt,
                "date_display": date_display,
                "show_name": ev["show_name"],
                "venue": ev["venue"],
                "city": ev["city"],
                "country": ev["country"],
                "cancelled": d["cancelled"],
            })

            if d["cancelled"]:
                total_cancelled += 1
            else:
                total_played += 1

    # Sort events within each year
    for year in events_by_year:
        events_by_year[year].sort(key=lambda e: e["datetime"])

    # Return as sorted list of tuples
    sorted_years = sorted(events_by_year.items())
    first_year = sorted_years[0][0] if sorted_years else 2003
    last_year = sorted_years[-1][0] if sorted_years else 2024

    return sorted_years, total_played, total_cancelled, first_year, last_year


def build():
    """Build the entire site."""
    print("Chargement des donn\u00e9es...")
    data = load_data()
    shows = prepare_shows(data)
    events_by_year, total_played, total_cancelled, first_year, last_year = prepare_calendar(data)

    # Sort shows chronologically for navigation
    shows_chrono = sorted(
        shows,
        key=lambda s: (0 if s.get("first_year") == "\u2014" else s.get("first_year", 0))
    )

    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
    )
    # Add striptags filter
    def striptags(text):
        return re.sub(r'<[^>]+>', '', text) if text else ''
    env.filters['striptags'] = striptags

    # Build name→slug mapping for show links
    show_slug_map = {s["name"]: s["slug"] for s in shows}
    def show_link(name):
        slug = show_slug_map.get(name)
        if slug:
            return '<a href="spectacle-{}.html">{}</a>'.format(slug, name)
        return name
    env.filters['show_link'] = show_link

    # Common context
    context = {
        "bio": data["bio"],
        "shows": shows,
        "current_year": datetime.now().year,
    }

    # Build main pages
    pages = {
        "index.html": {
            "shows_recent": sorted(
                shows,
                key=lambda s: (9999 if s.get("first_year") == "\u2014" else s.get("first_year", 0)),
                reverse=True,
            )[:6],
        },
        "spectacles.html": {},
        "parcours.html": {},
        "calendrier.html": {
            "events_by_year": events_by_year,
            "total_played": total_played,
            "total_cancelled": total_cancelled,
            "first_year": first_year,
            "last_year": last_year,
        },
        "contact.html": {},
    }

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    for page_name, page_context in pages.items():
        template = env.get_template(page_name)
        full_context = {**context, **page_context}
        html = template.render(**full_context)

        output_path = OUTPUT_DIR / page_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  OK {page_name}")

    # Build individual show pages
    show_template = env.get_template("spectacle.html")
    for i, show in enumerate(shows_chrono):
        prev_show = shows_chrono[i - 1] if i > 0 else None
        next_show = shows_chrono[i + 1] if i < len(shows_chrono) - 1 else None

        show_context = {
            **context,
            "show": show,
            "prev_show": prev_show,
            "next_show": next_show,
        }
        html = show_template.render(**show_context)

        page_name = f"spectacle-{show['slug']}.html"
        output_path = OUTPUT_DIR / page_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  OK {page_name}")

    # Copy static files
    static_dest = OUTPUT_DIR / "static"
    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(STATIC_DIR, static_dest)
    print(f"  OK static/")

    print(f"\nSite genere dans {OUTPUT_DIR}/")
    print(f"  {total_played} representations, {len(shows)} spectacles, {data['bio']['stats']['num_countries']} pays")


if __name__ == "__main__":
    build()
