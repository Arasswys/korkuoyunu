#!/usr/bin/env python3
import os
import sys
import ctypes
import random
import string
import time
import threading
import subprocess
import shutil
import tempfile
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(['"' + arg + '"' for arg in sys.argv]), None, 1
    )
    sys.exit(0)

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# =============================================================================
# ZORLUK SEVİYELERİ
# =============================================================================
DIFFICULTY = {
    "kolay": {
        "name": "KOLAY",
        "description": "Yeni avcılar icin. Hayalet yavas, kanitlar belirgin.",
        "color": "#00ff00",
        "sanity_drain": 0.4,
        "hunt_threshold": 15,
        "hunt_chance": 0.02,
        "false_positive_rate": 0.0,
        "evidence_chance": 0.75,
        "ghost_wait_min": 6,
        "ghost_wait_max": 14,
        "sanity_start": 100,
        "item_bonus": 1,
        "hunt_duration_min": 5,
        "hunt_duration_max": 9,
        "hunt_sanity_drain": 0.5,
        "score_multiplier": 0.7,
        "scan_hint": True,
        "ghost_activity_mult": 0.7,
    },
    "orta": {
        "name": "ORTA",
        "description": "Dengeli deneyim. Standart zorluk.",
        "color": "#ffaa00",
        "sanity_drain": 0.7,
        "hunt_threshold": 25,
        "hunt_chance": 0.04,
        "false_positive_rate": 0.08,
        "evidence_chance": 0.6,
        "ghost_wait_min": 4,
        "ghost_wait_max": 10,
        "sanity_start": 100,
        "item_bonus": 0,
        "hunt_duration_min": 7,
        "hunt_duration_max": 14,
        "hunt_sanity_drain": 1.2,
        "score_multiplier": 1.0,
        "scan_hint": False,
        "ghost_activity_mult": 1.0,
    },
    "zor": {
        "name": "ZOR",
        "description": "Uzman avcılar icin. Hayalet agresif, kanitlar belirsiz.",
        "color": "#ff0000",
        "sanity_drain": 1.2,
        "hunt_threshold": 40,
        "hunt_chance": 0.07,
        "false_positive_rate": 0.18,
        "evidence_chance": 0.42,
        "ghost_wait_min": 3,
        "ghost_wait_max": 7,
        "sanity_start": 85,
        "item_bonus": -1,
        "hunt_duration_min": 9,
        "hunt_duration_max": 18,
        "hunt_sanity_drain": 2.0,
        "score_multiplier": 1.5,
        "scan_hint": False,
        "ghost_activity_mult": 1.4,
    }
}

# =============================================================================
# 10 KANİT TÜRÜ
# =============================================================================
EVIDENCE_TYPES = {
    "isee_file": {
        "name": "ISEE.md Dosyasi",
        "short": "ISEE.md",
        "description": "Masaustunde gizemli ISEE.md dosyasi olusturur",
        "tool": "Dosya Tarayici",
        "icon": "[EYE]",
        "scan_time": (2, 4),
        "detail": "Hayaletin biraktigi gizemli dosyalari tarar."
    },
    "signal_emission": {
        "name": "Sinyal Yayimi",
        "short": "Sinyal",
        "description": "Radyo frekansinda paranormal sinyal yayar",
        "tool": "Sinyal Dedektoru",
        "icon": "[SIG]",
        "scan_time": (2, 5),
        "detail": "Paranormal radyo frekanslarini algilar."
    },
    "emf_spike": {
        "name": "EMF Yukselmesi",
        "short": "EMF",
        "description": "EMF seviyesi 5'e kadar cikiyor",
        "tool": "EMF Olcer",
        "icon": "[EMF]",
        "scan_time": (1, 3),
        "detail": "Elektromanyetik alan olcer. Level 5 = paranormal."
    },
    "temp_drop": {
        "name": "Dondurucu Soguk",
        "short": "Soguk",
        "description": "Sicaklik -10C altina duser",
        "tool": "Termometre",
        "icon": "[FRZ]",
        "scan_time": (2, 4),
        "detail": "Ortam sicakligindaki anormal dususleri tespit eder."
    },
    "ghost_writing": {
        "name": "Hayalet Yazisi",
        "short": "Yazi",
        "description": "Deftere gizemli semboller yazar",
        "tool": "Hayalet Defteri",
        "icon": "[WRT]",
        "scan_time": (3, 6),
        "detail": "Defterdeki gizemli yazilari analiz eder."
    },
    "folder_anomaly": {
        "name": "Klasor Anomalisi",
        "short": "Klasor",
        "description": "Masaustunde garip klasorler olusturur",
        "tool": "Klasor Izleyici",
        "icon": "[FLD]",
        "scan_time": (2, 4),
        "detail": "Anormal klasor olusumlarini takip eder."
    },
    "ghost_process": {
        "name": "Hayalet Process",
        "short": "Process",
        "description": "Arka planda gizli islemler olusturur",
        "tool": "Process Dedektoru",
        "icon": "[PRC]",
        "scan_time": (2, 5),
        "detail": "Gizli arka plan islemlerini tespit eder."
    },
    "spirit_box": {
        "name": "Spirit Box Yaniti",
        "short": "Spirit Box",
        "description": "Spirit box uzerinden sesli yanit verir",
        "tool": "Spirit Box",
        "icon": "[SPB]",
        "scan_time": (3, 6),
        "detail": "Radyo frekanslari uzerinden hayaletle iletisim kurar."
    },
    "ghost_orb": {
        "name": "Hayalet Kureleri",
        "short": "Kureler",
        "description": "Kamera goruntusunde parlak kureler belirir",
        "tool": "Gece Gorush Kamerasi",
        "icon": "[ORB]",
        "scan_time": (3, 5),
        "detail": "Gece gorush kamerasinda parlak kureleri arar."
    },
    "uv_fingerprint": {
        "name": "UV Parmak Izi",
        "short": "UV Izi",
        "description": "UV isik altinda parmak izleri gorunur",
        "tool": "UV Lambasi",
        "icon": "[UV]",
        "scan_time": (2, 4),
        "detail": "Ultraviyole isikla hayalet parmak izlerini arar."
    }
}

