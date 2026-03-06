import json

def lade_regeln():
    with open("data/regeln.json", "r") as f:
        return json.load(f)


def hole_wert(objekt, feldpfad):
    teile = feldpfad.split(".")
    wert = objekt
    for t in teile:
        if not isinstance(wert, dict):
            return None
        wert = wert.get(t)
        if wert is None:
            return None
    return wert


def pruefe_filter(regel, produkt, profil):
    typ = regel["typ"]
    user_wert = profil.get(regel["user_feld"])

    # Produktwert aus Root oder matching lesen
    if regel["produkt_feld"] in produkt:
        produkt_wert = produkt.get(regel["produkt_feld"])
    else:
        produkt_wert = hole_wert(produkt["matching"], regel["produkt_feld"])

    # Schicht
    if typ == "schicht_match":
        if user_wert == "egal":
            return True
        return produkt_wert == user_wert

    # Typ
    if typ == "typ_match":
        if user_wert == "egal":
            return True
        return produkt_wert == user_wert

    # Beruf muss in Liste sein
    if typ == "beruf_in_liste":
        if produkt_wert is None:
            return True
        return user_wert in produkt_wert

    # Beruf darf nicht in Liste sein
    if typ == "beruf_nicht":
        if produkt_wert is None:
            return True
        return user_wert not in produkt_wert

    # Mindestalter
    if typ == "alter_min":
        if produkt_wert is None:
            return True
        return user_wert >= produkt_wert

    # Höchstalter
    if typ == "alter_max":
        if produkt_wert is None:
            return True
        return user_wert <= produkt_wert

    # Maximale Rente
    if typ == "max_rente":
        if produkt_wert is None:
            return True
        return user_wert <= produkt_wert

    return True


def berechne_score(regel, produkt, profil):
    typ = regel["typ"]
    user_wert = profil.get(regel.get("user_feld"))

    # Produktwert aus Root oder matching lesen
    if regel["produkt_feld"] in produkt:
        produkt_wert = produkt.get(regel["produkt_feld"])
    else:
        produkt_wert = hole_wert(produkt["matching"], regel["produkt_feld"])

    # Beruf-Bonus
    if typ == "beruf_match":
        if produkt_wert and user_wert in produkt_wert:
            return regel["punkte"]

    # Schicht-Bonus
    if typ == "schicht_bonus":
        if user_wert != "egal" and produkt_wert == user_wert:
            return regel["punkte"]

    # Typ-Bonus
    if typ == "typ_bonus":
        if user_wert != "egal" and produkt_wert == user_wert:
            return regel["punkte"]

    return 0