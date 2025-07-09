print("Quesito B:")
print("")


def numero_float(s):
    parte_intera = ""
    parte_decimale = ""
    punto_trovato = False

    # Costruzione delle due parti
    for punto in s:
        if punto == "." and not punto_trovato:
            punto_trovato = True
        elif punto >= "0" and punto <= "9":
            if not punto_trovato:
                parte_intera += punto
            else:
                parte_decimale += punto

    # Crea un dizionario che associa le cifre come stringhe ai loro valori numerici
    cifre = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
        "5": 5, "6": 6, "7": 7, "8": 8, "9": 9
    }

    # Conversione parte intera
    intero = 0
    for converte in parte_intera:
        intero = intero * 10 + cifre[converte]

    # Conversione parte decimale
    decimale = 0
    base = 1
    for converte in parte_decimale:
        decimale = decimale * 10 + cifre[converte]
        base *= 10

    return intero + decimale / base if base > 1 else intero


def leggi_fermate(percorso):
    fermate = {}  # ID -> (x, y)
    nomi = {}  # ID -> nome

    file = open(percorso, "r")
    riga = file.readline()

    while riga != "":
        valori = riga.strip().split(",")
        if len(valori) >= 4:
            idf = valori[0]
            nome = valori[1]
            x_str = valori[2]
            y_str = valori[3]

            x = numero_float(x_str)
            y = numero_float(y_str)

            fermate[idf] = (x, y)
            nomi[idf] = nome

        riga = file.readline()

    file.close()
    return fermate, nomi


def leggi_tempi(percorso, fermate):
    massimo = -1
    id_partenza = ""
    id_arrivo = ""
    tempo_massimo = 0
    distanza_massima = 0

    file_2 = open(percorso, "r")
    riga = file_2.readline()

    while riga != "":
        valori = riga.strip().split(",")
        if len(valori) >= 4:
            id_1 = valori[0]
            id_2 = valori[1]
            t1_str = valori[2]
            t2_str = valori[3]

            t1 = numero_float(t1_str)
            t2 = numero_float(t2_str)
            tempo = t2 - t1

            if id_1 in fermate and id_2 in fermate and tempo > 0:
                x1, y1 = fermate[id_1]
                x2, y2 = fermate[id_2]

                dx = x2 - x1
                dy = y2 - y1

                distanza = (dx * dx + dy * dy) ** 0.5
                rapporto = distanza / tempo

                if rapporto > massimo:
                    massimo = rapporto
                    id_partenza = id_1
                    id_arrivo = id_2
                    tempo_massimo = tempo
                    distanza_massima = distanza

        riga = file_2.readline()

    file_2.close()
    return id_partenza, id_arrivo, tempo_massimo, distanza_massima, massimo


def main():
    percorso_fermate = "/Users/martaristori/Desktop/Anna/network_nodes.csv"
    percorso_tempi = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"

    fermate, nomi = leggi_fermate(percorso_fermate)
    id_partenza, id_arrivo, tempo, distanza, rapporto = leggi_tempi(percorso_tempi, fermate)

    print("Coppia di fermate consecutive con il rapporto distanza/tempo più alto:")
    print("Da", id_partenza, "a", id_arrivo)


# Esegui
main()
