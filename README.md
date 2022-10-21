# DIANAProject
Il Diana Project è un applicativo software focalizzato sullo studio del genoma del topo domestico
(Mus Musculus), in grado di combinare le informazioni contenute in diverse banche, e tracciare
le relazioni tra miRNA ed i Geni target.
L’ obiettivo per l’AA 2020-2021 è di aggiornare e migliorare il vecchio applicativo del DIANA
Project dell’AA 2015/2016 (A. di Marco, 2016) (Tucci Michele, 2016)
Esso, come già accennato, permette di tracciare le relazioni tra microRNA e Geni della specie
Mus Musculus (topo domestico).
I dati relativi al sequenziamento del genoma del topo sono pubblici e resi disponibili da diverse
banche dati; per questo elaborato sono state utilizzate PicTar, RNA22, TargetScan e
miRtarBase.
Le migliorie principali del progetto per l’AA 2020-2021 riguardano: definire un’architettura di
sistema che sia facilmente mantenibile per aggiornamenti futuri, verificare la disponibilità dei
dati utilizzati, aggiornando il database, e fornire all’utente finale un’interfaccia che permetta di
interrogare facilmente il database.

## Init

Create a Neo4J database:
- user: neo4j
- password: test



## Run

```
$ cd ../DIANAProject
$ pip3 install -r requirements.txt
$ flask run

```
