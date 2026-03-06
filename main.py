import json
from logic.regeln import lade_regeln, pruefe_filter, berechne_score
from logic.frage_engine import frage_benutzer

def lade_produkte():
    with open("data/produkte.json", "r") as f:
        return json.load(f)

def match_produkte(profil, produkte, regeln):
    ergebnisse = []

    for produkt in produkte:
        passed = True
        for regel in regeln["filter"]:
            if not pruefe_filter(regel, produkt, profil):
                passed = False
                break

        if not passed:
            continue

        score = 0
        for regel in regeln["scoring"]:
            score += berechne_score(regel, produkt, profil)

        ergebnisse.append({
            "produkt": produkt,
            "score": score
        })

    ergebnisse.sort(key=lambda x: x["score"], reverse=True)
    return ergebnisse

def main():
    produkte = lade_produkte()
    regeln = lade_regeln()

    print("\nBitte beantworte ein paar Fragen, damit ich passende Produkte finden kann.\n")
    profil = frage_benutzer()

    ergebnisse = match_produkte(profil, produkte, regeln)

    print("\nPassende Produkte:\n")
    for eintrag in ergebnisse:
        p = eintrag["produkt"]
        print(f"- {p['name']} (Score: {eintrag['score']})")

if __name__ == "__main__":
    main()