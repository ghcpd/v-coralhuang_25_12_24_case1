# text_report_original.py
#
# Simplistic baseline for generating a text report from user activity logs.
# The code works, but the output is hard to read and the structure is poor.
# This file is intentionally written in an "unpleasant" style to create room
# for enhancement, not just refactoring.

import datetime


def generate_report(logs):
    """
    logs: list of dicts, each dict example:
      {
        "user_id": "u123",
        "user_name": "Alice",
        "event": "login",
        "ts": "2025-03-01T10:21:30",
        "metadata": {"ip": "1.2.3.4"}
      }
    """
    report = "USER ACTIVITY REPORT\n"
    report = report + "===================\n"
    total = 0
    user_set = []
    events = {}
    first_ts = None
    last_ts = None

    for log in logs:
        total = total + 1
        uid = log.get("user_id", "UNKNOWN")
        if uid not in user_set:
            user_set.append(uid)
        evt = log.get("event", "UNKNOWN")
        if evt not in events:
            events[evt] = 1
        else:
            events[evt] = events[evt] + 1

        ts_str = log.get("ts")
        if ts_str:
            try:
                ts = datetime.datetime.fromisoformat(ts_str)
            except Exception:
                ts = None
        else:
            ts = None

        if ts is not None:
            if first_ts is None:
                first_ts = ts
            if last_ts is None:
                last_ts = ts
            if ts < first_ts:
                first_ts = ts
            if ts > last_ts:
                last_ts = ts

    report = report + "Total logs: " + str(total) + "\n"
    report = report + "Unique users: " + str(len(user_set)) + "\n"
    report = report + "User IDs: "
    for u in user_set:
        report = report + u + ","
    report = report + "\n"

    report = report + "Events count:\n"
    for evt in events:
        report = report + "- " + evt + ": " + str(events[evt]) + "\n"

    if first_ts and last_ts:
        report = (
            report
            + "Time range: "
            + first_ts.isoformat()
            + " -> "
            + last_ts.isoformat()
            + "\n"
        )
    elif first_ts:
        report = report + "Time range: from " + first_ts.isoformat() + "\n"
    else:
        report = report + "Time range: UNKNOWN\n"

    # Per-user details in a very rough way
    report = report + "\nDETAILS\n"
    report = report + "-------\n"

    # Extremely inefficient / ugly: re-scan for each user
    for u in user_set:
        report = report + "User: " + u + "\n"
        for log in logs:
            uid = log.get("user_id", "UNKNOWN")
            if uid == u:
                ts = log.get("ts", "UNKNOWN")
                evt = log.get("event", "UNKNOWN")
                name = log.get("user_name", "UNKNOWN")
                report = (
                    report
                    + "  - "
                    + str(ts)
                    + " "
                    + name
                    + " "
                    + evt
                    + "\n"
                )
        report = report + "\n"

    return report


if __name__ == "__main__":
    sample_logs = [
        {
            "user_id": "u1",
            "user_name": "Alice",
            "event": "login",
            "ts": "2025-03-01T10:21:30",
            "metadata": {"ip": "1.2.3.4"},
        },
        {
            "user_id": "u2",
            "user_name": "Bob",
            "event": "login",
            "ts": "2025-03-01T10:22:00",
            "metadata": {"ip": "5.6.7.8"},
        },
        {
            "user_id": "u1",
            "user_name": "Alice",
            "event": "view_page",
            "ts": "2025-03-01T10:23:10",
            "metadata": {"page": "/home"},
        },
        {
            "user_id": "u2",
            "user_name": "Bob",
            "event": "logout",
            "ts": "2025-03-01T10:25:00",
            "metadata": {},
        },
    ]

    print(generate_report(sample_logs))
