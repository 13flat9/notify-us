import datetime, logging
from .webcrawl import fetch_all_table_rows
from . import database as db
from .email import mail_new_listings, get_email_client, EmailFailed

logger = logging.getLogger(__name__)


def main() -> None:
    base_url = "https://buehnenjobs.de/?jobs_start={}&subcat=chor"

    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logger.info(f"Executing function at {utc_timestamp}")

    all_current_listings = fetch_all_table_rows(base_url)

    email_client = get_email_client()

    with db.create_session(db.create_engine()) as session:
        session_manager = db.SessionManager(session)
        old_listings = session_manager.fetch_listings()
        old_listing_hrefs = [listing.href for listing in old_listings]
        new_listings = [
            listing for listing in all_current_listings if listing.href not in old_listing_hrefs
        ]

        for user in session_manager.fetch_users():
            new_matching_listings = [
                listing for listing in new_listings if
                keywords_in_string(session_manager.fetch_keywords(user), listing.name)
            ]
            if new_matching_listings:
                try:
                    mail_new_listings(email_client, new_matching_listings, user)
                except EmailFailed as ex:
                    logger.critical("Failed to mail new listings to a user", exc_info=ex)

        session_manager.insert_listings(new_listings)


# TODO: Delete old listings.
# Also: what if something else went wrong, might want to preserve them?
# TODO: what if the same listing is reposted with a different href? seems to happen occasionally

def keywords_in_string(keywords: list[str], string: str) -> bool:
    for keyword in keywords:
        if keyword.lower() in string.lower():
            return True
    return False
