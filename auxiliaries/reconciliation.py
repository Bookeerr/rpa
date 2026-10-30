"""Emparejamiento determinista con multiplicidad; clasificacion visible en Studio."""
from collections import Counter, defaultdict
from decimal import Decimal


def key(row):
    if row.get("web_id"):
        return ("id", row["account"], str(row["web_id"]))
    return ("values", row["account"], row["date"], row["amount"], row["description_norm"], row.get("currency"))


def plan_pairs(web, master, rules):
    """Devuelve pares/diferencias. Studio recorre pares y llama classify_pair.

    IDs repetidos son ambiguos. Sin ID se empareja por ocurrencia y se conserva
    cada fila; si las multiplicidades difieren se marca el grupo ambiguo.
    """
    buckets = [defaultdict(list), defaultdict(list)]
    for rows, grouped in zip((web, master), buckets):
        for row in rows:
            account = row["account"]
            if account not in rules or not rules[account]["enabled"]:
                raise ValueError("Cuenta sin regla habilitada: " + account)
            grouped[key(row)].append(row)
    pairs = []
    for k in sorted(set(buckets[0]) | set(buckets[1]), key=str):
        left, right = buckets[0][k], buckets[1][k]
        ambiguous = (k[0] == "id" and max(len(left), len(right)) > 1) or (
            k[0] == "values" and max(len(left), len(right)) > 1 and len(left) != len(right))
        for i in range(max(len(left), len(right))):
            w = left[i] if i < len(left) else None
            m = right[i] if i < len(right) else None
            differences = []
            if w and m:
                for field in ("date", "description_norm", "currency"):
                    if w.get(field) != m.get(field):
                        differences.append(field)
                tolerance = Decimal(str(rules[w["account"]]["tolerance"]))
                if tolerance < 0:
                    raise ValueError("Tolerancia negativa")
                if abs(Decimal(w["amount"]) - Decimal(m["amount"])) > tolerance:
                    differences.append("amount")
            pairs.append({"web": w, "master": m, "ambiguous": ambiguous,
                          "differences": differences, "occurrence": i + 1})
    return pairs


def classify_pair(pair):
    if pair["ambiguous"]:
        return "AMBIGUO"
    if pair["web"] is None:
        return "SOLO_MASTER"
    if pair["master"] is None:
        return "SOLO_WEB"
    return "DISCREPANCIA" if pair["differences"] else "CONCILIADO"


def counts(results):
    return dict(Counter(r["status"] for r in results))
