# Warez-Szene Releaser

Dies ist die README-Datei für das Projekt "Warez-Szene Releaser". Dieses Projekt wurde entwickelt, um den Groups, noobs oder einfach nur Ordnungs vernatiker, eine einheitliche Struktur zu bieten.

## Beschreibung

Es ist ein wahres AiO Script, es kann einiges an Arbeit abnehmen, denoch sollte das ergebnis kontrolliert werden. Stichwort IMDB-Link.


## Features

* NFO erstellen, sowohl eigene Templates (ASCII Style) als auch simple Templates können genutzt werden
* Packen in Szene konformen grössen
* Naming (bennenung, der files) in Szene Style
* SFV Datei erstellung
* Dupe Check - Prüfung via API auf dupe ( Vorhanden sein eines gleichen Releases)
* FTP Upload
* Pre announce, auf Telegram
* läuft in threading standart sind 10 files gleichzeitig bearbeiten, config in der ini vornehmen


## Installation

1. Klonen Sie dieses Repository in Ihre lokale Umgebung:

    git clone https://github.com/zer0de-r00tSec/Warez-Releaser.git
    

2. Navigieren Sie in das Verzeichnis:

    bash
    cd Warez-Szene Releaser
    

3. Installieren Sie die notwendigen Abhängigkeiten:

    bash
    pip install -r requirements.txt

    Optional - GUI nutzung
    apt install python3-tk
    

## Verwendung

# zeigt die Syntax mit Hilfe an
python releaser_CLI.py <Ordnder mit zu packenden Files> <der Ziel Ordner> <Source der Files zB. DVD oder BDRiP> <deine config datei> <verbose>


# startet das program autonm
python releaser_CLI.py /source/ /dest/ DVD config_DVD.ini

# startet das program Interaktiv
python releaser_CLI.py /source/ /dest/ DVD config_DVD.ini verbose


## Mitwirken

ihr wisst es doch eh :-)

## Kontakt

Ihr Name - zer0.de@inbox.lv

Projekt Link: [https://github.com/zer0de-r00tSec/Warez-Releaser](https://github.com/zer0de-r00tSec/Warez-Releaser)
