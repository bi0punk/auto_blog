import logging
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.db import transaction

from blog.models import Post

logger = logging.getLogger(__name__)


def _parse_lat_lon(raw: str) -> tuple[float | None, float | None]:
    match = re.match(r'([\-\d.]+)\s*/\s*([\-\d.]+)', raw)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None


def _parse_utc_time(raw: str) -> datetime | None:
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S'):
        try:
            return datetime.strptime(raw.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


@shared_task
def scrape_and_save() -> int:
    today = datetime.now()
    url = (
        f'https://www.sismologia.cl/sismicidad/catalogo/'
        f'{today.year}/{today.month:02d}/{today.year}{today.month:02d}{today.day:02d}.html'
    )

    logger.info('Scraping %s', url)

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error('Error fetching %s: %s', url, e)
        return 0

    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', class_='sismologia detalle')
    if table is None:
        logger.warning('Table not found on page')
        return 0

    rows = table.find_all('tr')[1:]
    if not rows:
        logger.warning('No data rows found in table')
        return 0

    created = 0
    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all('td')]
        if len(cols) < 5:
            continue

        local_raw = cols[0]
        location = local_raw.split('/')[-1].strip() if '/' in local_raw else local_raw

        utc_time = _parse_utc_time(cols[1])
        lat, lon = _parse_lat_lon(cols[2])
        depth = _parse_float(cols[3])
        magnitude = _parse_float(cols[4])

        title = f'Sismo en {location}' if location else 'Sismo detectado'

        with transaction.atomic():
            Post.objects.create(
                title=title,
                location=location,
                magnitude=magnitude,
                depth_km=depth,
                latitude=lat,
                longitude=lon,
                utc_time=utc_time,
            )
            created += 1

    logger.info('Saved %d earthquake records', created)
    return created


def _parse_float(raw: str) -> float | None:
    try:
        return float(raw.strip().replace(',', '.'))
    except (ValueError, AttributeError):
        return None
