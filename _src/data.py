# -*- coding: utf-8 -*-
"""JA-HO — jedyne źródło prawdy dla treści strony (polski).

Materiał źródłowy:
  * ja-ho.pl (stara strona, 2011–2015) — historia firmy, motto, dane kontaktowe
  * Praca/Jaho/ja-ho.pl/_build/data.py — struktura kategorii, klienci, kolejność zdjęć
  * jahopl/img — 224 zdjęcia z realizacji w 10 kategoriach
  * logojaho.jpg — paleta marki (miedź / czerwień ceglana / grafit), „EST. 1999”

Zmieniasz telefon, adres albo opis kategorii? Tylko tutaj.
"""

COMPANY = {
    "name": "JA-HO",
    "legal": "F.R.B. „JA-HO”",
    "descriptor": "Firma remontowo-budowlana",
    "slogan": "Budujemy to… najlepiej.",
    "person": "inż. Mirosław Gieracz",
    "role": "Dyrektor generalny",
    "mobile": "695 225 505",
    "mobile_href": "+48695225505",
    "phone": "81 740 54 66",
    "phone_href": "+48817405466",
    "email": "miroslawgieracz@o2.pl",
    "street": "ul. Żołnierska 7",
    "postcode": "20-081 Lublin",
    "region": "województwo lubelskie",
    "founded": 1999,
    "years": 27,
    "domain": "https://ja-ho.pl",
    "motto": "Klient jest zadowolony — horyzont „JA-HO” poszerzony.",
}

NAV = [
    ("index.html", "Start"),
    ("services.html", "Oferta"),
    ("projects.html", "Realizacje"),
    ("about.html", "O nas"),
    ("contact.html", "Kontakt"),
]

# Stali klienci firmy. Logotypy leżą w assets/img/partnerzy/mono (białe wersje;
# CSS odwraca je na jasnym tle) — patrz komentarz w client_marquee().
CLIENTS = [
    dict(file="pekao",   name="Bank Pekao S.A.",                sector="sektor bankowy",     h=34, w=231),
    dict(file="zywiec",  name="Grupa Żywiec S.A.",              sector="branża spożywcza",   h=50, w=88),
    dict(file="perla",   name="Perła – Browary Lubelskie S.A.", sector="branża piwowarska",  h=44, w=91),
    dict(file="orzel",   name="Orzeł S.A.",                     sector="branża motoryzacyjna", h=50, w=101),
    dict(file="mazda",   name="Mazda",                          sector="branża motoryzacyjna", h=54, w=53),
    dict(file="citroen", name="Citroën Polska",                 sector="branża motoryzacyjna", h=54, w=56),
]

# Filar 1 — stolarka budowlana.
JOINERY = [
    ("Doradztwo", "Doradztwo w doborze okien, drzwi i bram garażowych — współczynniki "
                  "przenikania ciepła, profile, okucia i szyby dobrane do budynku."),
    ("Parapety i osłony", "Pomoc w wyborze parapetów, żaluzji czy rolet — wewnętrznych "
                          "i zewnętrznych, ręcznych albo sterowanych elektrycznie."),
    ("Terminy", "Ustalenie terminu dostawy oraz wszystkich szczegółów prac montażowych, "
                "zanim cokolwiek pojawi się na budowie."),
    ("Montaż", "Montaż stolarki budowlanej — ciepły montaż, uszczelnienie, regulacja "
               "i wykończenie ościeży."),
]

# Filar 2 — usługi remontowo-budowlane. Zakres przeniesiony 1:1 ze starej
# oferty; podział na branże zachowany.
SERVICES = [
    dict(
        id="wycena",
        name="Wycena",
        lead="Każda robota zaczyna się od wizyty, nie od cennika.",
        items=[
            "Oględziny i szczegółowe pomiary",
            "Wycena wstępna z jasno spisanym zakresem prac",
            "Transport materiałów na plac budowy",
        ],
    ),
    dict(
        id="murarskie",
        name="Prace murarsko-tynkarskie",
        lead="Konstrukcja, przegrody i wszystko, co ma być proste i suche.",
        items=[
            "Docieplenia budynków",
            "Tynki akrylowe i mineralne",
            "Tynki maszynowe cementowo-wapienne lub gipsowe",
            "Tynkowanie tradycyjne",
            "Murowanie z cegły, ytongu i porothermu",
            "Wylewki samopoziomujące i tradycyjne",
            "Montaż okien oraz drzwi",
            "Skuwanie tynku, wyburzanie i usunięcie gruzu po rozbiórkach",
        ],
    ),
    dict(
        id="glazura",
        name="Układanie glazury",
        lead="Ceramika ułożona tak, żeby światło nie wytknęło ani jednej fugi.",
        items=[
            "Kafelkowanie ścian i podłóg",
            "Glazura i terakota prosto albo w karo",
            "Ułożenie gresu",
            "Ułożenie dekorów i listew",
            "Skuwanie starej glazury",
        ],
    ),
    dict(
        id="malarskie",
        name="Prace malarskie",
        lead="Wnętrza, elewacje i ochrona drewna.",
        items=[
            "Malowanie ścian wewnętrznych",
            "Malowanie drzwi",
            "Malowanie elewacji budynków",
            "Impregnacja drewna",
        ],
    ),
    dict(
        id="gipsowe",
        name="Technologie gipsowe",
        lead="Sucha zabudowa — sufity, ścianki, obudowy, ocieplenia.",
        items=[
            "Wykonanie gładzi gipsowych",
            "Sufity podwieszane z płyt k.g.",
            "Ścianki działowe z płyt k.g. z wygłuszeniem wełną mineralną",
            "Montaż płyt gipsowych na klej",
            "Docieplanie poddasza (wełna + folia) z płytą k.g. na stelażu",
            "Montaż płyt k.g. na stelażu z ociepleniem styropianem lub wełną",
            "Zabudowy z płyt k.g.",
        ],
    ),
    dict(
        id="stolarskie",
        name="Prace stolarsko-okładzinowe",
        lead="Panele położone szybko i czysto.",
        items=[
            "Montaż paneli podłogowych",
            "Montaż paneli ściennych",
        ],
    ),
    dict(
        id="instalacje",
        name="Wykonywanie instalacji",
        lead="Instalacje skoordynowane z pracami wykończeniowymi.",
        items=[
            "Instalacje elektryczne",
            "Instalacje sanitarne",
            "Instalacje grzewcze",
        ],
    ),
]

