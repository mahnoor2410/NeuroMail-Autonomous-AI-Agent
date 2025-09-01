import base64
import re
from gmail_auth import gmail_service

# ===================  HELPER FUNCTIONS ==========================

def _safe_b64decode(s):
    """ Decode base64 string safely.Gmail API uses URL-safe base64 encoding. """
    if not s:
        return ""
    s = s.replace("-", "+").replace("_", "/") # Convert URL-safe base64 to standard base64
    padding = len(s) % 4
    if padding:
        s += "=" * (4 - padding)
    return base64.b64decode(s) # Decode to bytes

# ===============================================================

def _get_body_from_payload(payload):
    """
    Recursively extract plain text from email payload.
    Emails can be multi-part (text/plain, text/html, attachments, etc.)
    """
    if "parts" in payload: # If email has multiple parts
        for part in payload["parts"]:
            mime = part.get("mimeType", "")
            # If plain text part exists, decode and return it
            if mime == "text/plain" and part.get("body", {}).get("data"):
                return _safe_b64decode(part["body"]["data"]).decode(errors="ignore")
            # Otherwise, check nested parts
            nested = _get_body_from_payload(part)
            if nested:
                return nested
    else:
        # Single-part email
        data = payload.get("body", {}).get("data")
        if data:
            return _safe_b64decode(data).decode(errors="ignore")
    return "" # If no text found

# ================================================================

def extract_email_address(header_from):
    """
    Extracts the email address from the 'From' header.
    Example: "John Doe <john@example.com>" -> "john@example.com"
    """
    if not header_from:
        return None
    m = re.search(r"[\w\.-]+@[\w\.-]+", header_from)
    return m.group(0) if m else header_from

# ====================  MAIN FUNCTION  ==========================

def fetch_latest_emails(max_results=10, unread_only=False):
    """
    Returns a list of emails: dict with keys:
    id, threadId, from, from_email, to, subject, snippet, body
    """
    service = gmail_service() # Connect to Gmail API
    q = "is:unread" if unread_only else None
    # Fetch list of message IDs
    res = service.users().messages().list(userId="me", maxResults=max_results, q=q).execute()
    msgs = res.get("messages", []) or [] # Default to empty list if none found
    out = []

    for m in msgs: 
        # Fetch full email details by ID
        mdata = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        payload = mdata.get("payload", {}) # Get email headers + body
        headers = payload.get("headers", [])
        header_map = {h["name"]: h["value"] for h in headers} # Convert headers list to a dictionary for easier access
        
        # Extract useful fields
        subj = header_map.get("Subject", "")
        frm = header_map.get("From", "")
        to = header_map.get("To", "")
        snippet = mdata.get("snippet", "")
        body = _get_body_from_payload(payload) or snippet # Use snippet if body not found

        # Append email info to output list
        out.append({
            "id": m["id"],
            "threadId": mdata.get("threadId"),
            "from": frm,
            "from_email": extract_email_address(frm),
            "to": to,
            "subject": subj,
            "snippet": snippet,
            "body": body
        })
    return out

if __name__ == "__main__":
    emails = fetch_latest_emails(5, unread_only=False)
    for e in emails:
        print("From:", e["from"])
        print("Email:", e["from_email"])
        print("Subject:", e["subject"])
        print("Body (first 200 chars):", e["body"][:200])
        print("-"*40)
