#!/usr/bin/env python3
"""
mastercard_field_details.py
=============================
Value-level detail lookups for the Mastercard DMS ISO 8583 parser
(mastercard_iso8583_parser.py).

mastercard_iso8583_parser.py's describe_label()  -> "what IS this field/subfield?"
this file's get_value_detail()                    -> "what does THIS VALUE of it mean?"

STATUS / COVERAGE:
Built from (a) value tables confirmed against live sample traffic,
(b) enumerated-code tables transcribed directly from the "Mastercard
Network Processing - Dual Message Authorization System Guide" (16 June
2026 edition), and (c) a field-level GLOSSARY (see FIELD_GLOSSARY below)
transcribed from that guide's "Dual Message System data element
abbreviations" appendix, which gives one authoritative definition
paragraph per data element. The glossary is what fields like F4-F16
(amounts, dates, STAN), F32/33/35/37/38/41/42/43, F48, F52/55/61/63,
F90, and F122 get as their "Detail" line - those fields are structural/
free-form/binary data rather than enumerated codes, so there's no value
to look up, but the spec still defines exactly what the field IS and how
it's used, which is what get_value_detail() now returns instead of a
bare "N/A" for them. Enumerated-code tables (actual value -> meaning
lookups) are still used first wherever they exist and are more specific
than the glossary text.

Enumerated-code tables confirmed against the spec:
  - DE 39 (Response Code) - full Authorization Request Response/0110 table
  - DE 3 (Processing Code) - all 3 subfields (Transaction Type, Account
    Type From, Account Type To) - full tables
  - DE 22 (POS Entry Mode) - subfield 1 (PAN Entry Mode) and subfield 2
    (PIN Entry Capability) - full tables, decomposed from the single
    3-digit field value the parser emits
  - DE 48, subelement 61 (POS Data Extended Condition Codes) - all 5
    positional subfields, decomposed from the single 5-digit subelement
    value the parser emits
  - DE 48, subelement 87 (Card Validation Code Result) - CVC1/CVC2/CVC3/
    Amex CID value tables (the spec overloads this subelement across
    several validation types that share the same letter codes; the
    detail function surfaces all of them since the raw value alone
    doesn't disambiguate which one applies)
  - DE 48, subelement 42 (Electronic Commerce Indicators), subfield 1
    positions 1-3 (Security Protocol / Cardholder Authentication / UCAF
    Collection Indicator) - decomposed from the leading 3 digits of the
    subelement value; any additional digits (subfields 2-3, present only
    on SLI-modified transactions) are flagged but not yet decomposed
  - DE 49/50/51 (Currency Code) - the two codes actually seen in sample
    traffic (050 BDT, 840 USD); this is otherwise the external ISO 4217
    standard and is not duplicated here beyond what's been confirmed

DELIBERATELY NOT (yet) covered, and why:
  - DE 18 (MCC) / DE 19 (country codes): externally standardized code
    sets (ISO 18245 / ISO 3166-1) reused verbatim from those standards
    rather than transcribed here.
  - DE 39 value tables for message families other than 0110 (e.g.
    0120/0130, 0420/0430, 0810) - the spec lists these separately per
    message type and they haven't been transcribed yet.
  - DE 48 subelement VALUE meanings for subelements 32/37/43/63/66/71
    (Mastercard Assigned ID, Additional Merchant Data, UCAF, Trace ID,
    Authentication Data, On-behalf Services) - these are mostly
    free-form data (IDs, cryptographic material, merchant-supplied
    text) rather than enumerated codes, so there's no code table to
    transcribe; the parser's FIELD48_TAG_NAMES already names what they
    are, this file would only add a generic reminder of that.
  - DE 55 EMV tag *value* meanings beyond generic pass-through -
    individual TVR/CVM/AIP bit meanings are a large table on their own
    and weren't in scope yet (matches the same scoping decision the
    Visa parser's detail file made).
  - DE 61 (POS Data) and DE 122 subelement internal structure - not yet
    broken into named subfields at the parser level (see
    mastercard_iso8583_parser.py's docstring "KNOWN OPEN ITEMS"), so
    there's nothing to attach a value table to yet.
  - DE 90 subfield 5's meaning is unconfirmed at the parser level too -
    no detail function is registered for it.

Every entry below is either (a) transcribed from the Mastercard Dual
Message Authorization System Guide, or (b) derived directly from a
byte-for-byte confirmed sample.

CURRENCY FORMATTING (added):
currency_dict.py (CURRENCY_DISPLAY: {"050": ("BDT", "Taka"), ...}) must sit
in the same folder as this file and mastercard_iso8583_parser.py. It backs
two things:
  - _detail_currency() below now names the currency in the F49/50/51
    "Detail" line using the full table, not just the old 2-entry shortlist.
  - format_currency_amount() turns a raw DE4/5/6 amount (implied last-2-
    digit decimal, standard ISO 8583 convention) plus its paired DE49/50/51
    code into a human amount, e.g. "1,000 BDT (Taka)". format_field_report()
    calls this automatically and appends it as a new "* Formatted:" line
    right after "* Detail:" for F4, F5, and F6 only (the three DE that
    carry a monetary amount paired with a currency code field).
"""

try:
    from currency_dict import CURRENCY_DISPLAY
except ImportError:
    CURRENCY_DISPLAY = {}

# ---------------------------------------------------------------------------
# Simple code -> meaning tables
# ---------------------------------------------------------------------------

