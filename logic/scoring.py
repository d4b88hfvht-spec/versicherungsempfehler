def score_produkt(produkt, profil):
    score = 0

    ziel = produkt["zielgruppe"]

    # Beruf passt perfekt
    if ziel["berufe"]:
        if profil["beruf"] in ziel["berufe"]:
            score += 30

    # Alter passt perfekt
    if ziel["alter_min"] is not None and ziel["alter_max"] is not None:
        if ziel["alter_min"] <= profil["alter"] <= ziel["alter_max"]:
            score += 20

    # Leistungsumfang bewerten
    umfang = produkt["leistungsumfang"]
    if umfang == "hoch":
        score += 20
    elif umfang == "mittel":
        score += 10
    elif umfang == "gering":
        score += 5

    # Rente: je näher an der gewünschten Rente, desto besser
    differenz = produkt["max_rente"] - profil["wuensche_rente"]
    if differenz >= 0:
        score += 20
    else:
        score -= 50  # sollte eigentlich schon im Filter rausfallen

    return score


def sortiere_produkte(produkte, profil):
    return sorted(
        produkte,
        key=lambda p: score_produkt(p, profil),
        reverse=True
    )