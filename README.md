# Warez-Szene-Releaser

Dies ist die README-Datei für das Projekt "Warez-Szene-Releaser". Dieses Projekt wurde entwickelt, um den Groups, noobs oder einfach nur Ordnungs vernatiker, eine einheitliche Struktur zu bieten.

## Beschreibung

Es ist ein wahres AiO Script, es kann einiges an Arbeit abnehmen, dennoch sollte das ergebnis kontrolliert werden. Stichwort IMDB-Link.


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
    cd Warez-Szene-Releaser
    

3. Installieren Sie die notwendigen Abhängigkeiten:

    bash
    pip install -r requirements.txt

    Optional - GUI nutzung
    apt install python3-tk
    

## Verwendung

### zeigt die Syntax mit Hilfe an
![grafik](https://github.com/zer0de-r00tSec/Warez-Szene-Releaser/assets/118939020/c7dee607-86e6-492d-bf75-02f5b1352f46)

    python releaser_CLI.py <Ordnder mit zu packenden Files> <der Ziel Ordner> <Source der Files zB. DVD oder BDRiP> <deine config datei> <verbose>


### Startet das Programm Autonm
    python releaser_CLI.py /source/ /dest/ DVD config_DVD.ini

### Startet das Programm Interaktiv
    python releaser_CLI.py /source/ /dest/ DVD config_DVD.ini verbose



## ToDo
  GUI Updaten, Config bereich etc.
  dupe APIs adden
  ...

## Changelog
    2.2.3
        + in der INI können nur bei den NOTES, Steuerzeichen wie \t genutzt werden zum einrücken von Text
        + HDR Support, hier wird nun HDR10+ HDR10 und Dolby Vision geloggt und in die NFO geschrieben.
          hierzu, function get_hdr_info in Zeile 623 anpassen - THX hier an ... Du weisst bescheid :)
        +/- Bugs gefunden und beseitig und natürlich neue dazu geschrieben, soll ja nich Langweilig werden.
        
    2.2.2
        + OMDB Support, IMDB Free ist Abgeschaltet worden, daher die Alternative
        + Replacements vom Codec, statt MPEG-4 MP4 etc.
        + Release - IMDB ID DB, damit man die API nich strapaziert, wird eine DB angelegt, mit Name und ID, 
          abgleich und nur bei 0 treffer wird die API abgefragt
        + bisschen dies, bisschen das :)
        - fehler, hoffe ich

## Mitwirken

ihr wisst es doch eh :-)

## Kontakt
zer0.de - zer0.de@inbox.lv

Projekt Link: [https://github.com/zer0de-r00tSec/Warez-Releaser](https://github.com/zer0de-r00tSec/Warez-Releaser)


## Disclaimer
"This tool is for educational purposes only. Please use at your own risk"