# =============================================================================
# 27 HAYALET
# =============================================================================
GHOST_DATABASE = {
    "Wraith": {
        "turkish_name": "Hayalet Ruh",
        "description": "Duvarlardan gecebilen kadim bir varlik.",
        "lore": "Ortacag'dan beri bilinen en eski hayalet turu. Fiziksel engelleri asabilir.",
        "evidence": ["isee_file", "spirit_box", "emf_spike"],
        "danger_level": 7,
        "special": "Duvarlari gecebilir, farkli konumlara aninda ulasir.",
        "weakness": "Tuz uzerinde yuruyunce yavaslar ve iz birakir.",
        "hunt_speed": 1.0, "hunt_speed_var": 0.2,
        "activity_rate": 0.25, "shyness": 0.3, "aggression": 0.5, "intelligence": 0.8,
        "unique_ability": "teleport",
        "ability_desc": "Farkli dizinlere aninda dosya birakabilir",
        "footstep": "hafif surukleme",
        "ascii_art": "  .---.\n / o o \\\n|   ^   |\n \\=====/\n   | |"
    },
    "Phantom": {
        "turkish_name": "Fantom",
        "description": "Goruntulendiginde kaybolan gizemli varlik.",
        "lore": "Isik ile ozel iliskisi olan varlik, gozlemlendikce zayiflar.",
        "evidence": ["ghost_orb", "spirit_box", "uv_fingerprint"],
        "danger_level": 6,
        "special": "Gozlemlendikce aktivitesi azalir.",
        "weakness": "Kamera ile goruntulendikce gucunu kaybeder.",
        "hunt_speed": 0.8, "hunt_speed_var": 0.1,
        "activity_rate": 0.2, "shyness": 0.6, "aggression": 0.4, "intelligence": 0.7,
        "unique_ability": "invisibility",
        "ability_desc": "Gozlemlendikce gorunmez olur",
        "footstep": "sessiz",
        "ascii_art": "  .---.\n / o o \\\n|  ---  |\n \\_____/\n   |||"
    },
    "Poltergeist": {
        "turkish_name": "Gurultucu Hayalet",
        "description": "Nesneleri firlatma yetenegine sahip gurultucu ruh.",
        "lore": "Almanca 'gurultucu ruh'. Fiziksel dunyayla en cok etkilesen tur.",
        "evidence": ["folder_anomaly", "ghost_process", "uv_fingerprint"],
        "danger_level": 8,
        "special": "Dosya ve klasorleri firlatir, masaustunde kaos yaratir.",
        "weakness": "Bos ortamda gucunu kaybeder.",
        "hunt_speed": 1.2, "hunt_speed_var": 0.3,
        "activity_rate": 0.35, "shyness": 0.1, "aggression": 0.8, "intelligence": 0.5,
        "unique_ability": "telekinesis",
        "ability_desc": "Dosyalari firlatir ve klasorleri dagitir",
        "footstep": "agir adimlar",
        "ascii_art": "  /!\\ /!\\\n / ! X ! \\\n|  !!!!!  |\n \\_______/"
    },
    "Banshee": {
        "turkish_name": "Ciglikci",
        "description": "Tek bir kisiyi hedef alan olum habercisi.",
        "lore": "Irlanda mitolojisinden gelen olum habercisi.",
        "evidence": ["emf_spike", "ghost_orb", "uv_fingerprint"],
        "danger_level": 9,
        "special": "Hedefine kilitlenir, digerlerini yok sayar.",
        "weakness": "Hac onu uzak tutar ve hedefini degistirir.",
        "hunt_speed": 1.3, "hunt_speed_var": 0.1,
        "activity_rate": 0.2, "shyness": 0.4, "aggression": 0.9, "intelligence": 0.6,
        "unique_ability": "scream",
        "ability_desc": "Oldurucu ciglik atar, sanity hizla duser",
        "footstep": "ciglik",
        "ascii_art": "   ___\n  / x \\\n | X X |\n |  O  |\n  \\___/"
    },
    "Jinn": {
        "turkish_name": "Cin",
        "description": "Elektrikle guclenen toprak varligi.",
        "lore": "Islam mitolojisinden gelen dumansiz atesten yaratilmis varlik.",
        "evidence": ["signal_emission", "emf_spike", "ghost_process"],
        "danger_level": 7,
        "special": "Elektronik cihazlari manipule eder.",
        "weakness": "Elektrik kesildiginde cok zayiflar.",
        "hunt_speed": 1.1, "hunt_speed_var": 0.4,
        "activity_rate": 0.3, "shyness": 0.2, "aggression": 0.6, "intelligence": 0.9,
        "unique_ability": "electric_surge",
        "ability_desc": "Elektronik cihazlari bozar ve kontrol eder",
        "footstep": "elektrik cizirtisi",
        "ascii_art": "   /\\\n  /  \\\n / ~~ \\\n| >--< |\n \\____/"
    },
    "Mare": {
        "turkish_name": "Gece Kabusu",
        "description": "Karanligin gucunu kullanan kabus varligi.",
        "lore": "Uyuyan insanlarin gogusune oturup kabus gorduren kadim varlik.",
        "evidence": ["ghost_writing", "spirit_box", "ghost_orb"],
        "danger_level": 6,
        "special": "Karanlikta cok guclu, isikta zayif.",
        "weakness": "Mum ve isik onu buyuk olcude zayiflatir.",
        "hunt_speed": 0.9, "hunt_speed_var": 0.5,
        "activity_rate": 0.25, "shyness": 0.4, "aggression": 0.7, "intelligence": 0.6,
        "unique_ability": "darkness_control",
        "ability_desc": "Isiklari sondurur ve karanlikta guclanir",
        "footstep": "fisildama",
        "ascii_art": "  .===.\n / ~~~ \\\n| |   | |\n \\|___|/"
    },
    "Revenant": {
        "turkish_name": "Donen Olu",
        "description": "Normalde yavas ama hedefini gorunde inanilmaz hizlanan varlik.",
        "lore": "Mezarindan donmus intikam arayan olu.",
        "evidence": ["temp_drop", "ghost_process", "ghost_writing"],
        "danger_level": 10,
        "special": "Av sirasinda en hizli hayalet.",
        "weakness": "Hedefini goremezse son derece yavas.",
        "hunt_speed": 1.8, "hunt_speed_var": 1.2,
        "activity_rate": 0.15, "shyness": 0.6, "aggression": 1.0, "intelligence": 0.4,
        "unique_ability": "speed_burst",
        "ability_desc": "Hedefini gorünce hizi 3 katina cikar",
        "footstep": "agir surukleme",
        "ascii_art": "  .----.\n / R.I.P \\\n|  _____  |\n|_________|"
    },
    "Shade": {
        "turkish_name": "Golge",
        "description": "Son derece utangac bir varlik.",
        "lore": "En zayif ama en sinsi hayalet turlerinden.",
        "evidence": ["emf_spike", "ghost_writing", "ghost_orb"],
        "danger_level": 4,
        "special": "Cok utangac, nadiren aktivite gosterir.",
        "weakness": "Grup halindeyken neredeyse hic aktivite gostermez.",
        "hunt_speed": 0.6, "hunt_speed_var": 0.1,
        "activity_rate": 0.1, "shyness": 0.9, "aggression": 0.2, "intelligence": 0.5,
        "unique_ability": "extreme_shyness",
        "ability_desc": "Gozlemlendikce tamamen kaybolur",
        "footstep": "sessiz",
        "ascii_art": "  ___\n / . \\\n| . . |\n|  _  |\n \\___/"
    },
    "Demon": {
        "turkish_name": "Iblis",
        "description": "En agresif hayalet turu. Sebepsiz saldirir.",
        "lore": "Cehennemden gelen en tehlikeli varlik.",
        "evidence": ["isee_file", "ghost_writing", "temp_drop"],
        "danger_level": 10,
        "special": "Minimum sanity gereksinimi olmadan avlanir.",
        "weakness": "Hac onu gecici olarak durdurur.",
        "hunt_speed": 1.5, "hunt_speed_var": 0.2,
        "activity_rate": 0.35, "shyness": 0.05, "aggression": 1.0, "intelligence": 0.7,
        "unique_ability": "rage_hunt",
        "ability_desc": "Sanity'den bagimsiz avlanabilir",
        "footstep": "gurleme",
        "ascii_art": "  /\\  /\\\n /  \\/  \\\n| >    < |\n \\  \\/  /\n  \\____/"
    },
    "Yurei": {
        "turkish_name": "Japon Hayaleti",
        "description": "Tutsuyle kovulabilen Japon ruhu.",
        "lore": "Olenlerin intikam icin donen ruhu.",
        "evidence": ["temp_drop", "ghost_orb", "folder_anomaly"],
        "danger_level": 5,
        "special": "Odasindan cok uzaklasmaz.",
        "weakness": "Tutsu ile odaya hapsedilebilir.",
        "hunt_speed": 0.7, "hunt_speed_var": 0.1,
        "activity_rate": 0.2, "shyness": 0.5, "aggression": 0.5, "intelligence": 0.6,
        "unique_ability": "room_lock",
        "ability_desc": "Tutsu ile odaya hapsedilebilir",
        "footstep": "hafif ayak",
        "ascii_art": "  .---.\n / o o \\\n|  ---  |\n  '--'\n  |  |"
    },
    "Oni": {
        "turkish_name": "Oni",
        "description": "Cok aktif ve guclu Japon iblisi.",
        "lore": "Japon folklorundeki iblis.",
        "evidence": ["emf_spike", "signal_emission", "temp_drop"],
        "danger_level": 8,
        "special": "En aktif hayalet.",
        "weakness": "Cok aktif oldugu icin kolayca tespit edilir.",
        "hunt_speed": 1.3, "hunt_speed_var": 0.2,
        "activity_rate": 0.4, "shyness": 0.05, "aggression": 0.8, "intelligence": 0.5,
        "unique_ability": "constant_activity",
        "ability_desc": "Neredeyse surekli aktif",
        "footstep": "agir adimlar",
        "ascii_art": "  /\\_/\\\n / O O \\\n|  >w<  |\n \\_____/"
    },
    "Yokai": {
        "turkish_name": "Yokai",
        "description": "Ses ile cekilen Japon ruhu.",
        "lore": "Dogaustu varliklarin genel adi.",
        "evidence": ["ghost_writing", "ghost_process", "spirit_box"],
        "danger_level": 5,
        "special": "Yakininda konusulursa agresiflesir.",
        "weakness": "Sessiz kalirsan aktivitesi azalir.",
        "hunt_speed": 0.8, "hunt_speed_var": 0.3,
        "activity_rate": 0.22, "shyness": 0.4, "aggression": 0.5, "intelligence": 0.6,
        "unique_ability": "sound_sensitivity",
        "ability_desc": "Sese tepki verir, sessizlikte sakinlesir",
        "footstep": "tirmalama",
        "ascii_art": "   ___\n  (   )\n ( O O )\n  ( > )\n   ---"
    },
    "Hantu": {
        "turkish_name": "Hantu",
        "description": "Sogukta guclenen Malay kokenli ruh.",
        "lore": "Guneydogu Asya mitolojisinden gelen soguk ruhu.",
        "evidence": ["temp_drop", "uv_fingerprint", "ghost_orb"],
        "danger_level": 6,
        "special": "Soguk odalarda cok hizli.",
        "weakness": "Sicak ortamda zayiflar.",
        "hunt_speed": 0.9, "hunt_speed_var": 0.6,
        "activity_rate": 0.2, "shyness": 0.4, "aggression": 0.5, "intelligence": 0.5,
        "unique_ability": "freeze",
        "ability_desc": "Ortam sicakligini dondurur",
        "footstep": "buz kirigi",
        "ascii_art": "  *  *\n * ** *\n*  --  *\n *    *"
    },
    "Goryo": {
        "turkish_name": "Goryo",
        "description": "Sadece kamera ile gorulebilen Japon ruhu.",
        "lore": "Adaletsizlige ugramis soylularin intikam ruhu.",
        "evidence": ["emf_spike", "ghost_process", "uv_fingerprint"],
        "danger_level": 4,
        "special": "Dogrudan gozlemlenemez.",
        "weakness": "Odasindan asla ayrilmaz.",
        "hunt_speed": 0.7, "hunt_speed_var": 0.1,
        "activity_rate": 0.15, "shyness": 0.8, "aggression": 0.3, "intelligence": 0.8,
        "unique_ability": "camera_only",
        "ability_desc": "Sadece dijital cihazlarla tespit edilebilir",
        "footstep": "yok",
        "ascii_art": "  .---.\n / ___ \\\n| |   | |\n \\_____/"
    },
    "Myling": {
        "turkish_name": "Myling",
        "description": "Cok sessiz Iskandinav varligi.",
        "lore": "Vaftiz edilmeden olen cocuklarin ruhu.",
        "evidence": ["signal_emission", "folder_anomaly", "ghost_writing"],
        "danger_level": 7,
        "special": "Av sirasinda neredeyse hic ses cikarmaz.",
        "weakness": "Yakin mesafede bile sessiz.",
        "hunt_speed": 1.0, "hunt_speed_var": 0.2,
        "activity_rate": 0.18, "shyness": 0.6, "aggression": 0.6, "intelligence": 0.7,
        "unique_ability": "silent_hunt",
        "ability_desc": "Av sirasinda adim sesi cikmaz",
        "footstep": "neredeyse sessiz",
        "ascii_art": "  ,---.\n / ... \\\n| .   . |\n  '---'"
    },
    "Onryo": {
        "turkish_name": "Onryo",
        "description": "Intikam pesinde kosan, atesten korkan Japon ruhu.",
        "lore": "Japonya'nin en korkulan hayalet turu.",
        "evidence": ["spirit_box", "isee_file", "ghost_orb"],
        "danger_level": 8,
        "special": "Mum sonerse aninda avlanir.",
        "weakness": "Yanan mum onu avlanmaktan alikoyar.",
        "hunt_speed": 1.1, "hunt_speed_var": 0.3,
        "activity_rate": 0.25, "shyness": 0.3, "aggression": 0.8, "intelligence": 0.6,
        "unique_ability": "fire_fear",
        "ability_desc": "Ates varken avlanamaz ama sonunce cildirir",
        "footstep": "inleme",
        "ascii_art": "  .---.\n / x x \\\n|  ===  |\n \\_____/"
    },
    "TheTwins": {
        "turkish_name": "Ikizler",
        "description": "Iki farkli yerde ayni anda hareket eden ikiz ruhlar.",
        "lore": "Birlikte olen ikizlerin ruhu.",
        "evidence": ["signal_emission", "ghost_writing", "temp_drop"],
        "danger_level": 7,
        "special": "Iki farkli konumda ayni anda aktivite.",
        "weakness": "Ikisi farkli hizlarda hareket eder.",
        "hunt_speed": 1.0, "hunt_speed_var": 0.5,
        "activity_rate": 0.3, "shyness": 0.3, "aggression": 0.6, "intelligence": 0.7,
        "unique_ability": "dual_presence",
        "ability_desc": "Iki yerde birden olabilir",
        "footstep": "cift adim",
        "ascii_art": " .-.  .-.\n(o o)(o o)\n'~~~''~~~'"
    },
    "Raiju": {
        "turkish_name": "Raiju",
        "description": "Elektrikle guclenen yildirim canavari.",
        "lore": "Japon mitolojisindeki yildirim hayvani.",
        "evidence": ["emf_spike", "ghost_process", "signal_emission"],
        "danger_level": 8,
        "special": "Elektronik cihazlarin yakininda hizlanir.",
        "weakness": "Elektronik cihazlar kapatilirsa yavaslar.",
        "hunt_speed": 1.4, "hunt_speed_var": 0.5,
        "activity_rate": 0.28, "shyness": 0.2, "aggression": 0.7, "intelligence": 0.6,
        "unique_ability": "emp_burst",
        "ability_desc": "Elektronik cihazlari aninda bozar",
        "footstep": "elektrik carpma",
        "ascii_art": "    /\\\n   /  \\\n  / /\\ \\\n \\/    \\/"
    },
    "Obake": {
        "turkish_name": "Obake",
        "description": "Sekil degistirebilen varlik.",
        "lore": "Japonya'daki sekil degistiren yaratik.",
        "evidence": ["ghost_orb", "isee_file", "uv_fingerprint"],
        "danger_level": 5,
        "special": "Parmak izi ve kanitlari degistirebilir.",
        "weakness": "Bazen gercek formunu gosterir.",
        "hunt_speed": 0.8, "hunt_speed_var": 0.2,
        "activity_rate": 0.2, "shyness": 0.5, "aggression": 0.4, "intelligence": 0.9,
        "unique_ability": "shape_shift",
        "ability_desc": "Kanitlarini ve gorunumunu degistirebilir",
        "footstep": "degisken",
        "ascii_art": "  ???\n ?   ?\n?  ?  ?\n  ???"
    },
    "Mimic": {
        "turkish_name": "Taklitci",
        "description": "Diger hayaletleri taklit eden sinsi varlik.",
        "lore": "Gercek kimligini gizleyen en tehlikeli tur.",
        "evidence": ["signal_emission", "folder_anomaly", "spirit_box"],
        "danger_level": 9,
        "special": "Baska hayaletlerin davranislarini taklit eder.",
        "weakness": "Tutsu gercek formunu ortaya cikarir.",
        "hunt_speed": 1.0, "hunt_speed_var": 0.4,
        "activity_rate": 0.25, "shyness": 0.3, "aggression": 0.7, "intelligence": 1.0,
        "unique_ability": "mimic_ghost",
        "ability_desc": "Baska hayalet turlerini taklit eder",
        "footstep": "taklit",
        "ascii_art": "  .---.\n /  =  \\\n| ?? ?? |\n \\_____/"
    },
    "Moroi": {
        "turkish_name": "Moroi",
        "description": "Giderek guclenen lanetli vampir ruh.",
        "lore": "Romanya folklorundeki yasayan olu.",
        "evidence": ["temp_drop", "ghost_writing", "spirit_box"],
        "danger_level": 8,
        "special": "Sanity dususte daha hizli ve agresif.",
        "weakness": "Tutsu ile gecici olarak zayiflatilir.",
        "hunt_speed": 1.2, "hunt_speed_var": 0.6,
        "activity_rate": 0.25, "shyness": 0.3, "aggression": 0.8, "intelligence": 0.7,
        "unique_ability": "power_growth",
        "ability_desc": "Sanity dustukce guclanir",
        "footstep": "inleme",
        "ascii_art": "  .----.\n / vv   \\\n|  ('')  |\n \\______/"
    },
    "Deogen": {
        "turkish_name": "Deogen",
        "description": "Konumunuzu her zaman bilen varlik.",
        "lore": "Goren goz anlamina gelir.",
        "evidence": ["isee_file", "ghost_process", "spirit_box"],
        "danger_level": 9,
        "special": "Saklanma ise yaramaz ama yaklastikca yavaslar.",
        "weakness": "Yakininda cok yavas hareket eder.",
        "hunt_speed": 0.5, "hunt_speed_var": 0.3,
        "activity_rate": 0.2, "shyness": 0.2, "aggression": 0.7, "intelligence": 1.0,
        "unique_ability": "omniscience",
        "ability_desc": "Konumunuzu her zaman bilir",
        "footstep": "agir nefes",
        "ascii_art": "  (O)\n / | \\\n/  |  \\\n  / \\"
    },
    "Thaye": {
        "turkish_name": "Thaye",
        "description": "Zamanla yaslanan ve zayiflayan kadim ruh.",
        "lore": "Zamanin etkisinden kurtulamayan antik ruh.",
        "evidence": ["ghost_writing", "ghost_orb", "folder_anomaly"],
        "danger_level": 6,
        "special": "Baslangicta cok aktif, zamanla yavaslar.",
        "weakness": "Yeterince beklerseniz zararsiz olur.",
        "hunt_speed": 1.0, "hunt_speed_var": 0.4,
        "activity_rate": 0.35, "shyness": 0.2, "aggression": 0.7, "intelligence": 0.6,
        "unique_ability": "aging",
        "ability_desc": "Zamanla yaslanir, aktivitesi duser",
        "footstep": "degisken",
        "ascii_art": "  .---.\n / --- \\\n| | . | |\n \\|___|/"
    },
    "ShadowWalker": {
        "turkish_name": "Golge Yuruyucu",
        "description": "Golgelerde yasayan sessiz karanlik varlik.",
        "lore": "Isik ve golge arasindaki sinirda yasiyor.",
        "evidence": ["signal_emission", "uv_fingerprint", "temp_drop"],
        "danger_level": 7,
        "special": "Tamamen sessiz, golgelerde hareket eder.",
        "weakness": "Mum ile gorunur hale gelir.",
        "hunt_speed": 0.9, "hunt_speed_var": 0.2,
        "activity_rate": 0.15, "shyness": 0.7, "aggression": 0.6, "intelligence": 0.8,
        "unique_ability": "shadow_walk",
        "ability_desc": "Golgelerde gorunmez hareket eder",
        "footstep": "yok",
        "ascii_art": "  .....\n :     :\n : . . :\n :....:"
    },
    "VoidReaper": {
        "turkish_name": "Bosluk Bicicisi",
        "description": "Bosluktan gelen, her seyi yutan karanlik varlik.",
        "lore": "Boyutlar arasi bir varlik.",
        "evidence": ["emf_spike", "folder_anomaly", "ghost_process"],
        "danger_level": 10,
        "special": "Dosyalari yutar, tahripkar.",
        "weakness": "Hac ile bosluga gonderilir.",
        "hunt_speed": 1.6, "hunt_speed_var": 0.3,
        "activity_rate": 0.2, "shyness": 0.4, "aggression": 0.9, "intelligence": 0.8,
        "unique_ability": "void_consume",
        "ability_desc": "Dosyalari ve klasorleri siler",
        "footstep": "bosluk sesi",
        "ascii_art": "  +===+\n  | X |\n  |/ \\|\n  +===+"
    },
    "Wendigo": {
        "turkish_name": "Wendigo",
        "description": "Kuzey Amerika kokenli yamyam ruh.",
        "lore": "Algonquin yerlilerinin lanetli varligi.",
        "evidence": ["temp_drop", "signal_emission", "ghost_orb"],
        "danger_level": 9,
        "special": "Av icgudusu cok guclu.",
        "weakness": "Tutsu ile sakinlestirilebilir.",
        "hunt_speed": 1.4, "hunt_speed_var": 0.4,
        "activity_rate": 0.22, "shyness": 0.25, "aggression": 0.9, "intelligence": 0.8,
        "unique_ability": "predator_instinct",
        "ability_desc": "Hedefini izler ve en uygun anda saldirir",
        "footstep": "hayvan tirmalama",
        "ascii_art": "  /|\\\n / | \\\n/  O  \\\n  /|\\"
    },
    "Eidolon": {
        "turkish_name": "Eidolon",
        "description": "Antik Yunandan gelen goruntu hayaleti.",
        "lore": "Olulerin golge goruntusu.",
        "evidence": ["isee_file", "ghost_writing", "uv_fingerprint"],
        "danger_level": 5,
        "special": "Nadiren gorunur ama belirgin izler birakir.",
        "weakness": "Mum onu cezbeder.",
        "hunt_speed": 0.6, "hunt_speed_var": 0.1,
        "activity_rate": 0.15, "shyness": 0.85, "aggression": 0.3, "intelligence": 0.7,
        "unique_ability": "ethereal_trace",
        "ability_desc": "Gorunmez ama yazili izler birakir",
        "footstep": "ruya sesleri",
        "ascii_art": "  ~~~~~\n~ (O O) ~\n~   >   ~\n  ~~~~~"
    }
}

