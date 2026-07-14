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
    "12": "Routing Indicator [Fixed, 1 char]",
    "13": "Mastercard Hosted Mobile Phone Top-Up Request Data [Variable]",
    "14": "Account Type Indicator [Fixed, 1 char]",
    "15": "Authorization System Advice Date and Time [Fixed, 10 char]",
    "16": "Processor Pseudo ICA [Fixed, 7 char]",
    "17": "Authentication Indicator [Fixed, 1 char]",
    "18": "Service Parameters [Variable]",
    "20": "Cardholder Verification Method [Fixed, 1 char]",
    "21": "Acceptance Data [Fixed, 3 char]",
    "22": "Multi-Purpose Merchant Indicator [Variable]",
    "23": "Payment Initiation Channel [Fixed, 2 char]",
    "24": "Account Level Management (ALM) Service Data [Variable]",
    "25": "Mastercard Cash Program Data [Variable]",
    "26": "Wallet Program Data [Fixed, 3 char]",
    "27": "Transaction Analysis [Variable]",
    "28": "Cardless ATM Order ID [Fixed, 10 char]",
    "29": "Additional POS Terminal Locations [Fixed, 1 char]",
    "30": "Token Transaction Identifier [Variable]",
    "32": "Mastercard Assigned ID [Fixed, 6 char]",
    "33": "PAN Mapping File Information [Variable]",
    "34": "ATC Information [Fixed, 11 char]",
    "35": "Contactless Non-Card Form Factor Request/Response [Fixed, 1 char]",
    "36": "Additional Visa Request Data [Variable]",
    "37": "Additional Merchant Data [Variable]",
    "38": "Account Category [Fixed, 1 char]",
    "39": "Account Data Compromise Information [Fixed, 30 char]",
    "40": "E-Commerce Merchant/Cardholder Certificate Serial Number [Variable]",
    "41": "Electronic Commerce Certificate Qualifying Information [Variable]",
    "42": "Electronic Commerce Indicators [Fixed, 3 char]",
    "43": "Universal Cardholder Authentication Field (UCAF) Data [Variable]",
    "44": "3-D Secure Electronic Commerce Transaction Identifier (XID) [Variable]",
    "45": "3-D Secure Electronic Commerce Transaction Response Code [Fixed, 1 char]",
    "46": "Product ID (Visa Only) [Fixed, 2 char]",
    "47": "Mastercard Payment Gateway Transaction Indicator [Fixed, 8 char]",
    "48": "Digital Commerce Solutions Indicators [Variable]",
    "49": "Time Validation Information [Fixed, 15 char]",
    "50": "Embedded Interchange Data [Variable]",
    "51": "Merchant On-behalf Services [Variable]",
    "52": "Interchange Structure Indicator [Fixed, 2 char]",
    "53": "E-ID Request Code [Variable]",
    "55": "Merchant Fraud Scoring Data/Approval Probability Indicator [Variable]",
    "56": "Security Services Additional Data for Issuers [Variable]",
    "57": "Security Services Additional Data for Acquirers [Variable]",
    "58": "ATM Additional Data [Variable]",
    "60": "Additional Service Data For Issuers [Variable]",
    "61": "POS Data Extended Condition Codes [Fixed, 5 char]",
    "62": "Real-Time Payment Information [Variable]",
    "63": "Trace ID [Fixed, 15 char]",
    "64": "Transit Program [Fixed, 4 char]",
    "65": "Terminal Compliant Indicator [Fixed, 2 char]",
    "66": "Authentication Data [Variable]",
    "67": "Mastercard Send Information [Variable]",
    "68": "Financial Account Information [Variable]",
    "71": "On-behalf Services Result Flags [Variable Repeating, 3-char sets]",
    "72": "Issuer Chip Authentication [Variable]",
    "74": "Additional Processing Information [Variable]",
    "75": "Fraud Scoring Data [Variable]",
    "76": "Mastercard Electronic Acceptance Indicator [Fixed, 1 char]",
    "77": "Transaction Type Identifier [Fixed, 3 char]",
    "78": "Payment Service Indicators (Visa Only) [Fixed, 6 char]",
    "79": "Chip CVR/TVR Bit Error Results [Variable]",
    "80": "PIN Service Code [Fixed, 2 char]",
    "82": "Address Verification Service (AVS) Request [Fixed, 2 char]",
    "83": "Address Verification Service (AVS) Response [Fixed, 1 char]",
    "84": "Merchant Advice Code [Fixed, 2 char]",
    "85": "Account Status (Visa Only) [Fixed, 1 char]",
    "86": "Relationship Participant Indicator (Visa Only) [Fixed, 1 char]",
    "87": "Card Validation Code (CVC) Result [Fixed, 1 char]",
    "88": "Magnetic Stripe Compliance Status Indicator [Fixed, 1 char]",
    "89": "Magnetic Stripe Compliance Error Indicator [Fixed, 1 char]",
    "90": "Lodging and Auto Rental Indicator / Custom Payment Service [Fixed, 1 char]",
    "91": "Acquirer Reference Data / Custom Payment Service [Variable]",
    "92": "CVC 2 Value (Inbound Request Only) [Fixed, 3 char]",
    "93": "Fleet Card ID Request Data [Variable]",
    "94": "Commercial Card Inquiry Request/Response [Fixed, 1 char]",
    "95": "Mastercard Promotion Code / Amex CID Result [Fixed, 6 char]",
    "96": "Visa Market-Specific Data Identifier [Fixed, 1 char]",
    "97": "Prestigious Properties Indicator [Fixed, 1 char]",
    "98": "Mastercard Corporate Fleet Card ID/Driver Number [Variable]",
    "99": "Mastercard Corporate Fleet Card Vehicle Number [Variable]"
}

