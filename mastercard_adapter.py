"""
mastercard_adapter.py
=======================
Shared adapter layer between the raw mastercard_iso8583_parser.py engine
and any front end (Flask web app, CLI, etc).

This module contains ONLY presentation-adjacent glue code. It does not
reimplement any ISO 8583 / Mastercard DMS parsing logic - every actual
decode step is delegated to mastercard_iso8583_parser.py, unmodified:
    - clean_hex()
    - parse_header()
    - parse_all_bitmaps()
    - parse_message_full()
    - get_report_name()
    - write_txt_report()
    - write_xlsx_report()
    - write_detail_report()

Kept dependency-free of any UI toolkit so it can be safely imported from
a headless server process.

Mirrors visa_adapter.py's shape, with the structural differences the
Mastercard parser actually has:
    - No proprietary header block (H1-H14) - the message is just
      MTI + bitmap(s) + fields, so there is no MSG_HEADER section and
      no reject-message (H13/H14) warning to surface.
    - parse_header() returns a position that is ALREADY past the 4-char
      MTI (unlike the Visa parser, where the header and MTI are two
      separate steps) - so the bitmap starts at that position directly,
      with no "+2" offset needed.
"""

import re

# -- the untouched parser engine ---------------------------------------------
import mastercard_iso8583_parser as mc_parser

try:
    import openpyxl  # noqa: F401  (used internally by mc_parser.write_xlsx_report)
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# mastercard_field_details.py backs mc_parser's write_detail_report()/
# get_value_detail(). Imported here (not just re-used via mc_parser) so
# we can check *which* fields have a value-detail lookup available, to
# flag them in the UI.
try:
    import mastercard_field_details as _field_details
    HAS_FIELD_DETAILS = True
except ImportError:
    _field_details = None
    HAS_FIELD_DETAILS = False


def _label_has_detail(label: str) -> bool:
    """True if mastercard_field_details.py has a value-meaning lookup for
    this compact-format label (e.g. 'F39', 'F3.1', 'F48.61')."""
    if not HAS_FIELD_DETAILS:
        return False
    return (
        label in _field_details.DETAIL_FUNCS
        or label in _field_details._DIRECT_LOOKUP_LABELS
        or label in _field_details.VALUE_TABLES
        or label in _field_details.FIELD_GLOSSARY
    )


FIELD_KEY_RE = re.compile(r"^F(\d+)")


# ═══════════════════════════════════════════════════════════════════════════
# ── ADAPTER LAYER: turn mc_parser's (compact, rows) into the dict shape ────
# ── this GUI renders, and clean up noisy pasted/log input before handing ──
# ── it to the parser.                                                    ──
# ═══════════════════════════════════════════════════════════════════════════

def _prepare_hex_input(raw: str) -> str:
    """
    Strip common log-fragment noise (timestamps, 'inp>>'/'out<<' style
    direction markers, comment lines) so users can paste a raw hex string
    OR a log excerpt. The result is still handed to mc_parser.clean_hex()
    (unchanged) for the actual hex validation/decoding - this function
    only removes obviously non-hex noise beforehand.
    """
    cleaned_lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r"\d{2}[./]\d{2}[./]\d{4}", line):
            continue
        if line.lower().startswith(("inp>>", "out<<", "tx:", "rx:", "in:", "out:")):
            continue
        if line.startswith("#"):
            continue
        cleaned_lines.append(line)
    joined = " ".join(cleaned_lines) if cleaned_lines else raw
    hex_only = re.sub(r"[^0-9a-fA-F]", "", joined)
    return hex_only


def _group_field_rows(rows):
    """
    Group the parser's flat (label, description, raw_hex, value) rows by
    top-level field number. Composite fields (3/43/48/55/90/122) already
    come back from the parser as multiple rows sharing the same field
    number but distinct labels (e.g. 'F48.61', 'F48.87', ...) - those are
    grouped together here for display. There is no header/H-prefixed
    section for Mastercard (see module docstring).
    """
    mti_row = None
    fields = {}  # fnum -> {"desc": str, "items": [(label, value), ...]}
    for label, desc, raw_hex, value in rows:
        if label == "MTI":
            mti_row = (label, desc, raw_hex, value)
        else:
            m = re.match(r"^F(\d+)", label)
            if not m:
                continue
            fnum = int(m.group(1))
            entry = fields.setdefault(fnum, {"desc": None, "items": []})
            entry["desc"] = desc.split(" - ", 1)[0]
            entry["items"].append((label, value))
    return mti_row, fields