# Jak przebiega realizacja, od telefonu do odbioru.
PROCESS = [
    ("Kontakt", "Zadzwoń albo napisz. Odpowiadamy na każde zapytanie w ciągu "
                "24 godzin i umawiamy wizytę w dogodnym dla Ciebie terminie."),
    ("Oględziny i wycena", "Dokonujemy oględzin, pomiarów i przygotowujemy wycenę "
                           "wstępną z jasno spisanym zakresem prac."),
    ("Termin i materiały", "Ustalamy termin rozpoczęcia, zamawiamy materiały "
                           "i organizujemy transport na plac budowy."),
    ("Realizacja i odbiór", "Prace idą pod stałym nadzorem i w stałym kontakcie "
                            "z klientem, więc usterki rozwiązujemy na bieżąco — "
                            "a nie po odbiorze."),
]

# slug -> kategoria realizacji. `order` ustawia najlepsze ujęcia na początku
# galerii; pozostałe zdjęcia generator dokleja numerycznie.
CATEGORIES = [
    dict(slug="jednorodzinne", name="Budownictwo jednorodzinne", short="Domy",
         count=40, cover=2,
         order=[2, 6, 5, 1, 30, 27, 26, 19, 23, 17, 24, 3, 11, 20, 21, 7, 8, 22, 31, 33],
         desc="Domy w stanie surowym i pod klucz — elewacje, dachy, tynki, gładzie, "
              "sufity podwieszane, schody, kominki i pełne wykończenie wnętrz."),
    dict(slug="wielorodzinne", name="Budownictwo wielorodzinne", short="Bloki",
         count=9, cover=9,
         order=[9, 5, 2, 7, 3, 8, 1, 4, 6],
         desc="Bloki mieszkalne i apartamentowce — elewacje, balkony, klatki schodowe "
              "oraz wykończenia poszczególnych lokali."),
    dict(slug="hale", name="Hale i magazyny", short="Hale",
         count=60, cover=27,
         order=[27, 26, 21, 22, 24, 6, 25, 10, 11, 60, 8, 41, 39, 38, 45, 58],
         desc="Obiekty przemysłowe i magazynowe — konstrukcje, elewacje, dachy, "
              "świetliki dachowe, posadzki i instalacje."),
    dict(slug="zabytki", name="Zabytki", short="Zabytki",
         count=44, cover=23,
         order=[23, 12, 33, 17, 13, 19, 1, 20, 24, 25, 27, 32, 36, 37, 18, 38, 39, 43],
         desc="Prace przy obiektach objętych ochroną konserwatorską — renowacja "
              "stolarki okiennej, witraży, maswerków i elewacji ceglanych."),
    dict(slug="banki", name="Banki", short="Banki",
         count=12, cover=10,
         order=[10, 6, 5, 12, 9, 3, 11, 4, 1, 2, 7, 8],
         desc="Aranżacje i remonty placówek bankowych realizowane w standardzie "
              "i kolorystyce sieci."),
    dict(slug="biura", name="Biura", short="Biura",
         count=17, cover=1,
         order=[1, 11, 10, 13, 3, 4, 5, 12, 16, 2],
         desc="Remonty i wykończenia powierzchni biurowych — gładzie, sufity, "
              "posadzki, instalacje i węzły sanitarne."),
    dict(slug="uzytecznosc", name="Użyteczność publiczna", short="Publiczne",
         count=7, cover=2,
         order=[2, 1, 5, 4, 6, 3, 7],
         desc="Szkoły i budynki użyteczności publicznej — termomodernizacje, "
              "elewacje, wymiana stolarki."),
    dict(slug="stolarka", name="Stolarka budowlana", short="Stolarka",
         count=7, cover=5,
         order=[5, 1, 7, 4, 3, 2, 6],
         desc="Dobór, dostawa i montaż okien, drzwi, bram garażowych, parapetów, "
              "żaluzji i rolet."),
    dict(slug="ogrodzenia", name="Ogrodzenia", short="Ogrodzenia",
         count=8, cover=4,
         order=[4, 3, 5, 1, 7, 6, 2, 8],
         desc="Ogrodzenia murowane i stalowe wraz z podmurówkami, słupami i bramami."),
    dict(slug="pozostale", name="Pozostałe realizacje", short="Pozostałe",
         count=20, cover=19,
         order=[19, 18, 20, 1, 17, 16, 13, 15, 12, 10, 11, 9, 6, 5, 4, 3, 2, 14, 7, 8],
         desc="Konstrukcje drewniane, wiaty, altany, domki gospodarcze i drobne "
              "obiekty przydomowe."),
]

