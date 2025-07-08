def to_float_like(s):
    i = 0
    parte_intera = ""
    parte_decimale = ""
    punto = 0

    while i < len(s):
        c = s[i]
        if c == ".":
            punto = 1
        elif c >= "0" and c <= "9":
            if punto == 0:
                parte_intera = parte_intera + c
            else:
                parte_decimale = parte_decimale + c
        i = i + 1

    intero = 0
    j = 0
    while j < len(parte_intera):
        intero = intero * 10 + (ord(parte_intera[j]) - ord("0"))
        j = j + 1

    decimale = 0
    base = 1
    k = 0
    while k < len(parte_decimale):
        decimale = decimale * 10 + (ord(parte_decimale[k]) - ord("0"))
        base = base * 10
        k = k + 1

    return intero + decimale / base

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