def _bitmap_summary(data: bytes, pos: int):
    """
    Read the primary/secondary bitmap bytes for display purposes, and
    reuse mc_parser.parse_all_bitmaps() (unchanged) to get the actual
    list of present field numbers - no bitmap-walking logic is
    reimplemented here.
    """
    primary_bytes = data[pos:pos + 8]
    has_secondary = bool(primary_bytes and (primary_bytes[0] & 0x80))
    secondary_bytes = data[pos + 8:pos + 16] if has_secondary else b""
    present, _end_pos = mc_parser.parse_all_bitmaps(data, pos)
    return (
        primary_bytes.hex().upper(),
        secondary_bytes.hex().upper() if secondary_bytes else "",
        sorted(present.keys()),
    )


def decode_mastercard_message(raw_msg: str):
    """
    Adapter around mc_parser.parse_message_full(). Returns
    (result_dict, warnings_list, compact_string) - the same three-value
    shape the front end expects.
    On any failure, returns ({"error": "..."}, [], "").
    """
    hex_str = _prepare_hex_input(raw_msg)
    if not hex_str.strip():
        return {"error": "No hex characters found in input."}, [], ""

    try:
        data = mc_parser.clean_hex(hex_str)
    except Exception as e:
        return {"error": str(e)}, [], ""

    if len(data) < 4:
        return {"error": "Message too short (< 4 bytes) to contain an MTI"}, [], ""

    try:
        compact, rows = mc_parser.parse_message_full(hex_str)
    except Exception as e:
        return {"error": f"Parser error: {e}"}, [], ""

    mti_row, fields = _group_field_rows(rows)
    result = {}
    warnings = []

    if mti_row:
        _label, _desc, _raw, mti_val = mti_row
        detail = _field_details.get_value_detail("MTI", mti_val) if HAS_FIELD_DETAILS else ""
        result["MTI"] = {
            "Code": mti_val,
            "Description": detail or "Mastercard DMS Message",
        }

    try:
        header, hpos = mc_parser.parse_header(data)
        # mc_parser.parse_header() already returns a position PAST the
        # 4-char MTI (unlike the Visa parser), so the bitmap starts here
        # directly - no additional offset needed.
        primary_hex, secondary_hex, fields_present = _bitmap_summary(data, hpos)
        result["BITMAP"] = {
            "Primary (hex)": primary_hex,
            "Secondary (hex)": secondary_hex if secondary_hex else "— not present",
            "Fields present": fields_present,
        }
    except Exception as e:
        warnings.append(f"⚠ Could not summarize bitmap for display: {e}")

    fields_out = {}
    fields_with_detail = []
    parse_errors = {}
    for fnum in sorted(fields):
        entry = fields[fnum]
        key = f"F{fnum}  {entry['desc']}"
        items = entry["items"]
        if any(_label_has_detail(label) for label, _val in items):
            fields_with_detail.append(key)
        if len(items) == 1 and items[0][0] == f"F{fnum}":
            val = items[0][1]
            fields_out[key] = {"Value": val}
        else:
            fields_out[key] = {label: val for label, val in items}
        for label, val in items:
            if isinstance(val, str) and val.startswith("<parse-error:"):
                parse_errors[label] = val
    result["FIELDS"] = fields_out
    if fields_with_detail:
        # Field keys (same strings used as FIELDS' top-level keys) for
        # which mastercard_field_details.py has a value-meaning lookup.
        # The front end uses this to show an "ℹ details in export"
        # marker rather than duplicating the lookup text inline.
        result["FIELDS_WITH_DETAIL"] = fields_with_detail

    if parse_errors:
        result["PARSE_ERRORS"] = parse_errors
        for k, v in parse_errors.items():
            warnings.append(f"🔴 {k}: {v}")

    return result, warnings, compact


def _first_val(v):
    if isinstance(v, dict):
        for val in v.values():
            if val:
                return str(val)
        return ""
    return str(v) if v else ""


def _fields_by_num(fields):
    out = {}
    for k, v in fields.items():
        m = FIELD_KEY_RE.match(k)
        if m:
            out[int(m.group(1))] = v
    return out


def _extract_rrn(result):
    fields = result.get("FIELDS", {})
    by_num = _fields_by_num(fields)
    val = _first_val(by_num.get(37)) if 37 in by_num else ""
    if val.strip():
        return val.strip()
    val = _first_val(by_num.get(11)) if 11 in by_num else ""
    return val.strip() or "UNKNOWN"


def _extract_mti(result):
    m = result.get("MTI", {})
    if isinstance(m, dict):
        return m.get("Code", "UNK")
    return str(m)[:4]
