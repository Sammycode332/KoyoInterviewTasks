#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
from decimal import Decimal
import json


latest_attempts = {}
with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        txn_id = event.get("txn_id")
        if not txn_id:
            continue
        if txn_id not in latest_attempts:
            latest_attempts[txn_id] = event
        elif event["ts"] > latest_attempts[txn_id]["ts"]:
            latest_attempts[txn_id] = event
total = Decimal ("0.0")
count = 0
for event in latest_attempts.values():
    if event["status"] == "success":
        amount = Decimal(str(event["amount"]).replace(",", ""))
        total += Decimal(amount)
        count += 1
with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