PROTECTIVE_ITEMS = {
    "candle": {"name": "Kutsal Mum", "icon": "(i)", "base_uses": 3, "duration": 90,
               "description": "Akil sagligini korur, karanlik varliklari iter.",
               "effects": {"sanity_protection": 0.5, "ghost_repel": 0.3},
               "effective_against": ["Mare","Phantom","ShadowWalker","Onryo","Shade","Eidolon","Goryo"],
               "use_sound": "*fisss* Mum yandi...", "flavor": "Mumun sicakligi seni sariyor..."},
    "crucifix": {"name": "Kutsal Hac", "icon": "[+]", "base_uses": 2, "duration": 120,
                 "description": "Av modunu engeller, hayaleti zayiflatir.",
                 "effects": {"hunt_prevention": 0.75, "sanity_protection": 0.2},
                 "effective_against": ["Demon","Banshee","Poltergeist","Myling","VoidReaper","Obake"],
                 "use_sound": "*pir* Hac isik yayiyor...", "flavor": "Korunma hissediyorsun..."},
    "incense": {"name": "Kutsal Tutsu", "icon": "{~}", "base_uses": 4, "duration": 60,
                "description": "Hayaleti gecici uzaklastirir, sakinlestirir.",
                "effects": {"ghost_banish": 20, "activity_reduction": 0.6, "sanity_recovery": 8},
                "effective_against": ["Yurei","Jinn","Oni","Mimic","Moroi","Wendigo","TheTwins","Yokai"],
                "use_sound": "*duman yayiliyor*", "flavor": "Ortam sakinlesiyor..."},
    "salt": {"name": "Arindirma Tuzu", "icon": "[:]", "base_uses": 5, "duration": 150,
             "description": "Hayaletin izini surer, yavaslatir.",
             "effects": {"ghost_slow": 0.4, "evidence_boost": 0.2},
             "effective_against": ["Wraith","Hantu","Revenant","Raiju","Deogen","Thaye"],
             "use_sound": "*serpme sesi*", "flavor": "Izler daha belirgin..."},
    "sage": {"name": "Kutsal Adacayi", "icon": "<#>", "base_uses": 2, "duration": 45,
             "description": "Odayi arindirır, guclu korunma.",
             "effects": {"ghost_banish": 30, "sanity_recovery": 15},
             "effective_against": ["Demon","VoidReaper","Wendigo","Moroi","Banshee","Revenant"],
             "use_sound": "*yogun duman*", "flavor": "Karanlik geri celikiyor..."},
    "holy_water": {"name": "Kutsal Su", "icon": "{O}", "base_uses": 2, "duration": 30,
                   "description": "Hayaleti sersemletir, avi durdurur.",
                   "effects": {"ghost_stun": 10, "ghost_damage": 0.3, "sanity_recovery": 10},
                   "effective_against": ["Demon","Oni","Poltergeist","Revenant","Banshee","VoidReaper","Wendigo"],
                   "use_sound": "*splash!*", "flavor": "Hayalet kivriyor!"}
}

GHOST_EVENTS = {
    "teleport": ["[!] Dosya aniden baska yerde!"],
    "invisibility": ["[!] Figur goruldu ve kayboldu!"],
    "telekinesis": ["[!] Masaustu sarsildi!", "[!] Klasorler karistirildi!"],
    "scream": ["[!!!] KORKUNÇ BIR CIGLIK!!!"],
    "electric_surge": ["[!] Ekran titredi!"],
    "darkness_control": ["[!] Ortam karardi..."],
    "speed_burst": ["[!] Hizli adim sesleri!"],
    "extreme_shyness": ["[~] ...bir sey vardi ama kayboldu..."],
    "rage_hunt": ["[!!!] YOGUN AGRESIF ENERJI!!!"],
    "room_lock": ["[!] Hayalet odasina cekildi..."],
    "constant_activity": ["[!] Aktivite durmuyor!"],
    "sound_sensitivity": ["[~] Hayalet sese tepki veriyor..."],
    "freeze": ["[!] Sicaklik aniden dustu!"],
    "camera_only": ["[~] Dijital cihazda garip goruntu..."],
    "silent_hunt": ["[!] ...tehlikeli sessizlik..."],
    "fire_fear": ["[~] Mum hayaleti uzak tutuyor..."],
    "dual_presence": ["[!] IKI YERDE AYNI ANDA AKTIVITE!"],
    "emp_burst": ["[!] ELEKTRONIKLER BOZULDU!"],
    "shape_shift": ["[!] Kanitlar degismis gibi!"],
    "mimic_ghost": ["[!] Bu davranis baska bir hayalete ait!"],
    "power_growth": ["[!] Hayalet GUCLENIYOR!"],
    "omniscience": ["[!] Hayalet konumunuzu biliyor!"],
    "aging": ["[~] Hayalet yaslaniyor..."],
    "shadow_walk": ["[~] Golgelerde hareket..."],
    "void_consume": ["[!!!] BIR DOSYA YOK OLDU!"],
    "predator_instinct": ["[!] Izleniyorsun..."],
    "ethereal_trace": ["[~] Gorunmez iz birakilmis..."],
}
AMBIENT_CALM = ["...uzaktan bir ses...", "...soguk esinti...", "...sessizlik...", "...tahta gicirdadi..."]
AMBIENT_MED = ["...kapi gicirdadi...", "...isiklar titredi...", "...golge belirdi...", "...ayak sesleri..."]
AMBIENT_INT = ["...TIRMALAMA!...", "...isiklar cildirdi!...", "...duvarlar titriyor!...", "...ciglik!..."]
CREEPY = ["Arkandayim...", "Kacamazsin...", "Seni izliyorum...", "Karanlik geliyor...", "Cok yakinim..."]
SYMBOLS = ["* # @ ! % ^ &", "KORKU KORKU", ">>> CURSED <<<", "RUN RUN RUN", "KACAMAZSIN"]