VALUE_TABLES = {

    # ---- DE 39 (Response Code) - Authorization Request Response/0110
    # table, transcribed from the DMS Guide's "Authorization Request
    # Response/0110 response codes" section. ----
    "F39": {
        "00": "Approved or completed successfully.",
        "01": "Refer to card issuer.",
        "03": "Invalid merchant.",
        "04": "Capture card.",
        "05": "Do not honor. Issuers should use this response code only when no other reason code applies.",
        "08": "Honor with identification.",
        "10": "Partial approval.",
        "12": "Invalid transaction.",
        "13": "Invalid amount.",
        "14": "Invalid card number.",
        "15": "Invalid issuer.",
        "30": "Format error.",
        "41": "Lost card - capture.",
        "43": "Stolen card - capture.",
        "46": "Closed account.",
        "51": "Insufficient funds / over credit limit.",
        "54": "Expired card.",
        "55": "Invalid PIN.",
        "57": "Transaction not permitted to issuer/cardholder.",
        "58": "Transaction not permitted to acquirer/terminal.",
        "61": "Exceeds withdrawal amount limit (issuers may also use this for non-ATM transaction types).",
        "62": "Restricted card.",
        "63": "Security violation.",
        "65": "Exceeds withdrawal count limit, OR Identity Check soft-decline of EMV 3DS authentication "
              "(merchant should resubmit authentication).",
        "70": "Contact card issuer.",
        "71": "PIN not changed.",
        "72": "Account not yet activated.",
        "75": "Allowable number of PIN tries exceeded.",
        "76": "Invalid/nonexistent 'To Account' specified.",
        "77": "Invalid/nonexistent 'From Account' specified.",
        "78": "Invalid/nonexistent account specified (general).",
        "79": "Life cycle (Mastercard use only).",
        "81": "Domestic debit transaction not allowed (regional use only).",
        "82": "Policy (Mastercard use only).",
        "83": "Fraud/Security (Mastercard use only).",
        "84": "Invalid authorization life cycle.",
        "85": "Not declined. Valid for all zero-amount transactions.",
        "86": "PIN validation not possible.",
        "87": "Purchase amount only, no cash back allowed (approved).",
        "88": "Cryptographic failure - may indicate a failed AAV validation; a new authentication with a "
              "new AAV and DS Transaction ID may be necessary to complete AAV validation (Dynamic Linking).",
        "89": "Unacceptable PIN - transaction declined, retry.",
        "91": "Authorization system or issuer system inoperative.",
        "92": "Unable to route transaction.",
        "94": "Duplicate transmission detected.",
        "96": "System error.",
    },

    # ---- DE 3, subfield 1 (Cardholder Transaction Type Code) - full
    # table from the spec's "Subfield 1 values" section. ----
    "F3.TXN_TYPE": {
        "00": "Purchase (also used to identify Funding Transactions under the Mastercard Move - "
              "MoneySend and Funding Transactions Program Standards).",
        "01": "Withdrawal.",
        "02": "Debit Adjustment.",
        "09": "Purchase with Cash Back.",
        "17": "Cash Disbursement.",
        "18": "Scrip Issue.",
        "20": "Purchase Return/Refund.",
        "21": "Deposit.",
        "22": "Credit Adjustment.",
        "28": "Payment Transaction.",
        "30": "Balance Inquiry.",
        "40": "Account Transfer.",
        "90": "Reserved for Future Use.",
        "91": "PIN Unblock.",
        "92": "PIN Change.",
    },

    # ---- DE 3, subfield 2 (Cardholder From Account Type Code) - full
    # table from the spec's "Subfield 2 values" section. ----
    "F3.ACCT_FROM": {
        "00": "Default Account (not specified or not applicable).",
        "10": "Savings Account.",
        "20": "Checking Account.",
        "30": "Credit Card Account.",
        "38": "Credit Line Account.",
        "39": "Corporate.",
        "40": "Universal Account (Customer ID number).",
        "50": "Money Market Investment Account.",
        "60": "Stored Value Account.",
        "90": "Revolving Loan Account.",
    },

    # ---- DE 3, subfield 3 (Cardholder To Account Type Code) - full
    # table from the spec's "Subfield 3 values" section. ----
    "F3.ACCT_TO": {
        "00": "Default Account (not specified or not applicable).",
        "10": "Savings Account.",
        "20": "Checking Account.",
        "30": "Credit Card Account.",
        "38": "Credit Line Account.",
        "40": "Universal Account.",
        "50": "Money Market Investment Account.",
        "58": "IRA Investment Account.",
        "90": "Revolving Loan Account.",
        "91": "Installment Loan Account.",
        "92": "Real Estate Loan Account.",
    },

    # ---- DE 22, subfield 1 (POS Terminal PAN Entry Mode) - full table
    # from the spec. ----
    "F22.PAN_ENTRY": {
        "00": "Merchant terminal PAN entry mode unknown.",
        "01": "Merchant terminal PAN manual entry.",
        "02": "Merchant terminal PAN auto-entry via magnetic stripe.",
        "03": "Merchant terminal PAN auto-entry via bar code reader.",
        "04": "Merchant terminal PAN auto-entry via optical character reader (OCR).",
        "05": "Merchant terminal PAN auto-entry via integrated circuit card (chip).",
        "07": "Merchant terminal PAN auto-entry via contactless M/Chip.",
        "09": "PAN/Token entry via electronic commerce containing DSRP cryptogram in DE 55 (ICC "
              "System-Related Data).",
        "10": "Credential on File.",
        "79": "Chip fallback to magnetic-stripe voice transaction (hybrid terminal chip read/online "
              "send failed; PAN and expiry communicated by voice). See M/Chip Requirements for details.",
        "80": "Chip card at chip-capable terminal defaulted to magnetic-stripe read PAN; full track "
              "data read from the card and transmitted unaltered in DE 45 or DE 35.",
        "81": "PAN/Token entry via electronic commerce, with optional Identity Check AAV in DE 48 "
              "subelement 43 (UCAF) or DSRP cryptogram in DE 104 subelement 001.",
        "82": "Electronic Commerce PAN Auto Entry via Server (issuer, acquirer, or third-party vendor system).",
        "90": "PAN auto-entry via magnetic stripe - full track data read from the card and transmitted "
              "in DE 35 or DE 45 without alteration or truncation.",
        "91": "PAN auto-entry via contactless magnetic stripe - full track data transmitted in DE 35 "
              "or DE 45 without alteration or truncation.",
        "95": "Visa only. Chip card with unreliable Card Verification Value (CVV) data.",
    },

    # ---- DE 22, subfield 2 (POS Terminal PIN Entry Mode) - full table
    # from the spec. ----
    "F22.PIN_CAPABILITY": {
        "0": "Unspecified or unknown.",
        "1": "Terminal has PIN entry capability.",
        "2": "Terminal does not have PIN entry capability.",
        "3": "mPOS software-based PIN entry capability.",
        "8": "Terminal has PIN entry capability but the PIN pad is not currently operative.",
    },

    # ---- DE 48, subelement 61 - 5 positional subfields, full tables
    # from the spec. ----
    "F48.61.1": {
        "0": "Merchant terminal does not support receipt of partial approvals.",
        "1": "Merchant terminal supports receipt of partial approvals.",
    },
    "F48.61.2": {
        "0": "Merchant terminal does not support receipt of purchase-only approvals.",
        "1": "Merchant terminal supports receipt of purchase-only approvals.",
    },
    "F48.61.3": {
        "0": "Merchant terminal did not verify the purchased items against an Inventory Information "
             "Approval System (IIAS).",
        "1": "Merchant terminal verified the purchased items against an IIAS.",
        "2": "Merchant claims exemption from using an IIAS based on the IRS 90 percent rule.",
        "4": "Submitted as real-time substantiated but from a non-IIAS-certified merchant (Mastercard-"
             "inserted; acquirers may not use this value).",
    },
    "F48.61.4": {
        "0": "No action required.",
        "1": "Transaction to be scored by Expert Monitoring for Merchants.",
    },
    "F48.61.5": {
        "0": "Normal Authorization / Undefined Finality.",
        "1": "Final Authorization.",
    },

    # ---- DE 48, subelement 87 (Card Validation Code Result) - the spec
    # overloads this subelement's letter codes across CVC1/CVC2/CVC3/Amex
    # CID validation depending on context; all tables are given since the
    # raw value doesn't disambiguate which validation type produced it. ----
    "F48.87.CVC1": {
        "Y": "Invalid CVC 1 (only meaningful if DE 35 or DE 45 was present in the Authorization "
             "Request/0100 message).",
    },
    "F48.87.CVC2": {
        "M": "Valid CVC 2 (match).",
        "N": "Invalid CVC 2 (non-match).",
        "P": "CVC 2 not processed (issuer temporarily unavailable).",
        "U": "CVC 2 unverified (Mastercard use only).",
    },
    "F48.87.CVC3": {
        "E": "Length of unpredictable number was not a valid length.",
        "P": "Unable to process.",
        "Y": "Invalid.",
    },
    "F48.87.AMEX_CID": {
        "Y": "Valid CID (match).",
        "N": "Invalid CID (non-match).",
        "U": "CID not processed.",
    },

    # ---- DE 48, subelement 42, subfield 1, position 1 (Security Protocol) ----
    "F48.42.POS1": {
        "0": "Reserved for existing Mastercard Europe/Visa definitions.",
        "1": "Reserved for future use.",
        "2": "Channel.",
    },
    # ---- DE 48, subelement 42, subfield 1, position 2 (Cardholder Authentication) ----
    "F48.42.POS2": {
        "0": "Reserved for future use.",
        "1": "eCommerce / Identity Check.",
        "3": "Reserved for future use.",
        "4": "Tokenized payment.",
    },
    # ---- DE 48, subelement 42, subfield 1, position 3 (UCAF Collection Indicator) ----
    "F48.42.POS3": {
        "0": "Non-authenticated payment, Identity Check transaction with failed authentication, or "
             "Tokenized Payment with Dynamic Token Verification Code (DTVC).",
        "1": "UCAF data collection supported by the merchant; UCAF data must be present (DE 48.43 "
             "must contain an attempt AAV for Mastercard Identity Check).",
        "2": "UCAF data collection supported by the merchant; UCAF data must be present (DE 48.43 "
             "must contain a fully authenticated AAV; DSRP cryptogram optional for tokenized "
             "transactions). Includes cardholder-initiated transactions (CIT) for authentication.",
        "3": "UCAF data collection supported by the merchant; UCAF (Mastercard-assigned Static AAV) "
             "data must be present. DE 48 subelements 32 and 43 are required for Static AAV transactions.",
        "4": "Merchant has chosen to share authentication data within authorization; UCAF data must "
             "be present (DE 48.43 must contain an Insights AAV for Mastercard Identity Check).",
        "5": "Reserved for future use.",
        "6": "Merchant Risk Based Decisioning or Data Share Only for Mastercard Identity Check, or a "
             "tokenized transaction with a DSRP cryptogram (DE 104 subelement 001), or both.",
        "7": "Merchant-initiated transaction (DE 48.43 only required for Identity Check).",
    },

    # ---- MTI (Message Type Indicator) - names of the message types
    # actually confirmed in sample traffic; other DMS message types exist
    # in the spec (e.g. 0120/0130 Advice, 0800/0810 Network Management)
    # but haven't been sampled yet. ----
    "MTI": {
        "0100": "Authorization Request.",
        "0110": "Authorization Request Response.",
        "0400": "Reversal Request.",
        "0410": "Reversal Request Response.",
        "0420": "Reversal Advice.",
        "0430": "Reversal Advice Response.",
    },

    # ---- DE 49/50/51 (Currency Code) - only codes actually observed in
    # sample traffic; this is otherwise the external ISO 4217 standard. ----
    "CURRENCY_CODE": {
        "840": "US Dollar (USD).",
        "050": "Bangladeshi Taka (BDT).",
    },
}


