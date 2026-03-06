def produkt_passt(produkt, profil):
    ziel = produkt["zielgruppe"]

    # Beruf prüfen (falls Zielgruppe Berufe definiert)
    if ziel["berufe"]:
        if profil["beruf"] not in ziel["berufe"]:
            return False

    # Alter prüfen (falls min/max definiert)
    if ziel["alter_min"] is not None:
        if profil["alter"] < ziel["alter_min"]:
            return False

    if ziel["alter_max"] is not None:
        if profil["alter"] > ziel["alter_max"]:
            return False

    # Rente prüfen
    if profil["wuensche_rente"] > produkt["max_rente"]:
        return False

    return True


def filter_produkte(produkte, profil):
    return [p for p in produkte if produkt_passt(p, profil)]