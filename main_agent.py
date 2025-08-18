from gmail_fetcher import fetch_latest_emails
from tone_detector import detect_tone
from reply_generator import generate_reply
from gmail_drafts import create_draft, send_message

AUTO_SEND = False  # change to True if you want replies sent automatically (be careful!)

def run_once(max_emails=5, unread_only=True):
    emails = fetch_latest_emails(max_results=max_emails, unread_only=unread_only)
    if not emails:
        print("No emails to process.")
        return

    # Loop through each email
    for e in emails:
        print("Processing:", e["subject"], "from", e["from_email"])
        # Use body/snippet/subject for tone detection
        text_for_tone = e["body"] or e["snippet"] or e["subject"]
        tone = detect_tone(text_for_tone)
        print("Detected tone:", tone)

        reply_text = generate_reply(e["subject"], text_for_tone, tone)
        print("Generated reply (first 200 chars):", reply_text[:200])

        # Prepare recipient and subject
        to_addr = e.get("from_email") or e.get("from")
        reply_subject = "Re: " + (e.get("subject") or "")

        # If AUTO_SEND=True → send email directly
        if AUTO_SEND:
            sent = send_message(to_addr, reply_subject, reply_text, thread_id=e.get("threadId")) # Ensure reply is in same thread
            print("Sent message id:", sent.get("id"))

        # Else → create draft safely (prevent duplicate drafts)
        else:
           from gmail_drafts import draft_exists  # Check if draft exists for this thread

           if not draft_exists(e.get("threadId")):
                draft = create_draft(to_addr, reply_subject, reply_text, thread_id=e.get("threadId"))
                print("📝 Draft created:", draft.get("id"))
           else:
                print("⚠️ Draft already exists for this email. Skipping.")

if __name__ == "__main__":
    run_once(max_emails=5, unread_only=True)