# ---------------------------------------------------------------------------
# Field-level glossary: structural/definitional text for fields that do NOT
# have an enumerated code table (amounts, dates, IDs, free-text/binary
# fields). Transcribed from the DMS Guide's "Dual Message System data
# element abbreviations" appendix, which gives one authoritative paragraph
# per DE. Used as the fallback "Detail" line for any field/subfield that
# doesn't have a more specific DETAIL_FUNCS entry - this is what fields
# like F4-F16, F32/33/35/37/38/41/42/43, F48, F52/55/61/63, F90 and F122
# get instead of the old blanket "N/A" message.
# ---------------------------------------------------------------------------

FIELD_GLOSSARY = {
    "F2": "Primary Account Number (PAN) - identifies a customer account or relationship.",
    "F3": "Processing Code - describes the effect of a transaction on the customer account and "
          "the type of accounts affected (see subfields 1-3 for the decoded breakdown).",
    "F4": "Amount, Transaction - the amount of funds the cardholder requested, in the local "
          "currency of the acquirer or source location of the transaction (currency given by F49).",
    "F5": "Amount, Reconciliation (spec name: Amount, Settlement) - the amount of funds to be "
          "transferred between acquirer and issuer, equal to F4 but expressed in the settlement "
          "currency (F50). Mastercard programs and services use U.S. dollars as the settlement currency.",
    "F6": "Amount, Cardholder Billing - the transaction amount in the issuer's currency (F51); the "
          "amount billed to the cardholder in the cardholder account currency, excluding cardholder "
          "billing fees.",
    "F7": "Transmission Date and Time(MMDDHHMISS) - the date and time the message was entered into the "
          "Mastercard Network, expressed in Coordinated Universal Time (UTC).",
    "F9": "Conversion Rate, Reconciliation (spec name: Conversion Rate, Settlement) - the factor "
          "used to convert F4 (Amount, Transaction) into F5 (Amount, Settlement): F4 x F9 = F5.",
    "F10": "Conversion Rate, Cardholder Billing - the factor used to convert F4 (Amount, "
           "Transaction) into F6 (Amount, Cardholder Billing): F4 x F10 = F6.",
    "F11": "Systems Trace Audit Number (STAN) - a number the message initiator assigns to uniquely "
           "identify a transaction.",
    "F12": "Time, Local Transaction (hhmmss) [UTC Time Format] - the local time at which the transaction takes place at the "
           "point-of-interaction location.",
    "F13": "Date, Local Transaction(MMDD) - the local month and day on which the transaction takes place "
           "at the point-of-interaction location.",
    "F14": "Date, Expiration (YYMM) - the year and month after which the issuer designates the "
           "cardholder's card to be expired.",
    "F15": "Date, Settlement (MMDD)- the date (month and day) that funds will be transferred between an "
           "acquirer and an issuer or an appropriate intermediate network facility (INF).",
    "F16": "Date, Conversion (MMDD) - the effective date of F9 (Conversion Rate, Reconciliation) and F10 "
           "(Conversion Rate, Cardholder Billing) whenever those data elements are present in the message.",
    "F18": "Merchant Type - the classification (acceptor business code / Merchant Category Code "
           "[MCC]) of the merchant's type of business or service.",
    "F19": "Acquiring Institution Country Code - based on Mastercard franchise data information "
           "(ISO 3166-1 numeric country code).",
    "F23": "Card Sequence Number - distinguishes among separate cards sharing the same PAN (F2) or "
           "extended PAN (F34). Issuers may encode this on the chip; acquirers with chip-reading "
           "capability may pass it through here from an Authorization Request/0100 message.",
    "F32": "Acquiring Institution ID Code - identifies the acquiring institution (e.g. merchant "
           "bank) or its agent.",
    "F33": "Forwarding Institution ID Code - identifies the institution forwarding a Request or "
           "Advice message if it is not the same institution as F32; carries the Mastercard "
           "six-digit customer/INF ID responsible for routing the message to the DMS.",
    "F35": "Track 2 Data - the information encoded on track 2 of the card's magnetic stripe per "
           "ISO 7813, including data element separators but excluding the beginning/ending "
           "sentinels and the longitudinal redundancy check (LRC) character.",
    "F37": "Retrieval Reference Number (RRN) - a document reference number supplied by the system "
           "retaining the original source document of the transaction, used to locate that "
           "document or a copy of it (e.g. by automated merchant POS systems for regulatory/legal "
           "source-document capture).",
    "F38": "Authorization ID Response - the transaction response ID code the authorizing "
           "institution assigns; carries the card issuer's 'authorization code'.",
    "F41": "Acceptor Terminal ID - the identifier assigned by the acceptor or acquirer to the "
           "terminal, payment gateway, or other acceptance device used to capture account data at "
           "the acceptor location.",
    "F42": "Acceptor ID - the identifier assigned by the acquirer to the acceptor (merchant) and "
           "its location, or to the payment facilitator.",
    "F43": "Acceptor Name and Location - the name and location of the acceptor point of interaction "
           "(see subfields 1-5 for the decoded Name/City/Country breakdown).",
    "F48": "Additional Data - Private Use - data associated with various Mastercard programs, "
           "products, and services; a variable-length field used for multiple purposes not "
           "related to any other ISO-defined data element (see the F48.NN subelement for its "
           "specific purpose).",
    "F52": "Personal ID Number (PIN) Data - a number (or a derivative of it) assigned to a "
           "cardholder to uniquely identify them at the point of interaction, used to transmit PIN "
           "information from acquirer to issuer/network for verification. Subject to bilateral "
           "encryption agreement; always rendered masked here since it's encrypted binary.",
    "F55": "Integrated Circuit Card (ICC) System-Related Data - binary EMV chip data processed only "
           "by the issuer, issuer's agent, or MDES; used locally by the chip payment application at "
           "a chip-capable terminal. Present in chip full-grade transactions and can be present in "
           "DSRP transactions (see the F55.<tag> EMV tags for the decoded chain).",
    "F61": "Point-of-Service (POS) Data - indicates the conditions that existed at the point of "
           "service at the time of the transaction. In the Mastercard DMS, F61 supersedes and "
           "replaces the ISO-specified DE 25 (POS Condition Code), which is not used in this "
           "message family. Internal positional subfields are not yet decomposed by this parser "
           "(see mastercard_iso8583_parser.py's open items).",
    "F63": "Network Data - generated by the Dual Message Authorization System for each originating "
           "message routed through the network; the receiver must retain this value and echo it "
           "back in any response or acknowledgment associated with the originating message.",
    "F90": "Original Data Elements - the data elements from the original message, used to identify "
           "the transaction being corrected or reversed (see subfields 1-5 for the decoded "
           "original MTI / STAN / transmission date-time / amount breakdown).",
    "F122": "Additional Record Data - a free-format, variable-length field used for transmitting "
            "file record data in various message types (see the F122.NNN subelement(s) for the "
            "raw content actually present).",
}



