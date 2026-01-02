# config.py

# Mapa kolorów dla poszczególnych kategorii
COLOR_MAP = {
    "Wydatki<br>Konieczne (NEC)": "#3366CC",
    "Konto Wolności<br>Finansowej (FFA)": "#109618",
    "Oszczędności<br>Długoterminowe (LTSS)": "#FF9900",
    "Edukacja (EDU)": "#990099",
    "Przyjemności (PLAY)": "#DC3912",
    "Pomoc Innym<br>(GIVE)": "#0099C6"
}

# Domyślne wartości procentowe
DEFAULT_PERCENTS = [55.0, 10.0, 10.0, 10.0, 10.0, 5.0]

# Lista kategorii (klucze z mapy kolorów)
CATEGORIES = list(COLOR_MAP.keys())

# Opisy kategorii
DESCRIPTIONS = [
    "Jedzenie, rachunki, czynsz",
    "Inwestycje, pasywny dochód",
    "Wakacje, samochód, dom",
    "Książki, kursy, rozwój",
    "Kino, restauracje, hobby",
    "Charytatywność, prezenty"
]