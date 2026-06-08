import smtplib
import json
import random
import os
from datetime import date, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    ZOHO_EMAIL, ZOHO_APP_PASSWORD, SMTP_HOST, SMTP_PORT,
    SEED_ADDRESSES, RAMP_SCHEDULE, DEFAULT_DAILY_LIMIT, LOG_FILE
)
from templates import TEMPLATES


def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def already_sent_today(log):
    today = date.today().isoformat()
    return [e for e in log if e["date"] == today]


def get_day_number(log):
    if not log:
        return 1
    dates = sorted(set(e["date"] for e in log))
    today = date.today().isoformat()
    if today not in dates:
        return len(dates) + 1
    return dates.index(today) + 1


def get_daily_limit(day_number):
    week = ((day_number - 1) // 7) + 1
    return RAMP_SCHEDULE.get(week, DEFAULT_DAILY_LIMIT)


def send_email(recipient, subject, body):
    msg = MIMEMultipart("alternative")
    msg["From"] = ZOHO_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(ZOHO_EMAIL, ZOHO_APP_PASSWORD)
        server.sendmail(ZOHO_EMAIL, recipient, msg.as_string())


def main():
    log = load_log()
    sent_today = already_sent_today(log)
    day_number = get_day_number(log)
    daily_limit = get_daily_limit(day_number)
    already_sent_count = len(sent_today)
    remaining = daily_limit - already_sent_count
    week = ((day_number - 1) // 7) + 1

    print(f"Day {day_number} | Week {week} | Limit: {daily_limit}/day | Sent today: {already_sent_count} | Remaining: {remaining}")

    if remaining <= 0:
        print("Daily limit already reached. Come back tomorrow.")
        return

    already_sent_to_today = {e["recipient"] for e in sent_today}
    available_seeds = [s for s in SEED_ADDRESSES if s not in already_sent_to_today]

    if not available_seeds:
        print("All seed addresses already emailed today.")
        return

    to_send = min(remaining, len(available_seeds))
    targets = random.sample(available_seeds, to_send)

    for recipient in targets:
        template = random.choice(TEMPLATES)
        subject = template["subject"]
        body = template["body"]
        try:
            send_email(recipient, subject, body)
            log.append({
                "date": date.today().isoformat(),
                "time": datetime.now().strftime("%H:%M:%S"),
                "recipient": recipient,
                "subject": subject,
                "status": "sent",
            })
            print(f"  Sent to {recipient} | Subject: {subject}")
        except Exception as e:
            log.append({
                "date": date.today().isoformat(),
                "time": datetime.now().strftime("%H:%M:%S"),
                "recipient": recipient,
                "subject": subject,
                "status": f"failed: {e}",
            })
            print(f"  FAILED to send to {recipient}: {e}")

    save_log(log)
    print(f"Done. Sent {len(targets)} email(s) today.")


if __name__ == "__main__":
    main()