class GhostHunterGame:
    def __init__(self, difficulty="orta"):
        self.diff = DIFFICULTY[difficulty]
        self.diff_key = difficulty
        self.desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.temp = tempfile.gettempdir()
        self.game_active = False
        self.current_ghost = None
        self.current_ghost_name = None
        self.ghost_evidence = []
        self.found_evidence = []
        self.eliminated_ghosts = []
        self.remaining_ghosts = list(GHOST_DATABASE.keys())
        self.ghost_processes = []
        self.created_files = []
        self.created_folders = []
        self.sanity = self.diff["sanity_start"]
        self.investigation_time = 0
        self.ghost_activity_level = 0
        self.events_log = []
        self.tools_used = set()
        self.scan_results = {}
        self.scan_history = []
        self.running = True
        self.game_won = False
        self.game_over = False
        self.hunt_mode = False
        self.hunt_count = 0
        self.close_calls = 0
        self.wrong_guesses = 0
        self.special_events = 0
        self.total_scans = 0
        self.successful_scans = 0

        self.inventory = {}
        for k, info in PROTECTIVE_ITEMS.items():
            uses = info["base_uses"] + self.diff["item_bonus"]
            self.inventory[k] = {"count": max(1, uses), "active": False, "timer": 0, "used": 0}

        self.ghost_calm = 0
        self.ghost_banished = 0
        self.ghost_stunned = 0
        self.ghost_power = 1.0
        self.ghost_age = 0
        self.ghost_revealed = False

        self.ev_created = {k: 0 for k in EVIDENCE_TYPES}
        self.max_ev = 3

        self.temperature = 22.0
        self.base_temp = 22.0
        self.emf = 0
        self.signal = 0.0
        self.atmosphere = 0

        self.notebook_marks = {ev: "unknown" for ev in EVIDENCE_TYPES}

    def select_ghost(self):
        self.current_ghost_name = random.choice(list(GHOST_DATABASE.keys()))
        self.current_ghost = GHOST_DATABASE[self.current_ghost_name]
        self.ghost_evidence = self.current_ghost["evidence"]
        self.log("")
        self.log("=" * 58)
        self.log("  [SYS] Paranormal aktivite tespit edildi!")
        self.log("  [SYS] Zorluk: " + self.diff["name"])
        self.log("  [SYS] 10 kanit turu arasindan 3 tanesini bulun.")
        self.log("  [SYS] Eleme defteri ile suphelileri daraltin.")
        if self.diff_key == "zor":
            self.log("  [SYS] !! DIKKAT: Yanlis pozitif sonuclar olabilir!")
            self.log("  [SYS] !! Hayalet cok agresif ve hizli!")
        elif self.diff_key == "kolay":
            self.log("  [SYS] Ipuclari acik, yanlis pozitif yok.")
        self.log("=" * 58)
        self.log("")

    def activity_mod(self):
        m = 1.0
        for k in ["incense", "candle", "crucifix", "salt", "sage", "holy_water"]:
            if not self.inventory[k]["active"]:
                continue
            info = PROTECTIVE_ITEMS[k]
            if self.current_ghost_name in info["effective_against"]:
                m *= 0.3
            else:
                m *= 0.6
        if self.ghost_banished > 0:
            m *= 0.05
        if self.ghost_stunned > 0:
            m *= 0.0
        return m

    def sanity_mod(self):
        m = 1.0
        if self.inventory["candle"]["active"]: m *= 0.5
        if self.inventory["crucifix"]["active"]: m *= 0.8
        return m

    def can_hunt(self):
        if self.ghost_stunned > 0 or self.ghost_banished > 0:
            return False
        if self.inventory["crucifix"]["active"] and random.random() < 0.75:
            return False
        if self.inventory["candle"]["active"] and self.current_ghost_name != "Onryo":
            return False
        if self.inventory["sage"]["active"] or self.inventory["holy_water"]["active"]:
            return False
        return True

    def use_item(self, key):
        item = self.inventory[key]
        info = PROTECTIVE_ITEMS[key]
        if item["count"] <= 0:
            self.log("[!] " + info["name"] + " kalmadi!")
            return False
        if item["active"]:
            self.log("[!] " + info["name"] + " zaten aktif! (" + str(item["timer"]) + "s)")
            return False
        item["count"] -= 1
        item["active"] = True
        item["timer"] = info["duration"]
        item["used"] += 1
        self.log("")
        self.log("~" * 55)
        self.log("  [ITEM] " + info["icon"] + " " + info["name"] + " kullanildi!")
        self.log("  [ITEM] " + info["use_sound"])
        self.log("  [ITEM] " + info["flavor"])
        self.log("  [ITEM] Sure: " + str(info["duration"]) + "s | Kalan: x" + str(item["count"]))
        eff = info["effects"]
        if key == "incense":
            self.ghost_banished = eff["ghost_banish"]
            self.ghost_calm = info["duration"]
            self.sanity = min(100, self.sanity + eff["sanity_recovery"])
            self.log("  [ITEM] Hayalet uzaklastirildi! (+" + str(int(eff["sanity_recovery"])) + " akil)")
        elif key == "sage":
            self.ghost_banished = eff["ghost_banish"]
            self.sanity = min(100, self.sanity + eff["sanity_recovery"])
            self.log("  [ITEM] Oda arindiriliyor! (+" + str(int(eff["sanity_recovery"])) + " akil)")
        elif key == "holy_water":
            self.ghost_stunned = eff["ghost_stun"]
            self.sanity = min(100, self.sanity + eff["sanity_recovery"])
            self.ghost_power = max(0.5, self.ghost_power - eff["ghost_damage"])
            if self.hunt_mode:
                self.hunt_mode = False
                self.log("  [ITEM] !!! AV MODU DURDURULDU !!!")
            self.log("  [ITEM] Hayalet sersemledi!")
        if self.current_ghost_name in info["effective_against"]:
            self.log("  [ITEM] * Hayalet turune ozel etki! *")
        self.log("~" * 55)
        self.log("")
        return True

    def update_items(self):
        for k, item in self.inventory.items():
            if item["active"] and item["timer"] > 0:
                item["timer"] -= 1
                if item["timer"] <= 0:
                    item["active"] = False
                    self.log("[ITEM] " + PROTECTIVE_ITEMS[k]["icon"] + " " + PROTECTIVE_ITEMS[k]["name"] + " bitti.")
                    if k == "candle":
                        self.ghost_revealed = False
        if self.ghost_banished > 0: self.ghost_banished -= 1
        if self.ghost_calm > 0: self.ghost_calm -= 1
        if self.ghost_stunned > 0: self.ghost_stunned -= 1

    def make_isee(self):
        if self.ev_created["isee_file"] >= self.max_ev: return
        p = os.path.join(self.desktop, "ISEE.md")
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("# I SEE YOU\n\n> " + random.choice(CREEPY) + "\n\n" + random.choice(SYMBOLS) + "\n")
            self.created_files.append(p)
            self.ev_created["isee_file"] += 1
            self.log("[EYE] ISEE.md masaustunde!")
        except: pass

    def make_folder(self):
        if self.ev_created["folder_anomaly"] >= self.max_ev: return
        names = ["DONT_OPEN","HELP","room_217","BEHIND_YOU","NO_EXIT","WHO_AM_I","THE_END"]
        n = random.choice(names)
        p = os.path.join(self.desktop, n)
        try:
            if not os.path.exists(p):
                os.makedirs(p)
                self.created_folders.append(p)
                self.ev_created["folder_anomaly"] += 1
                self.log("[FLD] Garip klasor: " + n)
                inner = os.path.join(p, "message.txt")
                with open(inner, "w", encoding="utf-8") as f:
                    f.write(random.choice(CREEPY))
                self.created_files.append(inner)
        except: pass

    def make_writing(self):
        if self.ev_created["ghost_writing"] >= self.max_ev: return
        n = random.choice(["whisper.txt","warning.txt","prophecy.txt"])
        p = os.path.join(self.desktop, n)
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write("HAYALET YAZISI\n\n" + random.choice(SYMBOLS) + "\n" + random.choice(CREEPY))
            self.created_files.append(p)
            self.ev_created["ghost_writing"] += 1
            self.log("[WRT] Hayalet yazisi: " + n)
        except: pass

    def make_process(self):
        if self.ev_created["ghost_process"] >= self.max_ev: return
        n = random.choice(["shadow","dark","void","phantom"]) + "_" + "".join(random.choices(string.hexdigits[:16], k=6))
        bp = os.path.join(self.temp, n + ".bat")
        try:
            with open(bp, "w") as f:
                f.write("@echo off\ntitle " + n + "\n:l\ntimeout /t 5 /nobreak >nul\ngoto l\n")
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW; si.wShowWindow = 0
            proc = subprocess.Popen(["cmd", "/c", bp], startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
            self.ghost_processes.append(proc)
            self.created_files.append(bp)
            self.ev_created["ghost_process"] += 1
            self.log("[PRC] Gizli process: " + n)
        except: pass

    def ghost_loop(self):
        cycle = 0
        while self.game_active and self.running:
            base = random.uniform(self.diff["ghost_wait_min"], self.diff["ghost_wait_max"])
            shy = self.current_ghost.get("shyness", 0.5)
            wm = 1 + shy * 0.4
            am = self.activity_mod()
            if am < 0.3: wm *= 1.3
            if self.current_ghost_name == "Thaye":
                self.ghost_age += 1
                wm /= max(0.4, 1.0 - self.ghost_age / 200)
            if self.current_ghost_name == "Moroi" and self.sanity < 50:
                wm *= max(0.6, 1.0 - (50 - self.sanity) / 100)
            wait = max(2.5, min(base * wm, 18))
            time.sleep(wait)
            if not self.game_active: break
            cycle += 1
            self.update_items()
            if self.sanity > 0:
                drain = random.uniform(0.1, self.diff["sanity_drain"]) * self.sanity_mod() * self.ghost_power
                self.sanity = max(0, self.sanity - drain)

            if "temp_drop" in self.ghost_evidence:
                self.temperature += (random.uniform(-10, 5) - self.temperature) * 0.07
            else:
                self.temperature += (self.base_temp - self.temperature) * 0.1
            if self.current_ghost_name == "Hantu": self.temperature -= 0.4
            if "emf_spike" in self.ghost_evidence:
                self.emf = random.choices([0,1,2,3,4,5], weights=[20,18,20,20,15,7])[0]
            else:
                self.emf = random.choices([0,1,2], weights=[60,30,10])[0]
            if "signal_emission" in self.ghost_evidence:
                self.signal = random.uniform(15, 85) * am
            else:
                self.signal = random.uniform(0, 8)

            if self.ghost_stunned > 0 or self.ghost_banished > 0:
                if random.random() < 0.06: self.log("[~] ...uzaktan bir varlik hissediliyor...")
                continue

            self.atmosphere = 0 if self.sanity > 70 else (1 if self.sanity > 35 else 2)
            ar = self.current_ghost.get("activity_rate", 0.2) * am * self.ghost_power * self.diff["ghost_activity_mult"]
            ar *= (1 - shy * 0.3)
            roll = random.random()

            if roll < ar * 0.2:
                ev = random.choice(self.ghost_evidence)
                if ev == "isee_file": self.make_isee()
                elif ev == "folder_anomaly": self.make_folder()
                elif ev == "ghost_writing": self.make_writing()
                elif ev == "ghost_process": self.make_process()
                elif ev == "emf_spike":
                    self.emf = random.randint(3, 5)
                    self.log("[EMF] EMF yukseldi: Level " + str(self.emf))
                elif ev == "temp_drop":
                    self.temperature -= random.uniform(3, 8)
                    self.log("[FRZ] Sicaklik: " + str(round(self.temperature, 1)) + "C")
                elif ev == "signal_emission":
                    self.signal = random.uniform(50, 95)
                    self.log("[SIG] Sinyal: %" + str(round(self.signal, 1)))
                elif ev == "spirit_box": self.log("[SPB] Spirit box'tan garip ses!")
                elif ev == "ghost_orb": self.log("[ORB] Kamerada parlak kureler!")
                elif ev == "uv_fingerprint": self.log("[UV] UV isikta parmak izleri!")
            elif roll < ar * 0.45:
                msgs = [AMBIENT_CALM, AMBIENT_MED, AMBIENT_INT][self.atmosphere]
                self.log("[~] " + random.choice(msgs))
                self.ghost_activity_level = random.randint(self.atmosphere * 2, self.atmosphere * 3 + 4)
            elif roll < ar * 0.65:
                ab = self.current_ghost.get("unique_ability", "")
                if ab in GHOST_EVENTS:
                    self.log(random.choice(GHOST_EVENTS[ab]))
                    self.special_events += 1
                    if ab == "scream": self.sanity -= random.uniform(3, 7)
                    elif ab == "power_growth": self.ghost_power = min(2.0, self.ghost_power + 0.04)
                    elif ab == "aging": self.ghost_power = max(0.3, self.ghost_power - 0.02)
            elif roll < ar * 0.8:
                if random.random() < 0.2:
                    self.log("[WHISPER] ...\"" + random.choice(CREEPY) + "\"...")
                    self.sanity -= random.uniform(0.3, 1.5)
            elif roll < ar:
                self.ghost_activity_level = random.randint(2, 7)
                if self.ghost_activity_level >= 6:
                    self.log("[!!] Aktivite: " + str(self.ghost_activity_level) + "/10")

            ht = self.diff["hunt_threshold"]
            if self.current_ghost_name == "Demon": ht = 60
            elif self.current_ghost_name == "Onryo" and not self.inventory["candle"]["active"]: ht = 40
            hc = self.diff["hunt_chance"] * am * self.ghost_power
            if self.current_ghost_name == "Demon": hc *= 2
            if self.sanity < ht and random.random() < hc:
                if self.can_hunt(): self.trigger_hunt()
                elif random.random() < 0.2:
                    self.log("[+] Koruyucu esya avi engelledi!")
                    self.close_calls += 1

    def trigger_hunt(self):
        if self.hunt_mode: return
        self.hunt_mode = True
        self.hunt_count += 1
        self.log("")
        self.log("=" * 60)
        self.log("  !!!  AV MODU AKTIF! HAYALET AVLANIYOR!  !!!")
        self.log("=" * 60)
        self.log("")
        hs = self.current_ghost.get("hunt_speed", 1.0) * self.ghost_power
        hs += random.uniform(-self.current_ghost.get("hunt_speed_var", 0.2), self.current_ghost.get("hunt_speed_var", 0.2))
        if self.inventory["salt"]["active"] and self.current_ghost_name in PROTECTIVE_ITEMS["salt"]["effective_against"]:
            hs *= 0.4
            self.log("[ITEM] Tuz yavaslatıyor!")
        dur = random.randint(self.diff["hunt_duration_min"], self.diff["hunt_duration_max"])
        fs = self.current_ghost.get("footstep", "adim")
        for i in range(dur):
            if not self.game_active or not self.hunt_mode: break
            if self.inventory["holy_water"]["active"]:
                self.hunt_mode = False
                self.log("[ITEM] Kutsal su avi durdurdu!")
                break
            time.sleep(max(0.5, 1.2 / hs))
            if self.current_ghost_name == "Myling":
                if random.random() < 0.3: self.log(">>> *...sessizlik...*")
            else:
                msgs = [">>> *" + fs + " yaklsiyor*", ">>> *kapi carpildi*",
                        ">>> *" + fs + "*", ">>> *isiklar sondu*", ">>> *nefes sesleri*"]
                self.log(random.choice(msgs))
            self.sanity -= random.uniform(0.5, self.diff["hunt_sanity_drain"]) * self.ghost_power
        if self.hunt_mode:
            self.hunt_mode = False
            self.log("")
            self.log("[OK] Av sona erdi.")
            self.log("")

    def scan(self, ev_type):
        self.tools_used.add(ev_type)
        self.total_scans += 1
        info = EVIDENCE_TYPES[ev_type]
        t1, t2 = info.get("scan_time", (2, 4))
        time.sleep(random.uniform(t1, t2))
        has = ev_type in self.ghost_evidence
        boost = 0.2 if self.inventory["salt"]["active"] else 0
        fp_rate = self.diff["false_positive_rate"]
        if self.ghost_banished > 0 or self.ghost_stunned > 0:
            base = 0.2
        else:
            base = self.diff["evidence_chance"]
        base += boost

        if has:
            detected = random.random() < base
        else:
            detected = random.random() < fp_rate

        # Fiziksel kanıt dosya kontrolü
        if ev_type == "isee_file":
            exists = os.path.exists(os.path.join(self.desktop, "ISEE.md"))
            if has and (exists or detected):
                if not exists: self.make_isee()
                return self._pos(ev_type, "ISEE.md dosyasi TESPIT EDILDI!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "ISEE.md bulunamadi.")

        elif ev_type == "folder_anomaly":
            found = any(os.path.exists(os.path.join(self.desktop, f))
                       for f in ["DONT_OPEN","HELP","room_217","BEHIND_YOU","NO_EXIT","WHO_AM_I","THE_END"])
            if has and (found or detected):
                if not found: self.make_folder()
                return self._pos(ev_type, "Garip klasorler TESPIT EDILDI!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Anormal klasor bulunamadi.")

        elif ev_type == "ghost_writing":
            found = any(os.path.exists(os.path.join(self.desktop, f))
                       for f in ["whisper.txt","warning.txt","prophecy.txt"])
            if has and (found or detected):
                if not found: self.make_writing()
                return self._pos(ev_type, "Hayalet yazisi TESPIT EDILDI!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Yazi bulunamadi.")

        elif ev_type == "ghost_process":
            if has and (len(self.ghost_processes) > 0 or detected):
                if not self.ghost_processes: self.make_process()
                return self._pos(ev_type, str(max(1, len(self.ghost_processes))) + " gizli process TESPIT!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Gizli process yok.")

        elif ev_type == "emf_spike":
            if has and (self.emf >= 3 or detected):
                lv = max(3, self.emf) if self.emf >= 3 else random.randint(3, 5)
                return self._pos(ev_type, "EMF Level " + str(lv) + " TESPIT!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "EMF Level " + str(random.randint(0, 2)) + " - Normal.")

        elif ev_type == "temp_drop":
            if has and (self.temperature < 0 or detected):
                t = min(self.temperature, random.uniform(-12, -1))
                return self._pos(ev_type, "Dondurucu: " + str(round(t, 1)) + "C!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Sicaklik normal: " + str(round(random.uniform(15, 24), 1)) + "C")

        elif ev_type == "signal_emission":
            if has and (self.signal > 30 or detected):
                return self._pos(ev_type, "Sinyal %" + str(round(max(self.signal, random.uniform(40, 90)), 1)) + " TESPIT!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Sinyal yok.")

        elif ev_type == "spirit_box":
            if has and detected:
                r = random.choice(["'Uzaklas...'","'Buradayim...'","'Olum...'","'Gel...'"])
                return self._pos(ev_type, "Spirit Box yaniti: " + r)
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Spirit Box - Yanit yok.")

        elif ev_type == "ghost_orb":
            if has and detected:
                return self._pos(ev_type, "Kamerada parlak kureler TESPIT!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "Kamera - Normal goruntu.")

        elif ev_type == "uv_fingerprint":
            if has and detected:
                return self._pos(ev_type, "UV altinda parmak izleri TESPIT!")
            elif not has and detected:
                return self._fp(ev_type)
            return self._neg(ev_type, "UV - Parmak izi yok.")
        return False

    def _pos(self, ev, msg):
        self.scan_results[ev] = True
        self.successful_scans += 1
        self.log("[" + EVIDENCE_TYPES[ev]["icon"] + "] >> " + msg + " [VAR]")
        if self.diff["scan_hint"] and ev in self.ghost_evidence:
            self.log("  (Ipucu: Bu kanit kesin dogru.)")
        if ev not in self.found_evidence: self.found_evidence.append(ev)
        self.scan_history.append((ev, True, self.investigation_time))
        return True

    def _fp(self, ev):
        self.scan_results[ev] = "maybe"
        self.log("[" + EVIDENCE_TYPES[ev]["icon"] + "] >> Belirsiz sonuc... olabilir? [?]")
        self.log("  (Dikkat: Bu sonuc yaniltici olabilir!)")
        self.scan_history.append((ev, "maybe", self.investigation_time))
        return True

    def _neg(self, ev, msg):
        self.scan_results[ev] = False
        self.log("[" + EVIDENCE_TYPES[ev]["icon"] + "] >> " + msg + " [YOK]")
        self.scan_history.append((ev, False, self.investigation_time))
        return False

    def eliminate(self, ev_type, has_it):
        count = 0
        new_rem = []
        for gn in self.remaining_ghosts:
            g = GHOST_DATABASE[gn]
            gh = ev_type in g["evidence"]
            if (has_it and not gh) or (not has_it and gh):
                self.eliminated_ghosts.append(gn)
                count += 1
                self.log("  [X] " + gn + " (" + g["turkish_name"] + ") elendi")
            else:
                new_rem.append(gn)
        self.remaining_ghosts = new_rem
        self.log("[INFO] " + str(count) + " elendi. Kalan: " + str(len(self.remaining_ghosts)))
        return count

    def check_guess(self, gn):
        if gn == self.current_ghost_name:
            self.game_won = True
            return True
        self.sanity -= 20
        self.wrong_guesses += 1
        return False

    def cleanup(self):
        for p in self.ghost_processes:
            try: p.terminate(); p.kill()
            except: pass
        for f in self.created_files:
            try:
                if os.path.exists(f): os.remove(f)
            except: pass
        for f in self.created_folders:
            try:
                if os.path.exists(f): shutil.rmtree(f, ignore_errors=True)
            except: pass
        for f in ["ISEE.md","whisper.txt","warning.txt","prophecy.txt"]:
            try:
                p = os.path.join(self.desktop, f)
                if os.path.exists(p): os.remove(p)
            except: pass
        for f in ["DONT_OPEN","HELP","room_217","BEHIND_YOU","NO_EXIT","WHO_AM_I","THE_END"]:
            try:
                p = os.path.join(self.desktop, f)
                if os.path.exists(p): shutil.rmtree(p, ignore_errors=True)
            except: pass
        self.game_active = False
        self.running = False

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.events_log.append(("" if not msg.strip() else "[" + ts + "] ") + msg if msg.strip() else "")


class GhostHunterGUI:
    def __init__(self):
        self.game = GhostHunterGame()
        self.root = tk.Tk()
        self.root.title("WINDOWS PARANORMAL INVESTIGATOR v6.6.6")
        self.root.geometry("1550x960")
        self.root.configure(bg="#0a0a0a")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.last_log = 0
        self.C = {"bg": "#0a0a0a", "panel": "#111111", "card": "#1a1a1a", "text": "#00ff00",
                  "dim": "#006600", "bright": "#33ff33", "danger": "#ff0000", "warn": "#ff6600",
                  "info": "#00aaff", "accent": "#ff00ff", "ghost": "#8800ff", "border": "#222222",
                  "btn": "#1a1a2e", "btn_act": "#0f3460"}
        self.IC = {"candle": "#ffaa00", "crucifix": "#ffdd00", "incense": "#aa66ff",
                   "salt": "#cccccc", "sage": "#66cc66", "holy_water": "#4488ff"}
        self.selected_diff = "orta"
        self.create_main_menu()
        self.update_loop()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def create_main_menu(self):
        self.clear()
        m = tk.Frame(self.root, bg=self.C["bg"])
        m.pack(fill="both", expand=True)
        art = ("================================================================\n"
               "  W I N D O W S   P A R A N O R M A L   I N V E S T I G A T O R\n"
               "                         v 6 . 6 . 6\n"
               "================================================================\n"
               "         ___\n        /   \\\n       | o o |\n       |  >  |\n        \\___/\n"
               "================================================================")
        tk.Label(m, text=art, font=("Consolas", 10), fg=self.C["danger"], bg=self.C["bg"], justify="center").pack(pady=8)
        tk.Label(m, text="[ 27 Hayalet | 10 Kanit | 10 Arac | 6 Koruyucu Esya | Eleme Defteri ]",
                font=("Consolas", 11), fg=self.C["ghost"], bg=self.C["bg"]).pack(pady=3)

        # ZORLUK SEÇİMİ
        diff_frame = tk.Frame(m, bg=self.C["bg"])
        diff_frame.pack(pady=10)
        tk.Label(diff_frame, text="=== ZORLUK SECIMI ===", font=("Consolas", 14, "bold"),
                fg=self.C["warn"], bg=self.C["bg"]).pack(pady=5)

        self.diff_var = tk.StringVar(value="orta")
        diff_buttons_frame = tk.Frame(diff_frame, bg=self.C["bg"])
        diff_buttons_frame.pack(pady=5)

        for key, diff in DIFFICULTY.items():
            f = tk.Frame(diff_buttons_frame, bg=self.C["card"], relief="ridge", borderwidth=2, padx=10, pady=8)
            f.pack(side="left", padx=8)

            rb = tk.Radiobutton(f, text=diff["name"], variable=self.diff_var, value=key,
                               font=("Consolas", 14, "bold"), fg=diff["color"], bg=self.C["card"],
                               selectcolor=self.C["bg"], activebackground=self.C["card"],
                               activeforeground=diff["color"], indicatoron=0, padx=20, pady=5,
                               relief="flat", cursor="hand2",
                               command=lambda: self._update_diff_desc())
            rb.pack()

            tk.Label(f, text=diff["description"], font=("Consolas", 8), fg="#aaaaaa",
                    bg=self.C["card"], wraplength=180, justify="center").pack(pady=3)

            details = []
            if key == "kolay":
                details = ["Yanlis pozitif: YOK", "Kanit bulma: %75", "Esya bonusu: +1",
                           "Av suresi: Kisa", "Ipuclari: ACIK"]
            elif key == "orta":
                details = ["Yanlis pozitif: %8", "Kanit bulma: %60", "Esya: Normal",
                           "Av suresi: Normal", "Ipuclari: KAPALI"]
            elif key == "zor":
                details = ["Yanlis pozitif: %18", "Kanit bulma: %42", "Esya: -1",
                           "Av suresi: Uzun", "Baslangic akil: %85"]

            for d in details:
                clr = "#888888"
                if "YOK" in d or "ACIK" in d or "bonusu" in d: clr = "#66ff66"
                elif "%18" in d or "Uzun" in d or "%85" in d or "-1" in d: clr = "#ff6666"
                tk.Label(f, text=d, font=("Consolas", 7), fg=clr, bg=self.C["card"]).pack()

        self.diff_desc_label = tk.Label(diff_frame, text="", font=("Consolas", 10),
                                       fg=self.C["warn"], bg=self.C["bg"])
        self.diff_desc_label.pack(pady=3)

        # Butonlar
        bf = tk.Frame(m, bg=self.C["bg"])
        bf.pack(pady=10)
        tk.Button(bf, text=">>>  SORUSTURMAYI BASLAT  <<<", font=("Consolas", 16, "bold"),
                 fg="#ff0000", bg="#1a0000", activebackground="#330000", relief="ridge", borderwidth=3,
                 cursor="hand2", padx=30, pady=12, command=self.start).pack(pady=6)
        tk.Button(bf, text="[?] Ansiklopedi", font=("Consolas", 12), fg=self.C["info"], bg=self.C["btn"],
                 activebackground=self.C["btn_act"], relief="ridge", borderwidth=2, cursor="hand2",
                 padx=20, pady=6, command=self.encyclopedia).pack(pady=3)
        tk.Button(bf, text="[X] Cikis", font=("Consolas", 12), fg="#888", bg=self.C["panel"],
                 relief="ridge", borderwidth=2, cursor="hand2", padx=20, pady=6, command=self.on_close).pack(pady=3)

    def _update_diff_desc(self):
        key = self.diff_var.get()
        self.selected_diff = key

    def encyclopedia(self):
        w = tk.Toplevel(self.root); w.title("Ansiklopedi"); w.geometry("950x800"); w.configure(bg=self.C["bg"])
        c = tk.Canvas(w, bg=self.C["bg"], highlightthickness=0)
        sb = tk.Scrollbar(w, orient="vertical", command=c.yview)
        sf = tk.Frame(c, bg=self.C["bg"])
        sf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0, 0), window=sf, anchor="nw"); c.configure(yscrollcommand=sb.set)
        c.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(int(-1*(e.delta/120)), "units"))
        tk.Label(sf, text="HAYALET ANSIKLOPEDISI", font=("Consolas", 13, "bold"),
                fg=self.C["danger"], bg=self.C["bg"]).pack(pady=8)
        for i, (n, g) in enumerate(GHOST_DATABASE.items()):
            fr = tk.Frame(sf, bg=self.C["card"], relief="ridge", borderwidth=1, padx=6, pady=4)
            fr.pack(fill="x", padx=10, pady=2)
            ds = "!" * g["danger_level"]
            tk.Label(fr, text="#" + str(i+1) + " " + n + " - " + g["turkish_name"] + " [" + ds + "]",
                    font=("Consolas", 10, "bold"), fg=self.C["ghost"], bg=self.C["card"], anchor="w").pack(fill="x")
            tk.Label(fr, text=g["description"], font=("Consolas", 8), fg=self.C["text"],
                    bg=self.C["card"], anchor="w", wraplength=870).pack(fill="x")
            tk.Label(fr, text="Yetenek: " + g.get("ability_desc", ""), font=("Consolas", 8),
                    fg=self.C["accent"], bg=self.C["card"], anchor="w").pack(fill="x")
            tk.Label(fr, text="Zayiflik: " + g.get("weakness", ""), font=("Consolas", 8),
                    fg="#ff6666", bg=self.C["card"], anchor="w").pack(fill="x")
            evp = [EVIDENCE_TYPES[e]["name"] for e in g["evidence"]]
            tk.Label(fr, text="Kanitlar: " + " | ".join(evp), font=("Consolas", 8),
                    fg=self.C["info"], bg=self.C["card"], anchor="w").pack(fill="x")
        def cl(): c.unbind_all("<MouseWheel>"); w.destroy()
        w.protocol("WM_DELETE_WINDOW", cl)

    def start(self):
        diff_key = self.diff_var.get()
        self.game = GhostHunterGame(diff_key)
        self.game.select_ghost()
        self.game.game_active = True
        self.game.running = True
        self.last_log = 0
        threading.Thread(target=self.game.ghost_loop, daemon=True).start()
        threading.Thread(target=self._init_act, daemon=True).start()
        threading.Thread(target=self._timer, daemon=True).start()
        self.create_gui()

    def _init_act(self):
        time.sleep(3)
        self.game.log("[~] Ortam taranıyor...")
        time.sleep(2)
        self.game.log("[~] ...bir seyler hissediliyor...")
        time.sleep(random.uniform(3, 6))
        if self.game.ghost_evidence:
            ev = random.choice(self.game.ghost_evidence)
            if ev == "isee_file": self.game.make_isee()
            elif ev == "folder_anomaly": self.game.make_folder()
            elif ev == "ghost_writing": self.game.make_writing()
            elif ev == "ghost_process": self.game.make_process()
            else: self.game.log("[" + EVIDENCE_TYPES[ev]["icon"] + "] Hafif bir " + EVIDENCE_TYPES[ev]["name"].lower() + " algilandi...")

    def _timer(self):
        while self.game.game_active and self.game.running:
            time.sleep(1); self.game.investigation_time += 1

    def create_gui(self):
        self.clear()
        main = tk.Frame(self.root, bg=self.C["bg"])
        main.pack(fill="both", expand=True)

        diff_color = DIFFICULTY[self.game.diff_key]["color"]

        # TOP
        top = tk.Frame(main, bg=self.C["panel"], height=48)
        top.pack(fill="x", padx=4, pady=(4, 0)); top.pack_propagate(False)

        self.lbl_diff = tk.Label(top, text="[" + self.game.diff["name"] + "]", font=("Consolas", 10, "bold"),
                                fg=diff_color, bg=self.C["panel"])
        self.lbl_diff.pack(side="left", padx=6)
        self.lbl_san = tk.Label(top, text="AKIL:100%", font=("Consolas", 11, "bold"), fg=self.C["text"], bg=self.C["panel"])
        self.lbl_san.pack(side="left", padx=4)
        self.bar_f = tk.Frame(top, bg="#333", height=10, width=110); self.bar_f.pack(side="left", padx=3)
        self.bar_f.pack_propagate(False)
        self.bar_fill = tk.Frame(self.bar_f, bg="#0f0"); self.bar_fill.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self.lbl_time = tk.Label(top, text="00:00", font=("Consolas", 10), fg=self.C["info"], bg=self.C["panel"])
        self.lbl_time.pack(side="left", padx=8)
        self.lbl_temp = tk.Label(top, text="22.0C", font=("Consolas", 10), fg=self.C["warn"], bg=self.C["panel"])
        self.lbl_temp.pack(side="left", padx=6)
        self.lbl_emf = tk.Label(top, text="EMF:[.....]", font=("Consolas", 10), fg=self.C["dim"], bg=self.C["panel"])
        self.lbl_emf.pack(side="left", padx=6)
        self.lbl_rem = tk.Label(top, text="KALAN:27", font=("Consolas", 10), fg=self.C["ghost"], bg=self.C["panel"])
        self.lbl_rem.pack(side="left", padx=6)
        self.lbl_hunt = tk.Label(top, text="", font=("Consolas", 13, "bold"), fg=self.C["danger"], bg=self.C["panel"])
        self.lbl_hunt.pack(side="right", padx=10)

        cont = tk.Frame(main, bg=self.C["bg"])
        cont.pack(fill="both", expand=True, padx=4, pady=4)

        # LEFT
        left = tk.Frame(cont, bg=self.C["panel"], width=370)
        left.pack(side="left", fill="y", padx=(0, 2)); left.pack_propagate(False)
        lc = tk.Canvas(left, bg=self.C["panel"], highlightthickness=0)
        ls = tk.Scrollbar(left, orient="vertical", command=lc.yview)
        li = tk.Frame(lc, bg=self.C["panel"])
        li.bind("<Configure>", lambda e: lc.configure(scrollregion=lc.bbox("all")))
        lc.create_window((0, 0), window=li, anchor="nw"); lc.configure(yscrollcommand=ls.set)
        lc.pack(side="left", fill="both", expand=True); ls.pack(side="right", fill="y")
        lc.bind("<Enter>", lambda e: lc.bind_all("<MouseWheel>", lambda ev: lc.yview_scroll(int(-1*(ev.delta/120)), "units")))
        lc.bind("<Leave>", lambda e: lc.unbind_all("<MouseWheel>"))

        # 10 Araç
        tk.Label(li, text="=== ARACLAR (10) ===", font=("Consolas", 10, "bold"), fg=self.C["warn"], bg=self.C["panel"]).pack(pady=(3, 1))
        self.ev_btns = {}; self.ev_stats = {}
        for et, ei in EVIDENCE_TYPES.items():
            bf = tk.Frame(li, bg=self.C["card"], relief="ridge", borderwidth=1)
            bf.pack(fill="x", pady=1, padx=3)
            b = tk.Button(bf, text=ei["icon"] + " " + ei["name"], font=("Consolas", 8), fg=self.C["info"],
                         bg=self.C["card"], activebackground=self.C["btn_act"], relief="flat", cursor="hand2",
                         anchor="w", padx=3, pady=1, command=lambda t=et: self.use_tool(t))
            b.pack(fill="x", side="left", expand=True)
            s = tk.Label(bf, text="[?]", font=("Consolas", 8, "bold"), fg="#555", bg=self.C["card"])
            s.pack(side="right", padx=3)
            self.ev_btns[et] = b; self.ev_stats[et] = s

        # 6 Eşya
        tk.Label(li, text="-"*44, fg=self.C["border"], bg=self.C["panel"], font=("Consolas", 7)).pack(pady=1)
        tk.Label(li, text="=== KORUYUCU ESYALAR (6) ===", font=("Consolas", 10, "bold"), fg="#ffaa00", bg=self.C["panel"]).pack(pady=(1,1))
        self.it_btns = {}; self.it_stats = {}
        for ik, ii in PROTECTIVE_ITEMS.items():
            bf = tk.Frame(li, bg="#0d0d1a", relief="ridge", borderwidth=1)
            bf.pack(fill="x", pady=1, padx=3)
            clr = self.IC.get(ik, "#fff")
            b = tk.Button(bf, text=ii["icon"] + " " + ii["name"], font=("Consolas", 8, "bold"), fg=clr,
                         bg="#0d0d1a", activebackground="#1a1a3e", relief="flat", cursor="hand2",
                         anchor="w", padx=3, pady=1, command=lambda k=ik: self.use_it(k))
            b.pack(fill="x", side="left", expand=True)
            s = tk.Label(bf, text="x" + str(self.game.inventory[ik]["count"]), font=("Consolas", 8, "bold"),
                        fg=clr, bg="#0d0d1a")
            s.pack(side="right", padx=3)
            self.it_btns[ik] = b; self.it_stats[ik] = s

        # Bulunan kanıtlar
        tk.Label(li, text="-"*44, fg=self.C["border"], bg=self.C["panel"], font=("Consolas", 7)).pack(pady=1)
        tk.Label(li, text="BULUNAN KANITLAR", font=("Consolas", 10, "bold"), fg=self.C["bright"], bg=self.C["panel"]).pack()
        self.lbl_found = tk.Label(li, text="Henuz yok.", font=("Consolas", 8), fg=self.C["dim"],
                                 bg=self.C["panel"], justify="left", wraplength=340, anchor="w")
        self.lbl_found.pack(fill="x", padx=4)

        # ELEME DEFTERİ - TAM İSİMLERLE
        tk.Label(li, text="-"*44, fg=self.C["border"], bg=self.C["panel"], font=("Consolas", 7)).pack(pady=1)
        tk.Label(li, text="=== ELEME DEFTERI ===", font=("Consolas", 10, "bold"), fg=self.C["accent"], bg=self.C["panel"]).pack()
        tk.Label(li, text="Tarama sonucuna gore isaretleyin ve eleyin", font=("Consolas", 7), fg="#666", bg=self.C["panel"]).pack()

        self.nb_labels = {}
        for et, ei in EVIDENCE_TYPES.items():
            # Her kanıt için bir satır
            row = tk.Frame(li, bg=self.C["panel"])
            row.pack(fill="x", pady=1, padx=2)

            # Durum göstergesi
            status_lbl = tk.Label(row, text="[?]", font=("Consolas", 8, "bold"), fg="#666",
                                 bg=self.C["panel"], width=3)
            status_lbl.pack(side="left")

            # VAR / YOK / ? butonları
            tk.Button(row, text="✓", font=("Consolas", 8, "bold"), fg="#0f0", bg="#020", width=2,
                     activebackground="#040", relief="flat", padx=1, pady=0,
                     command=lambda t=et: self.nb_mark(t, "confirmed")).pack(side="left", padx=1)
            tk.Button(row, text="✗", font=("Consolas", 8, "bold"), fg="#f00", bg="#200", width=2,
                     activebackground="#400", relief="flat", padx=1, pady=0,
                     command=lambda t=et: self.nb_mark(t, "denied")).pack(side="left", padx=1)
            tk.Button(row, text="?", font=("Consolas", 8, "bold"), fg="#888", bg="#111", width=2,
                     activebackground="#222", relief="flat", padx=1, pady=0,
                     command=lambda t=et: self.nb_mark(t, "unknown")).pack(side="left", padx=1)

            # ELEME butonu
            tk.Button(row, text="ELE", font=("Consolas", 7, "bold"), fg=self.C["accent"], bg="#110011", width=3,
                     activebackground="#220022", relief="flat", padx=1, pady=0,
                     command=lambda t=et: self.elim_menu(t)).pack(side="left", padx=2)

            # TAM İSİM - kısaltma yok
            tk.Label(row, text=ei["name"], font=("Consolas", 7), fg=self.C["text"],
                    bg=self.C["panel"], anchor="w").pack(side="left", padx=2, fill="x", expand=True)

            self.nb_labels[et] = status_lbl

        # CENTER
        center = tk.Frame(cont, bg=self.C["panel"])
        center.pack(side="left", fill="both", expand=True, padx=2)
        tk.Label(center, text="=== SORUSTURMA GUNLUGU ===", font=("Consolas", 12, "bold"),
                fg=self.C["text"], bg=self.C["panel"]).pack(pady=3)
        self.log_text = scrolledtext.ScrolledText(center, font=("Consolas", 9), bg="#050505",
                                                  fg=self.C["text"], insertbackground=self.C["text"],
                                                  relief="flat", state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)
        for tag, clr in [("danger","#f00"),("warn","#f60"),("info","#0af"),("ghost","#80f"),
                        ("success","#0f0"),("sys","#888"),("item","#fa0"),("ambient","#464"),
                        ("whisper","#c44"),("fp","#ff0")]:
            self.log_text.tag_configure(tag, foreground=clr)
        self.log_text.tag_configure("hunt", foreground="#f00", font=("Consolas", 11, "bold"))

        # RIGHT
        right = tk.Frame(cont, bg=self.C["panel"], width=310)
        right.pack(side="right", fill="y", padx=(2, 0)); right.pack_propagate(False)
        tk.Label(right, text="=== SUPHELI HAYALETLER ===", font=("Consolas", 11, "bold"),
                fg=self.C["ghost"], bg=self.C["panel"]).pack(pady=3)
        gc = tk.Canvas(right, bg=self.C["panel"], highlightthickness=0)
        gs = tk.Scrollbar(right, orient="vertical", command=gc.yview)
        self.gl_frame = tk.Frame(gc, bg=self.C["panel"])
        self.gl_frame.bind("<Configure>", lambda e: gc.configure(scrollregion=gc.bbox("all")))
        gc.create_window((0, 0), window=self.gl_frame, anchor="nw"); gc.configure(yscrollcommand=gs.set)
        gc.pack(side="left", fill="both", expand=True); gs.pack(side="right", fill="y")
        gc.bind("<Enter>", lambda e: gc.bind_all("<MouseWheel>", lambda ev: gc.yview_scroll(int(-1*(ev.delta/120)), "units")))
        gc.bind("<Leave>", lambda e: gc.unbind_all("<MouseWheel>"))
        self.pop_ghosts()

        # BOTTOM
        bot = tk.Frame(main, bg=self.C["panel"], height=46)
        bot.pack(fill="x", padx=4, pady=(0, 4)); bot.pack_propagate(False)
        tk.Button(bot, text="[!] HAYALET TURUNU TAHMIN ET", font=("Consolas", 12, "bold"), fg=self.C["accent"],
                 bg="#1a001a", activebackground="#330033", relief="ridge", borderwidth=2, cursor="hand2",
                 padx=14, command=self.guess_win).pack(side="left", padx=6, pady=5)
        tk.Button(bot, text="[X] Temizle ve Cik", font=("Consolas", 10), fg="#888", bg=self.C["card"],
                 relief="ridge", borderwidth=1, cursor="hand2", padx=8, command=self.end).pack(side="right", padx=6, pady=5)
        tk.Button(bot, text="[H] Tarama Gecmisi", font=("Consolas", 9), fg=self.C["info"], bg=self.C["card"],
                 relief="ridge", borderwidth=1, cursor="hand2", padx=6, command=self.show_history).pack(side="right", padx=4, pady=5)
        self.lbl_active = tk.Label(bot, text="", font=("Consolas", 9), fg="#fa0", bg=self.C["panel"])
        self.lbl_active.pack(side="right", padx=8)

    def pop_ghosts(self):
        for w in self.gl_frame.winfo_children(): w.destroy()
        for gn in list(GHOST_DATABASE.keys()):
            g = GHOST_DATABASE[gn]
            el = gn in self.game.eliminated_ghosts
            fr = tk.Frame(self.gl_frame, bg="#1a0000" if el else self.C["card"], relief="ridge", borderwidth=1)
            fr.pack(fill="x", pady=1, padx=2)
            if el:
                tk.Label(fr, text=" [X] " + gn, font=("Consolas", 7, "overstrike"), fg="#600", bg="#1a0000",
                        anchor="w").pack(fill="x", padx=2)
            else:
                ms = self._match(gn)
                mc = self.C["dim"] if ms < 1 else (self.C["ghost"] if ms < 2 else ("#fa0" if ms < 3 else "#f33"))
                tk.Label(fr, text=" [?] " + gn + " (" + g["turkish_name"] + ")",
                        font=("Consolas", 7), fg=mc, bg=self.C["card"], anchor="w").pack(fill="x", padx=2)
                # Kanıt isimleri tam olarak
                evp = [EVIDENCE_TYPES[e]["short"] for e in g["evidence"]]
                tk.Label(fr, text="    " + " | ".join(evp),
                        font=("Consolas", 6), fg=self.C["dim"], bg=self.C["card"], anchor="w").pack(fill="x", padx=2)

    def _match(self, gn):
        g = GHOST_DATABASE[gn]
        s = 0
        for ev in self.game.found_evidence:
            if ev in g["evidence"]: s += 1
        for ev, mk in self.game.notebook_marks.items():
            if mk == "denied" and ev in g["evidence"]: s -= 1
            elif mk == "confirmed" and ev not in g["evidence"]: s -= 1
        return s

    def nb_mark(self, et, status):
        self.game.notebook_marks[et] = status
        lbl = self.nb_labels.get(et)
        if lbl:
            if status == "confirmed": lbl.configure(text="[✓]", fg="#0f0")
            elif status == "denied": lbl.configure(text="[✗]", fg="#f00")
            else: lbl.configure(text="[?]", fg="#666")
        self.root.after(100, self.pop_ghosts)

    def elim_menu(self, et):
        ei = EVIDENCE_TYPES[et]
        em = tk.Toplevel(self.root); em.title("Eleme"); em.geometry("450x220"); em.configure(bg=self.C["bg"])
        em.transient(self.root)
        tk.Label(em, text=ei["name"], font=("Consolas", 14, "bold"), fg=self.C["info"], bg=self.C["bg"]).pack(pady=8)
        tk.Label(em, text="Bu kanit VAR mi YOK mu?", font=("Consolas", 11), fg=self.C["text"], bg=self.C["bg"]).pack(pady=4)
        tk.Label(em, text="(Yanlis eleme geri alinamaz!)", font=("Consolas", 9), fg=self.C["danger"], bg=self.C["bg"]).pack(pady=2)
        bf = tk.Frame(em, bg=self.C["bg"]); bf.pack(pady=10)
        tk.Button(bf, text="  VAR - Bu kanit mevcut  ", font=("Consolas", 11, "bold"), fg="#0f0", bg="#020",
                 activebackground="#040", relief="ridge", padx=12, pady=6,
                 command=lambda: [em.destroy(), self.do_elim(et, True)]).pack(side="left", padx=8)
        tk.Button(bf, text="  YOK - Bu kanit yok  ", font=("Consolas", 11, "bold"), fg="#f00", bg="#200",
                 activebackground="#400", relief="ridge", padx=12, pady=6,
                 command=lambda: [em.destroy(), self.do_elim(et, False)]).pack(side="left", padx=8)

    def do_elim(self, ev, has):
        ei = EVIDENCE_TYPES[ev]
        self.game.log("")
        self.game.log("-" * 55)
        self.game.log("[ELEME] " + ei["name"] + " -> " + ("VAR" if has else "YOK"))
        self.game.log("-" * 55)
        self.game.eliminate(ev, has)
        self.root.after(100, self.pop_ghosts)
        r = len(self.game.remaining_ghosts)
        if r == 1:
            gn = self.game.remaining_ghosts[0]
            g = GHOST_DATABASE[gn]
            self.game.log("")
            self.game.log("=" * 55)
            self.game.log("[!!!] TEK SUPHELI: " + gn + " (" + g["turkish_name"] + ")")
            self.game.log("=" * 55)
        elif r == 0:
            self.game.log("[HATA] Tum hayaletler elendi! Sifirlanıyor...")
            self.game.remaining_ghosts = list(GHOST_DATABASE.keys())
            self.game.eliminated_ghosts = []
            self.root.after(100, self.pop_ghosts)

    def use_tool(self, et):
        ei = EVIDENCE_TYPES[et]
        self.game.log("")
        self.game.log("=" * 50)
        self.game.log("[ARAC] " + ei["tool"] + " kullaniliyor...")
        self.game.log("[ARAC] " + ei["detail"])
        self.game.log("=" * 50)
        self.game.sanity -= random.uniform(0.2, 0.7)
        def do():
            r = self.game.scan(et)
            self.root.after(0, lambda: self._upd_ev(et, r))
        threading.Thread(target=do, daemon=True).start()

    def _upd_ev(self, et, r):
        try:
            if et in self.ev_stats and self.ev_stats[et].winfo_exists():
                sr = self.game.scan_results.get(et)
                if sr == True: self.ev_stats[et].configure(text="[VAR]", fg="#0f0")
                elif sr == "maybe": self.ev_stats[et].configure(text="[?!]", fg="#ff0")
                elif sr == False: self.ev_stats[et].configure(text="[YOK]", fg="#f00")
        except: pass
        if self.game.found_evidence:
            pts = ["  " + EVIDENCE_TYPES[e]["icon"] + " " + EVIDENCE_TYPES[e]["name"] for e in self.game.found_evidence]
            try: self.lbl_found.configure(text="\n".join(pts), fg=self.C["bright"])
            except: pass

    def use_it(self, k):
        threading.Thread(target=lambda: [self.game.use_item(k), self.root.after(0, self._upd_it)], daemon=True).start()

    def _upd_it(self):
        for k, v in self.game.inventory.items():
            try:
                if k in self.it_stats and self.it_stats[k].winfo_exists():
                    t = "x" + str(v["count"])
                    if v["active"]: t += " " + str(v["timer"]) + "s"
                    self.it_stats[k].configure(text=t)
            except: pass

    def show_history(self):
        hw = tk.Toplevel(self.root); hw.title("Tarama Gecmisi"); hw.geometry("550x500"); hw.configure(bg=self.C["bg"])
        hw.transient(self.root)
        tk.Label(hw, text="TARAMA GECMISI", font=("Consolas", 14, "bold"), fg=self.C["info"], bg=self.C["bg"]).pack(pady=8)
        st = scrolledtext.ScrolledText(hw, font=("Consolas", 9), bg="#050505", fg=self.C["text"],
                                       relief="flat", state="disabled", wrap="word")
        st.pack(fill="both", expand=True, padx=8, pady=8)
        st.configure(state="normal")
        if not self.game.scan_history:
            st.insert("end", "Henuz tarama yapilmadi.\n")
        else:
            for ev, res, t in self.game.scan_history:
                m = t // 60; s = t % 60
                ei = EVIDENCE_TYPES[ev]
                if res == True:
                    st.insert("end", str(m).zfill(2) + ":" + str(s).zfill(2) + " | " + ei["name"] + " -> VAR\n")
                elif res == "maybe":
                    st.insert("end", str(m).zfill(2) + ":" + str(s).zfill(2) + " | " + ei["name"] + " -> BELIRSIZ (?)\n")
                else:
                    st.insert("end", str(m).zfill(2) + ":" + str(s).zfill(2) + " | " + ei["name"] + " -> YOK\n")
        st.configure(state="disabled")

    def guess_win(self):
        gw = tk.Toplevel(self.root); gw.title("Tahmin"); gw.geometry("750x780"); gw.configure(bg=self.C["bg"])
        gw.transient(self.root); gw.grab_set()
        tk.Label(gw, text="HANGI HAYALET?", font=("Consolas", 16, "bold"), fg=self.C["accent"], bg=self.C["bg"]).pack(pady=6)
        tk.Label(gw, text="Kalan: " + str(len(self.game.remaining_ghosts)) + " | Zorluk: " + self.game.diff["name"],
                font=("Consolas", 10), fg=self.C["text"], bg=self.C["bg"]).pack()
        if self.game.found_evidence:
            ep = [EVIDENCE_TYPES[e]["name"] for e in self.game.found_evidence]
            tk.Label(gw, text="Kanitlar: " + " | ".join(ep), font=("Consolas", 9), fg=self.C["info"], bg=self.C["bg"]).pack()
        tk.Label(gw, text="Yanlis tahmin = -20 Akil Sagligi!", font=("Consolas", 10), fg=self.C["danger"], bg=self.C["bg"]).pack(pady=3)
        c = tk.Canvas(gw, bg=self.C["bg"], highlightthickness=0)
        sb = tk.Scrollbar(gw, orient="vertical", command=c.yview)
        bf = tk.Frame(c, bg=self.C["bg"])
        bf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0, 0), window=bf, anchor="nw"); c.configure(yscrollcommand=sb.set)
        c.pack(side="left", fill="both", expand=True, padx=8, pady=6); sb.pack(side="right", fill="y")
        c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(int(-1*(e.delta/120)), "units"))

        for gn in sorted(GHOST_DATABASE.keys(), key=lambda x: (x in self.game.eliminated_ghosts, x)):
            g = GHOST_DATABASE[gn]
            el = gn in self.game.eliminated_ghosts
            if el:
                tk.Button(bf, text=" [X] " + gn + " - ELENDI", font=("Consolas", 8, "overstrike"),
                         fg="#400", bg="#100", relief="flat", anchor="w", state="disabled", padx=6, pady=1).pack(fill="x", pady=0, padx=4)
            else:
                evp = [EVIDENCE_TYPES[e]["short"] for e in g["evidence"]]
                ms = self._match(gn)
                mc = self.C["ghost"] if ms < 2 else ("#fa0" if ms < 3 else "#f33")
                tk.Button(bf, text=" [>] " + gn + " (" + g["turkish_name"] + ")  -  " + " | ".join(evp),
                         font=("Consolas", 8), fg=mc, bg=self.C["card"], activebackground=self.C["accent"],
                         activeforeground="#fff", relief="ridge", anchor="w", cursor="hand2", padx=6, pady=2,
                         command=lambda n=gn, w=gw, cv=c: self.do_guess(n, w, cv)).pack(fill="x", pady=1, padx=4)

        def cl(): c.unbind_all("<MouseWheel>"); gw.destroy()
        gw.protocol("WM_DELETE_WINDOW", cl)

    def do_guess(self, gn, win, canvas):
        canvas.unbind_all("<MouseWheel>"); win.destroy()
        if self.game.check_guess(gn):
            self.victory(gn)
        else:
            self.game.log("")
            self.game.log("=" * 50)
            self.game.log("[X] YANLIS! " + gn + " degil! (-20 Akil)")
            self.game.log("=" * 50)
            if gn in self.game.remaining_ghosts:
                self.game.remaining_ghosts.remove(gn)
                self.game.eliminated_ghosts.append(gn)
            self.pop_ghosts()
            if self.game.sanity <= 0: self.gameover()

    def victory(self, gn):
        self.game.game_active = False
        g = GHOST_DATABASE[gn]
        vw = tk.Toplevel(self.root); vw.title("KAZANDIN!"); vw.geometry("700x680"); vw.configure(bg="#001a00")
        vw.transient(self.root)
        tk.Label(vw, text="<<< SORUSTURMA TAMAMLANDI >>>", font=("Consolas", 18, "bold"), fg="#0f0", bg="#001a00").pack(pady=10)
        tk.Label(vw, text=g.get("ascii_art", ""), font=("Consolas", 10), fg=self.C["ghost"], bg="#001a00").pack()
        m = self.game.investigation_time // 60; s = self.game.investigation_time % 60
        sc = int((max(0, 2000 - self.game.investigation_time * 2) + self.game.sanity * 15 +
                  len(self.game.found_evidence) * 300 + self.game.special_events * 25 +
                  self.game.close_calls * 100 - self.game.wrong_guesses * 200) * self.game.diff["score_multiplier"])
        iu = [PROTECTIVE_ITEMS[k]["name"] + " x" + str(v["used"]) for k, v in self.game.inventory.items() if v["used"] > 0]
        evnames = [EVIDENCE_TYPES[e]["name"] for e in g["evidence"]]
        txt = ("\nHayalet: " + gn + " (" + g["turkish_name"] + ")\n" +
               g["description"] + "\n" +
               "Yetenek: " + g.get("ability_desc", "") + "\n" +
               "Zayiflik: " + g.get("weakness", "") + "\n" +
               "Kanitlari: " + " | ".join(evnames) + "\n\n" +
               "=" * 38 + "\n" +
               "Zorluk: " + self.game.diff["name"] + "\n" +
               "Sure: " + str(m) + ":" + str(s).zfill(2) +
               " | Akil: %" + str(int(self.game.sanity)) + "\n" +
               "Tarama: " + str(self.game.total_scans) +
               " | Kanit: " + str(len(self.game.found_evidence)) + "/3\n" +
               "Av: " + str(self.game.hunt_count) +
               " | Yanlis Tahmin: " + str(self.game.wrong_guesses) + "\n" +
               "Esyalar: " + (", ".join(iu) if iu else "-") + "\n" +
               "=" * 38 + "\n" +
               "SKOR: " + str(sc) + "\n" +
               "=" * 38)
        tk.Label(vw, text=txt, font=("Consolas", 9), fg="#0f0", bg="#001a00", justify="center").pack(pady=6)
        tk.Button(vw, text="[OK] Temizle ve Kapat", font=("Consolas", 12, "bold"), fg="#fff", bg="#040",
                 activebackground="#060", relief="ridge", padx=16, pady=6,
                 command=lambda: [vw.destroy(), self.end()]).pack(pady=6)

    def gameover(self):
        self.game.game_active = False
        g = GHOST_DATABASE[self.game.current_ghost_name]
        gow = tk.Toplevel(self.root); gow.title("OYUN BITTI"); gow.geometry("600x480"); gow.configure(bg="#1a0000")
        gow.transient(self.root)
        tk.Label(gow, text="!!! AKIL SAGLIGINIZ SIFIR !!!", font=("Consolas", 16, "bold"), fg="#f00", bg="#1a0000").pack(pady=10)
        tk.Label(gow, text=g.get("ascii_art", ""), font=("Consolas", 12), fg="#f00", bg="#1a0000").pack()
        evnames = [EVIDENCE_TYPES[e]["name"] for e in g["evidence"]]
        m = self.game.investigation_time // 60; s = self.game.investigation_time % 60
        txt = ("\nHayalet sizi ele gecirdi!\n\n" +
               "Gercek: " + self.game.current_ghost_name + " (" + g["turkish_name"] + ")\n" +
               "Yetenek: " + g.get("ability_desc", "") + "\n" +
               "Zayiflik: " + g.get("weakness", "") + "\n" +
               "Kanitlari: " + " | ".join(evnames) + "\n\n" +
               "Sure: " + str(m) + ":" + str(s).zfill(2) +
               " | Zorluk: " + self.game.diff["name"])
        tk.Label(gow, text=txt, font=("Consolas", 10), fg="#f66", bg="#1a0000", justify="center").pack(pady=6)
        tk.Button(gow, text="[OK] Temizle ve Kapat", font=("Consolas", 12, "bold"), fg="#fff", bg="#400",
                 relief="ridge", padx=16, pady=6, command=lambda: [gow.destroy(), self.end()]).pack(pady=6)

    def end(self):
        self.game.game_active = False; self.game.running = False
        time.sleep(0.3); self.game.cleanup()
        self.root.after(1000, self.create_main_menu)

    def update_loop(self):
        if self.game.game_active:
            try:
                san = max(0, self.game.sanity)
                clr = "#0f0" if san > 50 else ("#fa0" if san > 25 else "#f00")
                if hasattr(self, "lbl_san") and self.lbl_san.winfo_exists():
                    self.lbl_san.configure(text="AKIL:" + str(int(san)) + "%", fg=clr)
                if hasattr(self, "bar_fill") and self.bar_fill.winfo_exists():
                    self.bar_fill.configure(bg=clr)
                    self.bar_fill.place(x=0, y=0, relwidth=max(0.001, san/100), relheight=1.0)
                m = self.game.investigation_time // 60; s = self.game.investigation_time % 60
                if hasattr(self, "lbl_time") and self.lbl_time.winfo_exists():
                    self.lbl_time.configure(text=str(m).zfill(2) + ":" + str(s).zfill(2))
                if hasattr(self, "lbl_temp") and self.lbl_temp.winfo_exists():
                    t = round(self.game.temperature, 1)
                    tc = self.C["warn"] if t >= 5 else ("#0cf" if t >= 0 else "#08f")
                    self.lbl_temp.configure(text=str(t) + "C", fg=tc)
                if hasattr(self, "lbl_emf") and self.lbl_emf.winfo_exists():
                    e = self.game.emf
                    ec = self.C["dim"] if e < 3 else (self.C["warn"] if e < 5 else self.C["danger"])
                    self.lbl_emf.configure(text="EMF:[" + "|"*e + "."*(5-e) + "]", fg=ec)
                if hasattr(self, "lbl_rem") and self.lbl_rem.winfo_exists():
                    self.lbl_rem.configure(text="KALAN:" + str(len(self.game.remaining_ghosts)))
                if hasattr(self, "lbl_hunt") and self.lbl_hunt.winfo_exists():
                    if self.game.hunt_mode: self.lbl_hunt.configure(text="!!! AV !!!", fg="#f00")
                    elif self.game.ghost_stunned > 0: self.lbl_hunt.configure(text="[SERSEM " + str(self.game.ghost_stunned) + "s]", fg="#48f")
                    elif self.game.ghost_banished > 0: self.lbl_hunt.configure(text="[UZAK " + str(self.game.ghost_banished) + "s]", fg="#a6f")
                    else: self.lbl_hunt.configure(text="")
                self._upd_it()
                if hasattr(self, "lbl_active") and self.lbl_active.winfo_exists():
                    ap = [PROTECTIVE_ITEMS[k]["icon"] + str(v["timer"]) + "s"
                          for k, v in self.game.inventory.items() if v["active"]]
                    self.lbl_active.configure(text=" ".join(ap) if ap else "")
                self._upd_log()
                if san <= 0 and not self.game.game_over:
                    self.game.game_over = True; self.gameover()
            except: pass
        self.root.after(200, self.update_loop)

    def _upd_log(self):
        if not hasattr(self, "log_text"): return
        try:
            if not self.log_text.winfo_exists(): return
        except: return
        cl = len(self.game.events_log)
        if cl > self.last_log:
            self.log_text.configure(state="normal")
            for i in range(self.last_log, cl):
                msg = self.game.events_log[i]
                if not msg.strip():
                    self.log_text.insert("end", "\n"); continue
                tag = "sys"
                if "AV MODU" in msg or "!!!" in msg: tag = "hunt"
                elif ">>>" in msg: tag = "danger"
                elif "WHISPER" in msg: tag = "whisper"
                elif "TESPIT" in msg or "[VAR]" in msg or "TAMAMLANDI" in msg: tag = "success"
                elif "Belirsiz" in msg or "[?]" in msg: tag = "fp"
                elif "[YOK]" in msg or "elendi" in msg or "YANLIS" in msg: tag = "warn"
                elif "[ARAC]" in msg: tag = "ghost"
                elif "[ITEM]" in msg: tag = "item"
                elif "[~]" in msg: tag = "ambient"
                elif any(x in msg for x in ["[EYE]","[SIG]","[EMF]","[FRZ]","[WRT]","[FLD]","[PRC]","[SPB]","[ORB]","[UV]"]): tag = "info"
                elif "[!!]" in msg or "[!]" in msg: tag = "danger"
                self.log_text.insert("end", msg + "\n", tag)
            self.log_text.configure(state="disabled"); self.log_text.see("end")
            self.last_log = cl

    def on_close(self):
        if self.game.game_active:
            if not messagebox.askyesno("Cikis", "Devam ediyor!\nTemizleyip cikilsin mi?"): return
        self.game.game_active = False; self.game.running = False
        time.sleep(0.3); self.game.cleanup(); self.root.destroy(); sys.exit(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("  WINDOWS PARANORMAL INVESTIGATOR v6.6.6")
    print("  27 Hayalet | 10 Kanit | 10 Arac | 6 Esya")
    print("  Zorluk: Kolay / Orta / Zor")
    print("=" * 60)
    GhostHunterGUI().run()