# ---------------------------------------------------------------------------
# Fields whose "detail" needs decomposition/logic rather than a flat lookup
# ---------------------------------------------------------------------------

def _lookup(table_key, code, field_label):
    table = VALUE_TABLES.get(table_key, {})
    meaning = table.get(code)
    if meaning is None:
        return f"Unrecognized code '{code}' for {field_label} (not in the confirmed spec value table)."
    return meaning


def _detail_f39(value: str) -> str:
    return _lookup("F39", value.strip().upper(), "F39 response code")


def _detail_f3_1(value: str) -> str:
    return _lookup("F3.TXN_TYPE", value.strip(), "F3.1 transaction type")


def _detail_f3_2(value: str) -> str:
    return _lookup("F3.ACCT_FROM", value.strip(), "F3.2 account type, from")


def _detail_f3_3(value: str) -> str:
    return _lookup("F3.ACCT_TO", value.strip(), "F3.3 account type, to")


def _detail_f22(value: str) -> str:
    digits = value.strip()
    if len(digits) != 3:
        return f"POS Entry Mode (3 digits expected: PAN entry mode + PIN capability); got '{value}'."
    pan_mode, pin_cap = digits[0:2], digits[2]
    return (
        f"Positions 1-2 (PAN Entry Mode) = {pan_mode}: {_lookup('F22.PAN_ENTRY', pan_mode, 'F22 PAN entry mode')} | "
        f"Position 3 (PIN Entry Capability) = {pin_cap}: {_lookup('F22.PIN_CAPABILITY', pin_cap, 'F22 PIN capability')}"
    )


