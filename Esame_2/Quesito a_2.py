print("Quesito A:")
print("")
def leggi_collegamenti(file_path):
    """Legge il file dei collegamenti e restituisce un dizionario ID fermata → lista di servizi."""
    file = open(file_path, "r")
    fermate_con_servizi = {}

    file.readline()  # Salta intestazione
    for riga in file:
        campi = riga.strip().split(",")
        id_partenza = campi[0]
        id_arrivo = campi[1]
        servizio = campi[4]

        # Aggiungi servizio alla fermata di partenza
        if id_partenza not in fermate_con_servizi:
            fermate_con_servizi[id_partenza] = [servizio]
        elif servizio not in fermate_con_servizi[id_partenza]:
            fermate_con_servizi[id_partenza].append(servizio)

        # Aggiungi servizio alla fermata di arrivo
        if id_arrivo not in fermate_con_servizi:
            fermate_con_servizi[id_arrivo] = [servizio]
        elif servizio not in fermate_con_servizi[id_arrivo]:
            fermate_con_servizi[id_arrivo].append(servizio)

    file.close()
    return fermate_con_servizi


def trova_top_fermate(fermate_con_servizi, top_n=10):
    """Restituisce le top N fermate con il maggior numero di servizi diversi."""
    lista_id_fermate = list(fermate_con_servizi.keys())
    lista_numero_servizi = [len(fermate_con_servizi[id]) for id in lista_id_fermate]

    top_id = []
    top_valori = []

    while len(top_id) < top_n:
        massimo = max(lista_numero_servizi)
        indice_massimo = lista_numero_servizi.index(massimo)
        id_top = lista_id_fermate[indice_massimo]

        top_id.append(id_top)
        top_valori.append(massimo)

        lista_numero_servizi[indice_massimo] = 0  # Evita riutilizzo dello stesso indice

    return top_id, top_valori


def leggi_mappa_id_nome(file_path):
    """Legge il file dei nodi e restituisce un dizionario ID → nome fermata."""
    file = open(file_path, "r")
    mappa_id_nome = {}

    file.readline()  # Salta intestazione
    for riga in file:
        campi = riga.strip().split(",")
        mappa_id_nome[campi[0]] = campi[3]

    file.close()
    return mappa_id_nome


def stampa_top_fermate(top_ids, top_valori, id_to_name):
    """Stampa le top fermate in modo ordinato e chiaro."""
    print("Le 10 fermate attraversate da più servizi diversi sono:\n")
    for i in range(10):
        fid = top_ids[i]
        servizi = top_valori[i]
        nome = id_to_name.get(fid, "Nome non trovato")
        print(str(i + 1) + ". " + nome + " con " + str(servizi) + " servizi diversi")


# === Corpo principale ===

# Percorsi dei file
percorso_collegamenti = "/Users/martaristori/Desktop/Anna/network_temporal_day.csv"
percorso_nodi = "/Users/martaristori/Desktop/Anna/network_nodes.csv"

# Elaborazione
fermate_con_servizi = leggi_collegamenti(percorso_collegamenti)
top_ids, top_valori = trova_top_fermate(fermate_con_servizi)
id_to_name = leggi_mappa_id_nome(percorso_nodi)

# Output
stampa_top_fermate(top_ids, top_valori, id_to_name)
