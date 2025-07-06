# Apre e legge il file temporale dei collegamenti tra fermate
file_collegamenti = open("/Users/martaristori/Desktop/Anna/network_temporal_day.csv", "r")
fermate_con_servizi = {}  # Dizionario: ID fermata → lista dei servizi che la attraversano
riga = file_collegamenti.readline()  # salta intestazione



# Apre il file dei nodi per associare ID → nome fermata
file_nodi = open("/Users/martaristori/Desktop/Anna/network_nodes.csv", "r")
mappa_id_nome = {}
riga = file_nodi.readline()  # salta intestazione