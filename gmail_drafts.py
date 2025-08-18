from gmail_auth import gmail_service
from email.mime.text import MIMEText # For creating plain text email
import base64

# ============= Helper function: create a raw encoded email message =============

def _create_raw_message(to_addr, subject, body_text, in_reply_to=None):
    msg = MIMEText(body_text)
    msg["To"] = to_addr
    msg["Subject"] = subject

    # If replying to existing email
    if in_reply_to: 
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to

    # Encode email in base64 for Gmail API
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return raw

# ================== Function to create a draft email ====================

def create_draft(to_addr, subject, body_text, thread_id=None):
    service = gmail_service()
    raw = _create_raw_message(to_addr, subject, body_text) # Prepare raw message
    message = {"raw": raw}
    if thread_id: # If replying to a thread
        message["threadId"] = thread_id
    draft = service.users().drafts().create(userId="me", body={"message": message}).execute()
    return draft

# ============== Function to check if a draft already exists for a thread =============

def draft_exists(thread_id):
    service = gmail_service()
    drafts = service.users().drafts().list(userId="me").execute().get("drafts", [])     # List all drafts
    for d in drafts: 
        # Get full draft details
        draft_data = service.users().drafts().get(userId="me", id=d["id"]).execute()
        if draft_data.get("message", {}).get("threadId") == thread_id:
            return True # Check if draft belongs to the same thread
    return False

# ================== Function to send email directly ====================

def send_message(to_addr, subject, body_text, thread_id=None):
    service = gmail_service()
    raw = _create_raw_message(to_addr, subject, body_text, in_reply_to=None)
    body = {"raw": raw}
    if thread_id:
        body["threadId"] = thread_id
    # Call Gmail API to send email
    sent = service.users().messages().send(userId="me", body=body).execute()
    return sent

if __name__ == "__main__":
    d = create_draft("someone@example.com", "Re: Test", "This is a test reply", thread_id=None)
    print("Created draft id:", d.get("id"))
