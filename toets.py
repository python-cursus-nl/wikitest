import json

from openai import OpenAI, OpenAIError
from wiki import read_wiki

MODEL = "gpt-4o"


def create_test(text):
    """
    Gebruik OpenAI om de opgegeven tekst samen te vatten en er een toets over te maken.
    """
    client = OpenAI()

    # Bereid de instructies voor
    # Zorg ervoor dat het model JSON teruggeeft
    system_message = {
        "role": "system",
        "content": """
            Je bent een assistent die Wikipediapagina's samenvat en vragen bedenkt voor 
            studenten om hun kennis te toetsen. Je reageert altijd in JSON.
            """
    }

    # Zorg ook voor een voorbeeld van hoe de JSON eruit moet zien.
    # Er zijn geen garanties dat het model zich hier aan houdt, maar
    # in de praktijk gaat het 99% van de tijd wel goed.
    user_prompt = """
        Lees de tekst die hierna volgt\n. 
        Maak een samenvatting van de tekst in maximaal drie zinnen\n.
        Maak drie meerkeuzevragen met opties A, B en C over het onderwerp. 
        Er kan steeds 1 antwoord goed zijn\n.
        Geef van elke vraag aan wat het goede antwoord is (A, B of C)\n.
        Gebruik het volgende JSON-schema: \n\n
            
        {
            "samenvatting": "De samenvatting",
            "vragen: [
                {
                    "vraag": "De eerste vraag",
                    "opties: ["A: Optie A", "B: Optie B", "C: Optie C"],
                    "antwoord": A
                },
                {
                    "vraag": "De tweede vraag",
                    "opties: ["A: Optie A", "B: Optie B", "C: Optie C"],
                    "antwoord": B
                },                
            ]
        }
            
        De tekst is als volgt:\n\n
        """

    user_message = {
        "role": "user",
        "content": user_prompt + text

    }

    # Haal de response op
    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[system_message, user_message]
        )
    except OpenAIError:
        raise

    return response.choices[0].message.content


def take_test():
    """Functie die de samenvatting presenteert en de toets afneemt."""

    print("Over welke Wikipediapagina wil je een toets maken?")
    print("Geef de titel op (haal dit uit de url, na '/wiki/'")
    titel = input("Titel: ")

    # Lees de Wikipedia-pagina in
    try:
        text = read_wiki(titel=titel)
    except ValueError as e:
        print(e)
        exit()  # Stop het programma als de pagina niet gevonden kan worden.

    # Maak de samenvatting en toets
    try:
        result = create_test(text=text)
    except OpenAIError as e:
        print(e)
        exit()  # Stop het programma als er een fout optreedt in de API

    # Zet om van JSON naar dict
    try:
        result_json = json.loads(result)
        samenvatting = result_json.get("samenvatting")
        vragen = result_json.get("vragen")
    except KeyError as e:
        print(e)
        exit()

    # Toon samenvatting
    print("\nSAMENVATTING")
    print(samenvatting)
    print()

    # Begin de toets. Elke vraag bestaat uit een `dict` met vraag,
    # opties en correct antwoord.
    print("TOETS")
    for vraag in vragen:
        print(f"Vraag: {vraag['vraag']}\n")
        for optie in vraag["opties"]:
            print(optie)

        user_antwoord = input("Wat is je antwoord (A, B of C)? ")
        if user_antwoord.upper() == vraag["antwoord"]:
            print("Goed!\n")
        else:
            print(f"Helaas, het goede antwoord is {vraag['antwoord']}\n")
