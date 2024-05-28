import wikipediaapi

USER_AGENT = "WikiTest (info@python-cursus.nl)"
LANGUAGE = "nl"


def read_wiki(titel):
    """Lees een Wikipedia-artikel in."""

    # Initialiseer de Wikipedia client
    wiki = wikipediaapi.Wikipedia(
        user_agent=USER_AGENT,
        language=LANGUAGE,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    # Haal de pagina op, op basis van titel
    page = wiki.page(titel)

    # Controleer of de pagina bestaat
    if not page.exists():
        raise ValueError("Pagina bestaat niet")

    # Geef de tekst terug
    return page.text
