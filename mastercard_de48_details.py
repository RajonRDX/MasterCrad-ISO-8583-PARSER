#!/usr/bin/env python3
"""
mastercard_de48_details.py
===========================
Authoritative reference library for parsing layout structures and value tables
of Data Element 48 (Additional Data - Private Use) subelements (01 to 99) 
in the Mastercard Network Processing Dual Message Authorization System.
"""

# AUTHORITATIVE GLOSSARY OF ALL 99 SUBELEMENT LAYOUTS
DE48_SUBELEMENT_GLOSSARY = {
    "01": "Transaction Category Code (TCC) [Fixed, 1 char]",
    "02": "Special Acceptance Conditions Data [Variable]",
    "03": "Additional Visa Request Data (Visa Co-Routing) [Variable]",
    "04": "Acceptance Environment Response Data (Visa Co-Routing) [Variable]",
    "05": "Additional Visa Response Data (Visa Co-Routing) [Variable]",
    "06": "Advanced Digital Transaction Data 1 (Binding ID / Device Data) [Variable]",
    "07": "Advanced Digital Transaction Data 2 (Cardholder Email Address) [Variable]",
    "08": "Advanced Digital Transaction Data 3 (IP Address / Shipping Address) [Variable]",
    "09": "Additional PAN Data [Variable]",
    "10": "Encrypted PIN Block Key [Variable]",
    "11": "Key Exchange Block Data [Variable]",
    "12": "Routing Indicator [Variable]",
    "13": "Mastercard Hosted Mobile Phone Top-Up Request Data [Variable]",
    "14": "Account Type Indicator [Fixed, 1 char]",
    "15": "Authorization System Characteristics / Advice Timestamp [Fixed, 10 char]",
    "16": "Processor Pseudo ICA [Variable]",
    "17": "Authentication Indicator [Fixed, 1 char]",
    "18": "Service Parameters / Settlement Performance [Fixed, 1 char]",
    "20": "Cardholder Present Data / Verification Method [Fixed, 1 char]",
    "21": "Acceptance Data / POS Capability Profile [Fixed, 3 char]",
    "22": "Multi-Purpose Merchant Indicator (MIT/CIT Framework) [Fixed, 2 char]",
    "23": "Payment Initiation Channel [Fixed, 2 char]",
    "24": "Account Level Management (ALM) Service Data [Variable, Nested]",
    "25": "Mastercard Cash Program Data [Variable]",
    "26": "Wallet Program Data / Wallet Identifier [Fixed, 3 char]",
    "27": "Transaction Analysis [Variable]",
    "28": "Cardless ATM Order ID [Variable]",
    "29": "Additional POS Terminal Locations [Variable]",
    "30": "Token Transaction Identifier [Variable]",
    "32": "Mastercard Assigned ID / Customer ID [Variable]",
    "33": "PAN Mapping File Information / Status Indicator [Variable]",
    "34": "ATC Information [Variable]",
    "35": "Contactless Non-Card Form Factor Request/Response [Fixed, 1 char]",
    "36": "Additional Visa Request Data [Variable]",
    "37": "Additional Merchant Data (Payment Facilitator / Marketplace Data) [Variable]",
    "38": "Account Category Indicator [Fixed, 1 char]",
    "39": "Account Data Compromise Information [Fixed, 1 char]",
    "40": "E-Commerce Merchant/Cardholder Certificate Serial Number [Variable]",
    "41": "Electronic Commerce Certificate Qualifying Information [Variable]",
    "42": "Electronic Commerce Indicators (ECI) [Fixed, 3 char]",
    "43": "Universal Cardholder Authentication Field (UCAF) Data [Variable]",
    "44": "3-D Secure Electronic Commerce Transaction Identifier (XID) [Variable]",
    "45": "3-D Secure Electronic Commerce Transaction Response Code [Fixed, 1 char]",
    "46": "Product ID [Variable]",
    "47": "Mastercard Payment Gateway Transaction Indicator [Fixed, 1 char]",
    "48": "Digital Commerce Solutions Indicators (DCS Platform Data) [Variable]",
    "49": "Time Validation Information / Expiry Check Profile [Fixed, 1 char]",
    "50": "Embedded Interchange Data [Variable]",
    "51": "Business Activity Code / Fleet Data [Variable]",
    "52": "Merchant Electronic Commerce Indicator [Fixed, 1 char]",
    "55": "Integrated Circuit Card (ICC) Related Data [Variable, Binary]",
    "56": "Network Evaluation Indicator / Routing Optimization [Fixed, 2 char]",
    "57": "Fraud Scoring Data [Fixed, 4 char]",
    "58": "ATM Additional Data [Variable]",
    "61": "POS Data Extended Condition Codes [Fixed, 5 char]",
    "62": "Real-time Settlement Indicator [Fixed, 2 char]",
    "63": "Trace ID / Network Reference Data [Fixed, 15 char]",
    "66": "Authentication Data / Security Payload Status [Fixed, 1 char]",
    "71": "On-behalf Services Result Flags [Fixed, 6 char]",
    "72": "Issuer Chip Authentication [Variable]",
    "74": "Payment Account Reference (PAR) [Fixed, 29 char]",
    "75": "Token Cryptogram Validation Results [Fixed, 1 char]",
    "76": "Mastercard Digital Enablement Service (MDES) Token Data [Variable]",
    "77": "Dynamic Currency Conversion (DCC) Indicator [Variable, Struct]",
    "78": "Token Response Information / Assurance Level [Fixed, 2 char]",
    "82": "Address Verification Service (AVS) Request [Variable]",
    "83": "Address Verification Service (AVS) Response [Fixed, 1 char]",
    "84": "Merchant Advice Code [Fixed, 2 char]",
    "85": "Account Status Inquiry Result Code [Fixed, 2 char]",
    "86": "PIN Validation Code Result [Fixed, 1 char]",
    "87": "Card Validation Code (CVC) Result [Fixed, 1 char]",
    "90": "Custom Payment Service Request/Response [Variable]",
    "91": "Acquirer Reference Data [Variable]",
    "92": "CVC 2 Value (Inbound Request Only) [Fixed, 3 char]",
    "93": "Fleet Card ID Request Data [Variable]",
    "94": "Commercial Card Inquiry Request/Response [Fixed, 1 char]",
    "95": "Mastercard Promotion Code / Amex CID Result [Fixed, 1 char]",
    "96": "Visa Market-Specific Data Identifier [Variable]",
    "97": "Prestigious Properties Indicator [Variable]",
    "98": "Mastercard Corporate Fleet Card ID/Driver Number [Variable]",
    "99": "Mastercard Corporate Fleet Card Vehicle Number [Variable]"
}

