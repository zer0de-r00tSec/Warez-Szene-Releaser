#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Debug ON/OFF
DEBUG = 0

# iMPORT ALL MODULES
import json
import sqlite3
import platform
import random
import re
import threading
import requests
import socket
import binascii
import time
import datetime
import os
import sys

# iMPORT UPDATER
import updater

try:
    from ftplib import FTP, error_perm, FTP_TLS
except:
    print(f"Error: Missing ftplib, install it now")
    os.system("pip install ftplib")

try:
    import configparser
except:
    print(f"Error: Missing configparser, install it now")
    os.system("pip install configparser")
# END OF iMPORT

if platform.system() == 'Linux':
    linux = 1
    separator = "/"
elif platform.system() == 'Windows':
    linux = 0
    separator = "\\"
else:
    print(f"Unsupported OS {platform.system()}")
    sys.exit(1)

___AUTHOR___ = 'zer0.de^r00tSec'
___VERSION___ = '2.2.2'

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

# CODE START
DATABASE_FILE = 'releaser.db'
config_file = './config/config.ini'


class IRC:
    UTF8 = "UTF-8"

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.sendall(bytes(f"PRIVMSG {chan} {msg}\n", IRC.UTF8))

        # DEFiNES THE SOCKET
    def connect(self, server, port, channel, botnick, server_pw, channel_pw):
        try:
            self.irc.connect((server, port))  # connects to the server
            self.irc.send(bytes(f"PASS {server_pw}\r\n", IRC.UTF8))
            # user authentication
            self.irc.send(
                bytes(f"USER {botnick} {botnick} {botnick} :This is a fun bot!\r\n", IRC.UTF8))
            self.irc.send(bytes(f"NICK {botnick}\r\n", IRC.UTF8))
            time.sleep(2)
            # join the chan
            self.irc.send(bytes(f"JOIN {channel} {channel_pw}\r\n", IRC.UTF8))
            return True
        except Exception as e:
            print(f"Error: Failed to connect to {server}:{port}. {e}")
            return False

    def quit(self):
        self.irc.close()

