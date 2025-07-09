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


def leggi_fermate(nodes):
    fermate = {}  # ID -> (x, y)
    nomi = {}  # ID -> nome

    file = open(nodes, "r")
    riga = file.readline()

    while riga != "":
        estrai = riga.strip().split(",")
        if len(estrai) >= 4:
            id = estrai[0]
            nome = estrai[3]
            latitudine = estrai[1]
            longitudine = estrai[2]

            lat = numero_float(latitudine)
            lon = numero_float(longitudine)

            fermate[id] = (lat, lon)
            nomi[id] = nome

        riga = file.readline()

    file.close()
    return fermate, nomi


def leggi_tempi(temporal_day, fermate):
    massimo = -1
    id_partenza = ""
    id_arrivo = ""
    tempo_massimo = 0
    distanza_massima = 0

    file = open(temporal_day, "r")
    riga = (file.readline())

    while riga != "":
        estrai = riga.strip().split(",")
        if len(estrai) >= 4:
            from_stop = estrai[0]
            to_stop = estrai[1]
            dep_time = estrai[2]
            arr_time = estrai[3]

            dep = numero_float(dep_time)
            arr = numero_float(arr_time)
            tempo = arr - dep

            if from_stop in fermate and to_stop in fermate and tempo > 0:
                x1, y1 = fermate[from_stop]
                x2, y2 = fermate[to_stop]

                dx = x2 - x1
                dy = y2 - y1

                distanza = (dx * dx + dy * dy) ** 0.5
                rapporto = distanza / tempo

                if rapporto > massimo:
                    massimo = rapporto
                    id_partenza = from_stop
                    id_arrivo = to_stop
                    tempo_massimo = tempo
                    distanza_massima = distanza

        riga = file.readline()

    file.close()
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
