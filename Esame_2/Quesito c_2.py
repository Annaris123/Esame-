print("Quesito C:")
print("")

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


def leggi_fermate(percorso_file):
    dizionario_fermate = {}
    file = open(percorso_file, 'r')
    righe = file.readlines()
    file.close()

    if len(righe) == 0:
        print("File fermate vuoto!")
        return dizionario_fermate

    intestazione = righe[0].strip()
    separatore = ';'
    conta_virgole = 0
    conta_punto_e_virgola = 0

    indice = 0
    while indice < len(intestazione):
        carattere = intestazione[indice]
        if carattere == ',':
            conta_virgole = conta_virgole + 1
        if carattere == ';':
            conta_punto_e_virgola = conta_punto_e_virgola + 1
        indice = indice + 1

    if conta_virgole > conta_punto_e_virgola:
        separatore = ','

    riga_corrente = 1
    while riga_corrente < len(righe):
        riga = righe[riga_corrente].strip()
        colonne = riga.split(separatore)

        if len(colonne) >= 4:
            id_fermata = colonne[0].strip()
            lat = colonne[1].strip()
            lon = colonne[2].strip()
            nome = colonne[3].strip()

            # Controlla validità latitudine
            indice_carattere = 0
            lat_valida = 1
            while indice_carattere < len(lat):
                c = lat[indice_carattere]
                if c != '.' and c != '-' and (c < '0' or c > '9'):
                    lat_valida = 0
                indice_carattere = indice_carattere + 1

            # Controlla validità longitudine
            indice_carattere = 0
            lon_valida = 1
            while indice_carattere < len(lon):
                c = lon[indice_carattere]
                if c != '.' and c != '-' and (c < '0' or c > '9'):
                    lon_valida = 0
                indice_carattere = indice_carattere + 1

            if lat_valida == 1 and lon_valida == 1:
                latitudine = to_float_like(lat)
                longitudine = to_float_like(lon)
                dizionario_fermate[id_fermata] = (latitudine, longitudine, nome)

        riga_corrente = riga_corrente + 1

    return dizionario_fermate


def leggi_viaggi_bus(percorso_file):
    viaggi = {}

    file = open(percorso_file, 'r')
    righe = file.readlines()
    file.close()

    if len(righe) == 0:
        print("File viaggi vuoto!")
        return viaggi

    intestazione = righe[0].strip()
    separatore = ';'
    conta_virgole = 0
    conta_punto_e_virgola = 0

    i = 0
    while i < len(intestazione):
        carattere = intestazione[i]
        if carattere == ',':
            conta_virgole = conta_virgole + 1
        elif carattere == ';':
            conta_punto_e_virgola = conta_punto_e_virgola + 1
        i = i + 1

    if conta_virgole > conta_punto_e_virgola:
        separatore = ','

    # Mappa colonne
    colonne = {}
    nomi_colonne = intestazione.split(separatore)
    posizione = 0
    while posizione < len(nomi_colonne):
        nome = nomi_colonne[posizione].strip()
        colonne[nome] = posizione
        posizione = posizione + 1

    indice_riga = 1
    while indice_riga < len(righe):
        riga = righe[indice_riga].strip()
        parti = riga.split(separatore)

        if len(parti) >= len(colonne):
            tipo_mezzo = parti[colonne['route_type']].strip()
            if tipo_mezzo == '3':
                id_viaggio = parti[colonne['trip_I']]
                da_fermata = parti[colonne['from_stop_I']]
                a_fermata = parti[colonne['to_stop_I']]
                numero_seq = parti[colonne['seq']].strip()

                numero = True
                j = 0
                while j < len(numero_seq):
                    c = numero_seq[j]
                    if c < '0' or c > '9':
                        numero = False
                    j = j + 1

                if numero == True:
                    numero_seq_intero = int(numero_seq)

                    # se non esiste ancora la lista, la crea
                    if id_viaggio in viaggi:
                        viaggi[id_viaggio].append((numero_seq_intero, da_fermata, a_fermata))
                    else:
                        viaggi[id_viaggio] = [(numero_seq_intero, da_fermata, a_fermata)]

        indice_riga = indice_riga + 1

    return viaggi


