import datetime, logging
from sqlalchemy import select
from .webcrawl import fetch_all_table_rows
import check_new_jobs.database as db
from check_new_jobs.table_models import Listing
from .email import mail_new_listings, get_email_client, EmailFailed

logger = logging.getLogger(__name__)


def main() -> None:
    base_url = "https://buehnenjobs.de/?jobs_start={}&subcat=chor"

    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logger.info(f"Executing function at {utc_timestamp}")

    all_current_listings = fetch_all_table_rows(base_url)

    email_client = get_email_client()

    with (db.get_session(db.get_engine()) as session):
        old_listings = session.scalars(select(Listing)).all()
        old_listing_hrefs = [listing.href for listing in old_listings]
        new_listings = [
            listing for listing in all_current_listings if listing.href not in old_listing_hrefs
        ]

        for user in db.get_users(session):
            new_matching_listings = [
                listing for listing in new_listings if keywords_in_string(db.get_keywords(session, user), listing.name)
            ]
            if new_matching_listings:
                try:
                    mail_new_listings(email_client, new_matching_listings, user)
                except EmailFailed as ex:
                    logger.critical("Failed to mail new listings to a user", exc_info=ex)

        for listing in new_listings:
            session.add(listing)

def keywords_in_string(keywords: list[str], string: str) -> bool:
    for keyword in keywords:
        if keyword.lower() in string.lower():
            return True
    return False
