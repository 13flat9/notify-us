import logging
import os

from azure.communication.email import EmailClient
from .construct_msg import construct_msg
from .table_models import Listing

#from azure.identity import DefaultAzureCredential
#AZURE_TENANT_ID = "dffdfdd4-77f5-445a-9dc0-1f5c6d259395"
#AZURE_CLIENT_ID = ""
#AZURE_CLIENT_SECRET = ""   #can't find these since: 
                            #can't access azure active directory since:
                            #can't change user settings since:
                            #they're greyed out for some reason
                            
                            #therefore this can't run locally (?)

logger = logging.getLogger(__name__)


def get_email_client() -> EmailClient:
    #TODO: would this work with Azure AD?
    # To use Azure Active Directory Authentication (DefaultAzureCredential) make sure to have AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET as env variables.
    # endpoint = "https://<name>.europe.communication.azure.com"
    # email_client = EmailClient(endpoint, DefaultAzureCredential()) # credential not working

    connection_string = os.environ["COMMUNICATION_SERVICES_CONNECTION_STRING"]
    return EmailClient.from_connection_string(connection_string)


def mail_new_listings(email_client: EmailClient, new_listings: list[Listing], dest_address: str):
    try:

        message = construct_msg(new_listings, dest_address)

        POLLER_WAIT_TIME = 10

        poller = email_client.begin_send(message)
        time_elapsed = 0
        while not poller.done():
            print("Sending email, poller status: " + poller.status())

            poller.wait(POLLER_WAIT_TIME)
            time_elapsed += POLLER_WAIT_TIME

            if time_elapsed > 30 * POLLER_WAIT_TIME:
                raise RuntimeError("Polling timed out.")

        if poller.result()["status"] == "Succeeded":
            logger.info(f"Successfully sent the email (operation id: {poller.result()['id']})")
        else:
            raise RuntimeError(str(poller.result()["error"]))
    except Exception as ex: # or 'except (HttpResponseError, RuntimeError) as ex'
        raise EmailFailed(f"Problem sending listings: {new_listings} to user {dest_address}") from ex

class EmailFailed(Exception):
    pass