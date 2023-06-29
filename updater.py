import os
import sys
import subprocess
import platform
from time import sleep

if platform.system() == 'Linux':
    linux = 1
    separator = "/"
elif platform.system() == 'Windows':
    linux = 0
    separator = "\\"
else:
    print(f"Unsupported OS {platform.system()}")
    sys.exit(1)


if linux == 1:
    # LiNUX COLOR CODES (SHELL)
    BLACK = "\033[0;30m"        # Black
    RED = "\033[0;31m"          # Red
    GREEN = "\033[0;32m"        # Green
    YELLOW = "\033[0;33m"       # Yellow
    BLUE = "\033[0;34m"         # Blue
    PURPLE = "\033[0;35m"       # Purple
    CYAN = "\033[0;36m"         # Cyan
    WHITE = "\033[0;37m"        # White
    ENDC = "\033[0m"            # Clear/return
else:
    # WiNDOWS COLOR CODES (CMD)
    os.system("")
    BLACK = "\033[0;30m"        # Black
    RED = "\033[0;31m"          # Red
    GREEN = "\033[0;32m"        # Green
    YELLOW = "\033[0;33m"       # Yellow
    BLUE = "\033[0;34m"         # Blue
    PURPLE = "\033[0;35m"       # Purple
    CYAN = "\033[0;36m"         # Cyan
    WHITE = "\033[0;37m"        # White
    ENDC = "\033[0m"            # Clear/return



REQUIRED_PACKAGES = ['requests', 'wget', 'configparser', 'subprocess', 'datetime']

# Import-Anweisungen
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        print(f"{RED}    [!] Error: Missing {package}, installing it now...")
        os.system(f"pip install {package}")
    
        # Neustart der Anwendung nach der Installation der Pakete
        print(f"{YELLOW}    [*] Starte nun neu nach der Instalation der pakete!")
        sleep(1)
        sys.stdout.flush()
        subprocess.call([sys.executable] + sys.argv)

# Import-Anweisungen nach der Installation der Pakete
import requests
import wget
import configparser
import zipfile
import datetime

def should_run_updater():
    # Pfad zur update.ini-Datei
    ini_file_path = "updater.ini"

    # Aktuelles Datum
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    config = configparser.ConfigParser()
    config.read(ini_file_path)

    # Lesen des gespeicherten Datums aus der update.ini-Datei
    last_update_date = config.get('Updater', 'LastUpdateDate')

    if last_update_date != current_date:
        # Wenn das Datum in der update.ini-Datei nicht mit dem aktuellen Datum übereinstimmt,
        # wird der Updater ausgeführt und das Datum aktualisiert
        update_timestamp(ini_file_path, current_date)
        return True

    return False

def update_timestamp(ini_file_path, current_date):
    config = configparser.ConfigParser()
    config.read(ini_file_path)

    # Aktualisiere den Wert von 'LastUpdateDate' in der Konfigurationsdatei
    config['Updater']['LastUpdateDate'] = current_date

    # Schreibe die aktualisierten Werte zurück in die Datei
    with open(ini_file_path, 'w') as config_file:
        config.write(config_file)

def main():
    # GitHub URL zur Versionsdatei
    version_file_url = "https://github.com/zer0de-r00tSec/Warez-Szene-Releaser/version.txt"

    # Pfad zur lokalen INI-Datei
    ini_file_path = "updater.ini"

    # Überprüfung der Versionsnummer
    def check_version():
        response = requests.get(version_file_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            with open("versions.txt", "r") as file:
                current_version = file.read()
            if latest_version != current_version:
                return True
        print(f"{YELLOW}    [!] Kein Update gefunden!")
        return False

    # Überprüfung der Auto-Update-Einstellung in der INI-Datei
    def is_auto_update_enabled(updater_ini):
        config = configparser.ConfigParser()
        config.read(updater_ini)

        auto_update = config.getint('Updater', 'Autoupdate')
        
        if auto_update == 1:
            return True
        else:
            return False

    # Herunterladen und Aktualisieren
    def perform_update():
        download_url = "https://github.com/zer0de-r00tSec/Warez-Szene-Releaser/archive/main.zip"
        temp_zip_file = "/tmp/main.zip"
        target_dir = os.getcwd()
        
        # Herunterladen der ZIP-Datei
        print(f"{YELLOW}    [*] Lade Paket herunter")
        wget.download(download_url, temp_zip_file)
        
        # Entpacken der ZIP-Datei
        print(f"{YELLOW}    [*] Entpacke")
        with zipfile.ZipFile(temp_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        
        # Aufräumen
        print(f"{YELLOW}    [*] Räume auf")
        os.remove(temp_zip_file)
        
        print(f"{YELLOW}    [*] Update erfolgreich durchgeführt. Die Anwendung wird neu gestartet.")
        print(f"{YELLOW}    [*] Starte nun neu!")
        sleep(5)
        subprocess.call([sys.executable] + sys.argv)

    if check_version():
        if is_auto_update_enabled(ini_file_path):
            perform_update()
        else:
            choice = input("Es ist eine neue Version verfügbar. Möchten Sie das Update durchführen? (J/N): ")
            if choice.lower() == 'j':
                perform_update()
            else:
                print(f"{RED}    [*]Update abgebrochen. Die Anwendung wird normal gestartet.")

if __name__ == "__main__":
    if should_run_updater():
        main()
