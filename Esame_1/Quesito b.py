def to_float_like(s):
    parte_intera = ""
    parte_decimale = ""
    punto_trovato = False

    # Costruzione delle due parti
    for c in s:
        if c == "." and not punto_trovato:
            punto_trovato = True
        elif c >= "0" and c <= "9":
            if not punto_trovato:
                parte_intera += c
            else:
                parte_decimale += c

    # Mappa da cifra-carattere a numero
    cifre = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
        "5": 5, "6": 6, "7": 7, "8": 8, "9": 9
    }

    # Conversione parte intera
    intero = 0
    for c in parte_intera:
        intero = intero * 10 + cifre[c]

    # Conversione parte decimale
    decimale = 0
    base = 1
    for c in parte_decimale:
        decimale = decimale * 10 + cifre[c]
        base *= 10

    return intero + decimale / base if base > 1 else intero

# Leggi fermate da network_nodes.csv
fermate = {}  # ID -> (x, y)
nomi = {}     # ID -> nome

f = open("/Users/martaristori/Desktop/Anna/network_nodes.csv", "r")
riga = f.readline()

while riga != "":
    valori = riga.strip().split(",")
    if len(valori) >= 4:
        idf = valori[0]
        nome = valori[1]
        x_str = valori[2]
        y_str = valori[3]

        x = to_float_like(x_str)
        y = to_float_like(y_str)

        fermate[idf] = (x, y)
        nomi[idf] = nome

    riga = f.readline()

f.close()

# Inizializza il massimo
massimo = -1
id_partenza = ""
id_arrivo = ""
tempo_massimo = 0

f2 = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
riga = f2.readline()

while riga != "":
    valori = riga.strip().split(",")
    if len(valori) >= 4:
        id1 = valori[0]
        id2 = valori[1]
        t1_str = valori[2]
        t2_str = valori[3]

        t1 = to_float_like(t1_str)
        t2 = to_float_like(t2_str)

        tempo = t2 - t1

        if id1 in fermate and id2 in fermate and tempo > 0:
            x1, y1 = fermate[id1]
            x2, y2 = fermate[id2]

            dx = x2 - x1
            dy = y2 - y1

            distanza = (dx * dx + dy * dy) ** 0.5

            rapporto = distanza / tempo

            if rapporto > massimo:
                massimo = rapporto
                id_partenza = id1
                id_arrivo = id2
                tempo_massimo = tempo
                distanza_massima = distanza

    riga = f2.readline()

f2.close()

# Stampa finale
print("Coppia di fermate consecutive con il rapporto distanza/tempo più alto:")
print("Da ", id_partenza, " a ", id_arrivo)
