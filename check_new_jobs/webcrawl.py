from bs4 import BeautifulSoup
import requests, logging
from .config import ListingMaxLength
from check_new_jobs.table_models import Listing

logger = logging.getLogger(__name__)


class WebcrawlerStuckInLoop(Exception):
    pass


class TooManyUnsuccessfulHttpRequests(Exception):
    pass


def fetch_all_table_rows(url) -> list[Listing]:
    all_rows = []
    jobs_start = 0

    suspiciously_large_number_of_requests = 50
    n_unsuccessful_requests = 0
    while True:
        current_url = url.format(jobs_start)
        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except Exception as e:
            if n_unsuccessful_requests >= suspiciously_large_number_of_requests:
                raise TooManyUnsuccessfulHttpRequests(
                    f"Webcrawler made {n_unsuccessful_requests} unsuccessful GET requests") from e
            else:
                n_unsuccessful_requests += 1
                continue

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('tr')

        new_entries_added = False
        for row in rows[1:]:  # Skip the header row
            name_cell = row.select_one('td.name')
            if name_cell:
                name = name_cell.get_text().strip()
                href = name_cell.find('a').get('href').strip()
                entry = (name, href)

                if entry not in all_rows:
                    all_rows.append(entry)
                    new_entries_added = True

        if not new_entries_added:
            break
        if jobs_start > suspiciously_large_number_of_requests * 15:
            raise WebcrawlerStuckInLoop(
                f"Webcrawler made {suspiciously_large_number_of_requests * 15} GET requests and may be stuck in an infinite loop")

        jobs_start += 15

    return [Listing(name=entry[0][:ListingMaxLength], href=entry[1]) for entry in all_rows]