def create_database():
    print(f"{CYAN}    [!!] Creating Database please wait..")

    conn = sqlite3.connect(DATABASE_FILE)
    conn.close()

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME TEXT,
                 LINK_ID TEXT)''')

    conn.commit()
    conn.close()

def select_data(name):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Select data
    c.execute("SELECT LINK_ID FROM data WHERE NAME = ?", (name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return ""

def insert_data(name, link_id):
    print(f"{CYAN}    [!!] Insert Data: {name} {link_id}")
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Enter data (IGNORE INSERT uses INSERT OR IGNORE to ignore already existing entries)
    c.execute(
        "INSERT OR IGNORE INTO data (NAME, LINK_ID) VALUES (?, ?)", (name, link_id))

    conn.commit()
    conn.close()

def delete_data(name):
    print(f"{RED}    [!!] Delete Data: {name}")
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    try:
        c.execute("DELETE FROM data WHERE NAME=?", (name,))

        conn.commit()
    except sqlite3.Error as e:
        print(
            f"{RED}    [!] Szene Releaser {___VERSION___} Error in Delete SQLi: {e}")
    finally:
        conn.close()

def dupe_check_srrdb(release):
    readjson = requests.get(f"https://api.srrdb.com/v1/search/{release}").text
    data = json.loads(readjson)
    if data or json.JSONDecodeError:
        if 'results' in data and len(data['results']) > 0:
            num_results = len(data['results'])

            print(f"{BLUE}    [+] Ich habe {num_results} Ergebnisse gefunden.")
            print(
                f"{BLUE}    [+] Möchtest du alle durchgehen, Abbrechen oder Ignorieren?")
            print(
                f"{BLUE}    [+] Y - Alle durchgehen | I - Ignorieren | C - Abbrechen")
            user_input = ask_yes_no_dupe("Deine Wahl: ")

            if user_input == True:
                if len(data['results']) == 1:
                    rls_name = data['results'][0]['release']
                    user_input = ask_yes_no_dupe(f"Ist {rls_name} das dupe?: ")

                    if user_input == True:
                        sys.exit(1)
                    elif user_input == False:
                        return
                    elif user_input == "cancle":
                        sys.exit(1)
                    elif user_input == "ignore":
                        return

                else:
                    for index, result in enumerate(data['results']):
                        print("Multi Result ist: " + str(result))
                        rls_name = result['release']

                        user_input = ask_yes_no_dupe(
                            f"Ist {rls_name} das dupe?: ")
                        if user_input == True:
                            break  # Beendet die Schleife und das Skript
                        elif user_input == "cancle":
                            break  # Beendet die Schleife und das Skript
                        elif user_input == "ignore":
                            break  # Beendet die Schleife und das Skript

            elif user_input.lower() == "c":
                sys.exit(1)  # Beendet die Schleife und das Skript
        else:
            print(f"{GREEN}    [+] Nichts gefunden für {release}")

def calculate_part_size(compl_path):
    # GET ALL NECESERY VARs
    config = configparser.ConfigParser()
    config.read(config_file)
    RAR_PAKET_SMALL_SIZE = config.get('RAR', 'RAR_PAKET_SMALL_SIZE')
    RAR_PAKET_SMALL_COUNT = config.get('RAR', 'RAR_PAKET_SMALL_COUNT')
    RAR_PAKET_MID_SIZE = config.get('RAR', 'RAR_PAKET_MID_SIZE')
    RAR_PAKET_MID_COUNT = config.get('RAR', 'RAR_PAKET_MID_COUNT')
    RAR_PAKET_MAX_COUNT = config.get('RAR', 'RAR_PAKET_MAX_COUNT')

    stats = os.stat(compl_path)
    f_size = ((stats.st_size / 1024)/1024)
    file_size = round(f_size, 0)

    if file_size <= RAR_PAKET_SMALL_SIZE:
        package_size = RAR_PAKET_SMALL_COUNT
    elif file_size <= RAR_PAKET_MID_SIZE:
        package_size = RAR_PAKET_MID_COUNT
    else:
        package_size = RAR_PAKET_MAX_COUNT

    part_size = (file_size / package_size) * 1024 * 1024
    return round(part_size)

def rar_pack_size(compl_path):
    stats = os.stat(compl_path)
    f_size = ((stats.st_size / 1024)/1024)
    f_size = round(f_size, 0)

    # FiLE SiZE iN MB
    if f_size <= 1450.0:
        print(
            f"{PURPLE}    [~] File ist kleiner als/gleich 1450MB wähle 50MB Packs")
        return "50000000"
    elif f_size > 1450.0 and f_size < 14000.0:
        print(
            f"{PURPLE}    [~] File ist grösser als 1450MB aber kleiner als 14GB wähle 150MB Packs")
        return "150000000"
    elif f_size > 14000.0 and f_size < 30000.0:
        print(
            f"{PURPLE}    [~] File ist grösser als 15GB aber kleiner als 30GB 300MB Packs")
        return "300000000"
    else:
        print(f"{PURPLE}    [~] File ist grösser als 30GB 500MB Packs")
        return "500000000"

def write_to_file(file, text, modus='a'):
    if not os.path.exists(file):
        try:
            d = open(file, modus)
            d.write(text)
            d.close
        except:
            print(
                f"{RED}    [!] Szene Releaser {___VERSION___} Error: {file} to Write not found or access denied!")

    else:
        d = open(file, modus)
        d.write(text)
        d.close

def CRC32_from_file(filename):
    with open(filename, 'rb') as file:
        buf = file.read()
        buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

def upload(ftp, local_path):
    """
    Uploads a file or directory to the remote FTP server.
    """
    # GET ALL NECESERY VARs
    config = configparser.ConfigParser()
    config.read(config_file)
    FTP_PREDIR = config.get('FTP', 'FTP_PREDIR')

    if not os.path.exists(local_path):
        raise ValueError(f'Local path "{local_path}" does not exist')
    rel_dir = os.path.basename(local_path)
    if rel_dir in ('Sample', 'Proof', 'Subs'):
        return
    remote_dir = os.path.join(FTP_PREDIR, rel_dir)
    try:
        ftp.mkd(remote_dir)
    except Exception as e:
        if not e.args[0].startswith('550'):
            raise
    ftp.cwd(remote_dir)
    upload_directory(ftp, local_path, remote_dir)
    ftp.cwd(FTP_PREDIR)

def upload_directory(ftp, local_path):
    # GET ALL NECESERY VARs
    config = configparser.ConfigParser()
    config.read(config_file)
    FTP_PREDIR = config.get('FTP', 'FTP_PREDIR')

    base_dir = os.path.basename(os.path.normpath(local_path))

    if base_dir not in ["Sample", "Proof", "Subs"]:
        try:
            ftp.mkd(FTP_PREDIR + base_dir)
        except Exception as e:
            if e.args[0].startswith('550'):
                pass

    rel_dir = FTP_PREDIR + base_dir
    if "Sample" not in local_path:
        ftp.cwd(rel_dir)

    # UPLOAD SFV FiLES FiRST
    sorted_dir = sorted(os.listdir(local_path))
    for i in range(len(sorted_dir)):
        if ".sfv" in sorted_dir[i]:
            sorted_dir.insert(0, sorted_dir.pop(i))

    for name in sorted_dir:
        localpath = os.path.join(local_path, name)

        if os.path.isfile(localpath):
            filelist = []
            ftp.retrlines('NLST', filelist.append)

            if not name in filelist:
                ftp.storbinary('STOR ' + name, open(localpath, 'rb'))

        elif os.path.isdir(localpath):
            try:
                ftp.mkd(name)
            except Exception as e:
                if e.args[0].startswith('550'):
                    pass
            ftp.cwd(name)
            upload_directory(ftp, localpath)
            ftp.cwd(rel_dir)

def packing(ext, destination, filename, movie_complete_path):
    if DEBUG == 1:
        print(f"{YELLOW}    [*] Packing ")
        print(f"{YELLOW}    [*] ext {ext}")
        print(f"{YELLOW}    [*] destination {destination}")
        print(f"{YELLOW}    [*] filename {filename}")
        print(f"{YELLOW}    [*] source {movie_complete_path}")

    fname = os.path.basename(os.path.dirname(movie_complete_path))

    # GETTiNG RAR SiZE
    if movie_complete_path:
        PACK_SIZE = rar_pack_size(movie_complete_path)
    elif fname == "Subs" or fname == "Proof":
        PACK_SIZE = "15728640"

    if linux == 1:
        syntax = (
            f"rar a -m0 -ma4 -s -v{PACK_SIZE}b -vn -ep1 {ext} "
            f'"{os.path.join(destination, filename.lower())}.rar" '
            f'"{movie_complete_path}" >/dev/null 2>&1'
        )
    else:
        syntax = (
            f'addons{separator}rar.exe a -m0 -s -v{PACK_SIZE}b -vn -ep1 {ext} '
            f'"{os.path.join(destination, filename.lower())}.rar" '
            f'"{movie_complete_path}" >nul'
        )

    if DEBUG == 1:
        print(f"{YELLOW}    [*] RAR Syntax: {syntax}")

    ret = os.system(syntax)
    if ret != 0:
        raise Exception("Packing failed")
        print(f"{RED}    [*] Packing failed!")

def load_random_sentence(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        sentence = random.choice(lines).strip()
        return sentence

def filter_name(name):
    name = re.sub('[._\\-]', ' ', name)
    regex = r'^.*?(?=(19\d{2}|20\d{2}|german|S\d+E\d+|$))'
    match = re.search(regex, name)
    if match:
        found = match.group()
        # REMOVE CRAP
        found = found.rstrip('.mkv').rstrip('.')
        return found
    else:
        return ''

def extract_info(input_string, dupe=False):
    # GET ALL NECESERY VARs
    config = configparser.ConfigParser()
    config.read(config_file)
    RAR_USE = config.getint('RAR', 'RAR_USE')
    RAR_PACK_MOVIE = config.get('RAR', 'RAR_PACK_MOVIE')
    RAR_PACK_SERIES = config.get('RAR', 'RAR_PACK_SERIES')

    if RAR_USE == 1:

        input_string = input_string.replace(".", " ")

        # SEARCH PATTERN FOR DiFFERENT DELiMiTERS
        # year_pattern = r"\d{4}"
        year_pattern = r".19\d{2}|20\d{2}."
        season_episode_pattern = r".S\d{2}E\d{2,3}."
        episode_pattern = r".E\d{2,3}."
        lang_pattern = r".(GERMAN|FRENCH|DUTCH|MULTI)."
        audio_pattern = r".(DD5\.1|DL|ML|AC3|MIC|LINEDUB|DTS|DUBBED|AC3D)."
        codec_pattern = r".(H264|H265|X264|X265)."
        hdr_pattern = r".SDR."
        hdr1_pattern = r".HDR."
        hdr2_pattern = r".DV."
        screen_pattern = r".(WS|FS)."

        # SEARCH FOR DELiMiTERS
        year_match = re.search(year_pattern, input_string, re.IGNORECASE)
        season_episode_match = re.search(
            season_episode_pattern, input_string, re.IGNORECASE)
        episode_match = re.search(episode_pattern, input_string, re.IGNORECASE)
        lang_match = re.search(lang_pattern, input_string, re.IGNORECASE)
        audio_match = re.search(audio_pattern, input_string, re.IGNORECASE)
        codec_match = re.search(codec_pattern, input_string, re.IGNORECASE)
        hdr_match = re.search(hdr_pattern, input_string, re.IGNORECASE)
        hdr1_match = re.search(hdr1_pattern, input_string, re.IGNORECASE)
        hdr2_match = re.search(hdr2_pattern, input_string, re.IGNORECASE)
        screen_match = re.search(screen_pattern, input_string, re.IGNORECASE)

        # DETERMiTE START AND END POSiTiON OF THE TRACK
        start_pos = 0
        end_pos = len(input_string)
        if year_match:
            end_pos = year_match.start()
        if season_episode_match:
            end_pos = min(end_pos, season_episode_match.start())
        if episode_match:
            end_pos = min(end_pos, episode_match.start())
        if lang_match:
            end_pos = min(end_pos, lang_match.start())
        if audio_match:
            end_pos = min(end_pos, audio_match.start())
        if codec_match:
            end_pos = min(end_pos, codec_match.start())
        if hdr_match:
            end_pos = min(end_pos, hdr_match.start())
        if hdr1_match:
            end_pos = min(end_pos, hdr1_match.start())
        if hdr2_match:
            end_pos = min(end_pos, hdr2_match.start())
        if screen_match:
            end_pos = min(end_pos, screen_match.start())

        # EXTRACT TiTLE
        title = input_string[start_pos:end_pos].strip()

        # EXTRACT EPiSODE/SEASON
        if episode_match:
            episode = episode_match.group()
        else:
            episode = ""

        if season_episode_match:
            episode_season = season_episode_match.group()
            # iF SEASON iS SET, SET SiNGLE EPiSODE TO ""
            episode = ""
        else:
            episode_season = ""

        # EXTRACT LANGUAGE
        if lang_match:
            language = lang_match.group(1)
        else:
            language = ""

        # EXTRACT AUDiO FORMAT
        if audio_match:
            audio = audio_match.group(1)
        else:
            audio = ""

        # EXTRACT RESOLUTiON
        resolution_pattern = r"\d{3,4}p"
        resolution_match = re.search(
            resolution_pattern, input_string, re.IGNORECASE)
        if resolution_match:
            resolution = resolution_match.group()
        else:
            resolution = ""

        # EXTRACT CODEC
        if codec_match:
            codec = codec_match.group(1)
        else:
            codec = ""

        # EXTRACT YEAR
        if year_match:
            year = year_match.group()
        else:
            year = ""

        # EXTRACT 4K TAGS
        if hdr_match:
            hdr = hdr_match.group()
        else:
            hdr = ""

        if hdr1_match:
            hdr1 = hdr1_match.group()
        else:
            hdr1 = ""

        if hdr2_match:
            hdr2 = hdr2_match.group()
        else:
            hdr2 = ""

        # EXTRACT GROUP
        group_pattern = r"-(\w+)$"
        group_match = re.search(group_pattern, input_string, re.IGNORECASE)
        if group_match:
            group = group_match.group(1)
        else:
            group = ""

        # EXTRACT WS/FS
        if screen_match:
            screen = screen_match.group(1)
        else:
            screen = ""

        # CREATE RESULT TUPLE
        #          0        1            2         3      4        5        6          7   8     9      10      11    12
        result = (title, episode, episode_season, year, language,
                  audio, resolution, hdr, hdr1, hdr2, screen, codec, group)
        if (episode or episode_season):
            serie = 1
        else:
            serie = 0

        patterns = [(" ", "."), ("..", "."), ("..", ".")]

        # iF WE CHECK of DUPE
        if dupe == True:
            if serie == 1:
                dupe_str = "{}{}{}{} {}".format(
                    result[0], result[1], result[2], result[4], result[6])
            else:
                dupe_str = "{}{}{}".format(result[0], result[4], result[6])

            for pattern in patterns:
                dupe_str = dupe_str.replace(pattern[0], pattern[1])

            print(f"{CYAN}    [!] Search in PRE-DB: " + str(dupe_str))

            return dupe_str

        # iF iT iS a SERiES USE THE SERiES TEMPLATE
        if serie == 1:
            series_str = RAR_PACK_SERIES.format(series_group=result[12], series_title=result[0], series_episode=result[1], series_episode_season=result[2],
                                                series_resolution=result[6], series_hdr=result[7], series_hdr1=result[8], series_hdr2=result[9], series_screen=result[10])

            for pattern in patterns:
                series_str = series_str.replace(pattern[0], pattern[1])

            if series_str.endswith('.'):
                series_str = series_str.rstrip('.')

            return series_str

        # OTHERWiSE -> MOViE
        else:
            movie_str = RAR_PACK_MOVIE.format(movie_group=result[12], movie_title=result[0], movie_year=result[1],
                                              movie_resolution=result[6], movie_hdr=result[7], movie_hdr1=result[8], movie_hdr2=result[9], movie_screen=result[10])

            for pattern in patterns:
                movie_str = movie_str.replace(pattern[0], pattern[1])

            if movie_str.endswith('.'):
                movie_str = movie_str.rstrip('.')

            return movie_str
    else:
        return input_string

def find_imdb_link(imdb_search):
    # GET ALL NECESERY VARs
    config = configparser.ConfigParser()
    config.read(config_file)
    IMDB_API_KEY = config.get('IMDB', 'IMDB_API_KEY')

    try:
        url = f"https://imdb-api.com/de/API/SearchMovie/{IMDB_API_KEY}/{imdb_search}"
        response = requests.get(url)
        # Wirft eine Ausnahme, wenn der Statuscode nicht erfolgreich ist
        response.raise_for_status()
        data = response.json()

        if data['results']:
            # CHECK iF DESiRED RESULT IS FOUND iN SEARCH RESULTS
            for result in data['results']:
                if result['title'] == imdb_search:
                    imdb_id = result['id']
                    if DEBUG == 1:
                        print(
                            f"{YELLOW}    [*] ID des Films        : {imdb_id}")
                    return f"https://www.imdb.com/title/{imdb_id}/"

            # iF DESiRED RESULT iS NOT FOUND -> RETURN FiRST RESULT
            imdb_id = data['results'][0]['id']
            if DEBUG == 1:
                print(f"{YELLOW}    [*] ID des Films        : {imdb_id}")

            insert_data(imdb_search, imdb_id)

            return f"https://www.imdb.com/title/{imdb_id}/", imdb_id
        else:
            return "", ""

    except requests.exceptions.HTTPError as err:
        # Behandlung von HTTP-Fehlern
        print(f"{RED}    [!] IMDB-API sends a Error - {err}")
        return "", ""
    except requests.exceptions.RequestException as err:
        # Behandlung von anderen Ausnahmen (z.B. Verbindungsfehler)
        print(f"{RED}    [!] IMDB-API sends a Error - {err}")
        return "", ""

def get_imdb_link(movie_complete_path, destination_dir, IMDB_USE):
    movie = os.path.split(movie_complete_path)[1].lower()

    # FiND MOViE NAME
    filename = filter_name(movie)
    # iF EMPTY STRiNG SET TEMP NAME
    if filename == '':
        filename = movie

    # GET iMDB iD
    if IMDB_USE == 1:
        # CHECK WHETHER MOViE OR SERiES
        tmp = filename
        match = re.search(r"(.*?)\b(?:S\d{2}E\d{2}|E\d{2}|german)\b", tmp, flags=re.IGNORECASE)
        imdb_search = match.group(1) if match else ""
        
        imdb_search = re.sub(r"[.,_]", " ", imdb_search)

        # check if movie is in DB
        result = select_data(f"{imdb_search}")
        if result != "":
            return f"https://www.imdb.com/title/{result}", {imdb_search}
        else:
            IMDB_LINK, IMDB_ID = find_imdb_link(imdb_search)
    else:
        IMDB_LINK = ""

    return IMDB_LINK, imdb_search

def create_dirs(source_dir, release_dir_dest):
    dirs = ["Sample"]
    PROOF_DIR, SUBS_DIR = 0, 0

    if linux == 1:
        separator = "/"
    else:
        separator = "\\"

    if os.path.isdir(f"{source_dir}{separator}Proof"):
        dirs.append("Proof")
        PROOF_DIR = 1
    if os.path.isdir(f"{source_dir}{separator}Subs"):
        dirs.append("Subs")
        SUBS_DIR = 1

    for d in dirs:
        dir_path = f"{release_dir_dest}{separator}{d}"
        try:
            os.makedirs(dir_path, exist_ok=True)
        except:
            # DiR EXiSTS
            pass

    return PROOF_DIR, SUBS_DIR

def cut_movie(movie_complete_path, release_dir_dest, filename, CUT_FROM, CUT_TO):
    """
    Cut a movie using mkvmerge.

    Args:
        movie_complete_path (str): The complete path of the movie file.
        destination (str): The destination directory.
        CUT_FROM (int): The starting time (in seconds) of the cut.
        CUT_TO (int): The ending time (in seconds) of the cut.
        release_dir_dest (str): The name of the movie.

    Returns:
        bool: True if the cut was successful and the file was created, False otherwise.
    """
    movie = filename
    sample_file = f"{movie.lower()}_sample.mkv"
    movie_sample = os.path.join(release_dir_dest, "Sample", sample_file)

    if linux == 1:
        sample_cut = f'mkvmerge "{movie_complete_path}" --compression -1:none --split parts:{CUT_FROM}-{CUT_TO} -o "{movie_sample}" >/dev/null 2>&1'
    else:
        sample_cut = f'addons{separator}mkvmerge.exe "{movie_complete_path}" --compression -1:none --split parts:{CUT_FROM}-{CUT_TO} -o "{movie_sample}" > nul'

    try:
        if DEBUG == 1:
            print(f"{YELLOW}    [*] Sample Cut: {sample_cut}")
        os.system(sample_cut)

        # CHECK iF FiLE WAS CREATED
        sample_file = os.path.join(release_dir_dest, "Sample", movie_sample)
        if os.path.isfile(sample_file):
            print(f"{GREEN}    [+] Cutting done {movie}")
            return True
        else:
            print(f"{RED}    [-] Cutting failed for {movie}")
            return False

    except Exception as e:
        print(RED + "    [!] Szene Releaser " +
              ___VERSION___, " Sample Error: %s" % e)
        return False

def create_nfo(movie_complete_path, destination, movie, filename, file_source, IMDB_LINK) -> None:
    # CREATE NFO
    # GET ALL NECESSARY VARs
    config = configparser.ConfigParser()
    config.read(config_file)

    NFO_GROUP_NAME = config.get('NFO', 'NFO_GROUP_NAME')
    NFO_GROUP_NAME_SHORT = config.get('NFO', 'NFO_GROUP_NAME_SHORT')
    MORE_NOTES = config.get('NFO', 'NOTES')

    file = os.path.splitext(movie)[0]
    movie_nfo = f"{destination}{separator}{file}{separator}"
    movie_nfo += f"{filename}.nfo".lower()
    print(f"{YELLOW}    [*] NFO started for {filename}")

    if DEBUG == 1:
        print(f"{YELLOW}    [*] movie_nfo = {movie_nfo}")

    now = datetime.datetime.now()

    if file_source.lower() == "web":
        TOUCH = f" untouched\n                       {MORE_NOTES}"
    else:
        TOUCH = f" {MORE_NOTES}"

    # GET CODEC
    start = os.path.splitext(movie)[0].rfind(
        ".") + 1  # Index des ersten "." plus 1
    # Index des ersten "-" nach dem "." gefunden
    end = os.path.splitext(movie)[0].rfind("-", start)
    codec = os.path.splitext(movie)[0][start:end]

    # CHANGE iT HERE
    GROUP_NAME = f"{NFO_GROUP_NAME}\n\n"

    # PATH TO THE NFO TEMPLATE
    NFO_TEMPLATE = f".{separator}{NFO_GROUP_NAME_SHORT}_nfo.txt"
    # APPEND ON TOP
    NFO_HEADER = f"RELEASE               : {os.path.basename(destination + separator + os.path.splitext(movie)[0])}\nDATE                  : {now.strftime('%d-%m-%Y')}\nSOURCE                : {file_source}\nCODEC                 : {codec}"
    # APPEND ON FOOTER
    NFO_FOOTER = f"IMDB                  : {IMDB_LINK}\n\nNOTES                 :{TOUCH}"
    # CHANGE END!

    # ADD ADDiTiONAL iNFOS TO NFO ON TOP
    write_to_file(movie_nfo, f"{GROUP_NAME}{NFO_HEADER}")

    if linux == 1:
        syntax = f"mediainfo --Inform=file://\"{NFO_TEMPLATE}\"  \"{movie_complete_path}\" >> \"{movie_nfo}\""

        if DEBUG == 1:
            print(
                f"{YELLOW}    [*] movie_complete_path : {movie_complete_path}")
            print(f"{YELLOW}    [*] Mediainfo           : {syntax}")

        os.system(syntax)
    else:
        syntax = f"--Inform=file://\"{NFO_TEMPLATE}\"  \"{movie_complete_path}\" >> \"{movie_nfo}\""

        if DEBUG == 1:
            print(
                f"{YELLOW}    [*] movie_complete_path : {movie_complete_path}")
            print(f"{YELLOW}    [*] Mediainfo           : {syntax}")

        os.system(f"addons{separator}mediainfo.exe " + syntax)

    # AT THE END
    write_to_file(movie_nfo, NFO_FOOTER, "a")

    print(f"{GREEN}    [+] NFO Created for {movie[:-4]}")

def create_nfo_with_template(media_file_content, nfo_template, destination, filename, movie):
    general_duration, general_file_size, video_res, video_bit_rate, audio_string, subs_string = extract_info_of_file(media_file_content)

    file = os.path.splitext(movie)[0]
    movie_nfo = f"{destination}{separator}{file}{separator}"
    movie_nfo += f"{filename}.nfo".lower()

    if DEBUG == 1:
         print(f"{YELLOW}    NFO Template: {nfo_template}")
         print(f"{YELLOW}    NFO: {movie_nfo}")

    key = ["general_duration", "general_file_size", "video_duration", "video_bit_rate", "audio_duration", "audio_bit_rate", "subs_string"]
    value = [general_duration, general_file_size, video_res, video_bit_rate, audio_string, subs_string]

    # Tonspuren
    audios = ""
    for index, audio in enumerate(audio_string):
        if index > 0:
            indentation = calculate_indentation("{audio_string}", nfo_template)
            audio = indentation + audio
        audios += audio + "\n"

    # Subs
    subs = ""
    for index, sub in enumerate(subs_string):
        if index > 0:
            indentation = calculate_indentation("{subtitles}", nfo_template)
            sub = indentation + sub
        subs += sub + "\n"

    # cleanen
    audios = audios.strip()
    subs = subs.strip()

    replacements = {
    "{general_duration}": general_duration,
    "{general_file_size}": general_file_size,
    "{video_res}": video_res,
    "{video_bit_rate}": video_bit_rate,
    "{audio_string}": audios,
    "{subtitles}": subs
    }

    placeholder_replacer(nfo_template, replacements, movie_nfo)

def create_sfv_file(destination_path, filename, SUBS_DIR, PROOF_DIR):
    """Creates SFV file for a given movie and optional directories for subs and proof"""

    # SFV FOR MAIN DiRECTORY
    filename = filename.lower()
    write_to_file(
        f"{destination_path}{separator}{filename}.sfv", "", modus="w+")
    filelist = os.listdir(destination_path)
    filelist.sort()

    if DEBUG == 1:
        print(f"{YELLOW}    [*] filelist: {str(filelist)}")

    # REMOVE UNNECESSARY FiLES FROM LiST
    try:
        if DEBUG == 1:
            print(f"{YELLOW}    [*] Removing unnecessary files from the list")
            print(f"{YELLOW}    [*] Removing SFV {filename}.sfv")
            print(f"{YELLOW}    [*] Removing NFO {filename}.nfo")
            print(f"{YELLOW}    [*] Removing Sample")
            if SUBS_DIR:
                print(f"{YELLOW}    [*] Removing Subs")
            if PROOF_DIR:
                print(f"{YELLOW}    [*] Removing Proof")

        filelist.remove(f"{filename}.sfv")
        filelist.remove(f"{filename}.nfo")
        if "Sample" in filelist:
            smp = filelist.index("Sample")
            del filelist[smp]
        if SUBS_DIR in filelist:
            sub = filelist.index("Subs")
            del filelist[sub]
        if PROOF_DIR in filelist:
            pro = filelist.index("Proof")
            del filelist[pro]

    except Exception as e:
        print(f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

    # ADD FiLES AND THEiR CRC HASH TO SFV
    for file in filelist:
        file2check = f"{destination_path}{separator}{file}"

        try:
            crchash = CRC32_from_file(file2check)
        except Exception as e:
            print(f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

        write_to_file(
            f"{destination_path}{separator}{filename}.sfv", f"{file} {crchash}\n")

    # SFV FOR SUBS DiRECTORY
    if SUBS_DIR == 1:
        write_to_file(
            f"{destination_path}{separator}Subs{separator}{filename}_subs.sfv", "", modus="w+")
        filelist_subs = os.listdir(
            f"{destination_path}{separator}Subs{separator}")
        filelist_subs.sort()

        try:
            filelist_subs.remove(f"{filename}_subs.sfv")
        except Exception as e:
            print(f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

        for file in filelist_subs:
            file2check = f"{destination_path}{separator}Subs{separator}{file}"

            try:
                crchash = CRC32_from_file(file2check)
            except Exception as e:
                print(
                    f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

            write_to_file(
                f"{destination_path}{separator}Subs{separator}{filename}_subs.sfv", f"{file} {crchash}\n")

    # SFV FOR PROOF DiRECTORY
    if PROOF_DIR == 1:
        write_to_file(
            f"{destination_path}{separator}Proof{separator}{filename}_proof.sfv", "", modus="w+")
        filelist_proof = os.listdir(
            f"{destination_path}{separator}Proof{separator}")
        filelist_proof.sort()

        try:
            filelist_proof.remove(f"{filename}_proof.sfv")
        except Exception as e:
            print(f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

        for file in filelist_proof:
            file2check = f"{destination_path}{separator}Proof{separator}{file}"

            try:
                crchash = CRC32_from_file(file2check)
            except Exception as e:
                print(
                    f"{RED}    [!] Szene Releaser {___VERSION___} Error: {e}")

            write_to_file(
                f"{destination_path}{separator}Proof{separator}{filename}_proof.sfv", f"{file} {crchash}\n")

def ask_yes_no_imdb(question, name):
    while True:
        user_input = input(
            f"\n{BLUE}    {question} ((Y)es/(C)ustom): ").strip().lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['c', 'custom']:
            custom_input = input(f"{BLUE}    Input: ")
            return get_valid_input(custom_input, name)
        else:
            print(
                f"{RED}    [!] Invalid input. Please answer with 'Y' or 'C'.")

def ask_yes_no_dupe(question, default="Y"):
    valid_responses = {"y": True, "n": False, "c": "cancle", "i": "ignore"}
    if default.lower() not in valid_responses:
        default = "Y"
    prompt = f"{question} ({default}/I/C): "
    while True:
        user_input = input(prompt)
        if user_input.lower() in valid_responses:
            return valid_responses[user_input.lower()]
        elif user_input == "":
            return valid_responses[default]

def get_valid_input(input, name):
    while True:
        if re.match(r'^[A-Za-z0-9/:._-]+$', input):

            if DEBUG == 1:
                print(f"{YELLOW}    [*] IMDB-DB = Name: {name} Link: {input}")

            delete_data(name)
            insert_data(name, input)
            return input
        else:
            print(
                f"{RED}    [!] Invalid input. Allowed characters are alphanumeric, '.', '_', and '-'.")

def extract_info_of_file(source):
    general_duration = general_file_size = video_res = video_bit_rate = audio_string = ""
    text_entries = []
    audio_blocks = []
    current_block = {}
    is_audio_block = False
    is_text_block = False
    current_text_block = {}

    with open(source, "r") as file:
        content = file.read()

    # Parsing ohne Blocks - Audio und Text
    lines = content.split("\n")
    for line in lines:
        if line.startswith("Audio"):
            if current_block:
                audio_blocks.append(current_block)
                current_block = {}
            is_audio_block = True
            is_text_block = False
        elif line.startswith("Text"):
            if current_text_block:
                text_entries.append(current_text_block)
                current_text_block = {}
            is_audio_block = False
            is_text_block = True
        elif is_audio_block:
            if ":" in line:
                key, value = line.split(":", 1)
                current_block[key.strip()] = value.strip()
        elif is_text_block:
            if ":" in line:
                key, value = line.split(":", 1)
                current_text_block[key.strip()] = value.strip()

    # Füge den letzten Audio- und Text-Block hinzu, falls vorhanden
    if current_block:
        audio_blocks.append(current_block)
    if current_text_block:
        text_entries.append(current_text_block)

    # Verarbeite die Audio-Blöcke
    audio_string = []
    for audio_data in audio_blocks:
        audio_lang = audio_data.get("Language")
        audio_format = audio_data.get("Format")
        audio_channel = audio_data.get("Channel(s)")
        audio_bitrate = audio_data.get("Bit rate")
        audio_string.append(
            f"{audio_lang} {audio_format} {audio_channel} @ {audio_bitrate}")

    # Verarbeite die Text-Einträge
    subs_string = []
    for text_data in text_entries:
        sub = text_data.get("Title")
        # Hier weitere Text-Daten verarbeiten...
        subs_string.append(sub)

    # Split content into blocks based on empty lines
    blocks = content.split("\n\n")

    # Process each block
    for block in blocks:
        lines = block.strip().split("\n")
        section = lines[0]

        # Process different sections
        if section == "General":
            # Process General section
            general_data = {}
            for line in lines[1:]:
                key, value = line.split(":", 1)
                general_data[key.strip()] = value.strip()

            # Access specific values
            general_duration = general_data.get("Duration")
            general_file_size = general_data.get("File size")
            # ...

        elif section == "Video":
            # Process Video section
            video_data = {}
            for line in lines[1:]:
                key, value = line.split(":", 1)
                video_data[key.strip()] = value.strip()

            # Access specific values
            video_res_1 = video_data.get("Width")
            video_res_1 = video_res_1.replace(" pixels", "")

            video_res_2 = video_data.get("Height")
            video_res_2 = video_res_2.replace(" pixels", "")

            video_res = f"{video_res_1}x{video_res_2}"
            video_bit_rate = video_data.get("Bit rate")
            # ...

    return general_duration, general_file_size, video_res, video_bit_rate, audio_string, subs_string

def placeholder_replacer(nfo_template_file, replacements, target_nfo):
    if DEBUG == 1:
         print(f"{YELLOW}    NFO-File: {nfo_template_file} ZIEL NFO: {target_nfo}")

    with open(nfo_template_file, "r") as file:
        original_content = file.read()

    for key, value in replacements.items():
        original_content = original_content.replace(key, value)

    with open(target_nfo, "w") as target_file:
        target_file.write(original_content)

def calculate_indentation(placeholder, target_file):
    with open(target_file, "r") as file:
        content = file.read()
        start_index = content.index(placeholder)
        end_index = start_index + len(placeholder)
        line_start_index = content.rfind("\n", 0, start_index) + 1
        line_end_index = content.find("\n", end_index)
        line = content[line_start_index:line_end_index]
        indentation = start_index - line_start_index
        return " " * indentation

def run(source_dir, destination_dir, movie_complete_path, config_file, file_source='WEB', verbose_mode=False):
    # GET ALL NECESSARY VARs
    config = configparser.ConfigParser()
    config.read(config_file)

    DUPE_USE = config.getint('DUPE', 'DUPE_USE')
    FTP_USE = config.getint('FTP', 'FTP_USE')
    FTP_HOST = config.get('FTP', 'FTP_HOST')
    FTP_PORT = config.getint('FTP', 'FTP_PORT')
    FTP_SSL = config.get('FTP', 'FTP_SSL')
    FTP_USER = config.get('FTP', 'FTP_USER')
    FTP_PASS = config.get('FTP', 'FTP_PASS')
    IRC_USE = config.getint('IRC', 'IRC_USE')
    IRC_SERVER = config.get('IRC', 'IRC_SERVER')
    IRC_SERVER_PW = config.get('IRC', 'IRC_SERVER_PW')
    IRC_PORT = config.getint('IRC', 'IRC_PORT')
    IRC_BN = config.get('IRC', 'IRC_BN')
    IRC_CHAN = config.get('IRC', 'IRC_CHAN')
    IRC_CHAN_PW = config.get('IRC', 'IRC_CHAN_PW')
    IRC_MSG = config.get('IRC', 'IRC_MSG')
    CUT_FROM = config.get('SAMPLE', 'CUT_FROM')
    CUT_TO = config.get('SAMPLE', 'CUT_TO')
    NFO = config.getint('NFO', 'NFO_USE')
    NFO_GROUP_NAME_SHORT = config.get('NFO', 'NFO_GROUP_NAME_SHORT')
    IMDB_USE = config.getint('IMDB', 'IMDB_USE')
    TG_USE = config.getint('TELEGRAM', 'TG_USE')
    BOT_ID = config.get('TELEGRAM', 'BOT_ID')
    CHAN_ID = config.get('TELEGRAM', 'CHAN_ID')
    ERROR_CHAN_ID = config.get('TELEGRAM', 'ERROR_CHAN_ID')
    TELEGRAM_CAPTIONS_FILE = config.get('TELEGRAM', 'TELEGRAM_CAPTIONS_FILE')
    NFO_TEMPLATE_USE = config.getint('NFO_TEMPLATE', 'NFO_TEMPLATE_USE')
    NFO_TEMPLATE_FILE = config.get('NFO_TEMPLATE', 'NFO_TEMPLATE_FILE')

    movie = os.path.split(movie_complete_path)[1]
    release_dir_dest = f"{destination_dir}{separator}{movie[:-4]}"

    # FiND MOViE NAME
    filename = extract_info(movie[:-4])

    # Check if we are create a dupe
    if DUPE_USE == 1:
        PREDB_URL = config.get('DUPE', 'PREDB_URL')
        PREDB_BN = config.get('DUPE', 'PREDB_BN')
        PREDB_PW = config.get('DUPE', 'PREDB_PW')
        dupe_check_srrdb(extract_info(movie[:-4], dupe=True))

    # GET iMDB LiNK
    LINK, S = get_imdb_link(movie_complete_path, destination_dir, IMDB_USE)

    if verbose_mode == True:
        IMDB_LINK = ask_yes_no_imdb(f"Is the Link {LINK} right?", S)
    else:
        IMDB_LINK = LINK

    # GET TELEGRAM CAPTiON
    if TG_USE == 1:
        tg_captions = load_random_sentence(TELEGRAM_CAPTIONS_FILE)

    if DEBUG == 1:
        print(f"{YELLOW}    [*] Source              : {source_dir}")
        print(f"{YELLOW}    [*] Destination         : {destination_dir}")
        print(f"{YELLOW}    [*] Release Dir         : {release_dir_dest}")
        print(f"{YELLOW}    [*] Movie_Complete_Path : {movie_complete_path}")
        print(f"{YELLOW}    [*] Movie_File          : {movie}")
        print(f"{YELLOW}    [*] File_Source         : {file_source}")
        print(f"{YELLOW}    [*] Filename            : {filename}")
        print(f"{YELLOW}    [*] IMDB_LINK           : {IMDB_LINK}")
        if TG_USE == 1:
            print(f"{YELLOW}    [*] Telegramm_captions  : {tg_captions}\n\n\n")
        print("    ################################################")
        input("    Now check all Vars then press enter...\n\n\n")

    print(f"{CYAN}    [!!] Started for {movie}")

    print(f"{YELLOW}    [*] Creating Dirs for {movie}")
    # CREATE DiRECTORiES
    PROOF_DIR, SUBS_DIR = create_dirs(source_dir, release_dir_dest)
    print(f"{GREEN}    [+] Creating done for {movie}")

    if movie is not None:
        cut_movie(movie_complete_path, release_dir_dest, filename, CUT_FROM, CUT_TO)

    if NFO == 1:
        create_nfo(movie_complete_path, destination_dir, movie, filename, file_source, IMDB_LINK)

    if NFO_TEMPLATE_USE == 1:
        mediainfo_file = f"{source_dir}{separator}mediainfo.txt"
        
        os.system(f"mediainfo  {movie_complete_path} > {mediainfo_file}")
        
        create_nfo_with_template(mediainfo_file, NFO_TEMPLATE_FILE, destination_dir, filename, movie)
 
    # START RAR
    print(f"{YELLOW}    [*] Packing Started for {movie}")
    ext = "-n*" + ".mkv"
    packing(ext, release_dir_dest, filename, movie_complete_path)

    # SUBS
    if SUBS_DIR == 1:
        print(f"{YELLOW}    [*] Subs Packing for {movie}")
        ext = "-n*.*"
        packing(ext, f"{release_dir_dest}{separator}Subs{separator}",
                f"{filename}-subs", f"{source_dir}{separator}Subs{separator}")
        print(f"{GREEN}    [+] Subs Packing done for {movie}")

    # PRo0F
    if PROOF_DIR == 1:
        print(f"{YELLOW}    [*] Proof Packing for {movie}")
        ext = "-n*.jpg"
        packing(ext, f"{release_dir_dest}{separator}Proof{separator}",
                f"{filename}-proof", f"{source_dir}{separator}Proof{separator}")
        print(f"{GREEN}    [+] Proof Packing done for {movie}")

    print(f"{GREEN}    [+] All Packing done for {movie}")

    # CREATE A SFV FiLE OF FiLE iN DESTiNATiON
    print(f"{YELLOW}    [*] SFV Creating Started for {movie}")
    create_sfv_file(release_dir_dest, filename, SUBS_DIR, PROOF_DIR)
    print(f"{GREEN}    [+] SFV Creating done for {movie}")

    # ESTABLiSH FTP CONNECTiON
    # CONNECT
    if FTP_USE == 1:
        print(f"{YELLOW}    [*] Connecting to FTP and Uploading for {movie}")

        if FTP_SSL != 1:
            with FTP(FTP_HOST, FTP_PORT) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                upload(ftp, release_dir_dest)

        else:
            print(f"{YELLOW}    [*] Connectig to FTP and Uploading...")
            print(f"{YELLOW}    [*] using SSL to connect...")

            with FTP_TLS(FTP_HOST, FTP_PORT) as ftps:
                ftps.login(FTP_USER, FTP_PASS)
                upload(ftps, release_dir_dest)

        print(f"{GREEN}    [+] Upload for {movie} done")

    # DEFiNE FUNCTiON FOR SENDiNG MESSAGES TO iRC
    def send_irc_msg(msg):
        irc = IRC()
        con = irc.connect(IRC_SERVER, IRC_PORT, IRC_CHAN,
                          IRC_BN, IRC_SERVER_PW, IRC_CHAN_PW)
        if con == True:
            irc.send(IRC_CHAN, f":{msg} {int(time())}")
            time.sleep(5)
            irc.quit()
            print(f"{GREEN}   [+] IRC Send. {msg} {int(time())}")

    # CONNECT TO iRC iF REQUiRED
    if IRC_USE == 1:
        # SEND MESSAGE TO iRC
        release_name = os.path.basename(
            os.path.normpath(release_dir_dest + '/'))
        irc_msg = IRC_MSG.replace('<RELEASE>', release_name)
        send_irc_msg(irc_msg)

    # SEND PRE TO TELEGRAM
    if TG_USE == 1:
        try:
            URL = f"https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={CHAN_ID}&text={tg_captions}\n{os.path.basename(os.path.normpath(release_dir_dest + '/'))}"
            r = requests.post(URL)

            if DEBUG == 1:
                print(f"{YELLOW}    [*] Send Message to Telegramm : {URL}")

            if r.status_code != 200:
                URL = f"https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={ERROR_CHAN_ID}&text=Fehler bei {NFO_GROUP_NAME_SHORT} PRE: HTTP Error"
                r = requests.post(URL)
        except Exception as e:
            URL = f"https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={ERROR_CHAN_ID}&text=Fehler bei {NFO_GROUP_NAME_SHORT} PRE: {e.__str__()} occurred:\n{e.args}"
            r = requests.post(URL)

        if linux != 1:
            os.unlink("log.log")
    # else:
    #    print(f"{RED}    [!] Szene Releaser {___VERSION___} Error: No Video file")

def credits():
    print(f"""{WHITE}\n\n
    Feel free to donate:
    
    BTC        15tnxCkx22XkZV1tH7gYDY3MXcF7dinZWW
    BTCash     1QJeu2oYfefcenB7HrRL6aGiWCZr2eJvQq
    DASH       XgHeA9JAHMMtUFKbHHS5bheao6W9FZBB5b
    ETH        0x66B1Fb67745581A3C60bf1ddB8C6920a81af3757
    LTC        LN39sMfgUWDTaPNuezy3TLzjA5bmgsiDXE
    DOGE       D9uiMkvRo9aQYtcWjkztSYiYgXjhjDLtMh
             
    Thanks a lot!""")

def banner():
    print(BLUE+""" 
    ███████╗███████╗███████╗███╗   ██╗███████╗    ██████╗ ███████╗██╗     ███████╗ █████╗ ███████╗███████╗██████╗ 
    ██╔════╝╚══███╔╝██╔════╝████╗  ██║██╔════╝    ██╔══██╗██╔════╝██║     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗
    ███████╗  ███╔╝ █████╗  ██╔██╗ ██║█████╗      ██████╔╝█████╗  ██║     █████╗  ███████║███████╗█████╗  ██████╔╝
    ╚════██║ ███╔╝  ██╔══╝  ██║╚██╗██║██╔══╝      ██╔══██╗██╔══╝  ██║     ██╔══╝  ██╔══██║╚════██║██╔══╝  ██╔══██╗
    ███████║███████╗███████╗██║ ╚████║███████╗    ██║  ██║███████╗███████╗███████╗██║  ██║███████║███████╗██║  ██║
    ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝

    © by %s - 2019-2023   (v%s)
    --------------------------------------------------""" % (___AUTHOR___, ___VERSION___) + ENDC)

if __name__ == '__main__':
    if len(sys.argv) >= 5:
        banner()

        print(f"    [*] Szene Releaser check for Update")
        updater.main()

        # CHECK iF FiLE EXiSTS
        input_folder = sys.argv[1]
        destination_dir = sys.argv[2]
        file_source = sys.argv[3]
        config_file = sys.argv[4]

        # check if Config exists
        if os.path.isfile(f"./config/{config_file}"):
            config_file = f"./config/{config_file}"
        else:
            print(
                f"{RED}    [*] ./config/{config_file} doesnt exits, make sure it is in path!")
            sys.exit(1)
        # check if database file exists
        if not os.path.isfile(f"{DATABASE_FILE}"):
            create_database()
    elif len(sys.argv) >= 4:
        banner()

        if not os.path.isfile(f"{DATABASE_FILE}"):
            create_database()

        input_folder, destination_dir, file_source = sys.argv[1:]

        # check if database file exists
        if not os.path.isfile(f"{DATABASE_FILE}"):
            create_database()

    else:
        banner()
        print(f"\n    usage: {sys.argv[0]} \"Source Directory\" \"Destination Directory\" \"File Source e.g WEB or BR\" \"Optional: custom_config.ini\" \"verbose\" run it in interactiv mode\n\n\n")
        sys.exit(1)

    if DEBUG == 1:
        print(f"{YELLOW}    [*] ARGV               : {len(sys.argv)}")
        print(f"{YELLOW}    [*] ARGV1              : {sys.argv[1]}")
        print(f"{YELLOW}    [*] ARGV2              : {sys.argv[2]}")
        print(f"{YELLOW}    [*] ARGV3              : {sys.argv[3]}")
        print(f"{YELLOW}    [*] ARGV4              : {sys.argv[4]}")
        print(f"{YELLOW}    [*] INI FILE           : {config_file}")

    if "verbose" in sys.argv:
        verbose_mode = True
    else:
        verbose_mode = False

    def iterate_video_files(input_folder):
        for filename in os.listdir(input_folder):
            if filename.endswith(".mkv") or filename.endswith(".mp4"):
                yield os.path.join(input_folder, filename)

    # CREATE THREADS FOR EACH ViDEO FiLE FOUND
    threads = []
    for video_file in iterate_video_files(input_folder):
        thread = threading.Thread(target=run, args=(
            input_folder, destination_dir, video_file, config_file, file_source, verbose_mode, ))
        thread.start()
        threads.append(thread)

    # WAiTiNG FOR ALL THREADS TO END
    for thread in threads:
        thread.join()

    print(f"    [*] Szene Releaser {___VERSION___} Finish!\n")
    credits()
# eof