def calcola_distanze(viaggi, fermate):
    distanze_per_viaggio = {}

    for id_viaggio in viaggi:
        connessioni = viaggi[id_viaggio]

        # Ordina le connessioni in base al numero sequenziale
        indice_conn = 0
        while indice_conn < len(connessioni) - 1:
            indice_prossimo = indice_conn + 1
            while indice_prossimo < len(connessioni):
                if connessioni[indice_conn][0] > connessioni[indice_prossimo][0]:
                    temp = connessioni[indice_conn]
                    connessioni[indice_conn] = connessioni[indice_prossimo]
                    connessioni[indice_prossimo] = temp
                indice_prossimo = indice_prossimo + 1
            indice_conn = indice_conn + 1

        distanza_totale = 0.0

        indice = 0
        while indice < len(connessioni):
            da_fermata = connessioni[indice][1]
            a_fermata = connessioni[indice][2]

            if da_fermata in fermate and a_fermata in fermate:
                lat1 = fermate[da_fermata][0]
                lon1 = fermate[da_fermata][1]
                lat2 = fermate[a_fermata][0]
                lon2 = fermate[a_fermata][1]

                delta_lat = lat2 - lat1
                delta_lon = lon2 - lon1
                distanza = ((delta_lat * delta_lat) + (delta_lon * delta_lon)) ** 0.5
                distanza_totale = distanza_totale + distanza

            indice = indice + 1

        distanze_per_viaggio[id_viaggio] = distanza_totale

    return distanze_per_viaggio


def trova_massimo(distanze):
    massimo_valore = -1.0
    id_massimo = ''

    for id_viaggio in distanze:
        valore = distanze[id_viaggio]
        if valore > massimo_valore:
            massimo_valore = valore
            id_massimo = id_viaggio

    return id_massimo


def estrai_fermate(connessioni, fermate):
    # Ordinamento manuale per sequenza
    i = 0
    while i < len(connessioni) - 1:
        j = i + 1
        while j < len(connessioni):
            if connessioni[i][0] > connessioni[j][0]:
                temp = connessioni[i]
                connessioni[i] = connessioni[j]
                connessioni[j] = temp
            j = j + 1
        i = i + 1

    fermate_visitate = []
    nomi_fermate = []

    indice = 0
    while indice < len(connessioni):
        da_fermata = connessioni[indice][1]
        a_fermata = connessioni[indice][2]

        for f in [da_fermata, a_fermata]:
            esiste = False
            k = 0
            while k < len(fermate_visitate):
                if fermate_visitate[k] == f:
                    esiste = True
                k = k + 1

            if f in fermate and esiste == False:
                posizione = len(nomi_fermate)
                nomi_fermate.insert(posizione, fermate[f][2])
                posizione2 = len(fermate_visitate)
                fermate_visitate.insert(posizione2, f)

        indice = indice + 1

    return nomi_fermate


def main():
    fermate = leggi_fermate('/Users/martaristori/Desktop/Anna/network_nodes.csv')
    viaggi = leggi_viaggi_bus('/Users/martaristori/Desktop/Anna/network_temporal_day.csv')
    distanze = calcola_distanze(viaggi, fermate)
    id_massimo = trova_massimo(distanze)

    if id_massimo == '':
        print("Nessuna corsa bus trovata.")
        return

    fermate_ordinate = estrai_fermate(viaggi[id_massimo], fermate)

    print("Corsa più lunga:", id_massimo)
    print("")
    print("Fermate attraversate (solo nomi):")

    indice = 0
    while indice < len(fermate_ordinate):
        numero = indice + 1
        print(str(numero) + ". " + fermate_ordinate[indice])
        indice = indice + 1


main()