def _detail_f48_61(value: str) -> str:
    digits = value.strip()
    if len(digits) != 5:
        return f"POS Data Extended Condition Codes (5 positional digits expected); got '{value}'."
    labels = [
        ("1", "Partial Approval Terminal Support"),
        ("2", "Purchase Amount Only Terminal Support"),
        ("3", "Real-time Substantiation"),
        ("4", "Merchant Transaction Fraud Scoring"),
        ("5", "Final Authorization"),
    ]
    parts = []
    for i, (sub, name) in enumerate(labels):
        code = digits[i]
        parts.append(f"Position {i + 1} ({name}) = {code}: {_lookup('F48.61.' + sub, code, 'F48.61.' + sub)}")
    return " | ".join(parts)


def _detail_f48_87(value: str) -> str:
    code = value.strip().upper()
    interpretations = []
    for table_key, family in (
        ("F48.87.CVC2", "CVC 2"),
        ("F48.87.CVC1", "CVC 1"),
        ("F48.87.CVC3", "CVC 3"),
        ("F48.87.AMEX_CID", "American Express CID"),
    ):
        meaning = VALUE_TABLES.get(table_key, {}).get(code)
        if meaning:
            interpretations.append(f"if {family}: {meaning}")
    if not interpretations:
        return f"Unrecognized Card Validation Code Result value '{value}' (not in any confirmed CVC1/CVC2/CVC3/Amex CID table)."
    return ("The spec overloads this subelement's letter codes across CVC1/CVC2/CVC3/Amex CID "
            "validation - the raw value alone doesn't say which applies, most commonly CVC 2 for "
            "Mastercard transactions: " + "; ".join(interpretations))


