def leggi_luoghi(file_nodi):
    luoghi = {}
    network_nodes = open(file_nodi, 'r')  # Apri il file

    intestazione = network_nodes.readline().strip().split(",")
    indice_id = 0
    indice_nome = len(intestazione) - 1

    for riga in network_nodes:
        if riga.strip():
            campi = riga.strip().split(",")
            id_nodo = campi[indice_id]
            nome_luogo = campi[indice_nome]
            luoghi[id_nodo] = nome_luogo

    network_nodes.close()
    return luoghi


def leggi_servizi(file_servizi):
    servizi = {}
    network_temporal_day = open(file_servizi, 'r')

    intestazione = network_temporal_day.readline().strip().split(",")
    indice_id = 0
    indice_servizio = 4

    for riga in network_temporal_day:
        if riga.strip():
            campi = riga.strip().split(",")
            id_nodo = campi[indice_id]
            nome_servizio = campi[indice_servizio]

            if id_nodo not in servizi:
                servizi[id_nodo] = [nome_servizio]
            elif nome_servizio not in servizi[id_nodo]:
                    servizi[id_nodo].append(nome_servizio)

    network_temporal_day.close()
    return servizi


def collega_dati(luoghi, servizi_nodi):
    luogo_servizi = {}

    for id_nodo in servizi_nodi:
        if id_nodo in luoghi:
            nome_luogo = luoghi[id_nodo]
            lista_servizi = servizi_nodi[id_nodo]

            if nome_luogo not in luogo_servizi:
                luogo_servizi[nome_luogo] = []

            for servizio in lista_servizi:
                if servizio not in luogo_servizi[nome_luogo]:
                    luogo_servizi[nome_luogo].append(servizio)
        else:
            print("Node ID: ", id_nodo, " non trovato nel primo file.")

    return luogo_servizi

def trova_top10(luogo_servizi):
    top10 = []
    for luogo in luogo_servizi:
        numero_servizi = len(luogo_servizi[luogo])

        if len(top10) < 10:
            top10.append((luogo, numero_servizi))
        else:
            # Trova il minimo attuale nella lista top_10
            indice_min = 0
            for i in range(1, 10):
                if top10[i][1] < top10[indice_min][1]:
                    indice_min = i
            # Sostituisci se il nuovo valore è più grande
            if numero_servizi > top10[indice_min][1]:
                top10[indice_min] = (luogo, numero_servizi)

    return top10

def stampa_risultato(top10):
    print("Primi 10 luoghi:\n")
    numero = 1
    for luogo, quanti in top10:
        print(numero, ".", luogo, "ha", quanti, "servizi diversi")


file_nodi = '/Users/martaristori/Desktop/Anna/network_nodes.csv'
file_servzi = '/Users/martaristori/Desktop/Anna/network_temporal_day.csv'

luoghi = leggi_luoghi(file_nodi)
servizi = leggi_servizi(file_servzi)
luogo_servizi= collega_dati(luoghi, servizi)
top10 = trova_top10(luogo_servizi)
stampa_risultato(top10)