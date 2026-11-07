# Payment Reconciliation

A Python-based payment reconciliation script that processes payment events from a provider export and calculates the total amount successfully collected.

## How the data works

`payments.jsonl` contains payment events, with one JSON object per line.

Each event contains:

- `txn_id`: Unique identifier for a transaction.
- `status`: Payment status (`success`, `failed`, or `pending`).
- `amount`: Payment amount in naira.
- `currency`: Transaction currency.
- `ts`: Timestamp indicating when the payment attempt occurred (UTC).

A transaction may have multiple payment attempts. Only the latest attempt for each transaction determines whether the payment is considered collected.

## Implementation

The original reconciliation logic counted every successful payment event independently. This caused incorrect totals when a transaction had multiple attempts.

The updated implementation addresses this by:

1. **Reading payment events:** Processes `payments.jsonl` one line at a time.
2. **Handling malformed data:** Uses exception handling to skip lines that cannot be parsed as valid JSON.
3. **Validating transaction IDs:** Skips events that do not contain a usable `txn_id`.
4. **Tracking the latest attempts:** Uses a Python dictionary keyed by `txn_id` to keep the latest event for each transaction.
5. **Comparing timestamps:** Replaces an existing event only when a newer timestamp is encountered.
6. **Calculating collected payments:** Counts and sums only transactions whose latest attempt has a `success` status.
7. **Verifying the result:** Compares the calculated successful-payment count against the finance team's expected count in `expected.txt`.

Python's `Decimal` is used for monetary calculations to avoid floating-point precision issues. Thousands-separator commas are removed from formatted amounts before conversion.

## Requirements

- Python 3
- No third-party packages required.

## Project Structure

```text
koya-payment-reconciliation/
├── payments.jsonl
├── expected.txt
├── reconcile.py
└── README.md
```

## Running the Script

Run the following command from the project directory:

```bash
python reconcile.py
```

The script reads the payment records, performs reconciliation, and checks the calculated successful-payment count against `expected.txt`.

## Verification

A successful run produces output similar to:

```text
Check passed: 22733 successful payments.
Your code: KOYA-[generated-code]
```

The generated code is calculated from the total amount collected after reconciliation.

## Submission

The repository contains the updated reconciliation implementation and documentation. The generated code is obtained by running the script successfully.