def _detail_f48_92(value: str) -> str:
    return ("The CVC 2 value from the card's signature panel, as submitted by the acquirer for "
            "verification (raw data, not a coded field - rendered masked here if redacted).")


def _detail_f48_42(value: str) -> str:
    digits = value.strip()
    if len(digits) < 3:
        return f"Electronic Commerce Indicators: expected at least 3 digits (subfield 1); got '{value}'."
    pos1, pos2, pos3 = digits[0], digits[1], digits[2]
    parts = [
        f"Position 1 (Security Protocol) = {pos1}: {_lookup('F48.42.POS1', pos1, 'F48.42 position 1')}",
        f"Position 2 (Cardholder Authentication) = {pos2}: {_lookup('F48.42.POS2', pos2, 'F48.42 position 2')}",
        f"Position 3 (UCAF Collection Indicator) = {pos3}: {_lookup('F48.42.POS3', pos3, 'F48.42 position 3')}",
    ]
    rest = digits[3:]
    if rest:
        parts.append(f"Remaining {len(rest)} digit(s) = '{rest}': additional subfields (Original SLI / "
                      "UCAF Downgrade Reason, present only when Identity Check downgrade or MDES SLI "
                      "modification occurred) - not yet decomposed into their own value table.")
    return " | ".join(parts)


def _detail_f52(value: str) -> str:
    return ("PIN block - always rendered fully masked; the underlying value is encrypted binary "
            "and not recoverable here.")


_MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def _detail_f35(value: str) -> str:
    """
    DE 35 (Track 2 Data): <PAN><sep><YYMM expiration><3-digit service code><discretionary data>
    where <sep> is the field separator, either '=' (the usual ISO 7813 form)
    or 'D' (the alternate form some issuers/networks use), e.g.
      "37533171******5697=3102226*************" ->
      "37533171******5697D3102226*************" ->
      PAN                : 37533171******5697  (masked)
      Field Separator    : = (or D)
      Expiration (YYMM)  : 3102  -> February 2031
      Service Code       : 226
      Discretionary Data : *************
    """
    raw = value or ""
    sep_char, sep_index = None, None
    for i, ch in enumerate(raw):
        if ch in ("=", "D"):
            sep_char, sep_index = ch, i
            break

    if sep_index is None:
        return (f"Track 2 Data - no field separator ('=' or 'D') found in '{raw}'; cannot split PAN "
                "from expiration/service code/discretionary data.")

    pan, rest = raw[:sep_index], raw[sep_index + 1:]
    parts = [
        f"Primary Account Number (PAN) = {pan} (masked, the cardholder's account number)",
        f"Field Separator = '{sep_char}' (splits the PAN from expiration/service code/discretionary data)",
    ]
    if len(rest) < 4:
        parts.append(f"Remainder too short ({len(rest)} char(s)) to contain a 4-digit expiration "
                      f"date; got '{rest}'.")
        return " | ".join(parts)
    expiry, tail = rest[:4], rest[4:]
    yy, mm = expiry[:2], expiry[2:4]
    month_label = _MONTH_NAMES.get(mm, f"month {mm}")
    parts.append(f"Expiration Date (YYMM) = {expiry}: {month_label} 20{yy}")
    service_code, discretionary = tail[:3], tail[3:]
    if service_code:
        parts.append(f"Service Code = {service_code} (interoperability/authorization rules for "
                      "this card profile)")
    if discretionary:
        parts.append(f"Discretionary Data = {discretionary} (masked validation data payload, e.g. "
                      "CVV1/CVC1)")
    return " | ".join(parts)

def _detail_f37(value: str) -> str:
    """
    DE 37 (Retrieval Reference Number), CIS-style ydddhhnnnnnn format, 12 chars:
      y      (pos 1)    : last digit of the transmission year, equivalent to F7 (Transmission
                           Date and Time)
      ddd    (pos 2-4)  : day of year (001-366), equivalent to F7
      hh     (pos 5-6)  : hour (00-23), the hours value from F7
      nnnnnn (pos 7-12) : Systems Trace Audit Number, the value from F11
    Only positions 1-4 are edited by the network; positions 5-12 are expected
    to be constructed by the endpoint from F7 and F11.
    """
    digits = value.strip()
    if len(digits) != 12:
        return (f"Retrieval Reference Number (RRN) - expected 12 characters in 'ydddhhnnnnnn' "
                f"format; got '{value}' ({len(digits)} char(s)).")
    y, ddd, hh, stan = digits[0], digits[1:4], digits[4:6], digits[6:12]
    return (
        f"Position 1 (Year digit) = {y}: last digit of the transmission year (from F7) | "
        f"Positions 2-4 (Day of Year) = {ddd}: day {int(ddd)} of the year (from F7) | "
        f"Positions 5-6 (Hour) = {hh}: hour {hh} UTC (from F7) | "
        f"Positions 7-12 (STAN) = {stan}: should match F11 (Systems Trace Audit Number)"
    )


def format_f37_cross_check(value: str, value_map: dict):
    """
    Cross-check F37's decoded STAN/hour against this message's own F11 and
    F7, since per spec positions 5-12 are supposed to be built directly
    from those two fields. Returns None if F37 isn't 12 chars.
    """
    digits = value.strip()
    if len(digits) != 12:
        return None
    hh, stan = digits[4:6], digits[6:12]

    bits = [f"Year digit {digits[0]}, Day-of-year {digits[1:4]}, Hour {hh}, STAN {stan}"]

    f11 = (value_map.get("F11") or "").strip()
    if f11:
        bits.append("STAN matches F11" if stan == f11.zfill(6) else f"STAN does NOT match F11 ({f11})")

    f7 = (value_map.get("F7") or "").strip()  # F7 is MMDDhhmmss, 10 chars
    if len(f7) == 10:
        f7_hour = f7[4:6]
        bits.append("hour matches F7" if hh == f7_hour else f"hour does NOT match F7 ({f7_hour})")

    return " | ".join(bits)