# NESTED LOOKUP CODES TRANSCRIPTION
DE48_VALUE_TABLES = {
    "01": {
        "A": "Automotive / Vehicle Rental", 
        "C": "Cash Advance / Cash Disbursement",
        "F": "Restaurant / Food Service", 
        "H": "Hotel / Lodging", 
        "O": "Other / General Retail",
        "R": "Retail Transaction", 
        "T": "Phone, Mail, or Electronic Commerce Order", 
        "U": "Unique Transaction",
        "X": "Reversal / Administrative Adjustment", 
        "Z": "ATM / Automated Teller Machine Transaction"
    },
    "12": {
        "A": "Alternate issuer host routing", 
        "P": "Primary issuer host routing"
    },
    "14": {
        "C": "Credit Transaction", 
        "D": "Debit Transaction"
    },
    "17": {
        "1": "Qualified for Authentication Service Type 1", 
        "2": "Qualified for Authentication Service Type 2"
    },
    "20": {
        "P": "Online PIN verification", 
        "S": "Signature / Offline PIN / No CVM used"
    },
    "21.POS1": {
        "0": "Dedicated mPOS Terminal with PCI compliant dongle",
        "1": "Off the Shelf Mobile Device"
    },
    "21.POS2": {
        "00": "QR Not Supported | Barcode Not Supported",
        "01": "QR Not Supported | Barcode Supported",
        "10": "QR Supported | Barcode Not Supported",
        "11": "QR Supported | Barcode Supported"
    },
    "22.POS1": {
        "01": "CIT - Consumer agrees to store credential",
        "02": "CIT - Standing Order (variable amount)",
        "03": "CIT - Subscription (fixed amount)",
        "04": "CIT - Installment",
        "05": "MIT - Unscheduled Recurring",
        "06": "MIT - Standing Order",
        "07": "MIT - Subscription",
        "08": "MIT - Installment",
        "M208": "Resubmission",
    },
    "22.POS2": {
        "0": "First Transaction in Sequence / Agreement Initialized",
        "1": "Subsequent / Follow-on Transaction in Sequence"
    },
    "22.POS3": {
        "1": "Transaction contains intentionally duplicated (replayed) ATC value"
    },
    "22.POS4": {
        "1": "Issuer requests PIN in Single Tap mode"
    },
    "23": {
        "00": "Card",
        "01": "Mobile Network Operator (MNO) Controlled Removable Secure Element (SIM/UICC) - Mobile Phone/Smartphone",
        "02": "Key Fob",
        "03": "Watch with Contactless Chip or Fixed Secure Element (Not MNO Controlled)",
        "04": "Mobile Tag",
        "05": "Wristband",
        "06": "Mobile Phone Case or Sleeve",
        "07": "Mobile Phone/Smartphone with Fixed Secure Element (MNO Controlled)",
        "08": "Removable Secure Element (Not MNO Controlled) - Memory Card for Mobile Phone/Smartphone",
        "09": "Mobile Phone/Smartphone with Fixed Secure Element (Not MNO Controlled)",
        "10": "MNO Controlled Removable Secure Element (SIM/UICC) - Tablet/E-book",
        "11": "Tablet/E-book with Fixed Secure Element (MNO Controlled)",
        "12": "Removable Secure Element (Not MNO Controlled) - Memory Card for Tablet/E-book",
        "13": "Tablet/E-book with Fixed Secure Element (Not MNO Controlled)",
        "14": "Mobile Phone/Smartphone with Payment Application in Host Processor (HCE)",
        "15": "Tablet/E-book with Payment Application in Host Processor (HCE)",
        "16": "Mobile Phone/Smartphone with Payment Application in Trusted Execution Environment (TEE)",
        "17": "Tablet/E-book with Payment Application in Trusted Execution Environment (TEE)",
        "18": "Watch with Payment Application in Trusted Execution Environment (TEE)",
        "19": "Watch with Payment Application in Host Processor (HCE)",
        "20": "Card",
        "21": "Mobile Phone",
        "22": "Tablet / E-reader",
        "23": "Watch / Wristband",
        "24": "Sticker",
        "25": "PC / Laptop",
        "26": "Device Peripheral (Mobile Phone Case or Sleeve)",
        "27": "Tag (Key Fob or Mobile Tag)",
        "28": "Jewelry (Ring, Bracelet, Necklace, Cuff Links)",
        "29": "Fashion Accessory (Handbag, Bag Charm, Glasses)",
        "30": "Garment (Dress)",
        "31": "Domestic Appliance (Refrigerator, Washing Machine)",
        "32": "Vehicle / Vehicle-Attached Device",
        "33": "Media / Gaming Device (Set-top Box, Media Player, Television)",
        "34": "Virtual Reality Headset / Smart Glasses"
    },
    "25": {
        "CM": "Confirmation message",
        "LP": "Linked load request with a purchase",
        "LR": "Unlinked load request, or linked load request with no purchase",
        "LU": "Linked status update"
    },
    "26": {
        "101": "Masterpass Digital Wallet", 
        "103": "Apple Pay",
        "216": "Google Pay Tokenized Transaction", 
        "217": "Samsung Pay Tokenized Transaction",
        "327": "Remote commerce programs"
    },
    "29": {
        "A": "Transaction initiated remotely and completed at physical terminal on premises",
        "B": "Transaction initiated remotely and completed at physical terminal off premises"
    },
    "35": {
        "R": "Cardholder request for device", 
        "A": "Approve cardholder request for device",
        "D": "Decline cardholder request for device"
    },
    "37.SERVICE_ROLES": {
        "90000000001": "Payment Facilitator",
        "90000000003": "Staged Wallet",
        "90000000004": "Mastercard Defined Domestic Programs",
        "90000000005": "Independent Sales Organization (ISO)",
        "90000000007": "Mastercard Defined International Programs"
    },
    "38": {
        "A": "Consumer Card Profile", 
        "B": "Commercial Card Profile", 
        "C": "Corporate Fleet Profile",
        "Z": "Previously participated in Enhanced Value/Product Graduation/High Value"
    },
    "42.POS1": {
        "0": "Reserved for existing Mastercard Europe/Visa definitions",
        "1": "Reserved for future use",
        "2": "Channel encryption",
        "3": "Reserved for future use"
    },
    "42.POS2": {
        "0": "Reserved for future use",
        "1": "E-commerce / Identity Check",
        "3": "Reserved for future use",
        "4": "Tokenized payment"
    },
    "42.POS3": {
        "0": "Non-authenticated payment / Identity Check failed / DTVC",
        "1": "UCAF data collection supported; attempt AAV",
        "2": "UCAF data collection supported; fully authenticated AAV",
        "3": "Static AAV (Maestro Recurring/Utility Payment)",
        "4": "Insights AAV (Identity Check)",
        "5": "Reserved",
        "6": "Risk Based Decisioning / DSRP cryptogram",
        "7": "Merchant-initiated transactions",
    },
    "42.DOWNGRADE_REASON": {
        "0": "Missing Universal Cardholder Authentication Field (UCAF)",
        "1": "Incorrect AAV leading indicator in UCAF",
        "2": "Incorrect Security Level Indicator",
        "3": "X-Code Processing"
    },
    "45": {
        "0": "Verification Successful", 
        "1": "Verification Failed", 
        "2": "Verification Not Performed / Bypassed"
    },
    "47": {
        "MC-MPG/W": "Mastercard Payment Gateway transaction"
    },
    "48.SUB1": {
        "0": "Multi-Domain Platform", 
        "1": "Mastercard Core Solution Platform",
        "2": "Acquirer Managed Digital Ecosystem", 
        "3": "Issuer Managed Digital Ecosystem"
    },
    "48.SUB2": {
        "0": "Multi-Program",
        "1": "Mastercard QR (SQR)",
        "2": "Click to Pay",
        "3": "In-store Biometrics",
        "4": "Next Gen POI",
        "5": "Mastercard QR: Pay by Link",
        "6": "Mastercard QR: X QR",
        "8": "Mastercard Agent Pay"
    },
    "49": {
        "01": "Positive value within time validation window",
        "02": "Positive value outside time validation window",
        "03": "Negative value within time validation window",
        "04": "Negative value outside time validation window",
        "05": "Unknown (time validation not performed)"
    },
    "52": {
        "B1": "Small Business Level 1",
        "B2": "Small Business Level 2",
        "B3": "Small Business Level 3",
        "B4": "Small Business Level 4",
        "B5": "Small Business Level 5",
        "BB": "Commercial Business to Business",
        "BP": "Bill Pay",
        "CC": "Core Value",
        "CD": "Unregulated Consumer Debit",
        "CP": "Unregulated Consumer Prepaid",
        "EV": "Enhanced Value",
        "FP": "Commercial Flex Program",
        "FT": "Fleet",
        "HM": "Humanitarian",
        "HV": "World High Value",
        "IP": "Installment Payments",
        "LM": "Large Market",
        "MD": "Unregulated Commercial Debit",
        "MP": "Unregulated Commercial Prepaid",
        "NA": "Unknown Interchange Structure",
        "PA": "Commercial Payments Account",
        "PL": "Private Label",
        "PP": "Prepaid Commercial Payments Account",
        "RB": "Regulated Consumer Debit Base",
        "RC": "Regulated Commercial Debit Base",
        "RD": "Regulated Consumer Prepaid with Fraud Adjustment",
        "RE": "Regulated Commercial Prepaid with Fraud Adjustment",
        "RF": "Regulated Consumer Debit with Fraud Adjustment",
        "RG": "Regulated Commercial Debit with Fraud Adjustment",
        "RP": "Regulated Consumer Prepaid Base",
        "RR": "Regulated Commercial Prepaid Base",
        "VP": "Variable Interchange Programs",
        "WE": "World Elite",
        "WO": "World"
    },
    "53": {
        "01": "Pull cardholder personal data for E-ID/Health ID Verification",
        "02": "Verify and send the age of the cardholder"
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
        "1": "Terminal verified items against an IIAS.",
        "2": "Merchant claims exemption from IIAS based on IRS 90% rule",
        "4": "Transaction submitted as real-time substantiated but from non-IIAS certified merchant"
    },
    "61.POS4": {
        "0": "Normal tracking / scoring baseline.",
        "1": "Transaction to be scored by Expert Monitoring for Merchants."
    },
    "61.POS5": {
        "0": "Normal Estimated / Undefined Finality Authorization.", 
        "1": "Final Authorization."
    },
    "62.SUB1": {
        "Y": "Merchant account used for real-time settlement.",
        "N": "Acquiring Institution account used for real-time settlement."
    },
    "62.SUB2": {
        "D": "Domestic real-time payment", 
        "C": "Intercountry real-time payment",
        "R": "Intraregional real-time payment", 
        "X": "Interregional real-time payment",
        "Z": "Other custom real-time framework", 
        "N": "No participation"
    },
    "62.SUB3": {
        "PBA": "Mastercard Pay by Account"
    },
    "62.SUB4": {
        "01": "On-us Payment",
        "02": "Faster Payments",
        "03": "UPI",
        "04": "IMPS",
        "05": "TCH",
        "06": "Real-time Payment"
    },
    "62.SUB5": {
        "00": "Funds Transfer not initiated",
        "01": "Funds transferred to Acquiring Institution or merchant",
        "02": "Funds requested from Acquiring Institution or merchant"
    },
    "64.SUB1": {
        "01": "Prefunded",
        "02": "Real-time Authorized",
        "03": "Post-Authorized Aggregated",
        "04": "Authorized Aggregated Split Clearing",
        "05": "Other",
        "06": "Post-authorized Aggregated Maestro",
        "07": "Debt Recovery"
    },
    "64.SUB2": {
        "00": "Unknown",
        "01": "Urban Bus",
        "02": "Interurban Bus",
        "03": "Light Train Mass Transit (Underground Metro, LTR)",
        "04": "Train",
        "05": "Commuter Train",
        "06": "Water Borne Vehicle",
        "07": "Toll",
        "08": "Parking",
        "09": "Taxi",
        "10": "High Speed Train",
        "11": "Rural Bus",
        "12": "Express Commuter Train",
        "13": "Para Transit",
        "14": "Self Drive Vehicle",
        "15": "Coach",
        "16": "Locomotive",
        "17": "Powered Motor Vehicle",
        "18": "Trailer",
        "19": "Regional Train",
        "20": "Inter City",
        "21": "Funicular Train",
        "22": "Cable Car"
    },
    "65": {
        "1": "Not Certified",
        "2": "Certified"
    },
    "66.SUB1": {
        "1": "EMV 3-D Secure Version 2.1",
        "2": "EMV 3-D Secure Version 2.2",
        "3": "EMV 3-D Secure Version 2.3",
        "4": "EMV 3-D Secure Version 2.4",
        "5": "EMV 3-D Secure Version 2.5",
        "6": "EMV 3-D Secure Version 2.6",
        "7": "EMV 3-D Secure Version 2.7",
        "8": "EMV 3-D Secure Version 2.8",
        "9": "EMV 3-D Secure Version 2.9",
        "01": "EMV 3-D Secure Version 2.1",
        "02": "EMV 3-D Secure Version 2.2",
        "03": "EMV 3-D Secure Version 2.3",
        "04": "EMV 3-D Secure Version 2.4",
        "05": "EMV 3-D Secure Version 2.5",
        "06": "EMV 3-D Secure Version 2.6",
        "07": "EMV 3-D Secure Version 2.7",
        "08": "EMV 3-D Secure Version 2.8",
        "09": "EMV 3-D Secure Version 2.9"
    },
    "75.SUB1": {
        "001": "Least likely fraudulent transaction",
        "998": "Most likely fraudulent transaction"
    },
    "75.SUB2": {
        "00": "Successful",
        "01": "Not Enough Data (Dormant or New Card)"
    },
    "76": {
        "C": "Mastercard only participant (not Mastercard Electronic)",
        "E": "Acquirer and merchant both participate in Mastercard Electronic",
        "M": "Acquirer participates but merchant does not",
        "U": "Unidentified acquirer"
    },
    "77": {
        "C04": "Gaming Repay",
        "C07": "General Person-to-Person Transfer",
        "C51": "Mastercard Send Indicator (Reserved)",
        "C52": "General Transfer to Own Account",
        "C53": "Agent Cash Out",
        "C54": "Payment of Own Credit Card Bill",
        "C55": "Business Disbursement",
        "C56": "Government/Non-Profit Disbursement",
        "C57": "Rapid Merchant Settlement",
        "C58": "Cash-in at ATM",
        "C59": "Cash-in at Point of Sale",
        "C60": "Fast Refund to Original Card",
        "C61": "Mastercard Send Indicator (Reserved)",
        "C62": "Mastercard Send Indicator (Reserved)",
        "C63": "Mastercard Send Indicator (Reserved)",
        "C64": "Mastercard Send Indicator (Reserved)",
        "C65": "General Business-to-Business Transfer",
        "C66": "Mastercard Send Indicator (Reserved)",
        "C67": "Merchant Presented QR",
        "C68": "Merchant Presented QR Refund",
        "F07": "General Person-to-Person Transfer",
        "F08": "Person-to-Person Transfer to Card Account",
        "F52": "General Transfer to Own Account",
        "F53": "Agent Cash Out",
        "F54": "Payment of Own Credit Card Bill",
        "F55": "Business Disbursement",
        "F61": "Transfer to Own Staged Digital Wallet Account",
        "F64": "Transfer to Own Debit or Prepaid Card Account",
        "F65": "General Business-to-Business Transfer",
        "P10": "Purchase repayment",
        "P11": "Business-to-Business Payment",
        "P70": "Direct purchase of floating cryptocurrencies and other crypto tokens",
        "P71": "High-risk Securities",
        "P72": "Specialty Merchant (Mastercard use only)",
        "P76": "Direct purchase of fully fiat-backed stablecoins and central bank digital currencies"
    },
    "78.SUB1": {
        "N": "Spend assessment threshold not met",
        "B": "Basic spend assessment threshold level met",
        "Q": "Highest spend assessment threshold level met"
    },
    "78.SUB2": {
        "Y": "Dynamic Currency Conversion performed at point of sale"
    },
    "78.SUB3": {
        "D": "U.S. Deferred Billing Indicator"
    },
    "78.SUB4": {
        "Y": "Transaction processed through Visa Checkout"
    },
    "78.SUB5": {
        "0": "Incremental authorization",
        "1": "Resubmission",
        "2": "Delayed charges",
        "3": "Reauthorization",
        "4": "No show",
        "5": "Account top up",
        "6": "Deferred Authorization",
        "7": "AFD Completion Advice"
    },
    "78.SUB6": {
        "1": "Token program"
    },
    "80": {
        "PD": "The Dual Message Authorization System dropped the PIN (Credit Transactions with PIN)",
        "PV": "The Dual Message Authorization System verified the PIN.",
        "TV": "The Dual Message Authorization System translated the PIN for issuer verification.",
        "PI": "The Dual Message Authorization System was unable to verify the PIN.",
        "TI": "The Dual Message Authorization System was unable to translate the PIN."
    },
    "82": {
        "52": "AVS and Authorization Request/0100"
    },
    "83": {
        "A": "Address matches, ZIP code does not match.",
        "B": "Visa Only: Street address match; postal code not verified",
        "C": "Visa Only: Street address and postal code not verified",
        "D": "Visa Only: Street address and postal code match",
        "F": "Visa Only: Street address and postal code match (U.K. only)",
        "G": "Visa Only: Non-AVS participant; address not verified",
        "I": "Visa Only: Address information not verified for international transaction",
        "M": "Street addresses and postal code match",
        "N": "Neither address nor postal code matches.",
        "P": "Visa Only: Postal codes match; street address not verified",
        "R": "Retry - Issuer system unavailable or timed out.",
        "S": "AVS not supported by issuer for this card product.",
        "U": "Address information unavailable.",
        "W": "9-digit ZIP code matches, address does not match.",
        "X": "Exact match - Both street address and 9-digit ZIP match.",
        "Y": "Exact match - Both street address and 5-digit ZIP match.",
        "Z": "5-digit ZIP code matches, address does not match."
    },
    "84": {
        "01": "New account information available / Update credential files",
        "02": "Cannot approve at this time, try again later",
        "03": "Do not try again / Stop recurring payment logic",
        "04": "Token requirements not fulfilled for this token type",
        "05": "Negotiated value not approved",
        "21": "Payment Cancellation (Mastercard use only)",
        "22": "Merchant does not qualify for product code",
        "24": "Retry after 1 hour (Mastercard use only)",
        "25": "Retry after 24 hours (Mastercard use only)",
        "26": "Retry after 2 days (Mastercard use only)",
        "27": "Retry after 4 days (Mastercard use only)",
        "28": "Retry after 6 days (Mastercard use only)",
        "29": "Retry after 8 days (Mastercard use only)",
        "30": "Retry after 10 days (Mastercard use only)",
        "40": "Consumer non-reloadable prepaid card",
        "41": "Consumer single-use virtual card number",
        "42": "Sanctions Scoring Service: Score Exceeds Applicable Threshold Value",
        "43": "Consumer multi-use virtual card number"
    },
    "85": {
        "R": "Account is regulated",
        "N": "Account is non-regulated"
    },
    "86": {
        "C": "Credential on File",
        "I": "Installment Payment",
        "R": "Merchant/Cardholder Periodic Billing"
    },
    "87": {
        "M": "Valid CVC 2 / CVV2 Match.",
        "N": "Invalid CVC 2 / CVV2 Non-match.",
        "P": "CVC 2 not processed (Issuer validation host offline).",
        "S": "CVC 2 should be on card but merchant indicated not present.",
        "U": "CVC 2 unverified.",
        "Y": "Invalid CVC 1 / Stripe Validation Error.",
        "E": "Length of unpredictable number was not a valid length (CVC 3)"
    },
    "88": {
        "Y": "Dual Message Authorization System replaced DE 22 subfield 1 value 90 or 91 with 02"
    },
    "89": {
        "A": "Track 1 or Track 2 not present",
        "B": "Track 1 and Track 2 present",
        "C": "DE 2 PAN not equal in track data",
        "D": "DE 14 Expiration Date not equal in track data",
        "E": "Service code invalid in track data",
        "F": "Field separator(s) invalid in track data",
        "G": "A field within the track data has invalid length",
        "H": "DE 22 subfield 1 is 80, 90, or 91 when TCC is T",
        "I": "DE 61 subfield 4 is 1, 2, 3, 4, or 5",
        "J": "DE 61 subfield 5 is 1"
    },
    "90": {
        "P": "Cardholder enrolled in merchant preferred customer program",
        "I": "Incremental authorization",
        "R": "Recurring payment",
        "Y": "Request for Custom Payment Service participation"
    },
    "94": {
        "0": "Not a commercial card product", 
        "1": "Corporate Card identified", 
        "2": "Business Purchasing Card profile flagged"
    },
    "95": {
        "ARGCTA": "Installment payment transaction within Argentina",
        "AGROF1": "Mastercard Agro Card",
        "BNDES1": "Brazil intracountry transactions using Mastercard BNDES Card",
        "CHLCTA": "Installment payment transaction within Chile",
        "COLCTA": "Installment payment transaction within Colombia",
        "GREECE": "Installment payment transaction within Greece",
        "HGMINS": "Installment payment transaction for Georgia",
        "MCGARS": "Identifies Global Automated Service (GARS) Stand-In activity",
        "MCINST": "Installment payment transaction",
        "MEXCTA": "Installment payment transaction within Mexico",
        "PARCEL": "Installment payment transaction within Brazil",
        "PERCTA": "Installment payment transaction within Peru",
        "PHINST": "Installment payment transaction within Philippines",
        "PRYCTA": "Installment payment transaction within Paraguay",
        "URYCTA": "Installment payment transaction within Uruguay"
    },
    "97": {
        "D": "Visa established limits",
        "B": "Visa established limits",
        "S": "Visa established limits"
    },
    
    # ========================================================================
    # DE 48, SUBELEMENT 71 - On-Behalf Services (OBS) Complete Registry
    # ========================================================================
    "71.SERVICES": {
        "01": "Chip to Magnetic Stripe Conversion Service",
        "02": "M/Chip Cryptogram Pre-validation Service",
        "03": "M/Chip Cryptogram Validation in Stand-In Processing",
        "04": "M/Chip Cryptogram Regeneration Service",
        "05": "Mastercard Identity Check AAV Verification Service",
        "06": "Mastercard Identity Check AAV Verification in Stand-In Processing",
        "08": "Online PIN Pre-validation (Europe Only)",
        "09": "Online PIN Validation in Stand-In (Europe only)",
        "10": "CVC 1 Validation Stand-In Service",
        "11": "CVC 1 Pre-Validation Service",
        "14": "Contactless Mapping Service",
        "15": "Dynamic CVC 3 Pre-validation (with or without Contactless Mapping Service)",
        "16": "Dynamic CVC 3 Validation in Stand-In Processing",
        "17": "In Control Virtual Card Service",
        "18": "Fraud Scoring Service",
        "20": "In Control RCN Spend Control Service",
        "25": "Account Data Compromise Information",
        "26": "Point-of-Interaction Service",
        "31": "Chip CVC to CVC 1 Conversion Service (CVC 1 Key/Decision Matrix Only)",
        "32": "Chip CVC to CVC 1 Conversion Service (Separate Keys/Decision Matrices)",
        "33": "Send and other transactions blocking service",
        "37": "Mastercard Merchant Presented QR Blocking Service",
        "50": "MDES PAN Mapping service",
        "51": "MDES Pre-Validation Service for Secure Element tokens (ICC or DSRP data)",
        "52": "MDES Pre-Validation Service for Secure Element tokens (CVC3 data)",
        "54": "Mastercard Digital Enablement Service Digital Payment Data Validation Service",
        "55": "Merchant Validation Service",
        "61": "MDES Pre-Validation Service for Cloud and Static tokens (ICC, DSRP, or DTVC data)",
        "62": "MDES Pre-Validation Service for Cloud tokens (CVC3 data)",
        "71": "Token Service Provider Cloud Based Payments Chip Validation Service in Stand-In"
    },
    
    "71.OBS01": {
        "C": "Conversion of M/Chip transaction to magstripe completed from PAN Entry Mode 05 or 79",
        "M": "Conversion of M/Chip fallback transaction to magstripe completed from PAN Entry Mode 80",
        "S": "Conversion of M/Chip transaction to magstripe completed from PAN Entry Mode 07"
    },
    "71.OBS02_03_51": {
        "A": "Valid Application Cryptogram (AC); ATC outside allowed range",
        "E": "Valid Application Cryptogram; ATC Replay", 
        "F": "Format Error",
        "G": "Application Cryptogram is valid but not an ARQC nor a TC, status of TVR/CVR unknown",
        "I": "Invalid Cryptogram", 
        "K": "No matching key file for this PAN, PAN expiry date and KDI combination",
        "T": "Valid ARQC/TC and ATC; TVR/CVR invalid", 
        "U": "Unable to process", 
        "V": "Valid",
        "X": "Security platform time out", 
        "Z": "Security platform processing error"
    },
    "71.OBS04": {
        "C": "Regeneration of the M/Chip cryptogram was completed"
    },
    "71.OBS05_06": {
        "A": "DS Txn ID not provided; AAV, amount and currency verified",
        "B": "DS Txn ID not provided; AAV and currency verified; amount 0-20% different",
        "C": "DS Txn ID not provided; AAV and currency verified; amount greater than 20% different",
        "D": "DS Transaction ID does not match with PAN and SPA2 AAV within the authentication record",
        "E": "Format Error; AAV incorrectly formatted, failed authentication, or previously used in approved auth",
        "F": "Failed MAC key validation; Dynamic Linking validation not provided",
        "I": "Invalid AAV; Dynamic Linking unable to find matching authentication (expired, used, or non-DS)",
        "K": "No matching key file for PAN. SPA2 AAV provided not generated by Mastercard Identity Check",
        "M": "Monetary Currency mismatch between authorization and authentication",
        "P": "Passed MAC key Validation; Dynamic Linking validation not provided",
        "S": "DS Txn ID present; AAV and currency verified; amount 0-20% different",
        "T": "DS Txn ID present; AAV and currency verified; amount greater than 20% different",
        "U": "Unable to process", 
        "V": "Valid",
        "X": "Security platform time out or Authentication Challenge (Results Request) not received yet",
        "Z": "Security platform processing error or Authentication Response not received yet"
    },
    "71.OBS08_09": {
        "I": "Invalid PIN", 
        "P": "Mandatory PVV not on file", 
        "R": "PIN retry exceeded (invalid PIN)",
        "U": "Unable to process", 
        "V": "Valid"
    },
    "71.OBS10_11": {
        "I": "Invalid CVC 1", 
        "K": "No matching key file for this PAN/Expiry date combination",
        "U": "Unable to process", 
        "V": "Valid"
    },
    "71.OBS14": {
        "C": "Conversion of contactless account number to PAN was completed", 
        "I": "Invalid", 
        "U": "Unable to process"
    },
    "71.OBS15_16_62": {
        "A": "ATC outside allowed range (dynamic value profile)", 
        "E": "CVC 3 ATC Replay", 
        "F": "Format Error",
        "H": "Invalid Time Validation", 
        "I": "Invalid CVC 3", 
        "K": "No matching key file for this PAN, PAN expiry date, and KDI combination",
        "N": "Unpredictable Number Mismatch / Length Indicator Mismatch", 
        "U": "Unable to process", 
        "V": "Valid",
        "X": "Security platform time out", 
        "Z": "Security platform system error"
    },
    "71.OBS17": {
        "A": "Virtual Card Number (expiration date does not match)", 
        "B": "Virtual Card Number (expiration date expired)",
        "C": "Virtual Card Number Virtual CVC 2 does not match", 
        "D": "In Control Validity Period Limit",
        "E": "In Control Transaction Amount Limit Check", 
        "F": "In Control Cumulative Amount Limit Check",
        "G": "In Control Transaction Number Usage", 
        "H": "In Control Merchant ID Limit",
        "I": "In Control Invalid Virtual Card Number—Real Card Number mapping relationship", 
        "J": "In Control MCC Limit",
        "K": "In Control Database Status Bad", 
        "L": "In Control Geographic Restriction",
        "M": "In Control Transaction Type Restriction", 
        "P": "In Control Transaction Time/Date Restriction",
        "U": "Unable to process", 
        "V": "Valid", 
        "Y": "In Control Credit Block"
    },
    "71.OBS18": {
        "C": "Fraud Scoring Service was performed successfully", 
        "U": "Fraud Scoring Service was not performed successfully"
    },
    "71.OBS20": {
        "D": "In Control Validity Period Limit", 
        "E": "In Control Transaction Amount Limit Check",
        "F": "In Control Cumulative Amount Limit Check", 
        "G": "In Control Transaction Number Usage",
        "H": "In Control Merchant ID Limit", 
        "J": "In Control MCC Limit", 
        "K": "In Control Database Status Bad",
        "L": "In Control Geographic Restriction", 
        "M": "In Control Transaction Type Restriction",
        "P": "In Control Transaction Time/Date Restriction", 
        "U": "Unable to process", 
        "V": "Valid"
    },
    "71.OBS25": {
        "Y": "Compromised Event Data Found", 
        "N": "Compromised Event Data Not Found", 
        "U": "Unable to process"
    },
    "71.OBS26": {
        "C": "Enrichment completed for Installments", 
        "F": "PAN does not qualify for installments", 
        "U": "Unable to Process"
    },
    "71.OBS31_32": {
        "C": "Chip CVC Validated Successfully; Conversion performed successfully", 
        "F": "Track Data Formatted Incorrectly",
        "I": "Chip CVC Invalid; Conversion not performed",
        "K": "Key Record / Chip CVC Key Record not found for Account Range / Expiry Date combination",
        "L": "Issuer CVC 1 Key Record not Found for Account Range / Expiry Date combination",
        "M": "Issuer Chip CVC Key Record not Found for Account Range / Expiry Date combination", 
        "U": "Unable to process"
    },
    "71.OBS33": {
        "A": "Send issuer blocking: Limit not allowed for TTI", 
        "B": "Send issuer blocking: Merchant not allowed for TTI",
        "D": "Send issuer blocking: Country not allowed for TTI", 
        "E": "Send issuer blocking: Domestic activity only allowed for TTI",
        "F": "Send issuer blocking: Sanctions Score limit exceeded for TTI", 
        "G": "Send Mastercard blocking: Single transaction amount limit exceeded for Payment Txn",
        "H": "Mastercard blocking: General miscoding", 
        "I": "Send Mastercard blocking: Reserved for future use",
        "J": "Send Mastercard blocking: Transaction Count limit exceeded", 
        "K": "Send Mastercard blocking: Accumulated transaction amount limit exceeded",
        "L": "Send issuer blocking: Transaction Count exceeded for TTI", 
        "M": "Send issuer blocking: Aggregate transaction amount limit exceeded for TTI",
        "N": "Send issuer monitoring: Transaction Count exceeded for TTI", 
        "O": "Send issuer monitoring: Aggregate transaction amount limit exceeded for TTI",
        "P": "Send issuer monitoring: Transaction amount limit exceeded for TTI", 
        "Q": "Send issuer monitoring: Sanctions Score exceeded",
        "R": "Send issuer blocking: Invalid Card", 
        "S": "Send Mastercard blocking: Product code invalid for TTI or use case",
        "T": "Send Mastercard blocking: Single transaction amount limit exceeded for Funding Txn", 
        "U": "Unable to process",
        "V": "Valid", 
        "W": "Send Mastercard blocking: Geographical restriction", 
        "X": "Send Mastercard blocking: Reserved",
        "Y": "Send Mastercard blocking: Data quality controls"
    },
    "71.OBS37": {
        "D": "QR Blocking - Transaction Amount Limit Exceeded",
        "E": "QR Blocking - Cumulative Transaction Amount Or Count Limit Exceeded",
        "F": "QR Blocking - Domestic Activity Only", 
        "U": "Unable to Process", 
        "V": "Valid"
    },
    "71.OBS50": {
        "C": "Conversion of Token to PAN completed successfully", 
        "F": "Format Error", 
        "I": "Invalid Token", 
        "U": "Unable to process"
    },
    "71.OBS54": {
        "A": "DE 4 transaction amount <= approximate amount in cryptogram",
        "B": "DE 4 transaction amount greater than approximate amount by 0% to 19.99%",
        "C": "DE 4 transaction amount greater than approximate amount by 20% or more",
        "D": "DE 4 transaction amount is not zero and approximate amount in cryptogram is zero"
    },
    "71.OBS55": {
        "M": "Submitted merchant data matches Mastercard data", 
        "N": "Submitted merchant data is not a match", 
        "U": "Unable to Process"
    },
    "71.OBS61_71": {
        "D": "ATC Invalid - Not in list of currently active Single-Use Keys", 
        "E": "ATC Replay", 
        "F": "Format Error",
        "I": "Invalid MD AC and UMD AC", 
        "K": "No matching key file for this PAN, PAN expiry date and KDI combination",
        "L": "Invalid MD AC; Valid UMD AC", 
        "M": "Valid MD AC; Invalid UMD AC (Mobile PIN Try Counter Max Reached, Token Suspended)",
        "P": "Valid MD AC; Invalid UMD AC (Invalid Mobile PIN)", 
        "T": "Invalid TVR/CVR", 
        "U": "Unable to process",
        "V": "Valid", 
        "X": "Security platform time out", 
        "Z": "Security platform system error"
    },
    
    # ========================================================================
    # ALM Service Codes Complete Registry
    # ========================================================================
    "24.ALM_SERVICES": {
        "00000": "ALM SERVICE UNAVAILABLE IN AUTHORIZATION",
        "00126": "PAN NOT REGISTERED FOR ALM, BUT ISSUER'S ACCOUNT RANGE IS ACTIVE",
        "00127": "PAN IS REGISTERED FOR ALM, BUT TRANSACTION WAS PROCESSED AS DEBIT",
        "00402": "ENHANCED VALUE",
        "00513": "ENHANCED VALUE and PRODUCT GRADUATION PLUS",
        "00616": "PRODUCT GRADUATION PLUS",
        "00703": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 1",
        "00705": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 2",
        "00707": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 3",
        "00710": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 4",
        "00717": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 5",
        "00804": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 1 + PRODUCT GRADUATION PLUS",
        "00806": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 2 + PRODUCT GRADUATION PLUS",
        "00808": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 3 + PRODUCT GRADUATION PLUS",
        "00811": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 4 + PRODUCT GRADUATION PLUS",
        "00818": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 5 + PRODUCT GRADUATION PLUS",
        "00903": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 1",
        "00905": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 2",
        "00907": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 3",
        "00910": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 4",
        "00917": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 5",
        "01004": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 1 + PRODUCT GRADUATION PLUS",
        "01006": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 2 + PRODUCT GRADUATION PLUS",
        "01008": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 3 + PRODUCT GRADUATION PLUS",
        "01011": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 4 + PRODUCT GRADUATION PLUS",
        "01018": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 5 + PRODUCT GRADUATION PLUS",
        "01103": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 1",
        "01105": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 2",
        "01107": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 3",
        "01110": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 4",
        "01117": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 5",
        "01204": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 1 + PRODUCT GRADUATION PLUS",
        "01206": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 2 + PRODUCT GRADUATION PLUS",
        "01208": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 3 + PRODUCT GRADUATION PLUS",
        "01211": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 4 + PRODUCT GRADUATION PLUS",
        "01218": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 5 + PRODUCT GRADUATION PLUS",
        "01323": "AFFLUENT SHORTFALL WORLD ELITE MASTERCARD",
        "01425": "AFFLUENT SHORTFALL WORLD ELITE MASTERCARD + PRODUCT GRADUATION PLUS",
        "01519": "WORLD HIGH VALUE",
        "01620": "WORLD HIGH VALUE + PRODUCT GRADUATION PLUS",
        "01723": "AFFLUENT SHORTFALL WORLD MASTERCARD",
        "01825": "AFFLUENT SHORTFALL WORLD MASTERCARD + PRODUCT GRADUATION PLUS",
        "02205": "CONSUMER PRODUCT MONITORING: WORLD QUALIFIED",
        "02207": "CONSUMER PRODUCT MONITORING: MPE QUALIFIED",
        "02210": "CONSUMER PRODUCT MONITORING: WORLD ELITE QUALIFIED",
        "02217": "CONSUMER PRODUCT MONITORING: MUSE MASTERCARD QUALIFIED",
        "02301": "CONSUMER PRODUCT MONITORING: REQUALIFICATION 1 (MUSE REQUALIFIED)",
        "02424": "CONSUMER PRODUCT MONITORING: REQUALIFICATION 2 (WORLD ELITE REQUALIFIED)",
        "50000": "MASTERCARD ONE CREDENTIAL",
        "50127": "MASTERCARD ONE CREDENTIAL - NO CONSUMER PREFERENCE MET",
        "50402": "ENHANCED VALUE + MASTERCARD ONE CREDENTIAL",
        "50513": "ENHANCED VALUE + PRODUCT GRADUATION PLUS + MASTERCARD ONE CREDENTIAL",
        "50616": "PRODUCT GRADUATION PLUS + MASTERCARD ONE CREDENTIAL",
        "50703": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 1 + MASTERCARD ONE CREDENTIAL",
        "50705": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 2 + MASTERCARD ONE CREDENTIAL",
        "50707": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 3 + MASTERCARD ONE CREDENTIAL",
        "50710": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 4 + MASTERCARD ONE CREDENTIAL",
        "50717": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 5 + MASTERCARD ONE CREDENTIAL",
        "50804": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 1 + PRODUCT GRADUATION + MASTERCARD ONE",
        "50806": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 2 + PRODUCT GRADUATION + MASTERCARD ONE",
        "50808": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 3 + PRODUCT GRADUATION + MASTERCARD ONE",
        "50811": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 4 + PRODUCT GRADUATION + MASTERCARD ONE",
        "50818": "SMALL BUSINESS SPEND - CREDIT CORE LEVEL 5 + PRODUCT GRADUATION + MASTERCARD ONE",
        "50903": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 1 + MASTERCARD ONE CREDENTIAL",
        "50905": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 2 + MASTERCARD ONE CREDENTIAL",
        "50907": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 3 + MASTERCARD ONE CREDENTIAL",
        "50910": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 4 + MASTERCARD ONE CREDENTIAL",
        "50917": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 5 + MASTERCARD ONE CREDENTIAL",
        "51004": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 1 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51006": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 2 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51008": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 3 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51011": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 4 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51018": "SMALL BUSINESS SPEND - CREDIT WORLD LEVEL 5 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51103": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 1 + MASTERCARD ONE CREDENTIAL",
        "51105": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 2 + MASTERCARD ONE CREDENTIAL",
        "51107": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 3 + MASTERCARD ONE CREDENTIAL",
        "51110": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 4 + MASTERCARD ONE CREDENTIAL",
        "51117": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 5 + MASTERCARD ONE CREDENTIAL",
        "51204": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 1 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51206": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 2 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51208": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 3 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51211": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 4 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51218": "SMALL BUSINESS SPEND - CREDIT WORLD ELITE LEVEL 5 + PRODUCT GRADUATION + MASTERCARD ONE",
        "51323": "WORLD ELITE SHORTFALL + MASTERCARD ONE CREDENTIAL",
        "51425": "WORLD ELITE SHORTFALL + PRODUCT GRADUATION + MASTERCARD ONE CREDENTIAL",
        "51519": "WORLD HIGH VALUE + MASTERCARD ONE CREDENTIAL",
        "51620": "WORLD HIGH VALUE + PRODUCT GRADUATION + MASTERCARD ONE CREDENTIAL",
        "51723": "WORLD SHORTFALL + MASTERCARD ONE CREDENTIAL",
        "51825": "WORLD SHORTFALL + PRODUCT GRADUATION + MASTERCARD ONE CREDENTIAL",
        "52205": "CONSUMER PRODUCT MONITORING: WORLD QUALIFIED + MASTERCARD ONE CREDENTIAL",
        "52207": "CONSUMER PRODUCT MONITORING: MPE QUALIFIED + MASTERCARD ONE CREDENTIAL",
        "52210": "CONSUMER PRODUCT MONITORING: WORLD ELITE QUALIFIED + MASTERCARD ONE CREDENTIAL",
        "52217": "CONSUMER PRODUCT MONITORING: MUSE QUALIFIED + MASTERCARD ONE CREDENTIAL",
        "52301": "CONSUMER PRODUCT MONITORING: REQUALIFICATION 1 + MASTERCARD ONE CREDENTIAL",
        "52424": "CONSUMER PRODUCT MONITORING: REQUALIFICATION 2 + MASTERCARD ONE CREDENTIAL"
    },
    "24.ALM_RATE_TYPES": {
        "801": "Enhanced Value Rate Adjustment",
        "811": "Core Business to Level 1 Adjustment",
        "812": "Core Business to Level 2 Adjustment",
        "813": "Core Business to Level 3 Adjustment",
        "814": "Core Business to Level 4 Adjustment",
        "815": "Core Business to Level 5 Adjustment",
        "821": "World Business to Level 1 Adjustment",
        "822": "World Business to Level 2 Adjustment",
        "823": "World Business to Level 3 Adjustment",
        "824": "World Business to Level 4 Adjustment",
        "825": "World Business to Level 5 Adjustment",
        "831": "World Elite Business to Level 1 Adjustment",
        "832": "World Elite Business to Level 2 Adjustment",
        "833": "World Elite Business to Level 3 Adjustment",
        "834": "World Elite Business to Level 4 Adjustment",
        "835": "World Elite Business to Level 5 Adjustment",
        "850": "World High Value Adjustment",
        "851": "World Consumer Shortfall Adjustment",
        "852": "World Elite Consumer Shortfall Adjustment",
        "881": "Canada World Consumer Adjustment",
        "882": "Canada MPE Adjustment",
        "883": "Canada World Elite Adjustment",
        "884": "Canada MUSE Adjustment",
        "885": "Canada MUSE Requalified Down Adjustment",
        "886": "Canada World Elite Requalified Down Adjustment",
        "XXX": "RATE TYPE DOES NOT APPLY OR NOT CONFIGURED"
    },
    "24.ALM_ACCEPTANCE_BRAND": {
        "MCC": "Mastercard",
        "DMC": "Debit Mastercard",
        "MSI": "Maestro"
    },
    "24.ALM_INTERCHANGE": {
        "D": "Dynamic Interchange - based on Mastercard One Credential Funding PAN",
        "S": "Static Interchange - based on DE 2 primary PAN"
    }
}

