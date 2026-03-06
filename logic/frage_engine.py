import json

def lade_fragen():
    with open("data/questions.json", "r") as f:
        return json.load(f)

def frage_benutzer():
    fragen = lade_fragen()
    profil = {}

    for f in fragen:
        while True:
            eingabe = input(f"{f['frage']} ")

            if f["typ"] == "zahl":
                try:
                    profil[f["key"]] = int(eingabe)
                    break
                except ValueError:
                    print("Bitte eine gültige Zahl eingeben.")
            else:
                profil[f["key"]] = eingabe.strip()
                break

    return profil