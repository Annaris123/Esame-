def conta_luoghi_unici_giorno():
    luoghi = []
    file = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(",")
    indice_source = intestazione.index("from_stop_I")
    indice_target = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(",")
        if len(valori) > max(indice_source, indice_target):
            source = valori[indice_source]
            target = valori[indice_target]

            if source not in luoghi:
                luoghi = luoghi + [source]
            if target not in luoghi:
                luoghi = luoghi + [target]

    print("Numero di luoghi in network_temporal_day:", len(luoghi))


def conta_luoghi_unici_settimana():
    luoghi = []
    file = open("/Users/martaristori/Desktop/Anna/network_temporal_week.csv", "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(";")  # QUI CAMBIATO
    indice_source = intestazione.index("from_stop_I")
    indice_target = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(";")  # QUI CAMBIATO
        if len(valori) > max(indice_source, indice_target):
            source = valori[indice_source]
            target = valori[indice_target]

            if source not in luoghi:
                luoghi = luoghi + [source]
            if target not in luoghi:
                luoghi = luoghi + [target]

    print("Numero di luoghi in network_temporal_week:", len(luoghi))


# Chiamata delle funzioni
conta_luoghi_unici_giorno()
conta_luoghi_unici_settimana()

def conta_collegamenti_diretti_giorno():
    collegamenti = []
    file = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(",")
    indice_source = intestazione.index("from_stop_I")
    indice_target = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(",")
        if len(valori) > max(indice_source, indice_target):
            source = valori[indice_source]
            target = valori[indice_target]
            coppia = (source, target)

            if coppia not in collegamenti:
                collegamenti += [coppia]

    print("Collegamenti network_temporal_day:", len(collegamenti))


def conta_collegamenti_diretti_settimana():
    collegamenti = []
    file = open("/Users/martaristori/Desktop/Anna/network_temporal_week.csv", "r")
    righe = file.readlines()
    file.close()

    intestazione = righe[0].strip().split(";")  # attenzione al separatore
    indice_source = intestazione.index("from_stop_I")
    indice_target = intestazione.index("to_stop_I")

    for riga in righe[1:]:
        valori = riga.strip().split(";")
        if len(valori) > max(indice_source, indice_target):
            source = valori[indice_source]
            target = valori[indice_target]
            coppia = (source, target)

            if coppia not in collegamenti:
                collegamenti += [coppia]

    print("Collegamenti network_temporal_week:", len(collegamenti))


# Chiamata delle due funzioni
conta_collegamenti_diretti_giorno()
conta_collegamenti_diretti_settimana()