# Mastercard One Credential service code patterns for detection
MC_ONE_SERVICE_PATTERNS = [
    "50000", "50127", "50402", "50513", "50616",
    "50703", "50705", "50707", "50710", "50717",
    "50804", "50806", "50808", "50811", "50818",
    "50903", "50905", "50907", "50910", "50917",
    "51004", "51006", "51008", "51011", "51018",
    "51103", "51105", "51107", "51110", "51117",
    "51204", "51206", "51208", "51211", "51218",
    "51323", "51425", "51519", "51620", "51723", "51825",
    "52205", "52207", "52210", "52217", "52301", "52424"
]


def decode_de48_subelement(se_tag: str, value: str) -> str:
    """
    Decodes structural subelement layouts and positional parameters inside Data Element 48.
    Handles variable-length formats, spaces, and malformed inputs gracefully.
    """
    # Strip leading/trailing whitespace
    clean_val = value.strip()
    tag_name = DE48_SUBELEMENT_GLOSSARY.get(se_tag, f"Subelement {se_tag}")
    validation_err = ""
    
    # Check simple flat code enumerations first
    if se_tag in DE48_VALUE_TABLES and se_tag not in ("21", "22", "24", "37", "42", "48", "61", "62", "66", "71", "75", "78"):
        meaning = DE48_VALUE_TABLES[se_tag].get(clean_val, f"Value '{clean_val}' recognized but description unassigned")
        return f"{tag_name}: {meaning}"

    # Advanced Multi-Position Layouts Logic
    if se_tag in ("06", "07", "08"):
        return f"{tag_name} -> Raw E-Commerce Telemetry/Identity Verification Payload: `{clean_val}`"

    if se_tag == "21":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        if len(clean_val) >= 3:
            p1 = DE48_VALUE_TABLES["21.POS1"].get(clean_val[0], "Unknown Entry Mode")
            p2 = DE48_VALUE_TABLES["21.POS2"].get(clean_val[1:3], f"Unknown PIN/QR Mode: {clean_val[1:3]}")
            return f"{tag_name} -> Device Type: {p1} | Terminal Capability: {p2}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "22":
        if len(clean_val) < 2:
            validation_err = " [Warning: Expected at least 2 characters]"
            return f"{tag_name}: `{clean_val}`{validation_err}"
        
        pos = 0
        result_parts = []
        
        # Check for M208 (Resubmission) pattern
        if clean_val.startswith("M208"):
            result_parts.append("Type: Resubmission")
            remaining = clean_val[4:]
            if remaining:
                result_parts.append(f"Additional: {remaining}")
            return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"
        
        # Parse CIT/MIT indicators (2 chars each)
        if len(clean_val) >= 2:
            val1 = clean_val[pos:pos+2]
            pos += 2
            desc1 = DE48_VALUE_TABLES["22.POS1"].get(val1, f"Unknown Framework Type: {val1}")
            result_parts.append(f"Type: {desc1}")
        
        if len(clean_val) > pos:
            val2 = clean_val[pos]
            pos += 1
            desc2 = DE48_VALUE_TABLES["22.POS2"].get(val2, f"Unknown Sequence: {val2}")
            result_parts.append(f"Sequence: {desc2}")
        
        if len(clean_val) > pos:
            val3 = clean_val[pos]
            pos += 1
            if val3 == "1":
                result_parts.append("✓ Merchant supports single tap")
        
        if len(clean_val) > pos:
            val4 = clean_val[pos]
            pos += 1
            if val4 == "1":
                result_parts.append("Issuer requested PIN in Single Tap mode")
        
        if len(clean_val) > pos:
            remaining = clean_val[pos:]
            if remaining:
                result_parts.append(f"Additional: {remaining}")
        
        return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"

    if se_tag == "23":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        if len(clean_val) >= 2:
            meaning = DE48_VALUE_TABLES["23"].get(clean_val[:2], f"Unknown Payment Channel Code '{clean_val[:2]}'")
            return f"{tag_name} -> {meaning}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"
        
    if se_tag == "24":
        if len(clean_val) < 5:
            validation_err = " [Warning: Minimum 5 characters required for ALM Service Code]"
            return f"{tag_name}: `{clean_val}`{validation_err}"
        
        pos = 0
        service_code = clean_val[pos:pos+5]
        pos += 5
        
        result_parts = []
        
        service_desc = DE48_VALUE_TABLES["24.ALM_SERVICES"].get(service_code, f"UNKNOWN SERVICE: {service_code}")
        result_parts.append(f"Service: {service_code} ({service_desc})")
        
        if service_code in MC_ONE_SERVICE_PATTERNS:
            result_parts.append("✓ MASTERCARD ONE CREDENTIAL")
        
        if len(clean_val) >= pos + 3:
            product_code = clean_val[pos:pos+3]
            pos += 3
            if product_code != "XXX":
                result_parts.append(f"Product Code: {product_code}")
        
        if len(clean_val) >= pos + 3:
            class_code = clean_val[pos:pos+3]
            pos += 3
            if class_code != "XXX":
                result_parts.append(f"Class Code: {class_code}")
        
        if len(clean_val) >= pos + 3:
            rate_code = clean_val[pos:pos+3]
            pos += 3
            rate_desc = DE48_VALUE_TABLES["24.ALM_RATE_TYPES"].get(rate_code, f"UNKNOWN: {rate_code}")
            if rate_code != "XXX":
                result_parts.append(f"Rate: {rate_code} ({rate_desc})")
        
        if len(clean_val) >= pos + 4:
            brand = clean_val[pos:pos+3]
            pos += 3
            brand_desc = DE48_VALUE_TABLES["24.ALM_ACCEPTANCE_BRAND"].get(brand, f"UNKNOWN: {brand}")
            if brand in DE48_VALUE_TABLES["24.ALM_ACCEPTANCE_BRAND"]:
                result_parts.append(f"Brand: {brand} ({brand_desc})")
            
            indicator = clean_val[pos:pos+1]
            pos += 1
            ind_desc = DE48_VALUE_TABLES["24.ALM_INTERCHANGE"].get(indicator, f"UNKNOWN: {indicator}")
            if indicator in DE48_VALUE_TABLES["24.ALM_INTERCHANGE"]:
                result_parts.append(f"Interchange: {indicator} ({ind_desc})")
            
            account_range = clean_val[pos:]
            if account_range:
                result_parts.append(f"Issuer Account Range: {account_range}")
        
        return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"

    if se_tag == "26":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        meaning = DE48_VALUE_TABLES["26"].get(clean_val[:3], f"Unknown Wallet ID: {clean_val[:3]}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "32":
        if len(clean_val) != 6:
            validation_err = " [Warning: Expected length exactly 6]"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "37":
        # Parse Additional Merchant Data
        if len(clean_val) >= 11:
            # Try to parse as Service Provider ID (11 digits) + Role (11 digits)
            service_id = clean_val[:11]
            remaining = clean_val[11:]
            
            result_parts = [f"Service Provider ID: {service_id}"]
            
            if len(remaining) >= 11:
                role = remaining[:11]
                remaining = remaining[11:]
                role_desc = DE48_VALUE_TABLES["37.SERVICE_ROLES"].get(role, f"Unknown Role: {role}")
                result_parts.append(f"Role: {role} ({role_desc})")
                
                if len(remaining) >= 15:
                    seller_id = remaining[:15]
                    remaining = remaining[15:]
                    if seller_id.strip():
                        result_parts.append(f"Seller ID: {seller_id}")
                    
                    if len(remaining) >= 3:
                        merchant_country = remaining[:3]
                        remaining = remaining[3:]
                        if merchant_country.strip():
                            result_parts.append(f"Merchant Country: {merchant_country}")
                    
                    if len(remaining) >= 11:
                        gateway_id = remaining[:11]
                        remaining = remaining[11:]
                        if gateway_id.strip():
                            result_parts.append(f"Payment Gateway ID: {gateway_id}")
                    
                    if remaining.strip():
                        result_parts.append(f"Additional: {remaining}")
                
            return f"{tag_name} -> {' | '.join(result_parts)}"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "42":
        if len(clean_val) < 3:
            validation_err = " [Warning: Expected at least 3 characters]"
            return f"{tag_name}: Raw Matrix `{clean_val}`{validation_err}"
        
        # Parse the first 3 characters
        p1 = DE48_VALUE_TABLES["42.POS1"].get(clean_val[0], f"Unknown Protocol: {clean_val[0]}")
        p2 = DE48_VALUE_TABLES["42.POS2"].get(clean_val[1], f"Unknown Auth Status: {clean_val[1]}")
        p3 = DE48_VALUE_TABLES["42.POS3"].get(clean_val[2], f"Unknown UCAF Configuration: {clean_val[2]}")
        
        result_parts = [f"Protocol: {p1}", f"Auth: {p2}", f"UCAF: {p3}"]
        
        # If there are extra characters (positions 4+), they represent Original SLI and UCAF Downgrade Reason
        if len(clean_val) > 3:
            extra = clean_val[3:]
            if len(extra) >= 6:
                original_sli = extra[:3]
                downgrade_reason = extra[3:6]
                reason_desc = DE48_VALUE_TABLES["42.DOWNGRADE_REASON"].get(downgrade_reason, f"Unknown: {downgrade_reason}")
                result_parts.append(f"Original SLI: {original_sli}")
                result_parts.append(f"Downgrade Reason: {reason_desc}")
                if len(extra) > 6:
                    result_parts.append(f"Additional: {extra[6:]}")
            else:
                result_parts.append(f"Additional Data: {extra}")
        
        return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"

    if se_tag == "43":
        if len(clean_val) == 28:
            if clean_val.startswith(('k', 'i')):
                return f"{tag_name} -> Identity Check AAV: `{clean_val}`"
            elif clean_val.startswith('3') or clean_val.startswith('5'):
                return f"{tag_name} -> Static AAV: `{clean_val}`"
            else:
                return f"{tag_name} -> DSRP UCAF: `{clean_val}`"
        elif len(clean_val) == 21:
            return f"{tag_name} -> 3-D Secure (Visa/Amex): `{clean_val}`"
        else:
            return f"{tag_name}: `{clean_val}`"
    
    if se_tag == "48":
        if len(clean_val) >= 1:
            dom_id = DE48_VALUE_TABLES["48.SUB1"].get(clean_val[0], "Unknown Domain Operator")
            program_type = ""
            if len(clean_val) >= 2:
                program_type = DE48_VALUE_TABLES["48.SUB2"].get(clean_val[1], "")
            return f"{tag_name} -> Domain: {dom_id} | Program: {program_type if program_type else clean_val[1:]}"
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
        if len(clean_val) < 2:
            validation_err = " [Warning: Expected at least 2 characters]"
            return f"{tag_name}: `{clean_val}`{validation_err}"
        
        pos = 0
        result_parts = []
        
        if len(clean_val) > pos:
            f1 = DE48_VALUE_TABLES["62.SUB1"].get(clean_val[pos], "Unknown Account Config")
            result_parts.append(f"Settlement Node: {f1}")
            pos += 1
        
        if len(clean_val) > pos:
            f2 = DE48_VALUE_TABLES["62.SUB2"].get(clean_val[pos], "Unknown Speed Class")
            result_parts.append(f"Network: {f2}")
            pos += 1
        
        if len(clean_val) > pos:
            remaining = clean_val[pos:]
            if remaining.startswith("PBA"):
                result_parts.append("Rules: Mastercard Pay by Account")
            else:
                if len(remaining) >= 3:
                    sub3 = remaining[:3]
                    rules_desc = DE48_VALUE_TABLES["62.SUB3"].get(sub3, f"Unknown Rules: {sub3}")
                    result_parts.append(f"Rules: {rules_desc}")
                    remaining = remaining[3:]
                    
                    if len(remaining) >= 2:
                        sub4 = remaining[:2]
                        network_desc = DE48_VALUE_TABLES["62.SUB4"].get(sub4, f"Unknown Network: {sub4}")
                        result_parts.append(f"Network: {network_desc}")
                        remaining = remaining[2:]
                        
                        if len(remaining) >= 2:
                            sub5 = remaining[:2]
                            pos_desc = DE48_VALUE_TABLES["62.SUB5"].get(sub5, f"Unknown Position: {sub5}")
                            result_parts.append(f"Funds Position: {pos_desc}")
                            remaining = remaining[2:]
                            
                            if remaining:
                                result_parts.append(f"DSS Reference: {remaining}")
        
        return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"

    if se_tag == "63":
        if len(clean_val) != 15:
            validation_err = " [Warning: Expected length exactly 15]"
        return f"{tag_name} -> Network Tracking Index Reference ID: `{clean_val}`{validation_err}"

    if se_tag == "64":
        if len(clean_val) != 4:
            validation_err = " [Warning: Expected length exactly 4]"
        if len(clean_val) >= 4:
            transit_type = clean_val[:2]
            transport_mode = clean_val[2:4]
            type_desc = DE48_VALUE_TABLES["64.SUB1"].get(transit_type, f"Unknown Type: {transit_type}")
            mode_desc = DE48_VALUE_TABLES["64.SUB2"].get(transport_mode, f"Unknown Mode: {transport_mode}")
            return f"{tag_name} -> Type: {type_desc} | Mode: {mode_desc}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "65":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        if len(clean_val) >= 2:
            tle = DE48_VALUE_TABLES["65"].get(clean_val[0], f"Unknown TLE: {clean_val[0]}")
            dukpt = DE48_VALUE_TABLES["65"].get(clean_val[1], f"Unknown DUKPT: {clean_val[1]}")
            return f"{tag_name} -> TLE: {tle} | DUKPT: {dukpt}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "66":
        if len(clean_val) >= 2:
            # Protocol could be 1 or 2 digits
            if clean_val[0] == '0':
                protocol = clean_val[:2]
                ds_trans_id = clean_val[2:]
            else:
                protocol = clean_val[:1]
                ds_trans_id = clean_val[1:]
            proto_desc = DE48_VALUE_TABLES["66.SUB1"].get(protocol, f"Unknown Protocol: {protocol}")
            return f"{tag_name} -> Protocol: {protocol} ({proto_desc}) | DS Transaction ID: `{ds_trans_id}`"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "67":
        if len(clean_val) >= 3:
            score = clean_val[:3]
            remaining = clean_val[3:]
            return f"{tag_name} -> Sanctions Score: {score}{' | Info: ' + remaining if remaining else ''}"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "68":
        return f"{tag_name} -> Financial Account: `{clean_val}`"

    if se_tag == "71":
        # Remove all spaces from the value before parsing
        clean_val_no_spaces = clean_val.replace(" ", "")
        
        if len(clean_val_no_spaces) == 0:
            return f"{tag_name}: No data present"
            
        # Ensure the length is a multiple of 3
        if len(clean_val_no_spaces) % 3 != 0:
            validation_err = f" [Warning: Subelement 71 layout must be a repeating series of 3-char blocks. Raw length: {len(clean_val_no_spaces)}]"
            # Attempt to parse what we can
            clean_val_no_spaces = clean_val_no_spaces[: (len(clean_val_no_spaces) // 3) * 3]
            if not clean_val_no_spaces:
                return f"{tag_name}: Malformed data - cannot parse `{clean_val}`{validation_err}"
        
        parsed_services = []
        for i in range(0, len(clean_val_no_spaces), 3):
            block = clean_val_no_spaces[i:i+3]
            if len(block) < 3:
                parsed_services.append(f"Malformed block fragment: `{block}`")
                continue
            
            svc_code = block[:2]
            res_code = block[2]
            svc_desc = DE48_VALUE_TABLES["71.SERVICES"].get(svc_code, f"Unknown On-behalf Service '{svc_code}'")
            
            # Look up result description based on service code
            if svc_code == "01":
                res_desc = DE48_VALUE_TABLES["71.OBS01"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("02", "03", "51"):
                res_desc = DE48_VALUE_TABLES["71.OBS02_03_51"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "04":
                res_desc = DE48_VALUE_TABLES["71.OBS04"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("05", "06"):
                res_desc = DE48_VALUE_TABLES["71.OBS05_06"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("08", "09"):
                res_desc = DE48_VALUE_TABLES["71.OBS08_09"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("10", "11"):
                res_desc = DE48_VALUE_TABLES["71.OBS10_11"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "14":
                res_desc = DE48_VALUE_TABLES["71.OBS14"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("15", "16", "62"):
                res_desc = DE48_VALUE_TABLES["71.OBS15_16_62"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "17":
                res_desc = DE48_VALUE_TABLES["71.OBS17"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "18":
                res_desc = DE48_VALUE_TABLES["71.OBS18"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "20":
                res_desc = DE48_VALUE_TABLES["71.OBS20"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "25":
                res_desc = DE48_VALUE_TABLES["71.OBS25"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "26":
                res_desc = DE48_VALUE_TABLES["71.OBS26"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("31", "32"):
                res_desc = DE48_VALUE_TABLES["71.OBS31_32"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "33":
                res_desc = DE48_VALUE_TABLES["71.OBS33"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "37":
                res_desc = DE48_VALUE_TABLES["71.OBS37"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "50":
                res_desc = DE48_VALUE_TABLES["71.OBS50"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "54":
                res_desc = DE48_VALUE_TABLES["71.OBS54"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code == "55":
                res_desc = DE48_VALUE_TABLES["71.OBS55"].get(res_code, f"Unknown Code '{res_code}'")
            elif svc_code in ("61", "71"):
                res_desc = DE48_VALUE_TABLES["71.OBS61_71"].get(res_code, f"Unknown Code '{res_code}'")
            else:
                res_desc = f"Result Flag '{res_code}'"
                
            parsed_services.append(f"[{svc_desc} -> {res_desc}]")
            
        services_summary = " | ".join(parsed_services)
        return f"{tag_name} -> {services_summary}{validation_err}"

    if se_tag == "72":
        return f"{tag_name} -> Issuer Chip Authentication Data: `{clean_val}`"

    if se_tag == "74":
        if len(clean_val) >= 3:
            proc_ind = clean_val[:2]
            proc_info = clean_val[2:]
            proc_desc = {
                "02": "M/Chip Cryptogram Pre-validation",
                "03": "M/Chip Cryptogram Validation in Stand-In Processing",
                "50": "Issuer Chip Validation",
                "90": "Chip Fallback Transaction Downgrade Process"
            }.get(proc_ind, f"Unknown Processing: {proc_ind}")
            return f"{tag_name} -> {proc_desc} | Info: {proc_info if proc_info else 'N/A'}"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "75":
        # Parse Fraud Scoring Data
        if len(clean_val) < 5:
            validation_err = " [Warning: Expected at least 5 characters (Score + Reason Code)]"
            return f"{tag_name}: `{clean_val}`{validation_err}"
        
        pos = 0
        result_parts = []
        
        # Subfield 1: Fraud Score (3 chars)
        if len(clean_val) >= pos + 3:
            fraud_score = clean_val[pos:pos+3]
            pos += 3
            score_desc = DE48_VALUE_TABLES["75.SUB1"].get(fraud_score, f"Score value: {fraud_score}")
            result_parts.append(f"Fraud Score: {fraud_score} ({score_desc})")
        
        # Subfield 2: Reason Code (2 chars)
        if len(clean_val) >= pos + 2:
            reason_code = clean_val[pos:pos+2]
            pos += 2
            reason_desc = DE48_VALUE_TABLES["75.SUB2"].get(reason_code, f"Reason Code: {reason_code}")
            result_parts.append(f"Reason Code: {reason_code} ({reason_desc})")
        
        # Subfield 3: Model Score (3 chars) - optional
        if len(clean_val) >= pos + 3:
            model_score = clean_val[pos:pos+3]
            pos += 3
            result_parts.append(f"Model Score: {model_score}")
        
        # Subfield 4: Model Reason Code (2 chars) - optional
        if len(clean_val) >= pos + 2:
            model_reason = clean_val[pos:pos+2]
            pos += 2
            result_parts.append(f"Model Reason Code: {model_reason}")
        
        # Subfield 5: Reserved for Future Use (2 chars) - optional
        if len(clean_val) >= pos + 2:
            reserved = clean_val[pos:pos+2]
            pos += 2
            if reserved.strip():
                result_parts.append(f"Reserved: {reserved}")
        
        # Any remaining data
        if len(clean_val) > pos:
            remaining = clean_val[pos:]
            if remaining.strip():
                result_parts.append(f"Additional: {remaining}")
        
        return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"

    if se_tag == "76":
        meaning = DE48_VALUE_TABLES["76"].get(clean_val, f"Unknown Electronic Acceptance: {clean_val}")
        return f"{tag_name} -> {meaning}"

    if se_tag == "77":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        meaning = DE48_VALUE_TABLES["77"].get(clean_val[:3], f"Unknown TTI: {clean_val[:3]}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "78":
        if len(clean_val) != 6:
            validation_err = " [Warning: Expected length exactly 6]"
        if len(clean_val) >= 6:
            result_parts = []
            s1 = DE48_VALUE_TABLES["78.SUB1"].get(clean_val[0], f"Unknown Spend: {clean_val[0]}")
            result_parts.append(f"Spend: {s1}")
            s2 = DE48_VALUE_TABLES["78.SUB2"].get(clean_val[1], f"Unknown DCC: {clean_val[1]}")
            if s2 != "Unknown DCC: ":
                result_parts.append(f"DCC: {s2}")
            s3 = DE48_VALUE_TABLES["78.SUB3"].get(clean_val[2], f"Unknown: {clean_val[2]}")
            if s3 != "Unknown: ":
                result_parts.append(f"Deferred: {s3}")
            s4 = DE48_VALUE_TABLES["78.SUB4"].get(clean_val[3], f"Unknown: {clean_val[3]}")
            if s4 != "Unknown: ":
                result_parts.append(f"Checkout: {s4}")
            s5 = DE48_VALUE_TABLES["78.SUB5"].get(clean_val[4], f"Unknown: {clean_val[4]}")
            if s5 != "Unknown: ":
                result_parts.append(f"Reason: {s5}")
            s6 = DE48_VALUE_TABLES["78.SUB6"].get(clean_val[5], f"Unknown: {clean_val[5]}")
            if s6 != "Unknown: ":
                result_parts.append(f"Token: {s6}")
            return f"{tag_name} -> {' | '.join(result_parts)}{validation_err}"
        return f"{tag_name}: `{clean_val}`{validation_err}"

    if se_tag == "79":
        if len(clean_val) >= 5:
            cvr_tvr = clean_val[0]
            byte_id = clean_val[1:3]
            bit_id = clean_val[3:4]
            bit_val = clean_val[4:5] if len(clean_val) >= 5 else ""
            cvr_desc = "CVR" if cvr_tvr == "C" else "TVR" if cvr_tvr == "T" else f"Unknown: {cvr_tvr}"
            return f"{tag_name} -> {cvr_desc} | Byte: {byte_id} | Bit: {bit_id} | Value: {bit_val}"
        return f"{tag_name}: `{clean_val}`"

    if se_tag == "80":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        meaning = DE48_VALUE_TABLES["80"].get(clean_val, "Unknown PIN verification handling configuration")
        return f"{tag_name} -> Action context: {meaning}{validation_err}"

    if se_tag == "82":
        meaning = DE48_VALUE_TABLES["82"].get(clean_val, f"Unknown AVS request code: {clean_val}")
        return f"{tag_name} -> {meaning}"

    if se_tag == "83":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["83"].get(clean_val, f"Unknown AVS response: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "84":
        if len(clean_val) != 2:
            validation_err = " [Warning: Expected length exactly 2]"
        meaning = DE48_VALUE_TABLES["84"].get(clean_val, f"Unknown Merchant Advice Code: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "85":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["85"].get(clean_val, f"Unknown Account Status: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "86":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["86"].get(clean_val, f"Unknown Relationship: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "87":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["87"].get(clean_val, f"Unknown CVC Result: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "88":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["88"].get(clean_val, f"Unknown Compliance Status: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "89":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["89"].get(clean_val, f"Unknown Error Code: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "90":
        if clean_val in DE48_VALUE_TABLES["90"]:
            return f"{tag_name} -> {DE48_VALUE_TABLES['90'][clean_val]}"
        else:
            return f"{tag_name} -> Custom Payment Service: {clean_val}"

    if se_tag == "91":
        return f"{tag_name} -> Reference Data: `{clean_val}`"

    if se_tag == "92":
        if len(clean_val) != 3:
            validation_err = " [Warning: Expected length exactly 3]"
        return f"{tag_name} -> CVC 2 Value: {clean_val}{validation_err}"

    if se_tag == "93":
        return f"{tag_name} -> Fleet Card Data: `{clean_val}`"

    if se_tag == "94":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["94"].get(clean_val, f"Unknown Commercial Card Status: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "95":
        if clean_val in DE48_VALUE_TABLES["95"]:
            return f"{tag_name} -> {DE48_VALUE_TABLES['95'][clean_val]}"
        else:
            return f"{tag_name} -> Promotion Code: {clean_val}"

    if se_tag == "96":
        return f"{tag_name} -> Market-specific Data: `{clean_val}`"

    if se_tag == "97":
        if len(clean_val) != 1:
            validation_err = " [Warning: Expected length exactly 1]"
        meaning = DE48_VALUE_TABLES["97"].get(clean_val, f"Unknown Property Status: {clean_val}")
        return f"{tag_name} -> {meaning}{validation_err}"

    if se_tag == "98":
        return f"{tag_name} -> Driver Number: `{clean_val}`"

    if se_tag == "99":
        return f"{tag_name} -> Vehicle Number: `{clean_val}`"
        
    return f"{tag_name}: `{clean_val}`"


def parse_all_subelements(parsed_data: dict) -> str:
    """
    Parse all DE48 subelements and return them in ascending numeric order.
    
    Args:
        parsed_data: Dictionary with subelement tags as keys and values as values
        
    Returns:
        Formatted string with all subelements in ascending order
    """
    if not parsed_data:
        return "No DE48 subelements present"
    
    result = []
    # Sort by numeric value - convert to int for proper sorting
    # This ensures 01, 32, 37, 42, 43, 61, 66, 71, 77, 92 order
    for tag in sorted(parsed_data.keys(), key=lambda x: int(x) if str(x).isdigit() else 999):
        value = parsed_data[tag]
        decoded = decode_de48_subelement(tag, value)
        # Clean up the decoded string - remove "F48." prefix if present
        if decoded.startswith("F48."):
            decoded = decoded[4:]
        result.append(f"F48.{tag}: {decoded}")
    
    return "\n".join(result)
