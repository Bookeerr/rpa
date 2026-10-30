"""Validacion por fila; Rocketbot decide si agrega a validos o rechazados."""
from datetime import datetime
from decimal import Decimal
import re
import unicodedata
from uuid import UUID

ISO_DATE = r"^\d{4}-\d{2}-\d{2}$"
UUID_PATTERN = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
REPORT_PATTERN = r"^Reporte_TestFire_\d{8}_\d{6}_[0-9a-fA-F-]{36}\.xlsx$"
MONEY_US = r"^(?P<sign>-)?\$?(?P<number>(?:\d{1,3}(?:,\d{3})+|\d+)\.\d{2})$"


def valid_uuid(value):
    if not re.fullmatch(UUID_PATTERN, str(value)):
        raise ValueError("UUID invalido")
    return str(UUID(value))


def parse_date(value, date_format="iso"):
    patterns = {"iso": (ISO_DATE, "%Y-%m-%d"),
                "testfire_minute": (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", "%Y-%m-%d %H:%M"),
                "testfire": (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{1,6})?$", "%Y-%m-%d %H:%M:%S")}
    if date_format not in patterns:
        raise ValueError("Formato de fecha no configurado")
    pattern, fmt = patterns[date_format]
    if not re.fullmatch(pattern, str(value)):
        raise ValueError("Formato de fecha invalido")
    if "." in value and date_format == "testfire":
        fmt += ".%f"
    return datetime.strptime(value, fmt).date().isoformat()


def parse_money(value):
    value = str(value).strip()
    parens = value.startswith("(") and value.endswith(")")
    if parens:
        value = value[1:-1]
    match = re.fullmatch(MONEY_US, value)
    if not match or (parens and match["sign"]):
        raise ValueError("Importe invalido o ambiguo; se exige formato US con 2 decimales")
    amount = Decimal(match["number"].replace(",", ""))
    if match["sign"] or parens:
        amount = -amount
    if abs(amount) >= Decimal("10000000000000000"):
        raise ValueError("Importe fuera de DECIMAL(18,2)")
    return amount


def normalize_description(value):
    return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()


def validate_row(raw, execution_id, date_format="iso"):
    try:
        valid_uuid(execution_id)
        account = str(raw["account"]).strip()
        if not re.fullmatch(r"\d{1,32}", account):
            raise ValueError("Cuenta invalida")
        description = str(raw["description"])
        if not description.strip():
            raise ValueError("Descripcion vacia")
        row_index = int(raw["row_index"])
        if row_index < 1:
            raise ValueError("Indice invalido")
        normalized = dict(raw)
        normalized.update(execution_id=execution_id, account=account,
                          date=parse_date(raw["date_raw"], date_format),
                          amount=str(parse_money(raw["amount_raw"])),
                          description_norm=normalize_description(description), raw=dict(raw), row_index=row_index)
        normalized.setdefault("currency", None)
        normalized.setdefault("balance", None)
        normalized.setdefault("web_id", None)
        return {"valid": True, "row": normalized, "error": None}
    except (ValueError, TypeError, KeyError) as exc:
        return {"valid": False, "row": dict(raw), "error": str(exc)}
