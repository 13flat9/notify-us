MSG_SUBJECT = "New job postings"
#this needs to be fixed
SRC_ADDRESS = "DoNotReply@f18bd175-d34b-4510-bf53-1929a38740bd.azurecomm.net"

def format_msg_html(new_entries: list[tuple[str]]) -> str:
    prefix = "<p>Hey,</p>\n \
        <p>There are new job postings matching your criteria at buehnenjobs.de.</p>"
    postfix = "<p>I hope this is useful!</p>\n\
        <p>Cheers!</p>"
    return f"{prefix}\n{format_table(new_entries)}\n{postfix}"

def format_table(new_entries: list[tuple[str]]) -> str:
    href_prefix = "https://buehnenjobs.de"
    table_html = "<table>\n"
    for entry in new_entries:
        name, href = entry
        complete_href = f"{href_prefix}{href}"
        table_html += f"  <tr>\n    <td><a href='{complete_href}'>{name}</a></td>\n  </tr>\n"
    table_html += "</table>"
    return table_html

def format_msg_plaintext(new_entries: list[tuple[str]]) -> str:
    table_text = "Entries:\n"
    for entry in new_entries:
        name, href = entry
        table_text += f"- {name}: {href}\n"
    prefix = "Hey,\n \
        There are new job postings matching your criteria at buehnenjobs.de."
    postfix = "I hope this is useful!\n\
        Cheers!"
    return f"{prefix}\n{table_text}\n{postfix}"

def construct_msg(new_entries: list[tuple[str]], dest_address: str) -> dict:
    return {
        "content": {
            "subject": f"{MSG_SUBJECT}",
            "plainText": f"{format_msg_plaintext(new_entries)}",
            "html": f"{format_msg_html(new_entries)}"
        },
        "recipients": {
            "to": [
                {
                    "address": f"{dest_address}",
                    "displayName": "someone"
                }
            ]
        },
        "senderAddress": SRC_ADDRESS
    }
