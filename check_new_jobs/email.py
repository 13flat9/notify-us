import logging
import os

from azure.communication.email import EmailClient
from .construct_msg import construct_msg

logger = logging.getLogger(__name__)

def get_email_client() -> EmailClient:
    connection_string = os.environ["COMMUNICATION_SERVICES_CONNECTION_STRING"]
    return EmailClient.from_connection_string(connection_string)


def mail_new_listings(email_client, new_listings, dest_address):
    try:
        message = construct_msg([(listing.name, listing.href) for listing in new_listings], dest_address)

        POLLER_WAIT_TIME = 10

        poller = email_client.begin_send(message)
        time_elapsed = 0
        while not poller.done():
            print("Email send poller status: " + poller.status())

            poller.wait(POLLER_WAIT_TIME)
            time_elapsed += POLLER_WAIT_TIME

            if time_elapsed > 30 * POLLER_WAIT_TIME:
                raise RuntimeError("Polling timed out.")

        if poller.result()["status"] == "Succeeded":
            logger.info(f"Successfully sent the email (operation id: {poller.result()['id']})")
        else:
            raise RuntimeError(str(poller.result()["error"]))
    except Exception as ex:
        raise EmailFailed(f"Problem sending listings: {new_listings} to user {dest_address}") from ex

class EmailFailed(Exception):
    pass