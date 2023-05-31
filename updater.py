import os
import sys
from time import sleep

REQUIRED_PACKAGES = ['requests', 'wget', 'configparser']

# Import-Anweisungen
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        print(f"Error: Missing {package}, installing it now...")
        os.system(f"pip install {package}")
    
    # Neustart der Anwendung nach der Installation der Pakete
    sleep(1)
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)

# Import-Anweisungen nach der Installation der Pakete
import requests
import wget
import configparser
import zipfile

def main():
    # GitHub URL zur Versionsdatei
    version_file_url = "https://raw.githubusercontent.com/dein-repository/version.txt"

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
        download_url = "https://github.com/dein-repository/archive/main.zip"
        temp_zip_file = "/tmp/main.zip"
        target_dir = os.getcwd()
        
        # Herunterladen der ZIP-Datei
        wget.download(download_url, temp_zip_file)
        
        # Entpacken der ZIP-Datei
        with zipfile.ZipFile(temp_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        
        # Aufräumen
        os.remove(temp_zip_file)
        
        print("Update erfolgreich durchgeführt. Die Anwendung wird neu gestartet.")
        sleep(5)
        sys.stdout.flush()
        os.execv(sys.argv[0], sys.argv)

    if check_version():
        if is_auto_update_enabled(ini_file_path):
            perform_update()
        else:
            choice = input("Es ist eine neue Version verfügbar. Möchten Sie das Update durchführen? (J/N): ")
            if choice.lower() == 'j':
                perform_update()
            else:
                print("Update abgebrochen. Die Anwendung wird normal gestartet.")

if __name__ == "__main__":
    main()
