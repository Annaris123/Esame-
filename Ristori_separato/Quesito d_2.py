import time

print("Quesito D:")
print("")


def n_fermate(percorso, separatore, nome):
    # Conta il numero di fermate uniche presenti nel file CSV.
    fermate = set()

    file = open(percorso, "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(separatore)
    indice_partenza = intestazione.index("from_stop_I")
    indice_arrivo = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        estrai = riga.strip().split(separatore)
        if len(estrai) > max(indice_partenza, indice_arrivo):
            partenza = estrai[indice_partenza]
            arrivo = estrai[indice_arrivo]
            fermate.add(partenza)
            fermate.add(arrivo)

    print("Numero di fermate uniche in " + nome + ": " + str(len(fermate)))


def n_collegamenti(percorso, separatore, nome):
    # Conta il numero di collegamenti diretti unici tra fermate.

    collegamenti = set()

    file = open(percorso, "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(separatore)
    indice_partenza = intestazione.index("from_stop_I")
    indice_arrivo = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(separatore)
        if len(valori) > max(indice_partenza, indice_arrivo):
            partenza = valori[indice_partenza]
            arrivo = valori[indice_arrivo]
            collegamenti.add((partenza, arrivo))

    print("Numero di collegamenti diretti in " + nome + ": " + str(len(collegamenti)))


# Percorsi dei file CSV
network_temporal_day = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"
network_temporal_week = "/Users/martaristori/Desktop/Anna/network_temporal_week.csv"

# Tempo per network_temporal_day
start_day = time.time()
n_fermate(network_temporal_day, ",", "network_temporal_day")
n_collegamenti(network_temporal_day, ",", "network_temporal_day")
end_day = time.time()

print("")

# Tempo per network_temporal_week
start_week = time.time()
n_fermate(network_temporal_week, ";", "network_temporal_week")
n_collegamenti(network_temporal_week, ";", "network_temporal_week")
end_week = time.time()

# Stampa risultati
print("Tempi risposta D:", (end_day - start_day), "e", (end_week - start_week))
