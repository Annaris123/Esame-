# Domanda A
def File1(file1):  # Definiamo una funzione File1 che prende in input il percorso di un file
    dati_primo = {}  # Inizializziamo un dizionario
    network_nodes = open('/Users/martaristori/Desktop/Anna/network_nodes.csv', 'r') # Apri il file

    header = network_nodes.readline().strip().split(",")
    i_first = 0
    i_last = len(header) - 1

    for riga in network_nodes:
        if riga.strip():
            campi = riga.strip().split(",")
            id_col = campi[i_first]
            last_col = campi[i_last]
            dati_primo[id_col] = last_col

    network_nodes.close()
    return dati_primo


def File2(file2):
    dati_secondo = {}
    network_temporal_day = open('/Users/martaristori/Desktop/Anna/network_temporal_day.csv', 'r')

    header = network_temporal_day.readline().strip().split(",")
    i_first = 0
    i_fifth = 4

    for riga in network_temporal_day:
        if riga.strip():
            campi = riga.strip().split(",")
            id_col = campi[i_first]
            fifth_col = campi[i_fifth]

            if id_col not in dati_secondo:
                dati_secondo[id_col] = [fifth_col]
            else:
                if fifth_col not in dati_secondo[id_col]:
                    dati_secondo[id_col].append(fifth_col)

    network_temporal_day.close()
    return dati_secondo


def collega_dati(dati_primo, dati_secondo):
    # Dizionario nome luogo -> insieme di servizi diversi
    luogo_servizi = {}

    for node_id in dati_secondo:
        if node_id in dati_primo:
            nome = dati_primo[node_id]
            servizi = dati_secondo[node_id]
            if nome not in luogo_servizi:
                luogo_servizi[nome] = set()
            for s in servizi:
                luogo_servizi[nome].add(s)
        else:
            print("Node ID: ", node_id, " non trovato nel primo file.")

    # Ora creiamo una lista [(nome, numero_servizi), ...]
    lista_luoghi = []
    for nome, servizi in luogo_servizi.items():
        lista_luoghi.append((nome, len(servizi)))

    # Ordiniamo decrescente per numero servizi
    lista_luoghi.sort(key=lambda x: x[1], reverse=True)

    # Stampiamo i primi 10
    print("Top 10 luoghi attraversati da più servizi diversi:\n")
    for i, (nome, n_servizi) in enumerate(lista_luoghi[:10], start=1):
        print(i, ".", nome, " - ", n_servizi, "servizi diversi")


# --- Usa i percorsi corretti ai file ---

file1_path = '/Users/martaristori/Desktop/Anna/network_nodes.csv'
file2_path = '/Users/martaristori/Desktop/Anna/network_temporal_day.csv'

dati_primo = File1(file1_path)
dati_secondo = File2(file2_path)
collega_dati(dati_primo, dati_secondo)