# NESTED LOOKUP CODES TRANSCRIPTION
DE48_VALUE_TABLES = {
    "01": {
        "A": "Automotive / Vehicle Rental", "C": "Cash Advance / Cash Disbursement",
        "F": "Restaurant / Food Service", "H": "Hotel / Lodging", "O": "Other / General Retail",
        "R": "Retail Transaction", "T": "Airline / Transportation", "U": "Electronic Commerce (E-Commerce)",
        "X": "Reversal / Administrative Adjustment", "Z": "ATM / Automated Teller Machine Transaction"
    },
    "14": {
        "C": "Checking Account", "D": "Debit Account", "S": "Savings Account", "G": "General Ledger / Credit Card Account"
    },
    "15": {
        "0": "Normal Transaction Pathway", "1": "Mastercard On-behalf (Stand-In) Authorized", "2": "X-Code Stand-In Authorized"
    },
    "17": {
        "1": "Qualified for Authentication Service Type 1", "2": "Qualified for Authentication Service Type 2"
    },
    "18": {
        "0": "Standard Tier Clearing Window", "1": "Accelerated Financial Settlement", "2": "Deferred Interbank Clearing"
    },
    "20": {
        "0": "Cardholder Not Present", "1": "Cardholder Present", "2": "Cardholder Present - Mail/Phone Order"
    },
    "21.POS1": {
        "0": "Unspecified Capability", "1": "Terminal supports Manual Entry Only", "2": "Terminal supports Magnetic Stripe",
        "3": "Terminal supports Contact EMV Chip", "4": "Terminal supports Contactless / NFC Capability"
    },
    "21.POS2": {
        "0": "No PIN input capability", "1": "Terminal has online PIN verification pads", "2": "Terminal has offline PIN verification support"
    },
    "21.POS3": {
        "0": "No printing support", "1": "Terminal can generate physical or electronic customer receipts"
    },
    "22.POS1": {
        "0": "Unspecified / Baseline Customer Initiated Transaction (CIT)",
        "1": "Cardholder Initiated Credential-on-File (CIT COF)",
        "2": "Merchant Initiated Recurring Transaction (MIT)",
        "3": "Merchant Initiated Unscheduled Credential-on-File (MIT UCOF)",
        "4": "Delayed Charges / No Show Processing"
    },
    "22.POS2": {
        "0": "First Transaction in Sequence / Agreement Initialized",
        "1": "Subsequent / Follow-on Transaction in Sequence"
    },
    "23": {
        "01": "Mobile App / Consumer Device checkout", "02": "Web Browser / Traditional Desktop checkout",
        "03": "Interactive Voice Response (IVR)", "04": "M2M / Automated IoT Machine Channel"
    },
    "24.SUB1": {
        "ALM": "Account Level Management Base Service", "CHI": "Interchange Optimization Indicator"
    },
    "24.SUB5": {
        "MCC": "Mastercard Brand", "DMC": "Debit Mastercard", "MSI": "Maestro Core Brand"
    },
    "24.SUB6": {
        "D": "Dynamic Interchange Applied", "S": "Static Interchange Applied"
    },
    "26": {
        "101": "Masterpass Digital Wallet", "216": "Apple Pay Tokenized Transaction",
        "217": "Google Pay Tokenized Transaction", "218": "Samsung Pay Tokenized Transaction"
    },
    "35": {
        "0": "Physical Plastic Card Profile", "1": "Keyfob / Wearable Active Device Element",
        "2": "Sticker / Passive Transponder Form Factor", "3": "HCE / Mobile NFC Token Form Factor"
    },
    "38": {
        "A": "Consumer Card Profile", "B": "Commercial Card Profile", "C": "Corporate Fleet Profile"
    },
    "39": {
        "0": "No active compromise monitoring rule triggered", "1": "Card is part of a high-risk data breach list; validation strictness escalated"
    },
    "42.POS1": {
        "0": "Channel-encrypted transaction (e.g., SSL/TLS)",
        "1": "Identity Check / 3-D Secure authenticated",
        "2": "Non-authenticated secure e-commerce transaction"
    },
    "42.POS2": {
        "0": "Non-authenticated payment transaction",
        "1": "Mastercard Identity Check / 3DS authentication attempted",
        "2": "Mastercard Identity Check / 3DS fully authenticated successful match"
    },
    "42.POS3": {
        "0": "No UCAF data present",
        "1": "UCAF data collection supported by merchant; authentication attempted",
        "2": "UCAF data collection supported by merchant; fully authenticated security payload"
    },
    "45": {
        "0": "Verification Successful", "1": "Verification Failed", "2": "Verification Not Performed / Bypassed"
    },
    "47": {
        "0": "Standard Direct API Routing Entry", "1": "Hosted Checkout Payment Gateway Session Token Used"
    },
    "48.SUB1": {
        "0": "Multi-Domain Platform", "1": "Mastercard Core Solution Platform",
        "2": "Acquirer Managed Digital Ecosystem", "3": "Issuer Managed Digital Ecosystem"
    },
    "49": {
        "0": "Bypass validation profile", "1": "Standard system real-time expiry date validation enabled"
    },
    "52": {
        "0": "Non-secure / Generic Web Transaction", "1": "Authenticated merchant server verified endpoint"
    },
    "61.POS1": {
        "0": "Terminal does not support receipt of partial approvals.",
        "1": "Terminal supports receipt of partial approvals."
    },
    "61.POS2": {
        "0": "Terminal does not support receipt of purchase-only approvals.",
        "1": "Terminal supports receipt of purchase-only approvals."
    },
    "61.POS3": {
        "0": "Terminal did not verify items against an Integrated Inventory Account System (IIAS).",
        "1": "Terminal verified items against an IIAS."
    },
    "61.POS4": {
        "0": "Normal tracking / scoring baseline.",
        "1": "Transaction to be scored by Expert Monitoring for Merchants."
    },
    "61.POS5": {
        "0": "Normal Estimated / Undefined Finality Authorization.", "1": "Final Authorization."
    },
    "62.SUB1": {
        "Y": "Merchant account used for real-time settlement.",
        "N": "Acquiring Institution account used for real-time settlement."
    },
    "62.SUB2": {
        "D": "Domestic real-time payment", "C": "Intercountry real-time payment",
        "R": "Intraregional real-time payment", "X": "Interregional real-time payment",
        "Z": "Other custom real-time framework", "N": "No participation"
    },
    "66": {
        "0": "Authentication token absent or empty", "1": "Cryptographic authentication token parsed successfully"
    },
    "71.POS1": {
        "0": "PIN verification not modified by network", "1": "PIN block processed via Mastercard On-Behalf rules"
    },
    "71.POS2": {
        "0": "CVC validation not modified", "1": "CVC checked via Mastercard On-Behalf services"
    },
    "75": {
        "0": "Cryptogram Validation Successful", "1": "Cryptogram Verification Failed / Non-match", "2": "Not Checked / Validation Hub Offline"
    },
    "77.POS1": {
        "0": "DCC not offered to cardholder",
        "1": "DCC offered and accepted by cardholder",
        "2": "DCC offered but declined by cardholder (processed in local currency)",
        "3": "DCC eligible but terminal unable to calculate or apply conversion"
    },
    "78.POS1": {
        "00": "Unspecified assurance status", "01": "Level 1: Low-assurance baseline token authentication",
        "02": "Level 2: Mid-assurance credential identity verified", "03": "Level 3: High-assurance biometrically linked token verification"
    },
    "83": {
        "A": "Address matches, ZIP code does not match.", "N": "Neither address nor ZIP code matches.",
        "R": "Retry - Issuer system unavailable or timed out.", "S": "AVS not supported by issuer for this card product.",
        "U": "Address information unavailable.", "W": "9-digit ZIP code matches, address does not match.",
        "X": "Exact match - Both street address and 9-digit ZIP match.",
        "Y": "Exact match - Both street address and 5-digit ZIP match.", "Z": "5-digit ZIP code matches, address does not match."
    },
    "84": {
        "01": "New account information available / Update credential files",
        "02": "Try again later / Issuer transient system issue",
        "03": "Do not try again / Stop recurring payment logic",
        "21": "Cancellation of recurring transaction registration"
    },
    "85": {
        "00": "Account Valid / Active", "01": "Account Closed", "02": "Account Suspended"
    },
    "86": {
        "M": "PIN Valid / Match", "N": "PIN Invalid / Non-match", "P": "Not Verified / PIN block missing"
    },
    "87": {
        "M": "Valid CVC 2 / CVV2 Match.", "N": "Invalid CVC 2 / CVV2 Non-match.",
        "P": "CVC 2 not processed (Issuer validation host offline).",
        "S": "CVC 2 should be on card but merchant indicated not present.",
        "U": "CVC 2 unverified.", "Y": "Invalid CVC 1 / Stripe Validation Error."
    },
    "94": {
        "0": "Not a commercial card product", "1": "Corporate Card identified", "2": "Business Purchasing Card profile flagged"
    },
    "95": {
        "M": "CID Security Code Matches", "N": "CID Security Code Non-match", "P": "Not Checked / Bypassed"
    }
}


