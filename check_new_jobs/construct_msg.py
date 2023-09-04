MSG_SUBJECT = "New job postings from buehnenjobs.de"
SRC_ADDRESS = "DoNotReply@f18bd175-d34b-4510-bf53-1929a38740bd.azurecomm.net"
from .table_models import Listing, User

def format_msg_html(new_entries: list[Listing]) -> str:
    prefix = "<p>Hey,</p>\n \
        <p>There are new job postings matching your criteria at buehnenjobs.de.</p>"
    postfix = "<p>I hope this is useful!</p>\n\
        <p>Cheers!</p>"
    return f"{prefix}\n{format_table(new_entries)}\n{postfix}"

def format_table(new_entries: list[Listing]) -> str:
    href_prefix = "https://buehnenjobs.de"
    table_html = "<table>\n"
    for entry in new_entries:
        name, href = entry.name, entry.href
        complete_href = f"{href_prefix}{href}"
        table_html += f"  <tr>\n    <td><a href='{complete_href}'>{name}</a></td>\n  </tr>\n"
    table_html += "</table>"
    return table_html

def format_msg_plaintext(new_entries: list[Listing]) -> str:
    table_text = "Entries:\n"
    for entry in new_entries:
        table_text += entry.__str__()
    prefix = "Hey,\n \
        There are new job postings matching your criteria at buehnenjobs.de."
    postfix = "I hope this is useful!\n\
        Cheers!"
    return f"{prefix}\n{table_text}\n{postfix}"

def construct_msg(new_entries: list[Listing], recipient: User) -> dict:
    return {
        "content": {
            "subject": f"{MSG_SUBJECT}",
            "plainText": f"{format_msg_plaintext(new_entries)}",
            "html": f"{format_msg_html(new_entries)}"
        },
        "recipients": {
            "to": [
                {
                    "address": f"{recipient.email}",
                    "displayName": "someone"
                }
            ]
        },
        "senderAddress": SRC_ADDRESS
    }