def _detail_f55_generic(tag: str, value: str) -> str:
    return (
        f"EMV tag {tag.upper()} value, rendered as hex pass-through (or decimal for a small set of "
        "confirmed tags like 9F27). Bit/byte-level meaning for this tag has not been transcribed yet."
    )


def _detail_currency(value: str) -> str:
    code = value.strip()
    entry = CURRENCY_DISPLAY.get(code)
    if entry:
        alpha, name = entry
        return f"{name} ({alpha}) (ISO 4217 numeric currency code)."
    meaning = VALUE_TABLES.get("CURRENCY_CODE", {}).get(code)
    if meaning:
        return f"{meaning} (ISO 4217 numeric currency code)."
    return f"ISO 4217 numeric currency code '{code}' - not yet in the confirmed short-list here; refer to the ISO 4217 standard."


def _detail_mti(value: str) -> str:
    code = value.strip()
    meaning = VALUE_TABLES.get("MTI", {}).get(code)
    if meaning:
        return meaning
    return (f"Message Type Indicator '{code}' - not yet in the confirmed short-list here "
            "(only 0100/0110/0400/0410/0420/0430 are confirmed against sample traffic so far).")


# ---------------------------------------------------------------------------
# DE4/5/6 amount + DE49/50/51 currency code -> human amount, e.g.
# "1,000 BDT (Taka)". Amounts in these three fields carry an IMPLIED last-2-
# digit decimal (standard ISO 8583 convention, confirmed here against
# 000000100000 + F49="050" -> 1,000.00 BDT).
# ---------------------------------------------------------------------------

AMOUNT_FIELD_TO_CURRENCY_FIELD = {
    "F4": "F49",   # Amount, Transaction        <-> Currency Code, Transaction
    "F5": "F50",   # Amount, Reconciliation      <-> Currency Code, Reconciliation
    "F6": "F51",   # Amount, Cardholder Billing  <-> Currency Code, Cardholder Billing
}


def _currency_label(code: str):
    """Return (alpha_code, name) for a DE49/50/51 numeric code, spec-sourced
    CURRENCY_DISPLAY table first, then the small legacy shortlist, else None."""
    code = (code or "").strip()
    if not code:
        return None
    entry = CURRENCY_DISPLAY.get(code)
    if entry:
        return entry
    legacy = VALUE_TABLES.get("CURRENCY_CODE", {}).get(code)
    if legacy:
        return (code, legacy.rstrip("."))
    return None


def format_currency_amount(amount_value: str, currency_code: str):
    """
    Turn a raw DE4/5/6 amount string plus its paired DE49/50/51 currency
    code into a human-readable amount, e.g.
        format_currency_amount("000000100000", "050") -> "1,000 BDT (Taka)"
    The last 2 digits are always the implied decimal places, per ISO 8583.
    Returns None if there's no amount to format.
    """
    digits = "".join(ch for ch in (amount_value or "") if ch.isdigit())
    if not digits:
        return None
    digits = digits.zfill(3)  # guarantee at least 1 major + 2 minor digits
    major, minor = digits[:-2], digits[-2:]
    major_grouped = f"{int(major):,}"
    amount_display = major_grouped if minor == "00" else f"{major_grouped}.{minor}"

    label = _currency_label(currency_code)
    if label is None:
        code = (currency_code or "").strip()
        return f"{amount_display} {code}".strip() if code else amount_display
    alpha, name = label
    return f"{amount_display} {alpha} ({name})"


# ---------------------------------------------------------------------------
# DE9/10 (Conversion Rate) -> "Conversion: ... | Settlement amount = ..."
# DE9/10 is 8 digits: digit 1 = exponent (decimal places), digits 2-8 =
# 7-digit mantissa. rate = mantissa / 10**exponent (e.g. "70081500" ->
# 81500 / 10**7 = 0.0081500). Paired with F4 (source amount) and the
# matching currency field (F50 for F9, F51 for F10) to derive the
# settlement/billing amount: F4 x rate = settlement amount.
# ---------------------------------------------------------------------------

CONVERSION_FIELD_MAP = {
    "F9":  {"amount_field": "F4", "currency_field": "F50"},   # -> Amount, Reconciliation (F5)
    "F10": {"amount_field": "F4", "currency_field": "F51"},   # -> Amount, Cardholder Billing (F6)
}


def parse_conversion_rate(raw_value: str):
    """8-digit DE9/10 -> float rate, or None if not exactly 8 digits."""
    digits = "".join(ch for ch in (raw_value or "") if ch.isdigit())
    if len(digits) != 8:
        return None
    exponent = int(digits[0])
    mantissa = int(digits[1:])
    return mantissa / (10 ** exponent)