def decode_de48_subelement(se_tag: str, value: str) -> str:
    """
    Decodes structural subelement layouts and positional parameters inside Data Element 48.
    Does not crash on validation discrepancies; instead records lightweight tracking markers.
    """
    clean_val = value.strip()
    tag_name = DE48_SUBELEMENT_GLOSSARY.get(se_tag, f"Subelement {se_tag}")
    validation_err = ""
    
    # Check simple flat code enumerations first
    if se_tag in DE48_VALUE_TABLES and se_tag not in ("21", "22", "24", "42", "48", "61", "62", "71", "77", "78"):
        meaning = DE48_VALUE_TABLES[se_tag].get(clean_val, "Value recognized but description unassigned")
        return f"{tag_name}: {meaning}"

    # Advanced Multi-Position Layouts Logic
    if se_tag in ("06", "07", "08"):
        return f"{tag_name} -> Raw E-Commerce Telemetry/Identity Verification Payload: `{clean_val}`"

    if se_tag == "21":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        if len(clean_val) >= 3:
            p1 = DE48_VALUE_TABLES["21.POS1"].get(clean_val[0], "Unknown Entry Mode")
            p2 = DE48_VALUE_TABLES["21.POS2"].get(clean_val[1], "Unknown PIN Mode")
            p3 = DE48_VALUE_TABLES["21.POS3"].get(clean_val[2], "Unknown Printer Mode")
            return f"{tag_name} -> Entry Mode: {p1} | PIN: {p2} | Receipt: {p3}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "22":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        if len(clean_val) >= 2:
            p1 = DE48_VALUE_TABLES["22.POS1"].get(clean_val[0], "Unknown Framework Type")
            p2 = DE48_VALUE_TABLES["22.POS2"].get(clean_val[1], "Unknown Sequence Index")
            return f"{tag_name} -> Context: {p1} | Chain Order: {p2}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "24":
        if len(clean_val) >= 3:
            sub1 = DE48_VALUE_TABLES["24.SUB1"].get(clean_val[:3], f"Service: {clean_val[:3]}")
            brand, ind = "N/A", "N/A"
            if len(clean_val) >= 7:
                brand = DE48_VALUE_TABLES["24.SUB5"].get(clean_val[3:6], f"Brand Code: {clean_val[3:6]}")
                ind = DE48_VALUE_TABLES["24.SUB6"].get(clean_val[6:7], f"Indicator: {clean_val[6:7]}")
            return f"{tag_name} -> Service Variant: {sub1} | Product Brand Association: {brand} | Rate Strategy: {ind}"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "42":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        if len(clean_val) >= 3:
            p1 = DE48_VALUE_TABLES["42.POS1"].get(clean_val[0], "Unknown Protocol")
            p2 = DE48_VALUE_TABLES["42.POS2"].get(clean_val[1], "Unknown Auth Status")
            p3 = DE48_VALUE_TABLES["42.POS3"].get(clean_val[2], "Unknown UCAF Configuration")
            return f"{tag_name} -> Protocol: {p1} | Status: {p2} | UCAF: {p3}{validation_err}"
        return f"{tag_name}: Raw Matrix `{clean_val}`{validation_err}"

    if se_tag == "43":
        return f"{tag_name} -> Parsed Base64 Security Signature Verification String: `{clean_val}`"
    
    if se_tag == "48":
        if len(clean_val) >= 1:
            dom_id = DE48_VALUE_TABLES["48.SUB1"].get(clean_val[0], "Unknown Domain Operator")
            return f"{tag_name} -> Digital Domain Platform: {dom_id} | Security Token Fragment: `{clean_val[1:]}`"
        return f"{tag_name}: `{clean_val}`"
    
    if se_tag == "61":
        if len(clean_val) != 5:
            validation_err = " [Warning: Expected length exactly 5]"
        if len(clean_val) >= 5:
            s1 = DE48_VALUE_TABLES["61.POS1"].get(clean_val[0], "Unknown")
            s2 = DE48_VALUE_TABLES["61.POS2"].get(clean_val[1], "Unknown")
            s3 = DE48_VALUE_TABLES["61.POS3"].get(clean_val[2], "Unknown")
            s4 = DE48_VALUE_TABLES["61.POS4"].get(clean_val[3], "Unknown")
            s5 = DE48_VALUE_TABLES["61.POS5"].get(clean_val[4], "Unknown")
            return f"{tag_name} -> Partials: {s1} | Purchase-Only: {s2} | IIAS: {s3} | Risk Scoring: {s4} | Finality: {s5}{validation_err}"
        return f"{tag_name}: Raw Condition Array `{clean_val}`{validation_err}"

    if se_tag == "62":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        if len(clean_val) >= 2:
            f1 = DE48_VALUE_TABLES["62.SUB1"].get(clean_val[0], "Unknown Account Config")
            f2 = DE48_VALUE_TABLES["62.SUB2"].get(clean_val[1], "Unknown Speed Class")
            return f"{tag_name} -> Funding Node: {f1} | Network Speed Context: {f2}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "63":
        if len(clean_val) != 15:
            validation_err = " [Warning: Expected length exactly 15]"
        return f"{tag_name} -> Network Tracking Index Reference ID: `{clean_val}`{validation_err}"

    if se_tag == "71":
        if len(clean_val) != 6:
            validation_err = " [Warning: Expected length exactly 6]"
        if len(clean_val) >= 2:
            o1 = DE48_VALUE_TABLES["71.POS1"].get(clean_val[0], "Normal PIN Processing")
            o2 = DE48_VALUE_TABLES["71.POS2"].get(clean_val[1], "Normal CVC Validation")
            return f"{tag_name} -> On-behalf Actions -> PIN Strategy: {o1} | CVC Evaluation: {o2}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "76":
        return f"{tag_name} -> MDES Ecosystem Real PAN Virtual Identifier Data Vault Reference: `{clean_val}`"

    if se_tag == "77":
        if len(clean_val) >= 1:
            status = DE48_VALUE_TABLES["77.POS1"].get(clean_val[0], "Unknown DCC Profile")
            remainder = clean_val[1:]
            return f"{tag_name} -> Offers Matrix: {status}" + (f" | Rate Metadata: `{remainder}`" if remainder else "")
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "78":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        desc = DE48_VALUE_TABLES["78.POS1"].get(clean_val, f"Custom Level ({clean_val})")
        return f"{tag_name} -> Assurance Profile: {desc}{validation_err}"

    if se_tag == "90":
        return f"{tag_name} -> Co-routing Switch Metadata Segment: `{clean_val}`"
        
    return f"{tag_name}: `{clean_val}`"