SPONSORSHIP = dict(
    slug="sponsoring", count=6, order=[1, 2, 3, 4, 5, 6],
    title="Sponsorujemy lubelski sport",
    desc="JA-HO jest sponsorem sekcji rugby Budowlani Lublin. Budowanie regionu to "
         "coś więcej niż stawianie ścian — to także wsparcie dla tych, którzy grają "
         "w jego barwach.",
)

# Dofinansowanie z FUS, przeniesione ze starej strony.
FUNDING = dict(
    title="Dofinansowano ze środków Funduszu Ubezpieczeń Społecznych",
    lead="Projekt dotyczący utrzymania zdolności do pracy przez cały okres "
         "aktywności zawodowej.",
    body="Projekt dofinansowany ze środków Funduszu Ubezpieczeń Społecznych, "
         "dotyczący poprawy warunków BHP i bezpieczeństwa pracy naszych "
         "pracowników poprzez zakup profesjonalnego sprzętu budowlanego.",
    project="Poprawa BHP w firmie F.R.B. Honorata Pędzisz",
    grant="149 511,48 zł",
    grant_label="kwota dofinansowania",
    total="186 889,35 zł",
    total_label="całkowita wartość inwestycji",
)

# Kamienie milowe na oś czasu na stronie „O nas”.
TIMELINE = [
    ("1999", "Powstanie firmy",
     "F.R.B. „JA-HO” powstaje w czerwcu 1999 roku jako działalność "
     "handlowo-usługowa. Podstawą działalności jest sprzedaż i montaż stolarki "
     "budowlanej."),
    ("2004", "Przejście na profil usługowy",
     "W lipcu 2004 roku, po wejściu Polski do Unii Europejskiej, zmieniamy "
     "siedzibę i profil działalności firmy na wyłącznie usługowy. Głównym "
     "zajęciem stają się remonty mieszkań, biur oraz wykończenia wnętrz."),
    ("Dziś", "Dwa filary, jeden region",
     "Usługi remontowo-budowlane uzupełnione o sprzedaż i montaż stolarki "
     "budowlanej — na terenie Lublina i całego województwa lubelskiego."),
]

STATS = [
    ("27", "", "lat na rynku", "Nieprzerwanie od czerwca 1999 roku."),
    ("224", "", "udokumentowane zdjęcia", "Każde zrobione na budowie JA-HO."),
    ("10", "", "kategorie realizacji", "Od domów jednorodzinnych po zabytkowe elewacje."),
    ("6", "", "stałych klientów", "Firmy, dla których pracujemy wielokrotnie."),
]

FAQ = [
    ("Na jakim terenie pracujecie?",
     "Działamy na terenie całego województwa lubelskiego, a Lublin i okoliczne "
     "powiaty to nasz teren macierzysty. Przy większych kontraktach jeździmy "
     "dalej — zapytaj, a powiemy wprost, czy logistyka ma sens."),
    ("Jak dostać wycenę?",
     "Zadzwoń pod 695 225 505 albo wyślij zapytanie. Umawiamy wizytę na miejscu, "
     "robimy pomiary i przygotowujemy wycenę wstępną z pisemnym zakresem prac. "
     "Oględziny i wycena nic nie kosztują."),
    ("Robicie i stolarkę, i prace budowlane?",
     "Tak — na tym polegają dwa filary. Możemy dostarczyć i zamontować okna, "
     "drzwi czy bramy garażowe, a wokół nich wykonać prace murarskie, tynkarskie, "
     "gipsowe, glazurnicze, malarskie i instalacyjne. Jeden kontakt, jeden "
     "harmonogram, żadnego zrzucania winy między ekipami."),
    ("Bierzecie prace przy zabytkach?",
     "Bierzemy. Renowacja stolarki okiennej, witraży, maswerków i elewacji "
     "ceglanych w obiektach pod ochroną konserwatorską to jedna z naszych "
     "największych kategorii realizacji."),
    ("Czy kupujecie materiały?",
     "Możemy. Transport materiałów na plac budowy jest częścią naszego "
     "standardowego zakresu, doradzimy też przy doborze. Jeśli wolisz kupić "
     "materiały samodzielnie — też nie ma problemu."),
    ("Jak szybko odpowiadacie?",
     "W ciągu 24 godzin od zapytania, w każdy dzień roboczy."),
]