def format_conversion_and_settlement(conversion_label: str, conversion_value: str, value_map: dict):
    """
    Build the "Conversion: ... | Settlement amount = ..." line for F9/F10.
    Uses value_map (label -> value, built once per message by
    format_field_report) to pull the paired amount field (F4) and currency
    field (F50/F51). Returns None if the rate or amount can't be parsed.
    """
    cfg = CONVERSION_FIELD_MAP.get(conversion_label)
    if cfg is None:
        return None
    rate = parse_conversion_rate(conversion_value)
    if rate is None:
        return None

    amount_digits = "".join(ch for ch in (value_map.get(cfg["amount_field"], "") or "") if ch.isdigit())
    rate_str = f"{rate:.7f}".rstrip("0").rstrip(".")
    if not amount_digits:
        return f"Conversion: {rate_str}"

    base_amount = int(amount_digits) / 100          # F4's own implied 2 decimals
    settlement_cents = round(base_amount * rate * 100)
    settlement_str = format_currency_amount(str(settlement_cents), value_map.get(cfg["currency_field"]))

    return f"Conversion: {rate_str} | Settlement amount = {settlement_str}"


DETAIL_FUNCS = {
    "MTI": _detail_mti,
    "F39": _detail_f39,
    "F3.1": _detail_f3_1,
    "F3.2": _detail_f3_2,
    "F3.3": _detail_f3_3,
    "F22": _detail_f22,
    "F35": _detail_f35,
    "F37": _detail_f37,
    "F48.61": _detail_f48_61,
    "F48.87": _detail_f48_87,
    "F48.92": _detail_f48_92,
    "F48.42": _detail_f48_42,
    "F52": _detail_f52,
    "F49": _detail_currency,
    "F50": _detail_currency,
    "F51": _detail_currency,
}

# Direct-lookup labels: value is looked up straight out of VALUE_TABLES
# under the same key, no decomposition needed.
_DIRECT_LOOKUP_LABELS = set()


_NO_DETAIL_YET = "N/A - not yet transcribed into mastercard_field_details.py (confirm against spec or a live sample)."


def get_value_detail(label: str, value: str) -> str:
    """
    Given a compact-format label (e.g. 'F39', 'F3.1', 'F48.61') and its
    already-decoded value string, return a human-readable detail line
    describing what that specific value means, per the Mastercard DMS
    spec where confirmed.

    Resolution order:
      1. A specific DETAIL_FUNCS entry for this exact label (enumerated
         code lookups / positional decompositions).
      2. F55.<tag> generic EMV pass-through note.
      3. A direct VALUE_TABLES lookup for this exact label.
      4. FIELD_GLOSSARY structural text for this exact label (e.g. 'F61').
      5. FIELD_GLOSSARY structural text for the PARENT field of a
         subfield/subelement label (e.g. 'F43.1' falls back to 'F43''s
         glossary text, annotated to make clear it's the parent field's
         general definition rather than something specific to the
         subfield).
      6. Honest "not covered yet" fallback.
    """
    if label in DETAIL_FUNCS:
        try:
            return DETAIL_FUNCS[label](value)
        except Exception as e:
            return f"<detail lookup error: {e}>"

    if label.startswith("F55.") and len(label.split(".")) == 2:
        tag = label.split(".", 1)[1]
        return _detail_f55_generic(tag, value)

    if label in _DIRECT_LOOKUP_LABELS:
        return _lookup(label, value.strip(), label)

    table = VALUE_TABLES.get(label)
    if table is not None:
        meaning = table.get(value) or table.get(value.upper()) or table.get(value.lower())
        if meaning is not None:
            return meaning
        return f"Unrecognized value '{value}' for {label} (not in the confirmed spec value table)."

    if label in FIELD_GLOSSARY:
        return FIELD_GLOSSARY[label]

    if "." in label:
        parent = label.split(".", 1)[0]
        if parent in FIELD_GLOSSARY:
            return f"(Parent field {parent}) {FIELD_GLOSSARY[parent]}"

    return _NO_DETAIL_YET


def format_field_report(rows) -> str:
    """
    Given a list of (label, description, raw_hex, value) rows - the same
    shape mastercard_iso8583_parser.py's parse_message_full() produces -
    render the 'F39: Response Code / * Value: `00` / * Detail: ...' style
    report. For F4/F5/F6 (Amount, Transaction/Reconciliation/Cardholder
    Billing), a "* Formatted:" line is appended after "* Detail:", pairing
    the amount with its currency code from F49/F50/F51 respectively, e.g.
    "* Formatted: 1,000 BDT (Taka)". For F9/F10 (Conversion Rate), a
    "* Formatted:" line shows the decoded rate and the derived settlement/
    billing amount, e.g. "* Formatted: Conversion: 0.00815 | Settlement
    amount = 8.15 USD (US dollar)".
    """
    value_map = {label: value for label, _desc, _raw, value in rows}

    lines = []
    for label, desc, _raw_hex, value in rows:
        title = desc.split(" - ")[-1]
        if ":" in title and title.split(":")[0].strip().lower().startswith("subfield"):
            title = title.split(":", 1)[1].strip()
        lines.append(f"{label}: {title}")
        lines.append("")
        lines.append(f"* Value: `{value}`")
        lines.append(f"* Detail: {get_value_detail(label, value)}")

        currency_field = AMOUNT_FIELD_TO_CURRENCY_FIELD.get(label)
        if currency_field:
            formatted = format_currency_amount(value, value_map.get(currency_field))
            if formatted:
                lines.append(f"* Formatted: {formatted}")

        if label in CONVERSION_FIELD_MAP:
            formatted = format_conversion_and_settlement(label, value, value_map)
            if formatted:
                lines.append(f"* Formatted: {formatted}")

        if label == "F37":
            formatted = format_f37_cross_check(value, value_map)
            if formatted:
                lines.append(f"* Formatted: {formatted}")

        lines.append("")
    return "\n".join(lines)
