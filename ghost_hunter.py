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
import hashlib
import json
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
# HAYALET VERİTABANI - GENİŞLETİLMİŞ
# =============================================================================
GHOST_DATABASE = {
    "Wraith": {
        "turkish_name": "Hayalet Ruh",
        "description": "Duvarlardan gecebilen kadim bir varlik. Tuz ile etkilesime girer.",
        "lore": "Ortacag'dan beri bilinen en eski hayalet turlerinden biri. Fiziksel engelleri asabilir.",
        "evidence": ["creates_isee_md", "signal_emission", "temp_fluctuation"],
        "danger_level": 7,
        "special": "Farkli dizinlerde dosya birakir.",
        "weakness": "Tuz ile yavaslar ve iz birakir.",
        "behavior": "Dosyalari farkli konumlara tasiyabilir.",
        "hunt_speed": 1.0,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.25,
        "shyness": 0.3,
        "aggression": 0.5,
        "intelligence": 0.8,
        "preferred_time": "gece",
        "footstep_sound": "hafif surukleme",
        "ghost_model": "beyaz duman",
        "unique_ability": "teleport",
        "ability_description": "Farkli dizinlere aninda dosya birakabilir",
        "interaction_rate": 0.4,
        "favorite_room": "koridor",
        "fear_response": "tuz_serpilince_geri_cekilir",
        "ascii_art": r"""
      .---.
     / o o \
    |   ^   |
    |  ===  |
     \_____/
      |   |
     _|   |_
    """
    },
    "Phantom": {
        "turkish_name": "Fantom",
        "description": "Karanlikta gorulebilen ama fotograf cekildiginde kaybolan varlik.",
        "lore": "Isik ile ozel bir iliskisi olan bu varlik, gozlemlendikce zayiflar.",
        "evidence": ["emf_spike", "creates_isee_md", "ghost_writing"],
        "danger_level": 6,
        "special": "Goruntulendiginde aktivitesi azalir.",
        "weakness": "Gozlemlendikce gucunu kaybeder.",
        "behavior": "Nadiren gorunur ama guclü EMF birakir.",
        "hunt_speed": 0.8,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.2,
        "shyness": 0.6,
        "aggression": 0.4,
        "intelligence": 0.7,
        "preferred_time": "gece",
        "footstep_sound": "sessiz",
        "ghost_model": "siyah golge",
        "unique_ability": "invisibility",
        "ability_description": "Gozlemlendikce gorunmez olur",
        "interaction_rate": 0.3,
        "favorite_room": "yatak_odasi",
        "fear_response": "isiktan_kacar",
        "ascii_art": r"""
      .---.
     / o o \
    |  ---  |
     \_____/
       |||
      / | \
    """
    },
    "Poltergeist": {
        "turkish_name": "Gurultucu Hayalet",
        "description": "Nesneleri firlatma yetenegine sahip gurultucu bir ruh.",
        "lore": "Almanca 'gurultucu ruh' anlamina gelir. Fiziksel dunyayla en cok etkilesime giren tur.",
        "evidence": ["signal_emission", "folder_creation", "process_spawning"],
        "danger_level": 8,
        "special": "Masaustunde kaos yaratir, dosya ve klasorleri karistirir.",
        "weakness": "Bos bir ortamda gucunu kaybeder.",
        "behavior": "Surekli dosya ve klasor olusturur/tasiyor.",
        "hunt_speed": 1.2,
        "hunt_speed_variance": 0.3,
        "activity_rate": 0.35,
        "shyness": 0.1,
        "aggression": 0.8,
        "intelligence": 0.5,
        "preferred_time": "her_zaman",
        "footstep_sound": "agir_adimlar",
        "ghost_model": "gorunmez_kuvvet",
        "unique_ability": "telekinesis",
        "ability_description": "Dosyalari firlatir ve klasorleri dagitir",
        "interaction_rate": 0.7,
        "favorite_room": "mutfak",
        "fear_response": "hac_ile_sakinlesir",
        "ascii_art": r"""
      /!\ /!\
     / ! X ! \
    |  !!!!!  |
    |  CRASH  |
     \_______/
    """
    },
    "Banshee": {
        "turkish_name": "Ciglikci",
        "description": "Tek bir kisiyi hedef alan ve ciglik atan bir varlik.",
        "lore": "Irlanda mitolojisinden gelen olum habercisi. Cigligi olumu muzdeler.",
        "evidence": ["emf_spike", "temp_fluctuation", "creates_isee_md"],
        "danger_level": 9,
        "special": "Hedefine kilitlenir, diger herkesi yok sayar.",
        "weakness": "Hac onu uzak tutar ve hedefini degistirir.",
        "behavior": "Tek bir hedefe odaklanir, cok agresif avlanir.",
        "hunt_speed": 1.3,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.2,
        "shyness": 0.4,
        "aggression": 0.9,
        "intelligence": 0.6,
        "preferred_time": "gece",
        "footstep_sound": "ciglik",
        "ghost_model": "soluk_kadin",
        "unique_ability": "scream",
        "ability_description": "Oldurucu ciglik atar, sanity hizla duser",
        "interaction_rate": 0.3,
        "favorite_room": "salon",
        "fear_response": "hac_ile_geri_cekilir",
        "ascii_art": r"""
       ___
      /   \
     | X X |
     |  O  |  << SCREAM
      \___/
      /| |\
    """
    },
    "Jinn": {
        "turkish_name": "Cin",
        "description": "Elektrikle guclenen toprak varligi. Elektrik kesilince zayiflar.",
        "lore": "Islam mitolojisinden gelen dumansiz atesten yaratilmis varlik.",
        "evidence": ["signal_emission", "emf_spike", "process_spawning"],
        "danger_level": 7,
        "special": "Elektronik cihazlari manipule eder.",
        "weakness": "Elektrik kesildiginde cok zayiflar.",
        "behavior": "Process'ler ve sinyaller uzerinden hareket eder.",
        "hunt_speed": 1.1,
        "hunt_speed_variance": 0.4,
        "activity_rate": 0.3,
        "shyness": 0.2,
        "aggression": 0.6,
        "intelligence": 0.9,
        "preferred_time": "her_zaman",
        "footstep_sound": "elektrik_cizirtisi",
        "ghost_model": "elektrik_kuvveti",
        "unique_ability": "electric_surge",
        "ability_description": "Elektronik cihazlari bozar ve kontrol eder",
        "interaction_rate": 0.5,
        "favorite_room": "bilgisayar_odasi",
        "fear_response": "elektrik_kesilince_donar",
        "ascii_art": r"""
       /\
      /  \
     / ~~ \
    | >--< |
     \____/
      |  |
    """
    },
    "Mare": {
        "turkish_name": "Gece Kabusu",
        "description": "Karanligin gucunu kullanan bir kabus varligi.",
        "lore": "Uyuyan insanlarin gogusune oturup kabus gorduren kadim varlik.",
        "evidence": ["ghost_writing", "creates_isee_md", "folder_creation"],
        "danger_level": 6,
        "special": "Karanlikta cok guclu, isikta zayif.",
        "weakness": "Mum ve isik onu buyuk olcude zayiflatir.",
        "behavior": "Isiklari kapatmaya calisir, karanlikta agresiflesir.",
        "hunt_speed": 0.9,
        "hunt_speed_variance": 0.5,
        "activity_rate": 0.25,
        "shyness": 0.4,
        "aggression": 0.7,
        "intelligence": 0.6,
        "preferred_time": "gece",
        "footstep_sound": "fisildama",
        "ghost_model": "karanlik_golge",
        "unique_ability": "darkness_control",
        "ability_description": "Isiklari sondurur ve karanlikta guclanir",
        "interaction_rate": 0.4,
        "favorite_room": "yatak_odasi",
        "fear_response": "isiktan_kacar",
        "ascii_art": r"""
      .===.
     / ~~~ \
    | |   | |
    | | . | |
     \|___|/
    """
    },
    "Revenant": {
        "turkish_name": "Donen Olu",
        "description": "Normalde yavas ama hedefini gordugunde inanilmaz hizlanan varlik.",
        "lore": "Mezarindan donmus, intikam arayan olu. Hedefini gorunce durdurulamaz.",
        "evidence": ["temp_fluctuation", "process_spawning", "signal_emission"],
        "danger_level": 10,
        "special": "Av sirasinda en hizli hayalet. Saklanirsan yavaslar.",
        "weakness": "Hedefini goremezse son derece yavas hareket eder.",
        "behavior": "Normalda cok yavas, tetiklenince inanilmaz hizli.",
        "hunt_speed": 1.8,
        "hunt_speed_variance": 1.2,
        "activity_rate": 0.15,
        "shyness": 0.6,
        "aggression": 1.0,
        "intelligence": 0.4,
        "preferred_time": "gece",
        "footstep_sound": "agir_surukleme",
        "ghost_model": "curumis_beden",
        "unique_ability": "speed_burst",
        "ability_description": "Hedefini gorünce hizi 3 katina cikar",
        "interaction_rate": 0.2,
        "favorite_room": "bodrum",
        "fear_response": "saklaninca_yavaslar",
        "ascii_art": r"""
      .----.
     / R.I.P \
    |  _____  |
    | |     | |
    | |_____| |
    |_________|
    """
    },
    "Shade": {
        "turkish_name": "Golge",
        "description": "Son derece utangac bir varlik. Yalniz oldugunuzda ortaya cikar.",
        "lore": "En zayif ama en sinsi hayalet turlerinden. Sessizce yaklasir.",
        "evidence": ["emf_spike", "ghost_writing", "folder_creation"],
        "danger_level": 4,
        "special": "Cok utangac, nadiren aktivite gosterir.",
        "weakness": "Grup halindeyken neredeyse hic aktivite gostermez.",
        "behavior": "Sessiz ve sinsi, nadiren iz birakir.",
        "hunt_speed": 0.6,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.12,
        "shyness": 0.9,
        "aggression": 0.2,
        "intelligence": 0.5,
        "preferred_time": "gece",
        "footstep_sound": "sessiz",
        "ghost_model": "belirsiz_golge",
        "unique_ability": "extreme_shyness",
        "ability_description": "Gozlemlendikce tamamen kaybolur",
        "interaction_rate": 0.15,
        "favorite_room": "depo",
        "fear_response": "insanlardan_kacar",
        "ascii_art": r"""
      ___
     / . \
    | . . |
    |  _  |
     \___/
       |
    """
    },
    "Demon": {
        "turkish_name": "Iblis",
        "description": "En agresif hayalet turu. Sebepsiz yere saldirir, korkusuz.",
        "lore": "Cehennemden gelen en tehlikeli varlik. Hicbir sebep olmadan saldirabilir.",
        "evidence": ["creates_isee_md", "signal_emission", "ghost_writing"],
        "danger_level": 10,
        "special": "En sik avlanan hayalet, minimum sanity gereksinimi yok.",
        "weakness": "Hac onu gecici olarak durdurur.",
        "behavior": "Surekli agresif, av moduna cok kolay gecer.",
        "hunt_speed": 1.5,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.35,
        "shyness": 0.05,
        "aggression": 1.0,
        "intelligence": 0.7,
        "preferred_time": "her_zaman",
        "footstep_sound": "gurleme",
        "ghost_model": "kizil_golge",
        "unique_ability": "rage_hunt",
        "ability_description": "Sanity seviyesinden bagimsiz avlanabilir",
        "interaction_rate": 0.6,
        "favorite_room": "her_yer",
        "fear_response": "hac_ile_gecici_durur",
        "ascii_art": r"""
      /\  /\
     /  \/  \
    | >    < |
    |  \  /  |
     \  \/  /
      \____/
    """
    },
    "Yurei": {
        "turkish_name": "Japon Hayaleti",
        "description": "Japon kokenli, tutsuyle kovulabilen bir ruh.",
        "lore": "Japonya'da olenlerin intikam icin donen ruhu. Belirli bir alana baglidir.",
        "evidence": ["temp_fluctuation", "folder_creation", "ghost_writing"],
        "danger_level": 5,
        "special": "Odasindan cok fazla uzaklasmaz.",
        "weakness": "Tutsu ile odaya hapsedilebilir.",
        "behavior": "Belirli bir alanda kalir, uzaklasmaz.",
        "hunt_speed": 0.7,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.2,
        "shyness": 0.5,
        "aggression": 0.5,
        "intelligence": 0.6,
        "preferred_time": "gece",
        "footstep_sound": "hafif_ayak",
        "ghost_model": "beyaz_kimono",
        "unique_ability": "room_lock",
        "ability_description": "Tutsu ile odaya hapsedilebilir",
        "interaction_rate": 0.35,
        "favorite_room": "ust_kat",
        "fear_response": "tutsu_ile_hapsedilir",
        "ascii_art": r"""
      .---.
     / o o \
    |  ---  |
     \    /
      '--'
      |  |
    """
    },
    "Oni": {
        "turkish_name": "Oni",
        "description": "Japon iblisi. Cok aktif, guclu ve gorunur.",
        "lore": "Japon folklorundeki iblis. Maskesi ve sopasi ile ikoniktir.",
        "evidence": ["emf_spike", "signal_emission", "creates_isee_md"],
        "danger_level": 8,
        "special": "En aktif hayalet, surekli hareket eder.",
        "weakness": "Cok aktif oldugu icin kolayca tespit edilir.",
        "behavior": "Surekli aktivite gosterir, saklanamaz.",
        "hunt_speed": 1.3,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.4,
        "shyness": 0.05,
        "aggression": 0.8,
        "intelligence": 0.5,
        "preferred_time": "her_zaman",
        "footstep_sound": "agir_adimlar",
        "ghost_model": "kirmizi_iblis",
        "unique_ability": "constant_activity",
        "ability_description": "Neredeyse surekli aktif, cok fazla kanit birakir",
        "interaction_rate": 0.7,
        "favorite_room": "her_yer",
        "fear_response": "tutsu_ile_yavaslar",
        "ascii_art": r"""
      /\_/\
     / O O \
    |  >w<  |
    |  ---  |
     \_____/
    """
    },
    "Yokai": {
        "turkish_name": "Yokai",
        "description": "Ses ile cekilen bir Japon ruhu. Sessizlikte sakinlesir.",
        "lore": "Japonya'daki dogaustu varliklarin genel adi. Sese karsi hassas.",
        "evidence": ["ghost_writing", "process_spawning", "folder_creation"],
        "danger_level": 5,
        "special": "Yakininda konusulursa agresiflesir.",
        "weakness": "Sessiz kalirsan aktivitesi azalir.",
        "behavior": "Sese tepki verir, sessizlikte sakinlesir.",
        "hunt_speed": 0.8,
        "hunt_speed_variance": 0.3,
        "activity_rate": 0.22,
        "shyness": 0.4,
        "aggression": 0.5,
        "intelligence": 0.6,
        "preferred_time": "gece",
        "footstep_sound": "tirmalama",
        "ghost_model": "belirsiz_sekil",
        "unique_ability": "sound_sensitivity",
        "ability_description": "Sese tepki verir, sessizlikte sakinlesir",
        "interaction_rate": 0.35,
        "favorite_room": "cocuk_odasi",
        "fear_response": "sessizlikte_uyur",
        "ascii_art": r"""
       ___
      (   )
     ( O O )
      ( > )
       ---
    """
    },
    "Hantu": {
        "turkish_name": "Hantu",
        "description": "Sogukta guclenen Malay kokenli bir ruh.",
        "lore": "Guneydogu Asya mitolojisinden gelen soguk ruhu.",
        "evidence": ["temp_fluctuation", "signal_emission", "creates_isee_md"],
        "danger_level": 6,
        "special": "Soguk odalarda cok hizli, sicak odalarda yavas.",
        "weakness": "Sicak ortamda belirgin sekilde zayiflar.",
        "behavior": "Sicaklik dusurur, sogukta guclanir.",
        "hunt_speed": 0.9,
        "hunt_speed_variance": 0.6,
        "activity_rate": 0.2,
        "shyness": 0.4,
        "aggression": 0.5,
        "intelligence": 0.5,
        "preferred_time": "gece",
        "footstep_sound": "buz_kirigi",
        "ghost_model": "buzlu_figur",
        "unique_ability": "freeze",
        "ability_description": "Ortam sicakligini dondurur",
        "interaction_rate": 0.3,
        "favorite_room": "banyo",
        "fear_response": "sicakta_zayiflar",
        "ascii_art": r"""
      *  *
     * ** *
    *  --  *
    * |  | *
     *    *
    """
    },
    "Goryo": {
        "turkish_name": "Goryo",
        "description": "Sadece kamera araciligiyla gorulebilen Japon ruhu.",
        "lore": "Adaletsizlige ugramis soylularin intikam ruhu.",
        "evidence": ["emf_spike", "ghost_writing", "process_spawning"],
        "danger_level": 4,
        "special": "Dogrudan gozlemlenemez, dolayili yollarla tespit edilir.",
        "weakness": "Odasindan asla ayrilmaz.",
        "behavior": "Cok sessiz ve sinsi, sadece dolayili kanitlar birakir.",
        "hunt_speed": 0.7,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.15,
        "shyness": 0.8,
        "aggression": 0.3,
        "intelligence": 0.8,
        "preferred_time": "gece",
        "footstep_sound": "yok",
        "ghost_model": "saydam_figur",
        "unique_ability": "camera_only",
        "ability_description": "Sadece dijital cihazlarla tespit edilebilir",
        "interaction_rate": 0.2,
        "favorite_room": "calisma_odasi",
        "fear_response": "odasinda_kalir",
        "ascii_art": r"""
      .---.
     / ___ \
    | |   | |
    |  ---  |
     \_____/
    """
    },
    "Myling": {
        "turkish_name": "Myling",
        "description": "Iskandinav kokenli, cok sessiz bir varlik.",
        "lore": "Vaftiz edilmeden olen cocuklarin ruhu. Sessizce yaklasir.",
        "evidence": ["signal_emission", "folder_creation", "emf_spike"],
        "danger_level": 7,
        "special": "Av sirasinda neredeyse hic ses cikarmaz.",
        "weakness": "Yakin mesafede bile cok sessiz, bu sayede tespit zor.",
        "behavior": "Son derece sessiz, yaklastigini anlamak imkansiz.",
        "hunt_speed": 1.0,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.18,
        "shyness": 0.6,
        "aggression": 0.6,
        "intelligence": 0.7,
        "preferred_time": "gece",
        "footstep_sound": "neredeyse_sessiz",
        "ghost_model": "cocuk_silueti",
        "unique_ability": "silent_hunt",
        "ability_description": "Av sirasinda adim sesi cikmaz",
        "interaction_rate": 0.25,
        "favorite_room": "cocuk_odasi",
        "fear_response": "hac_ile_uzaklasir",
        "ascii_art": r"""
      ,---.
     / ... \
    | .   . |
     \ === /
      '---'
    """
    },
    "Onryo": {
        "turkish_name": "Onryo",
        "description": "Intikam pesinde kosan Japon ruhu. Atesten korkar.",
        "lore": "Japonya'nin en korkulan hayalet turu. Intikam ile hareket eder.",
        "evidence": ["temp_fluctuation", "creates_isee_md", "process_spawning"],
        "danger_level": 8,
        "special": "Mum sonerse aninda avlanmaya baslar.",
        "weakness": "Yanan mum onu avlanmaktan alikoyar.",
        "behavior": "Mum yakildikca sakinlesir, sonunce deliye doner.",
        "hunt_speed": 1.1,
        "hunt_speed_variance": 0.3,
        "activity_rate": 0.25,
        "shyness": 0.3,
        "aggression": 0.8,
        "intelligence": 0.6,
        "preferred_time": "gece",
        "footstep_sound": "inleme",
        "ghost_model": "kizgin_kadin",
        "unique_ability": "fire_fear",
        "ability_description": "Ates/mum varken avlanamaz ama sonunce cilidirır",
        "interaction_rate": 0.4,
        "favorite_room": "salon",
        "fear_response": "atesten_korkar",
        "ascii_art": r"""
      .---.
     / x x \
    |  ===  |
    |  ~~~  |
     \_____/
    """
    },
    "TheTwins": {
        "turkish_name": "Ikizler",
        "description": "Iki farkli yerde ayni anda hareket edebilen ikiz ruhlar.",
        "lore": "Birlikte olen ikizlerin ruhu. Biri hizli digeri yavas hareket eder.",
        "evidence": ["signal_emission", "ghost_writing", "temp_fluctuation"],
        "danger_level": 7,
        "special": "Iki farkli konumda ayni anda aktivite gosterir.",
        "weakness": "Ikisi farkli hizlarda hareket eder, bu onlari ele verir.",
        "behavior": "Ayni anda birden fazla yerde iz birakir.",
        "hunt_speed": 1.0,
        "hunt_speed_variance": 0.5,
        "activity_rate": 0.3,
        "shyness": 0.3,
        "aggression": 0.6,
        "intelligence": 0.7,
        "preferred_time": "her_zaman",
        "footstep_sound": "cift_adim",
        "ghost_model": "cift_golge",
        "unique_ability": "dual_presence",
        "ability_description": "Iki yerde birden olabilir, cift kanit birakir",
        "interaction_rate": 0.5,
        "favorite_room": "cift_oda",
        "fear_response": "tutsu_ile_ayrilir",
        "ascii_art": r"""
     .-.  .-.
    (o o)(o o)
    | O || O |
    '~~~''~~~'
    """
    },
    "Raiju": {
        "turkish_name": "Raiju",
        "description": "Elektrikli ekipmanlarla guclenen yildirim canavari.",
        "lore": "Japon mitolojisindeki yildirim hayvani. Elektronikleri bozar.",
        "evidence": ["emf_spike", "process_spawning", "signal_emission"],
        "danger_level": 8,
        "special": "Elektronik cihazlarin yakininda cok hizlanir.",
        "weakness": "Elektronik cihazlar kapatilirsa yavaslar.",
        "behavior": "Elektronik cihazlari bozar ve onlardan enerji emer.",
        "hunt_speed": 1.4,
        "hunt_speed_variance": 0.5,
        "activity_rate": 0.28,
        "shyness": 0.2,
        "aggression": 0.7,
        "intelligence": 0.6,
        "preferred_time": "her_zaman",
        "footstep_sound": "elektrik_carpma",
        "ghost_model": "yildirim",
        "unique_ability": "emp_burst",
        "ability_description": "Elektronik cihazlari aninda bozar",
        "interaction_rate": 0.5,
        "favorite_room": "bilgisayar_odasi",
        "fear_response": "elektronik_kapatilinca_zayiflar",
        "ascii_art": r"""
        /\
       /  \
      / /\ \
     / /  \ \
     \/    \/
    """
    },
    "Obake": {
        "turkish_name": "Obake",
        "description": "Sekil degistirebilen bir varlik. Kanitlari degistirebilir.",
        "lore": "Japonya'daki sekil degistiren yaratik. Gercek formu bilinmez.",
        "evidence": ["ghost_writing", "creates_isee_md", "emf_spike"],
        "danger_level": 5,
        "special": "Parmak izi ve kanitlari degistirebilir.",
        "weakness": "Bazen gercek formunu gosterir.",
        "behavior": "Kanitlarini degistirir, yanlis iz birakabilir.",
        "hunt_speed": 0.8,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.2,
        "shyness": 0.5,
        "aggression": 0.4,
        "intelligence": 0.9,
        "preferred_time": "gece",
        "footstep_sound": "degisken",
        "ghost_model": "degisen_sekil",
        "unique_ability": "shape_shift",
        "ability_description": "Kanitlarini ve gorunumunu degistirebilir",
        "interaction_rate": 0.35,
        "favorite_room": "ayna_odasi",
        "fear_response": "hac_ile_gercek_form",
        "ascii_art": r"""
      ???
     ?   ?
    ?  ?  ?
     ?   ?
      ???
    """
    },
    "Mimic": {
        "turkish_name": "Taklitci",
        "description": "Diger hayaletleri taklit edebilen sinsi bir varlik.",
        "lore": "Gercek kimligini gizleyen en tehlikeli tur. Her seyi taklit edebilir.",
        "evidence": ["signal_emission", "folder_creation", "process_spawning"],
        "danger_level": 9,
        "special": "Baska hayaletlerin davranislarini taklit eder.",
        "weakness": "Tutsu gercek formunu ortaya cikarir.",
        "behavior": "Diger hayaletlerin kanitlarini taklit edebilir.",
        "hunt_speed": 1.0,
        "hunt_speed_variance": 0.4,
        "activity_rate": 0.25,
        "shyness": 0.3,
        "aggression": 0.7,
        "intelligence": 1.0,
        "preferred_time": "her_zaman",
        "footstep_sound": "taklit",
        "ghost_model": "degisen",
        "unique_ability": "mimic_ghost",
        "ability_description": "Baska hayalet turlerini taklit eder",
        "interaction_rate": 0.45,
        "favorite_room": "her_yer",
        "fear_response": "tutsu_ile_ortaya_cikar",
        "ascii_art": r"""
      .---.
     /  =  \
    | ?? ?? |
    |  <>   |
     \_____/
    """
    },
    "Moroi": {
        "turkish_name": "Moroi",
        "description": "Romen kokenli, lanetli bir vampir ruh. Giderek guclenir.",
        "lore": "Romanya folklorundeki yasayan olu. Zamanla daha da tehlikeli olur.",
        "evidence": ["temp_fluctuation", "ghost_writing", "signal_emission"],
        "danger_level": 8,
        "special": "Sanity dususte daha hizli ve agresif olur.",
        "weakness": "Tutsu ile gecici olarak zayiflatilir.",
        "behavior": "Dusuk sanity'de inanilmaz hizlanir ve agresiflesir.",
        "hunt_speed": 1.2,
        "hunt_speed_variance": 0.6,
        "activity_rate": 0.25,
        "shyness": 0.3,
        "aggression": 0.8,
        "intelligence": 0.7,
        "preferred_time": "gece",
        "footstep_sound": "inleme",
        "ghost_model": "soluk_vampir",
        "unique_ability": "power_growth",
        "ability_description": "Sanity dustukce guclanir ve hizlanir",
        "interaction_rate": 0.4,
        "favorite_room": "bodrum",
        "fear_response": "tutsu_ile_zayiflar",
        "ascii_art": r"""
      .----.
     / vv   \
    |  ('')  |
    |   --   |
     \______/
    """
    },
    "Deogen": {
        "turkish_name": "Deogen",
        "description": "Her zaman nerede oldugunuzu bilen bir varlik.",
        "lore": "Goren goz anlamina gelir. Saklanmak imkansizdir.",
        "evidence": ["creates_isee_md", "process_spawning", "emf_spike"],
        "danger_level": 9,
        "special": "Konumunuzu her zaman bilir, saklanma ise yaramaz.",
        "weakness": "Yakininda cok yavas hareket eder.",
        "behavior": "Her zaman sizi bulur ama yaklastikca yavaslar.",
        "hunt_speed": 0.5,
        "hunt_speed_variance": 0.3,
        "activity_rate": 0.2,
        "shyness": 0.2,
        "aggression": 0.7,
        "intelligence": 1.0,
        "preferred_time": "her_zaman",
        "footstep_sound": "agir_nefes",
        "ghost_model": "dev_goz",
        "unique_ability": "omniscience",
        "ability_description": "Konumunuzu her zaman bilir ama yaklastikca yavaslar",
        "interaction_rate": 0.35,
        "favorite_room": "her_yer",
        "fear_response": "yakininda_yavaslar",
        "ascii_art": r"""
      (O)
     / | \
    /  |  \
       |
      / \
    """
    },
    "Thaye": {
        "turkish_name": "Thaye",
        "description": "Yaslanan ve zamanla zayiflayan kadim bir ruh.",
        "lore": "Zamanin etkisinden kurtulamayan antik ruh. Baslangicta tehlikeli.",
        "evidence": ["ghost_writing", "temp_fluctuation", "folder_creation"],
        "danger_level": 6,
        "special": "Baslangicta cok aktif, zamanla yavaslar ve sakinlesir.",
        "weakness": "Yeterince beklerseniz neredeyse zararsiz hale gelir.",
        "behavior": "Zamanla yaslanir, aktivitesi ve hizi azalir.",
        "hunt_speed": 1.0,
        "hunt_speed_variance": 0.4,
        "activity_rate": 0.35,
        "shyness": 0.2,
        "aggression": 0.7,
        "intelligence": 0.6,
        "preferred_time": "her_zaman",
        "footstep_sound": "degisken",
        "ghost_model": "yasli_ruh",
        "unique_ability": "aging",
        "ability_description": "Zamanla yaslanir, hizi ve aktivitesi duser",
        "interaction_rate": 0.5,
        "favorite_room": "eski_oda",
        "fear_response": "zamanla_zayiflar",
        "ascii_art": r"""
      .---.
     / --- \
    | | . | |
    |  ---  |
     \|___|/
    """
    },
    "ShadowWalker": {
        "turkish_name": "Golge Yuruyucu",
        "description": "Golgelerde yasayan ve hic ses cikarmayan karanlik varlik.",
        "lore": "Isik ve golge arasindaki sinirda yasayan gizemli varlik.",
        "evidence": ["signal_emission", "creates_isee_md", "temp_fluctuation"],
        "danger_level": 7,
        "special": "Hic ses cikarmaz, sadece golgelerde hareket eder.",
        "weakness": "Mum ve isik ile gorunur hale gelir.",
        "behavior": "Tamamen sessiz, sadece golgelerde var olur.",
        "hunt_speed": 0.9,
        "hunt_speed_variance": 0.2,
        "activity_rate": 0.15,
        "shyness": 0.7,
        "aggression": 0.6,
        "intelligence": 0.8,
        "preferred_time": "gece",
        "footstep_sound": "yok",
        "ghost_model": "kara_golge",
        "unique_ability": "shadow_walk",
        "ability_description": "Golgelerde gorunmez sekilde hareket eder",
        "interaction_rate": 0.2,
        "favorite_room": "karanlik_oda",
        "fear_response": "isiktan_kacar",
        "ascii_art": r"""
      .....
     :     :
     : . . :
     :  v  :
     :.....:
    """
    },
    "VoidReaper": {
        "turkish_name": "Bosluk Bicicisi",
        "description": "Bosluktan gelen ve her seyi yutan karanlik varlik.",
        "lore": "Boyutlar arasi bir varlik. Varliginin oldugu yerde gerceklik bukulur.",
        "evidence": ["emf_spike", "folder_creation", "process_spawning"],
        "danger_level": 10,
        "special": "Dosyalari ve klasorleri 'yutar', silme ozelligi var.",
        "weakness": "Hac ile bosluga geri gonderilir.",
        "behavior": "Her seyi yok etmeye calisir, en tahripkar tur.",
        "hunt_speed": 1.6,
        "hunt_speed_variance": 0.3,
        "activity_rate": 0.2,
        "shyness": 0.4,
        "aggression": 0.9,
        "intelligence": 0.8,
        "preferred_time": "her_zaman",
        "footstep_sound": "bosluk_sesi",
        "ghost_model": "siyah_delik",
        "unique_ability": "void_consume",
        "ability_description": "Dosyalari ve klasorleri siler/yutar",
        "interaction_rate": 0.35,
        "favorite_room": "her_yer",
        "fear_response": "hac_ile_kovulur",
        "ascii_art": r"""
      +===+
      | X |
      | X |
      |/ \|
      +===+
    """
    },
    "Wendigo": {
        "turkish_name": "Wendigo",
        "description": "Kuzey Amerika kokenli yamyam ruh. Av icgudusuyle hareket eder.",
        "lore": "Algonquin yerlilerinin lanetli varligi. Yamyamliga dusen kisinin ruhu.",
        "evidence": ["temp_fluctuation", "signal_emission", "ghost_writing"],
        "danger_level": 9,
        "special": "Av icgudusu cok guclu, hedefini izler.",
        "weakness": "Tutsu ile sakinlestirilebilir.",
        "behavior": "Avci gibi davranir, sabırla bekler ve aniden saldirır.",
        "hunt_speed": 1.4,
        "hunt_speed_variance": 0.4,
        "activity_rate": 0.22,
        "shyness": 0.25,
        "aggression": 0.9,
        "intelligence": 0.8,
        "preferred_time": "gece",
        "footstep_sound": "hayvan_tirmalama",
        "ghost_model": "iskelet_yaratik",
        "unique_ability": "predator_instinct",
        "ability_description": "Hedefini izler ve en uygun anda saldırır",
        "interaction_rate": 0.3,
        "favorite_room": "orman_yolu",
        "fear_response": "tutsu_ile_sakinlesir",
        "ascii_art": r"""
      /|\
     / | \
    /  O  \
    \  |  /
      /|\
    """
    },
    "Eidolon": {
        "turkish_name": "Eidolon",
        "description": "Antik Yunandan gelen goruntu hayaleti.",
        "lore": "Antik Yunan'da olulerin golge goruntusu. Nadir gorunur ama iz birakir.",
        "evidence": ["creates_isee_md", "ghost_writing", "folder_creation"],
        "danger_level": 5,
        "special": "Nadiren gorunur ama belirgin izler birakir.",
        "weakness": "Mum onu cezbeder ve gorunur kilar.",
        "behavior": "Gorunmez ama cevresine etkiler birakir.",
        "hunt_speed": 0.6,
        "hunt_speed_variance": 0.1,
        "activity_rate": 0.15,
        "shyness": 0.85,
        "aggression": 0.3,
        "intelligence": 0.7,
        "preferred_time": "gece",
        "footstep_sound": "ruya_sesleri",
        "ghost_model": "saydam_goruntu",
        "unique_ability": "ethereal_trace",
        "ability_description": "Gorunmez ama yazili izler birakir",
        "interaction_rate": 0.25,
        "favorite_room": "kutuphane",
        "fear_response": "mum_ile_cezbedilir",
        "ascii_art": r"""
      ~~~~~
     ~     ~
    ~ (O O) ~
    ~   >   ~
      ~~~~~
    """
    }
}

# =============================================================================
# KANİT TÜRLERİ
# =============================================================================
EVIDENCE_TYPES = {
    "creates_isee_md": {
        "name": "ISEE.md Dosyasi",
        "description": "Masaustunde ISEE.md dosyasi olusturur",
        "tool": "Dosya Tarayici",
        "icon": "[EYE]",
        "scan_time": (2, 4),
        "detail": "Hayaletin biraktigi korkunç dosyalari tarar."
    },
    "signal_emission": {
        "name": "Sinyal Yayimi",
        "description": "Radyo frekansinda sinyal yayar",
        "tool": "Sinyal Dedektoru",
        "icon": "[SIG]",
        "scan_time": (2, 5),
        "detail": "Paranormal radyo frekanslarini algilar."
    },
    "emf_spike": {
        "name": "EMF Yukselmesi",
        "description": "Elektromanyetik alan seviyesi yukselir",
        "tool": "EMF Olcer",
        "icon": "[EMF]",
        "scan_time": (1, 3),
        "detail": "Ortamdaki elektromanyetik alan seviyesini olcer."
    },
    "temp_fluctuation": {
        "name": "Sicaklik Dalgalanmasi",
        "description": "Ortam sicakligi anormal degisir",
        "tool": "Termometre",
        "icon": "[TMP]",
        "scan_time": (2, 4),
        "detail": "Ortam sicakligindaki anormal degisimleri tespit eder."
    },
    "ghost_writing": {
        "name": "Hayalet Yazisi",
        "description": "Garip semboller ve yazilar birakir",
        "tool": "Yazi Defteri",
        "icon": "[WRT]",
        "scan_time": (3, 6),
        "detail": "Hayaletin biraktigi gizemli yazilari arar."
    },
    "folder_creation": {
        "name": "Klasor Olusturma",
        "description": "Masaustunde garip isimli klasorler olusturur",
        "tool": "Klasor Izleyici",
        "icon": "[FLD]",
        "scan_time": (2, 4),
        "detail": "Masaustundeki anormal klasorleri tespit eder."
    },
    "process_spawning": {
        "name": "Hayalet Process",
        "description": "Gizli arka plan islemleri olusturur",
        "tool": "Process Dedektoru",
        "icon": "[PRC]",
        "scan_time": (2, 5),
        "detail": "Arka planda calisan gizli islemleri tarar."
    }
}

# =============================================================================
# KORUYUCU EŞYALAR
# =============================================================================
PROTECTIVE_ITEMS = {
    "candle": {
        "name": "Mum",
        "turkish_name": "Kutsal Mum",
        "description": "Karanlik varliklari uzak tutar, akil sagligini korur.",
        "icon": "(i)",
        "max_uses": 3,
        "duration": 90,
        "effects": {
            "sanity_protection": 0.5,
            "ghost_repel": 0.3,
            "hunt_delay": 15,
            "visibility": True
        },
        "effective_against": ["Mare", "Phantom", "ShadowWalker", "Onryo", "Goryo", "Shade", "Eidolon"],
        "flavor_text": "Mumun alevi hafifce titriyor... Sicakligini hissedebiliyorsun.",
        "use_sound": "*fisss* Mum yandi..."
    },
    "crucifix": {
        "name": "Hac",
        "turkish_name": "Kutsal Hac",
        "description": "Hayalet avini engeller ve hayaleti zayiflatir.",
        "icon": "[+]",
        "max_uses": 2,
        "duration": 120,
        "effects": {
            "hunt_prevention": 0.75,
            "ghost_weaken": 0.4,
            "sanity_protection": 0.2,
            "damage_reduction": True
        },
        "effective_against": ["Demon", "Banshee", "Poltergeist", "Myling", "VoidReaper", "Obake"],
        "flavor_text": "Hac hafifce isik yayiyor... Korunma hissediyorsun.",
        "use_sound": "*pir* Hac aktif edildi..."
    },
    "incense": {
        "name": "Tutsu",
        "turkish_name": "Kutsal Tutsu",
        "description": "Hayaleti gecici olarak uzaklastirir ve sakinlestirir.",
        "icon": "{~}",
        "max_uses": 4,
        "duration": 60,
        "effects": {
            "ghost_banish_temp": 20,
            "activity_reduction": 0.6,
            "sanity_recovery": 8,
            "calm_ghost": True
        },
        "effective_against": ["Yurei", "Jinn", "Oni", "Mimic", "Moroi", "Wendigo", "TheTwins", "Yokai"],
        "flavor_text": "Tutsu dumani yayiliyor... Ortam belirgin sekilde sakinlesiyor.",
        "use_sound": "*duman yayiliyor* Tutsu aktif..."
    },
    "salt": {
        "name": "Tuz",
        "turkish_name": "Arindirma Tuzu",
        "description": "Hayaletin izini surer ve yavaslatir.",
        "icon": "[:]",
        "max_uses": 5,
        "duration": 150,
        "effects": {
            "ghost_tracking": True,
            "ghost_slow": 0.4,
            "evidence_boost": 0.25,
            "trail_detection": True
        },
        "effective_against": ["Wraith", "Hantu", "Revenant", "Raiju", "Deogen", "Thaye"],
        "flavor_text": "Tuz yere serpildi... Hayaletin izleri daha belirgin.",
        "use_sound": "*serpme sesi* Tuz yere serpildi..."
    },
    "sage": {
        "name": "Adacayi",
        "turkish_name": "Kutsal Adacayi",
        "description": "Odayi arindirır ve hayaleti uzaklastirir.",
        "icon": "<#>",
        "max_uses": 2,
        "duration": 45,
        "effects": {
            "room_cleanse": True,
            "ghost_banish_temp": 30,
            "sanity_recovery": 15,
            "evidence_reset": False
        },
        "effective_against": ["Demon", "VoidReaper", "Wendigo", "Moroi", "Banshee", "Revenant"],
        "flavor_text": "Adacayi dumani ortami aritiyor... Karanlik geri celikiyor.",
        "use_sound": "*yogun duman* Adacayi yakildi..."
    },
    "holy_water": {
        "name": "Kutsal Su",
        "turkish_name": "Kutsal Su",
        "description": "Hayaleti yakar ve buyuk hasar verir.",
        "icon": "{O}",
        "max_uses": 2,
        "duration": 30,
        "effects": {
            "ghost_damage": 0.5,
            "hunt_instant_stop": True,
            "sanity_recovery": 10,
            "ghost_stun": 10
        },
        "effective_against": ["Demon", "Oni", "Poltergeist", "Revenant", "Banshee", "VoidReaper", "Wendigo", "Moroi"],
        "flavor_text": "Kutsal su serpildi! Hayalet acindan kivriyor!",
        "use_sound": "*splash!* Kutsal su etrafa savruldu!"
    }
}

# =============================================================================
# ATMOSFER
# =============================================================================
AMBIENT_MESSAGES_CALM = [
    "...uzaktan hafif bir ses duyuldu...",
    "...havada soguk bir esinti var...",
    "...sessizlik rahatsiz edici...",
    "...pencere caminda hafif buhar olustu...",
    "...duvardan hafif bir titresim geldi...",
    "...bir yerlerde tahta gicirdadi...",
    "...hava biraz agirlasmis gibi...",
]

AMBIENT_MESSAGES_MEDIUM = [
    "...bir kapi gicirdadi...",
    "...isiklar hafifce titredi...",
    "...duvarlarda bir golge belirdi ve kayboldu...",
    "...yerden bir vibrasyon hissedildi...",
    "...uzaktan bir fisildama duyuldu...",
    "...tavan arasinda ayak sesleri var...",
    "...bir nesne dustu...",
    "...elektrikler bir anligina kesildi...",
    "...duvardaki saat durdu...",
]

AMBIENT_MESSAGES_INTENSE = [
    "...GUCLÜ BIR TIRMALAMA SESI!...",
    "...isiklar cildirca yanip sonuyor!...",
    "...duvarlar titremeye basladi!...",
    "...yogun bir soguk dalgasi!...",
    "...bir ciglik duyuldu!...",
    "...her yer karanliga gomuldu!...",
    "...cam parcalandi!...",
    "...yer sarsıldı!...",
]

CREEPY_MESSAGES = [
    "Arkandayim...",
    "Beni gorebilir misin?",
    "Kac... kacamazsin",
    "Seni izliyorum",
    "Buradan cikamazsin",
    "Yalniz degilsin...",
    "Karanlik geliyor",
    "Duyuyor musun?",
    "YARDIM... yardim...",
    "Kapiyi acma...",
    "Nefesini duyuyorum...",
    "Isiklar sonecek...",
    "Cok yakinim...",
    "Buradasin... biliyorum...",
    "Korkuyor musun?",
]

GHOST_WRITING_SYMBOLS = [
    "* # @ ! % ^ & ~ +",
    "KORKU KORKU KORKU",
    ">>> CURSED <<<",
    "RUN RUN RUN",
    "KACAMAZSIN",
    "=== LANET ===",
    "!!! TEHLIKE !!!",
    "BEHIND YOU",
    "OLUM YAKIN",
    "HELP ME",
]

# =============================================================================
# OLAY SİSTEMİ - HAYALET ÖZEL OLAYLARI
# =============================================================================
GHOST_EVENTS = {
    "teleport": [
        "[!] Dosya aniden farkli bir konumda belirdi!",
        "[!] Bir dosya gorunmez bir sekilde tasinmis!",
    ],
    "invisibility": [
        "[!] Bir an icin bir figur goruldu ve kayboldu!",
        "[!] Golge bir an belirdi ve yok oldu!",
    ],
    "telekinesis": [
        "[!] Masaustundeki simgeler sarsıldi!",
        "[!] Klasorler birden karistirildi!",
        "[!] Bir sey firlatilmis gibi hissedildi!",
    ],
    "scream": [
        "[!!!] KULAK TIRMALAYICI BIR CIGLIK!!!",
        "[!!!] DONDURICI BIR CIGLIK DUYULDU!!!",
    ],
    "electric_surge": [
        "[!] Ekran bir an titredi!",
        "[!] Elektrik cizirtisi duyuldu!",
    ],
    "darkness_control": [
        "[!] Ortam aniden karardi...",
        "[!] Isiklar sondurulmeye calisiyor!",
    ],
    "speed_burst": [
        "[!] Cok hizli adim sesleri!",
        "[!] Bir sey inanilmaz hizla gecti!",
    ],
    "extreme_shyness": [
        "[~] ...bir sey vardi ama kayboldu...",
        "[~] ...hava hafifce kipiradandi...",
    ],
    "rage_hunt": [
        "[!!!] YOĞUN AGRESIF ENERJI TESPIT EDILDI!",
        "[!!!] HAYALET CIGIN GIBI HAREKET EDIYOR!",
    ],
    "room_lock": [
        "[!] Hayalet odasina cekildi...",
        "[!] Belirli bir alan yogun enerji yayiyor...",
    ],
    "constant_activity": [
        "[!] Surekli hareket algilaniyor!",
        "[!] Aktivite durmuyor!",
    ],
    "sound_sensitivity": [
        "[~] Hayalet seslere tepki veriyor...",
        "[~] Ortam sesleri hayaleti kışkırttı...",
    ],
    "freeze": [
        "[!] Sicaklik aniden dustu!",
        "[!] Nefesler buhar oluyor!",
    ],
    "camera_only": [
        "[~] Dijital cihazlarda garip bir goruntu...",
        "[~] Process monitor'da anormal aktivite...",
    ],
    "silent_hunt": [
        "[!] ...sessizlik...(bu iyi bir sey degil)...",
    ],
    "fire_fear": [
        "[~] Hayalet atesten cekiniyor...",
        "[~] Mum alevi hayaleti uzak tutuyor...",
    ],
    "dual_presence": [
        "[!] IKI FARKLI YERDE AYNI ANDA AKTIVITE!",
        "[!] Ayni anda birden fazla iz tespit edildi!",
    ],
    "emp_burst": [
        "[!] ELEKTRONIK CIHAZLAR BOZULDU!",
        "[!] Guclu bir elektromanyetik darbe!",
    ],
    "shape_shift": [
        "[!] Kanitlar degismis gibi gorunuyor!",
        "[!] Bir seyin sekli degisti!",
    ],
    "mimic_ghost": [
        "[!] Bu davranıs baska bir hayalete ait gibi!",
        "[!] Hayalet baska bir turu taklit ediyor olabilir!",
    ],
    "power_growth": [
        "[!] Hayalet GUCLENIYOR!",
        "[!] Aktivite seviyesi artiyor!",
    ],
    "omniscience": [
        "[!] Hayalet konumunuzu biliyor!",
        "[!] Saklanmaniz imkansiz!",
    ],
    "aging": [
        "[~] Hayalet yaslaniyor gibi gorunuyor...",
        "[~] Aktivite yavasliyor...",
    ],
    "shadow_walk": [
        "[~] ...golgelerde bir hareket...",
        "[~] ...karanlik bir kose'de bir sey var...",
    ],
    "void_consume": [
        "[!!!] BIR DOSYA YOK OLDU!",
        "[!!!] Bosluk genisliyor!",
    ],
    "predator_instinct": [
        "[!] Avci icgudusu hissediliyor...",
        "[!] Izleniyorsun...",
    ],
    "ethereal_trace": [
        "[~] Gorunmez bir iz birakilmis...",
        "[~] Havada garip bir enerji var...",
    ],
}


# =============================================================================
# OYUN MOTORU
# =============================================================================
class GhostHunterGame:
    def __init__(self):
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.temp_path = tempfile.gettempdir()
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
        self.ghost_exe_path = None
        self.sanity = 100.0
        self.investigation_time = 0
        self.ghost_activity_level = 0
        self.events_log = []
        self.tools_used = set()
        self.evidence_scan_results = {}
        self.ghost_thread = None
        self.running = True
        self.game_won = False
        self.game_over = False
        self.hunt_mode = False
        self.hunt_count = 0
        self.close_calls = 0

        # Koruyucu eşya sistemi
        self.inventory = {}
        for key, info in PROTECTIVE_ITEMS.items():
            self.inventory[key] = {
                "count": info["max_uses"],
                "active": False,
                "timer": 0,
                "total_used": 0
            }

        # Hayalet davranış
        self.ghost_calm_timer = 0
        self.ghost_banished_timer = 0
        self.ghost_stunned_timer = 0
        self.ghost_revealed = False
        self.ghost_age = 0
        self.ghost_power = 1.0

        self.evidence_created_count = {}
        for ev in EVIDENCE_TYPES:
            self.evidence_created_count[ev] = 0
        self.max_evidence_per_type = 3

        # Atmosfer
        self.room_temperature = 22.0
        self.base_temperature = 22.0
        self.emf_level = 0
        self.signal_strength = 0.0
        self.atmosphere_level = 0  # 0=sakin, 1=orta, 2=yogun
        self.total_events = 0
        self.special_events_triggered = 0

        # Moroi özel
        self.moroi_power_bonus = 0

    def select_random_ghost(self):
        self.current_ghost_name = random.choice(list(GHOST_DATABASE.keys()))
        self.current_ghost = GHOST_DATABASE[self.current_ghost_name]
        self.ghost_evidence = self.current_ghost["evidence"]
        self.log_event("")
        self.log_event("=" * 55)
        self.log_event("  [SISTEM] Paranormal aktivite tespit edildi!")
        self.log_event("  [SISTEM] Hayalet turunu belirlemek icin kanit toplayin.")
        self.log_event("  [SISTEM] Koruyucu esyalarinizi akillica kullanin.")
        self.log_event("  [SISTEM] Dikkatli olun... o sizi izliyor olabilir.")
        self.log_event("=" * 55)
        self.log_event("")

    # =========================================================================
    # EŞYA SİSTEMİ
    # =========================================================================
    def get_activity_modifier(self):
        modifier = 1.0

        if self.inventory["incense"]["active"]:
            modifier *= (1.0 - PROTECTIVE_ITEMS["incense"]["effects"]["activity_reduction"])

        if self.inventory["candle"]["active"]:
            if self.current_ghost_name in PROTECTIVE_ITEMS["candle"]["effective_against"]:
                modifier *= 0.3
            else:
                modifier *= 0.6

        if self.inventory["crucifix"]["active"]:
            if self.current_ghost_name in PROTECTIVE_ITEMS["crucifix"]["effective_against"]:
                modifier *= 0.4
            else:
                modifier *= 0.7

        if self.inventory["salt"]["active"]:
            if self.current_ghost_name in PROTECTIVE_ITEMS["salt"]["effective_against"]:
                modifier *= 0.5

        if self.inventory.get("sage", {}).get("active", False):
            modifier *= 0.2

        if self.inventory.get("holy_water", {}).get("active", False):
            modifier *= 0.3

        if self.ghost_banished_timer > 0:
            modifier *= 0.05
        if self.ghost_stunned_timer > 0:
            modifier *= 0.0

        return modifier

    def get_sanity_drain_modifier(self):
        modifier = 1.0
        if self.inventory["candle"]["active"]:
            modifier *= (1.0 - PROTECTIVE_ITEMS["candle"]["effects"]["sanity_protection"])
        if self.inventory["crucifix"]["active"]:
            modifier *= (1.0 - PROTECTIVE_ITEMS["crucifix"]["effects"]["sanity_protection"])
        return modifier

    def can_hunt(self):
        if self.ghost_stunned_timer > 0:
            return False
        if self.ghost_banished_timer > 0:
            return False

        if self.inventory["crucifix"]["active"]:
            if random.random() < PROTECTIVE_ITEMS["crucifix"]["effects"]["hunt_prevention"]:
                return False

        if self.inventory["candle"]["active"]:
            if self.current_ghost_name == "Onryo":
                pass  # Onryo mum sonunce avlanir
            else:
                return False

        if self.inventory.get("holy_water", {}).get("active", False):
            return False

        if self.inventory.get("sage", {}).get("active", False):
            return False

        return True

    def use_protective_item(self, item_key):
        if item_key not in self.inventory:
            return False
        item = self.inventory[item_key]
        item_info = PROTECTIVE_ITEMS[item_key]

        if item["count"] <= 0:
            self.log_event("[!] " + item_info["turkish_name"] + " kalmadi!")
            return False

        if item["active"]:
            self.log_event("[!] " + item_info["turkish_name"] + " zaten aktif! (Kalan: " + str(item["timer"]) + "s)")
            return False

        item["count"] -= 1
        item["active"] = True
        item["timer"] = item_info["duration"]
        item["total_used"] += 1

        self.log_event("")
        self.log_event("~" * 55)
        self.log_event("  [ITEM] " + item_info["icon"] + " " + item_info["turkish_name"] + " kullanildi!")
        self.log_event("  [ITEM] " + item_info["use_sound"])
        self.log_event("  [ITEM] " + item_info["flavor_text"])
        self.log_event("  [ITEM] Sure: " + str(item_info["duration"]) + "s | Kalan: x" + str(item["count"]))

        effects = item_info["effects"]

        if item_key == "incense":
            self.ghost_banished_timer = effects["ghost_banish_temp"]
            self.ghost_calm_timer = item_info["duration"]
            recovery = effects["sanity_recovery"]
            self.sanity = min(100, self.sanity + recovery)
            self.log_event("  [ITEM] Hayalet gecici olarak uzaklastirildi! (+%d sanity)" % int(recovery))

        elif item_key == "candle":
            if self.current_ghost_name in item_info["effective_against"]:
                self.ghost_revealed = True
                self.log_event("  [ITEM] >> Mum bu hayaleti etkiliyor! Daha gorunur hale geldi.")

        elif item_key == "crucifix":
            pass

        elif item_key == "salt":
            if self.current_ghost_name in item_info["effective_against"]:
                self.log_event("  [ITEM] >> Tuz bu hayaletin izini ortaya cikariyor!")

        elif item_key == "sage":
            self.ghost_banished_timer = effects["ghost_banish_temp"]
            recovery = effects["sanity_recovery"]
            self.sanity = min(100, self.sanity + recovery)
            self.log_event("  [ITEM] Oda arindiriliyor! Hayalet uzaklastirildi! (+%d sanity)" % int(recovery))

        elif item_key == "holy_water":
            self.ghost_stunned_timer = effects.get("ghost_stun", 10)
            recovery = effects["sanity_recovery"]
            self.sanity = min(100, self.sanity + recovery)
            self.ghost_power = max(0.5, self.ghost_power - effects.get("ghost_damage", 0.3))
            if self.hunt_mode:
                self.hunt_mode = False
                self.log_event("  [ITEM] !!! AV MODU ANINDA DURDURULDU !!!")
            self.log_event("  [ITEM] Hayalet sersemledi! (+%d sanity, Guc azaldi)" % int(recovery))

        if self.current_ghost_name in item_info["effective_against"]:
            self.log_event("  [ITEM] * Bu hayalet turune ozel etki! *")

        self.log_event("~" * 55)
        self.log_event("")
        return True

    def update_item_timers(self):
        for item_key, item in self.inventory.items():
            if item["active"] and item["timer"] > 0:
                item["timer"] -= 1
                if item["timer"] <= 0:
                    item["active"] = False
                    item_info = PROTECTIVE_ITEMS[item_key]
                    self.log_event("[ITEM] " + item_info["icon"] + " " + item_info["turkish_name"] + " etkisi bitti.")

                    if item_key == "candle":
                        self.ghost_revealed = False
                        if self.current_ghost_name == "Onryo" and self.sanity < 50:
                            self.log_event("[!!!] Onryo'nun mumu sondu! Tehlike artti!")

        if self.ghost_banished_timer > 0:
            self.ghost_banished_timer -= 1
        if self.ghost_calm_timer > 0:
            self.ghost_calm_timer -= 1
        if self.ghost_stunned_timer > 0:
            self.ghost_stunned_timer -= 1

    # =========================================================================
    # DOSYA OLUŞTURMA
    # =========================================================================
    def create_ghost_exe(self):
        if self.evidence_created_count["process_spawning"] >= self.max_evidence_per_type:
            return
        ghost_names = [
            "shadow_svc", "dark_process", "null_entity", "void_runner",
            "phantom_proc", "ghost_worker", "specter_svc", "wraith_bg"
        ]
        name = random.choice(ghost_names) + "_" + "".join(random.choices(string.hexdigits[:16], k=6))
        bat_content = "@echo off\ntitle " + name + "\n:loop\ntimeout /t 5 /nobreak >nul\ngoto loop\n"
        bat_path = os.path.join(self.temp_path, name + ".bat")
        try:
            with open(bat_path, "w") as f:
                f.write(bat_content)
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0
            proc = subprocess.Popen(["cmd", "/c", bat_path], startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
            self.ghost_processes.append(proc)
            self.created_files.append(bat_path)
            self.evidence_created_count["process_spawning"] += 1
            self.log_event("[PRC] Bilinmeyen process tespit edildi: " + name)
        except Exception:
            pass

    def create_isee_file(self):
        if "creates_isee_md" not in self.ghost_evidence:
            return
        if self.evidence_created_count["creates_isee_md"] >= self.max_evidence_per_type:
            return
        content = "# I SEE YOU\n\n"
        content += "> " + random.choice(CREEPY_MESSAGES) + "\n\n---\n\n"
        content += "Tarih: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        content += "Durum: **AKTIF**\n\n---\n\n"
        content += random.choice(GHOST_WRITING_SYMBOLS) + "\n"
        file_path = os.path.join(self.desktop_path, "ISEE.md")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.created_files.append(file_path)
            self.evidence_created_count["creates_isee_md"] += 1
            self.log_event("[EYE] ISEE.md dosyasi masaustunde tespit edildi!")
        except Exception:
            pass

    def create_creepy_folders(self):
        if "folder_creation" not in self.ghost_evidence:
            return
        if self.evidence_created_count["folder_creation"] >= self.max_evidence_per_type:
            return
        folder_names = ["DONT_OPEN", "HELP", "room_217", "BEHIND_YOU",
                       "THEY_WATCH", "NO_EXIT", "LAST_WARNING", "HELP_ME", "WHO_AM_I", "THE_END"]
        name = random.choice(folder_names)
        folder_path = os.path.join(self.desktop_path, name)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                self.created_folders.append(folder_path)
                self.evidence_created_count["folder_creation"] += 1
                self.log_event("[FLD] Garip klasor tespit edildi: " + name)
                inner_file = os.path.join(folder_path, "message.txt")
                with open(inner_file, "w", encoding="utf-8") as f:
                    f.write(random.choice(CREEPY_MESSAGES) + "\n\n" + random.choice(GHOST_WRITING_SYMBOLS))
                self.created_files.append(inner_file)
        except Exception:
            pass

    def create_ghost_writing(self):
        if "ghost_writing" not in self.ghost_evidence:
            return
        if self.evidence_created_count["ghost_writing"] >= self.max_evidence_per_type:
            return
        file_names = ["whisper.txt", "warning.txt", "prophecy.txt", "message_from_beyond.txt"]
        name = random.choice(file_names)
        file_path = os.path.join(self.desktop_path, name)
        try:
            content = "=" * 40 + "\n  HAYALET YAZISI\n" + "=" * 40 + "\n\n"
            content += random.choice(GHOST_WRITING_SYMBOLS) + "\n\n"
            content += random.choice(CREEPY_MESSAGES) + "\n\n"
            content += "Zaman: " + datetime.now().strftime("%H:%M:%S") + "\n"
            content += "=" * 40 + "\n"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.created_files.append(file_path)
            self.evidence_created_count["ghost_writing"] += 1
            self.log_event("[WRT] Hayalet yazisi bulundu: " + name)
        except Exception:
            pass

    # =========================================================================
    # ANA AKTİVİTE DÖNGÜSÜ - DENGELİ HIZ
    # =========================================================================
    def ghost_activity_loop(self):
        cycle = 0
        while self.game_active and self.running:
            # DENGELI HIZ: 4-10 saniye baz bekleme
            base_wait = random.uniform(4, 10)

            shyness = self.current_ghost.get("shyness", 0.5)
            wait_modifier = 1 + (shyness * 0.5)  # Utangaçlar biraz daha yavaş

            activity_mod = self.get_activity_modifier()
            if activity_mod < 0.3:
                wait_modifier *= 1.5

            # Thaye zamanla yavaslar
            if self.current_ghost_name == "Thaye":
                self.ghost_age += 1
                age_factor = max(0.4, 1.0 - (self.ghost_age / 200))
                wait_modifier /= age_factor
                if self.ghost_age % 50 == 0:
                    self.log_event("[~] Hayalet yaslaniyor... aktivitesi azaliyor.")

            # Moroi dusuk sanity'de guclanir
            if self.current_ghost_name == "Moroi":
                if self.sanity < 50:
                    self.moroi_power_bonus = (50 - self.sanity) / 100
                    wait_modifier *= max(0.5, 1.0 - self.moroi_power_bonus)

            actual_wait = base_wait * wait_modifier
            actual_wait = max(3, min(actual_wait, 18))  # 3-18 saniye arası

            time.sleep(actual_wait)
            if not self.game_active:
                break

            cycle += 1
            self.update_item_timers()

            # Sanity kaybı
            if self.sanity > 0:
                drain = random.uniform(0.15, 0.8) * self.get_sanity_drain_modifier() * self.ghost_power
                self.sanity -= drain
                if self.sanity < 0:
                    self.sanity = 0

            # Sıcaklık simülasyonu
            if "temp_fluctuation" in self.ghost_evidence:
                target = random.uniform(-8, 8)
                self.room_temperature += (target - self.room_temperature) * 0.08
            else:
                self.room_temperature += (self.base_temperature - self.room_temperature) * 0.12
            # Hantu özel
            if self.current_ghost_name == "Hantu":
                self.room_temperature -= 0.5

            # EMF simülasyonu
            if "emf_spike" in self.ghost_evidence:
                self.emf_level = random.choices([0, 1, 2, 3, 4, 5], weights=[25, 20, 20, 18, 12, 5])[0]
            else:
                self.emf_level = random.choices([0, 1, 2], weights=[60, 30, 10])[0]

            # Sinyal
            if "signal_emission" in self.ghost_evidence:
                self.signal_strength = random.uniform(15, 85) * activity_mod
            else:
                self.signal_strength = random.uniform(0, 8)

            # Stunned/banished kontrolü
            if self.ghost_stunned_timer > 0:
                continue
            if self.ghost_banished_timer > 0:
                if random.random() < 0.1:
                    self.log_event("[~] ...uzaktan hafif bir varlik hissediliyor...")
                continue

            # Atmosfer seviyesi
            if self.sanity > 70:
                self.atmosphere_level = 0
            elif self.sanity > 35:
                self.atmosphere_level = 1
            else:
                self.atmosphere_level = 2

            # Aktivite olasılığı
            activity_rate = self.current_ghost.get("activity_rate", 0.2) * activity_mod * self.ghost_power
            activity_rate *= (1 - shyness * 0.3)

            roll = random.random()

            if roll < activity_rate * 0.25:
                # Kanıt bırakma
                ev = random.choice(self.ghost_evidence)
                if ev == "creates_isee_md":
                    self.create_isee_file()
                elif ev == "folder_creation":
                    self.create_creepy_folders()
                elif ev == "ghost_writing":
                    self.create_ghost_writing()
                elif ev == "process_spawning":
                    self.create_ghost_exe()
                elif ev == "emf_spike":
                    lv = random.randint(3, 5)
                    self.emf_level = lv
                    self.log_event("[EMF] EMF seviyesi yukseldi: Level " + str(lv))
                elif ev == "temp_fluctuation":
                    drop = round(random.uniform(-12, -2), 1)
                    self.room_temperature += drop
                    self.log_event("[TMP] Sicaklik dustu: " + str(round(self.room_temperature, 1)) + " C")
                elif ev == "signal_emission":
                    sig = round(random.uniform(50, 95), 1)
                    self.signal_strength = sig
                    self.log_event("[SIG] Guclu sinyal algilandi: %" + str(sig))

            elif roll < activity_rate * 0.5:
                # Ambient mesaj
                if self.atmosphere_level == 0:
                    msg = random.choice(AMBIENT_MESSAGES_CALM)
                elif self.atmosphere_level == 1:
                    msg = random.choice(AMBIENT_MESSAGES_MEDIUM)
                else:
                    msg = random.choice(AMBIENT_MESSAGES_INTENSE)
                self.log_event("[~] " + msg)
                self.ghost_activity_level = random.randint(self.atmosphere_level * 2, self.atmosphere_level * 4 + 3)

            elif roll < activity_rate * 0.7:
                # Hayalet özel olay
                ability = self.current_ghost.get("unique_ability", "")
                if ability in GHOST_EVENTS:
                    event_msg = random.choice(GHOST_EVENTS[ability])
                    self.log_event(event_msg)
                    self.special_events_triggered += 1
                    self.ghost_activity_level = random.randint(4, 8)

                    # Özel yetenek yan etkileri
                    if ability == "scream":
                        self.sanity -= random.uniform(3, 8)
                        self.log_event("  >> Akil sagliginiz sarsıldı!")
                    elif ability == "power_growth":
                        self.ghost_power = min(2.0, self.ghost_power + 0.05)
                    elif ability == "aging":
                        self.ghost_power = max(0.3, self.ghost_power - 0.02)
                    elif ability == "dual_presence":
                        ev = random.choice(self.ghost_evidence)
                        if ev == "creates_isee_md":
                            self.create_isee_file()
                        elif ev == "folder_creation":
                            self.create_creepy_folders()

            elif roll < activity_rate * 0.85:
                # Fısıltı
                if random.random() < 0.3:
                    msg = random.choice(CREEPY_MESSAGES)
                    self.log_event("[WHISPER] ...\"" + msg + "\"...")
                    self.sanity -= random.uniform(0.5, 2)

            elif roll < activity_rate:
                # Genel aktivite
                self.ghost_activity_level = random.randint(2, 7)
                if self.ghost_activity_level >= 6:
                    self.log_event("[!!] Aktivite yukseliyor: " + str(self.ghost_activity_level) + "/10")

            self.total_events += 1

            # Av modu kontrolü
            hunt_threshold = 25
            if self.current_ghost_name == "Demon":
                hunt_threshold = 60  # Demon her zaman avlanabilir
            elif self.current_ghost_name == "Onryo" and not self.inventory["candle"]["active"]:
                hunt_threshold = 40

            hunt_chance = 0.04 * activity_mod * self.ghost_power
            if self.current_ghost_name == "Demon":
                hunt_chance *= 2

            if self.sanity < hunt_threshold and random.random() < hunt_chance:
                if self.can_hunt():
                    self.trigger_hunt()
                elif random.random() < 0.3:
                    self.log_event("[+] Koruyucu esyalar hayaletin avini engelledi!")
                    self.close_calls += 1

    def trigger_hunt(self):
        if self.hunt_mode:
            return
        self.hunt_mode = True
        self.hunt_count += 1
        self.log_event("")
        self.log_event("=" * 60)
        self.log_event("  !!!  AV MODU AKTIF! HAYALET AVLANIYOR!  !!!")
        self.log_event("=" * 60)
        self.log_event("")

        hunt_speed = self.current_ghost.get("hunt_speed", 1.0) * self.ghost_power
        variance = self.current_ghost.get("hunt_speed_variance", 0.2)
        hunt_speed += random.uniform(-variance, variance)
        hunt_duration = random.randint(7, 15)

        if self.inventory["salt"]["active"]:
            if self.current_ghost_name in PROTECTIVE_ITEMS["salt"]["effective_against"]:
                hunt_speed *= PROTECTIVE_ITEMS["salt"]["effects"]["ghost_slow"]
                self.log_event("[ITEM] Tuz hayaleti yavaslatiyor!")

        footstep = self.current_ghost.get("footstep_sound", "adim")

        for i in range(hunt_duration):
            if not self.game_active or not self.hunt_mode:
                break

            # Holy water av sırasında kullanılabilir
            if self.inventory.get("holy_water", {}).get("active", False):
                self.hunt_mode = False
                self.log_event("[ITEM] !!! Kutsal su av modunu durdurdu !!!")
                break

            time.sleep(max(0.6, 1.2 / hunt_speed))

            if self.current_ghost_name == "Myling":
                # Sessiz av
                if random.random() < 0.3:
                    self.log_event(">>> *...sessizlik...*")
            else:
                messages = [
                    ">>> *" + footstep + " yaklsiyor*",
                    ">>> *kapi carpıldı*",
                    ">>> *" + footstep + "*",
                    ">>> *sicaklik dususyor*",
                    ">>> *isiklar sondü*",
                    ">>> *nefes sesleri*",
                ]
                self.log_event(random.choice(messages))

            self.sanity -= random.uniform(0.8, 2.5) * self.ghost_power

        if self.hunt_mode:
            self.hunt_mode = False
            self.log_event("")
            self.log_event("[OK] Av modu sona erdi. Simdilik guvendesiniz...")
            self.log_event("")

    # =========================================================================
    # KANİT TARAMA
    # =========================================================================
    def scan_evidence(self, evidence_type):
        self.tools_used.add(evidence_type)
        ev_info = EVIDENCE_TYPES[evidence_type]
        scan_min, scan_max = ev_info.get("scan_time", (2, 4))
        time.sleep(random.uniform(scan_min, scan_max))

        has_evidence = evidence_type in self.ghost_evidence

        evidence_boost = 0
        if self.inventory["salt"]["active"]:
            evidence_boost = PROTECTIVE_ITEMS["salt"]["effects"]["evidence_boost"]

        if self.ghost_banished_timer > 0 or self.ghost_stunned_timer > 0:
            self.log_event("[!] Hayalet uzakta/sersem... Kanit bulmak zor olabilir.")
            base_chance = 0.25
        else:
            base_chance = 0.6

        base_chance += evidence_boost

        # Mimic özel: bazen yanlış kanıt verebilir
        if self.current_ghost_name == "Mimic" and not has_evidence and random.random() < 0.1:
            self.log_event("[!] Garip... bu kanit beklenmedik. Taklitci olabilir mi?")

        if evidence_type == "creates_isee_md":
            file_path = os.path.join(self.desktop_path, "ISEE.md")
            exists = os.path.exists(file_path)
            if has_evidence and (exists or random.random() < base_chance):
                if not exists:
                    self.create_isee_file()
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[EYE] >> ISEE.md dosyasi TESPIT EDILDI! [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[EYE] >> ISEE.md bulunamadi. [YOK]")
                return False

        elif evidence_type == "signal_emission":
            if has_evidence and random.random() < base_chance:
                sig = round(max(self.signal_strength, random.uniform(40, 90)), 1)
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[SIG] >> Sinyal TESPIT EDILDI! Guc: %" + str(sig) + " [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                sig = round(random.uniform(0, 10), 1)
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[SIG] >> Sinyal yok. Gurultu: %" + str(sig) + " [YOK]")
                return False

        elif evidence_type == "emf_spike":
            if has_evidence and random.random() < base_chance:
                lv = max(3, self.emf_level) if self.emf_level >= 3 else random.randint(3, 5)
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[EMF] >> EMF Level " + str(lv) + " TESPIT EDILDI! [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                lv = random.randint(0, 2)
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[EMF] >> EMF Level " + str(lv) + " - Normal. [YOK]")
                return False

        elif evidence_type == "temp_fluctuation":
            if has_evidence and random.random() < base_chance:
                temp = round(min(self.room_temperature, random.uniform(-12, 2)), 1)
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[TMP] >> Anormal sicaklik: " + str(temp) + " C [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                temp = round(random.uniform(18, 24), 1)
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[TMP] >> Sicaklik normal: " + str(temp) + " C [YOK]")
                return False

        elif evidence_type == "ghost_writing":
            file_found = any(os.path.exists(os.path.join(self.desktop_path, fn))
                           for fn in ["whisper.txt", "warning.txt", "prophecy.txt", "message_from_beyond.txt"])
            if has_evidence and (file_found or random.random() < base_chance):
                if not file_found:
                    self.create_ghost_writing()
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[WRT] >> Hayalet yazisi TESPIT EDILDI! [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[WRT] >> Hayalet yazisi bulunamadi. [YOK]")
                return False

        elif evidence_type == "folder_creation":
            folder_found = any(os.path.exists(os.path.join(self.desktop_path, fn))
                             for fn in ["DONT_OPEN", "HELP", "room_217", "BEHIND_YOU",
                                       "THEY_WATCH", "NO_EXIT", "LAST_WARNING",
                                       "HELP_ME", "WHO_AM_I", "THE_END"])
            if has_evidence and (folder_found or random.random() < base_chance):
                if not folder_found:
                    self.create_creepy_folders()
                self.evidence_scan_results[evidence_type] = True
                self.log_event("[FLD] >> Garip klasorler TESPIT EDILDI! [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[FLD] >> Anormal klasor bulunamadi. [YOK]")
                return False

        elif evidence_type == "process_spawning":
            if has_evidence and (len(self.ghost_processes) > 0 or random.random() < base_chance * 0.8):
                if len(self.ghost_processes) == 0:
                    self.create_ghost_exe()
                self.evidence_scan_results[evidence_type] = True
                ct = len(self.ghost_processes)
                self.log_event("[PRC] >> " + str(ct) + " gizli process TESPIT EDILDI! [VAR]")
                if evidence_type not in self.found_evidence:
                    self.found_evidence.append(evidence_type)
                return True
            else:
                self.evidence_scan_results[evidence_type] = False
                self.log_event("[PRC] >> Gizli process bulunamadi. [YOK]")
                return False
        return False

    def eliminate_by_evidence(self, evidence_type, has_it):
        eliminated_count = 0
        new_remaining = []
        for ghost_name in self.remaining_ghosts:
            ghost = GHOST_DATABASE[ghost_name]
            ghost_has = evidence_type in ghost["evidence"]
            if has_it and not ghost_has:
                self.eliminated_ghosts.append(ghost_name)
                eliminated_count += 1
                self.log_event("  [X] " + ghost_name + " (" + ghost["turkish_name"] + ") elendi")
            elif not has_it and ghost_has:
                self.eliminated_ghosts.append(ghost_name)
                eliminated_count += 1
                self.log_event("  [X] " + ghost_name + " (" + ghost["turkish_name"] + ") elendi")
            else:
                new_remaining.append(ghost_name)
        self.remaining_ghosts = new_remaining
        self.log_event("[INFO] " + str(eliminated_count) + " elendi. Kalan supheli: " + str(len(self.remaining_ghosts)))
        return eliminated_count

    def check_guess(self, ghost_name):
        if ghost_name == self.current_ghost_name:
            self.game_won = True
            return True
        else:
            self.sanity -= 20
            return False

    def cleanup(self):
        for proc in self.ghost_processes:
            try:
                proc.terminate()
                proc.kill()
            except Exception:
                pass
        for fp in self.created_files:
            try:
                if os.path.exists(fp):
                    os.remove(fp)
            except Exception:
                pass
        for fp in self.created_folders:
            try:
                if os.path.exists(fp):
                    shutil.rmtree(fp, ignore_errors=True)
            except Exception:
                pass
        for f in ["ISEE.md", "whisper.txt", "warning.txt", "prophecy.txt", "message_from_beyond.txt"]:
            try:
                p = os.path.join(self.desktop_path, f)
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass
        for f in ["DONT_OPEN", "HELP", "room_217", "BEHIND_YOU", "THEY_WATCH",
                  "NO_EXIT", "LAST_WARNING", "HELP_ME", "WHO_AM_I", "THE_END"]:
            try:
                p = os.path.join(self.desktop_path, f)
                if os.path.exists(p):
                    shutil.rmtree(p, ignore_errors=True)
            except Exception:
                pass
        self.game_active = False
        self.running = False

    def log_event(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if message.strip() == "":
            self.events_log.append("")
        else:
            self.events_log.append("[" + timestamp + "] " + message)


# =============================================================================
# ARAYÜZ
# =============================================================================
class GhostHunterGUI:
    def __init__(self):
        self.game = GhostHunterGame()
        self.root = tk.Tk()
        self.root.title("WINDOWS PARANORMAL INVESTIGATOR v6.6.6")
        self.root.geometry("1500x950")
        self.root.configure(bg="#0a0a0a")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen",
                                                                not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.last_log_index = 0

        self.colors = {
            "bg": "#0a0a0a",
            "bg_panel": "#111111",
            "bg_card": "#1a1a1a",
            "text": "#00ff00",
            "text_dim": "#006600",
            "text_bright": "#33ff33",
            "danger": "#ff0000",
            "warning": "#ff6600",
            "info": "#00aaff",
            "accent": "#ff00ff",
            "ghost": "#8800ff",
            "border": "#222222",
            "button_bg": "#1a1a2e",
            "button_active": "#0f3460",
            "candle": "#ffaa00",
            "crucifix": "#ffdd00",
            "incense": "#aa66ff",
            "salt": "#cccccc",
            "sage": "#66cc66",
            "holy_water": "#4488ff",
            "item_bg": "#0d0d1a",
        }

        self.item_colors = {
            "candle": self.colors["candle"],
            "crucifix": self.colors["crucifix"],
            "incense": self.colors["incense"],
            "salt": self.colors["salt"],
            "sage": self.colors["sage"],
            "holy_water": self.colors["holy_water"],
        }

        self.create_main_menu()
        self.update_loop()

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    # =========================================================================
    # ANA MENÜ
    # =========================================================================
    def create_main_menu(self):
        self.clear_window()
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(fill="both", expand=True)

        title_text = (
            "================================================================\n"
            "  W I N D O W S   P A R A N O R M A L   I N V E S T I G A T O R\n"
            "                       v 6 . 6 . 6\n"
            "================================================================\n"
            "         ___\n"
            "        /   \\\n"
            "       | o o |\n"
            "       |  >  |\n"
            "        \\___/\n"
            "        /| |\\\n"
            "       / | | \\\n"
            "================================================================"
        )
        tk.Label(main, text=title_text, font=("Consolas", 10), fg=self.colors["danger"],
                bg=self.colors["bg"], justify="center").pack(pady=12)

        tk.Label(main, text="[ Windows icinde paranormal aktivite tespit edildi... ]",
                font=("Consolas", 12), fg=self.colors["ghost"], bg=self.colors["bg"]).pack(pady=3)

        info_text = (
            "\n  NASIL OYNANIR:\n"
            "     * 27 benzersiz hayaletten biri rastgele secilir\n"
            "     * Her hayaletin kendine ozgu yetenekleri, zayifliklari ve davranislari var\n"
            "     * 7 arac ile kanit toplayin, 6 koruyucu esya kullanin\n"
            "     * Hayaletin izlerini takip edin ve turunu belirleyin\n"
            "\n  KORUYUCU ESYALAR:\n"
            "     (i) Mum          - Akil sagligini korur, karanlik varliklari iter\n"
            "     [+] Hac          - Av modunu engeller, hayaleti zayiflatir\n"
            "     {~} Tutsu        - Hayaleti uzaklastirir, sakinlestirir\n"
            "     [:] Tuz          - Hayaletin izini surer, yavaslatir\n"
            "     <#> Adacayi      - Odayi arindirır, guclu korunma\n"
            "     {O} Kutsal Su    - Hayaleti sersemletir, avi durdurur\n"
            "\n  HAYALET OZELLIKLERI:\n"
            "     * Her hayaletin benzersiz yetenegi var (teleport, ciglik, sekil degistirme...)\n"
            "     * Agresiflik, zeka, utangaclik, av hizi gibi ozellikler farkli\n"
            "     * Bazi hayaletler zamanla guclanir, bazilari zayiflar\n"
            "     * Koruyucu esyalar bazi hayaletlere ozel etki yapar\n"
        )
        tk.Label(main, text=info_text, font=("Consolas", 9), fg=self.colors["text"],
                bg=self.colors["bg"], justify="left").pack(pady=5)

        bf = tk.Frame(main, bg=self.colors["bg"])
        bf.pack(pady=12)

        tk.Button(bf, text=">>>  SORUSTURMAYI BASLAT  <<<", font=("Consolas", 16, "bold"),
                 fg="#ff0000", bg="#1a0000", activebackground="#330000", activeforeground="#ff3333",
                 relief="ridge", borderwidth=3, cursor="hand2", padx=30, pady=12,
                 command=self.start_investigation).pack(pady=6)

        tk.Button(bf, text="[?]  Hayalet Ansiklopedisi", font=("Consolas", 12),
                 fg=self.colors["info"], bg=self.colors["button_bg"],
                 activebackground=self.colors["button_active"],
                 relief="ridge", borderwidth=2, cursor="hand2", padx=20, pady=6,
                 command=self.show_ghost_encyclopedia).pack(pady=3)

        tk.Button(bf, text="[X]  Cikis", font=("Consolas", 12),
                 fg="#888888", bg=self.colors["bg_panel"], activebackground="#333333",
                 relief="ridge", borderwidth=2, cursor="hand2", padx=20, pady=6,
                 command=self.on_close).pack(pady=3)

    # =========================================================================
    # ANSİKLOPEDİ
    # =========================================================================
    def show_ghost_encyclopedia(self):
        enc = tk.Toplevel(self.root)
        enc.title("Hayalet Ansiklopedisi")
        enc.geometry("900x780")
        enc.configure(bg=self.colors["bg"])

        canvas = tk.Canvas(enc, bg=self.colors["bg"], highlightthickness=0)
        sb = tk.Scrollbar(enc, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=self.colors["bg"])
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        tk.Label(sf, text="HAYALET ANSIKLOPEDISI - 27 TUR", font=("Consolas", 14, "bold"),
                fg=self.colors["danger"], bg=self.colors["bg"]).pack(pady=8)

        # Eşya bilgisi
        itf = tk.Frame(sf, bg=self.colors["bg_card"], relief="ridge", borderwidth=2, padx=10, pady=8)
        itf.pack(fill="x", padx=10, pady=5)
        tk.Label(itf, text="KORUYUCU ESYALAR", font=("Consolas", 12, "bold"),
                fg=self.colors["candle"], bg=self.colors["bg_card"]).pack()
        for ik, ii in PROTECTIVE_ITEMS.items():
            t = ii["icon"] + " " + ii["turkish_name"] + " (x" + str(ii["max_uses"]) + ", " + str(ii["duration"]) + "s) - " + ii["description"]
            tk.Label(itf, text=t, font=("Consolas", 8), fg=self.colors["text"],
                    bg=self.colors["bg_card"], anchor="w", wraplength=830).pack(fill="x", pady=1)

        for i, (name, g) in enumerate(GHOST_DATABASE.items()):
            fr = tk.Frame(sf, bg=self.colors["bg_card"], relief="ridge", borderwidth=1, padx=8, pady=5)
            fr.pack(fill="x", padx=10, pady=2)

            ds = "!" * g["danger_level"]
            spd = str(g["hunt_speed"])
            agg = str(int(g["aggression"] * 100)) + "%"
            iq = str(int(g["intelligence"] * 100)) + "%"
            shy = str(int(g["shyness"] * 100)) + "%"

            tk.Label(fr, text="#" + str(i+1) + " " + name + " - " + g["turkish_name"] + " [" + ds + "]",
                    font=("Consolas", 10, "bold"), fg=self.colors["ghost"],
                    bg=self.colors["bg_card"], anchor="w").pack(fill="x")

            tk.Label(fr, text=g["description"], font=("Consolas", 8), fg=self.colors["text"],
                    bg=self.colors["bg_card"], anchor="w", wraplength=820).pack(fill="x")

            tk.Label(fr, text="Lore: " + g.get("lore", ""), font=("Consolas", 8), fg="#888888",
                    bg=self.colors["bg_card"], anchor="w", wraplength=820).pack(fill="x")

            stats = "Hiz:" + spd + " | Agresiflik:" + agg + " | Zeka:" + iq + " | Utangaclik:" + shy
            tk.Label(fr, text=stats, font=("Consolas", 8), fg=self.colors["warning"],
                    bg=self.colors["bg_card"], anchor="w").pack(fill="x")

            tk.Label(fr, text="Yetenek: " + g.get("ability_description", ""), font=("Consolas", 8),
                    fg=self.colors["accent"], bg=self.colors["bg_card"], anchor="w").pack(fill="x")

            tk.Label(fr, text="Zayiflik: " + g.get("weakness", ""), font=("Consolas", 8),
                    fg="#ff6666", bg=self.colors["bg_card"], anchor="w").pack(fill="x")

            evp = [EVIDENCE_TYPES[e]["icon"] + " " + EVIDENCE_TYPES[e]["name"] for e in g["evidence"]]
            tk.Label(fr, text="Kanitlar: " + ", ".join(evp), font=("Consolas", 8),
                    fg=self.colors["info"], bg=self.colors["bg_card"], anchor="w", wraplength=820).pack(fill="x")

        def close_enc():
            canvas.unbind_all("<MouseWheel>")
            enc.destroy()
        enc.protocol("WM_DELETE_WINDOW", close_enc)

    # =========================================================================
    # OYUN BAŞLAT
    # =========================================================================
    def start_investigation(self):
        self.game = GhostHunterGame()
        self.game.select_random_ghost()
        self.game.game_active = True
        self.game.running = True
        self.last_log_index = 0

        threading.Thread(target=self.game.ghost_activity_loop, daemon=True).start()
        threading.Thread(target=self._initial_activity, daemon=True).start()
        threading.Thread(target=self._timer_loop, daemon=True).start()

        self.create_investigation_gui()

    def _initial_activity(self):
        time.sleep(3)
        self.game.log_event("[~] Ortam taranıyor...")
        time.sleep(2)
        self.game.log_event("[~] ...bir seyler hissediliyor...")
        time.sleep(random.uniform(4, 8))

        # İlk kanıt
        if self.game.ghost_evidence:
            first = random.choice(self.game.ghost_evidence)
            if first == "creates_isee_md":
                self.game.create_isee_file()
            elif first == "folder_creation":
                self.game.create_creepy_folders()
            elif first == "ghost_writing":
                self.game.create_ghost_writing()
            elif first == "process_spawning":
                self.game.create_ghost_exe()
            elif first == "emf_spike":
                self.game.log_event("[EMF] EMF okuyucusu titredi... Seviye: " + str(random.randint(2, 4)))
            elif first == "temp_fluctuation":
                self.game.log_event("[TMP] Havada hafif bir soguma...")
            elif first == "signal_emission":
                self.game.log_event("[SIG] Radyoda hafif bir parazit...")

    def _timer_loop(self):
        while self.game.game_active and self.game.running:
            time.sleep(1)
            self.game.investigation_time += 1

    # =========================================================================
    # SORUŞTURMA ARAYÜZÜ
    # =========================================================================
    def create_investigation_gui(self):
        self.clear_window()
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(fill="both", expand=True)

        # ÜST BAR
        top = tk.Frame(main, bg=self.colors["bg_panel"], height=50)
        top.pack(fill="x", padx=4, pady=(4, 0))
        top.pack_propagate(False)

        self.sanity_label = tk.Label(top, text="AKIL: 100%", font=("Consolas", 11, "bold"),
                                    fg=self.colors["text"], bg=self.colors["bg_panel"])
        self.sanity_label.pack(side="left", padx=8)

        self.sanity_bar_frame = tk.Frame(top, bg="#333333", height=10, width=120)
        self.sanity_bar_frame.pack(side="left", padx=4)
        self.sanity_bar_frame.pack_propagate(False)
        self.sanity_bar_fill = tk.Frame(self.sanity_bar_frame, bg="#00ff00")
        self.sanity_bar_fill.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.time_label = tk.Label(top, text="SURE: 00:00", font=("Consolas", 10),
                                  fg=self.colors["info"], bg=self.colors["bg_panel"])
        self.time_label.pack(side="left", padx=12)

        self.temp_label = tk.Label(top, text="SICAKLIK: 22.0C", font=("Consolas", 10),
                                  fg=self.colors["warning"], bg=self.colors["bg_panel"])
        self.temp_label.pack(side="left", padx=8)

        self.emf_label = tk.Label(top, text="EMF: [.....]", font=("Consolas", 10),
                                 fg=self.colors["text_dim"], bg=self.colors["bg_panel"])
        self.emf_label.pack(side="left", padx=8)

        self.remaining_label = tk.Label(top, text="KALAN: 27", font=("Consolas", 10),
                                       fg=self.colors["ghost"], bg=self.colors["bg_panel"])
        self.remaining_label.pack(side="left", padx=8)

        self.power_label = tk.Label(top, text="", font=("Consolas", 9),
                                   fg=self.colors["danger"], bg=self.colors["bg_panel"])
        self.power_label.pack(side="left", padx=8)

        self.hunt_label = tk.Label(top, text="", font=("Consolas", 13, "bold"),
                                  fg=self.colors["danger"], bg=self.colors["bg_panel"])
        self.hunt_label.pack(side="right", padx=12)

        # İÇERİK
        content = tk.Frame(main, bg=self.colors["bg"])
        content.pack(fill="both", expand=True, padx=4, pady=4)

        # SOL PANEL
        left = tk.Frame(content, bg=self.colors["bg_panel"], width=340)
        left.pack(side="left", fill="y", padx=(0, 2))
        left.pack_propagate(False)

        left_canvas = tk.Canvas(left, bg=self.colors["bg_panel"], highlightthickness=0)
        left_sb = tk.Scrollbar(left, orient="vertical", command=left_canvas.yview)
        left_inner = tk.Frame(left_canvas, bg=self.colors["bg_panel"])
        left_inner.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.create_window((0, 0), window=left_inner, anchor="nw")
        left_canvas.configure(yscrollcommand=left_sb.set)
        left_canvas.pack(side="left", fill="both", expand=True)
        left_sb.pack(side="right", fill="y")
        left_canvas.bind("<Enter>", lambda e: left_canvas.bind_all("<MouseWheel>",
                         lambda ev: left_canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        left_canvas.bind("<Leave>", lambda e: left_canvas.unbind_all("<MouseWheel>"))

        # Araçlar
        tk.Label(left_inner, text="=== ARACLAR ===", font=("Consolas", 10, "bold"),
                fg=self.colors["warning"], bg=self.colors["bg_panel"]).pack(pady=(4, 2))

        self.evidence_buttons = {}
        self.evidence_status_labels = {}
        for et, ei in EVIDENCE_TYPES.items():
            bf = tk.Frame(left_inner, bg=self.colors["bg_card"], relief="ridge", borderwidth=1)
            bf.pack(fill="x", pady=1, padx=3)
            btn = tk.Button(bf, text=ei["icon"] + " " + ei["name"], font=("Consolas", 9),
                           fg=self.colors["info"], bg=self.colors["bg_card"],
                           activebackground=self.colors["button_active"],
                           relief="flat", cursor="hand2", anchor="w", padx=4, pady=2,
                           command=lambda t=et: self.use_tool(t))
            btn.pack(fill="x", side="left", expand=True)
            st = tk.Label(bf, text="[ ? ]", font=("Consolas", 9, "bold"),
                         fg="#555555", bg=self.colors["bg_card"])
            st.pack(side="right", padx=4)
            self.evidence_buttons[et] = btn
            self.evidence_status_labels[et] = st

        # Eşyalar
        tk.Label(left_inner, text="-" * 42, fg=self.colors["border"],
                bg=self.colors["bg_panel"], font=("Consolas", 8)).pack(pady=2)
        tk.Label(left_inner, text="=== KORUYUCU ESYALAR ===", font=("Consolas", 10, "bold"),
                fg=self.colors["candle"], bg=self.colors["bg_panel"]).pack(pady=(2, 2))

        self.item_buttons = {}
        self.item_status_labels = {}
        for ik, ii in PROTECTIVE_ITEMS.items():
            bf = tk.Frame(left_inner, bg=self.colors["item_bg"], relief="ridge", borderwidth=1)
            bf.pack(fill="x", pady=1, padx=3)
            clr = self.item_colors.get(ik, "#ffffff")
            btn = tk.Button(bf, text=ii["icon"] + " " + ii["turkish_name"],
                           font=("Consolas", 9, "bold"), fg=clr, bg=self.colors["item_bg"],
                           activebackground="#1a1a3e", relief="flat", cursor="hand2",
                           anchor="w", padx=4, pady=2,
                           command=lambda k=ik: self.use_item_gui(k))
            btn.pack(fill="x", side="left", expand=True)
            inv = self.game.inventory[ik]
            st = tk.Label(bf, text="x" + str(inv["count"]), font=("Consolas", 9, "bold"),
                         fg=clr, bg=self.colors["item_bg"])
            st.pack(side="right", padx=4)
            self.item_buttons[ik] = btn
            self.item_status_labels[ik] = st

        # Bulunan kanıtlar
        tk.Label(left_inner, text="-" * 42, fg=self.colors["border"],
                bg=self.colors["bg_panel"], font=("Consolas", 8)).pack(pady=2)
        tk.Label(left_inner, text="BULUNAN KANITLAR", font=("Consolas", 10, "bold"),
                fg=self.colors["text_bright"], bg=self.colors["bg_panel"]).pack()
        self.found_evidence_text = tk.Label(left_inner, text="Henuz kanit bulunamadi.",
                                          font=("Consolas", 9), fg=self.colors["text_dim"],
                                          bg=self.colors["bg_panel"], justify="left",
                                          wraplength=310, anchor="w")
        self.found_evidence_text.pack(fill="x", padx=5)

        # Eleme
        tk.Label(left_inner, text="-" * 42, fg=self.colors["border"],
                bg=self.colors["bg_panel"], font=("Consolas", 8)).pack(pady=2)
        tk.Label(left_inner, text="KANIT ILE ELEME", font=("Consolas", 10, "bold"),
                fg=self.colors["accent"], bg=self.colors["bg_panel"]).pack()

        for et, ei in EVIDENCE_TYPES.items():
            ef = tk.Frame(left_inner, bg=self.colors["bg_panel"])
            ef.pack(fill="x", pady=1)
            tk.Label(ef, text=ei["icon"], font=("Consolas", 8), fg=self.colors["text"],
                    bg=self.colors["bg_panel"], width=5).pack(side="left")
            tk.Button(ef, text="VAR", font=("Consolas", 8, "bold"), fg="#00ff00", bg="#002200",
                     activebackground="#004400", relief="flat", padx=3, pady=1,
                     command=lambda t=et: self.eliminate_ghosts_gui(t, True)).pack(side="left", padx=2)
            tk.Button(ef, text="YOK", font=("Consolas", 8, "bold"), fg="#ff0000", bg="#220000",
                     activebackground="#440000", relief="flat", padx=3, pady=1,
                     command=lambda t=et: self.eliminate_ghosts_gui(t, False)).pack(side="left", padx=2)
            tk.Label(ef, text=ei["name"][:16], font=("Consolas", 7), fg=self.colors["text_dim"],
                    bg=self.colors["bg_panel"]).pack(side="left", padx=2)

        # ORTA PANEL
        center = tk.Frame(content, bg=self.colors["bg_panel"])
        center.pack(side="left", fill="both", expand=True, padx=2)

        tk.Label(center, text="=== SORUSTURMA GUNLUGU ===", font=("Consolas", 12, "bold"),
                fg=self.colors["text"], bg=self.colors["bg_panel"]).pack(pady=4)

        self.log_text = scrolledtext.ScrolledText(center, font=("Consolas", 9), bg="#050505",
                                                  fg=self.colors["text"], insertbackground=self.colors["text"],
                                                  selectbackground=self.colors["ghost"], relief="flat",
                                                  state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

        for tag, color in [("danger", self.colors["danger"]), ("warning", self.colors["warning"]),
                          ("info", self.colors["info"]), ("ghost", self.colors["ghost"]),
                          ("success", "#00ff00"), ("system", "#888888"), ("item", self.colors["candle"]),
                          ("ambient", "#446644"), ("whisper", "#cc4444")]:
            self.log_text.tag_configure(tag, foreground=color)
        self.log_text.tag_configure("hunt", foreground="#ff0000", font=("Consolas", 11, "bold"))

        # SAĞ PANEL
        right = tk.Frame(content, bg=self.colors["bg_panel"], width=310)
        right.pack(side="right", fill="y", padx=(2, 0))
        right.pack_propagate(False)

        tk.Label(right, text="=== SUPHELI HAYALETLER ===", font=("Consolas", 11, "bold"),
                fg=self.colors["ghost"], bg=self.colors["bg_panel"]).pack(pady=4)

        gc = tk.Canvas(right, bg=self.colors["bg_panel"], highlightthickness=0)
        gsb = tk.Scrollbar(right, orient="vertical", command=gc.yview)
        self.ghost_list_frame = tk.Frame(gc, bg=self.colors["bg_panel"])
        self.ghost_list_frame.bind("<Configure>", lambda e: gc.configure(scrollregion=gc.bbox("all")))
        gc.create_window((0, 0), window=self.ghost_list_frame, anchor="nw")
        gc.configure(yscrollcommand=gsb.set)
        gc.pack(side="left", fill="both", expand=True)
        gsb.pack(side="right", fill="y")
        gc.bind("<Enter>", lambda e: gc.bind_all("<MouseWheel>",
                lambda ev: gc.yview_scroll(int(-1*(ev.delta/120)), "units")))
        gc.bind("<Leave>", lambda e: gc.unbind_all("<MouseWheel>"))

        self.populate_ghost_list()

        # ALT BAR
        bottom = tk.Frame(main, bg=self.colors["bg_panel"], height=48)
        bottom.pack(fill="x", padx=4, pady=(0, 4))
        bottom.pack_propagate(False)

        tk.Button(bottom, text="[!] HAYALET TURUNU TAHMIN ET", font=("Consolas", 12, "bold"),
                 fg=self.colors["accent"], bg="#1a001a", activebackground="#330033",
                 relief="ridge", borderwidth=2, cursor="hand2", padx=16,
                 command=self.open_guess_window).pack(side="left", padx=8, pady=6)

        tk.Button(bottom, text="[X] Temizle ve Cik", font=("Consolas", 10),
                 fg="#888888", bg=self.colors["bg_card"], activebackground="#333333",
                 relief="ridge", borderwidth=1, cursor="hand2", padx=8,
                 command=self.end_game).pack(side="right", padx=8, pady=6)

        self.active_items_label = tk.Label(bottom, text="", font=("Consolas", 10),
                                          fg=self.colors["candle"], bg=self.colors["bg_panel"])
        self.active_items_label.pack(side="right", padx=10)

    def populate_ghost_list(self):
        for w in self.ghost_list_frame.winfo_children():
            w.destroy()
        for gn in list(GHOST_DATABASE.keys()):
            g = GHOST_DATABASE[gn]
            elim = gn in self.game.eliminated_ghosts
            fr = tk.Frame(self.ghost_list_frame, bg="#1a0000" if elim else self.colors["bg_card"],
                         relief="ridge", borderwidth=1)
            fr.pack(fill="x", pady=1, padx=3)
            if elim:
                tk.Label(fr, text="  [X] " + gn + " (" + g["turkish_name"] + ")",
                        font=("Consolas", 8, "overstrike"), fg="#660000", bg="#1a0000",
                        anchor="w").pack(fill="x", padx=2, pady=1)
            else:
                tk.Label(fr, text="  [?] " + gn + " (" + g["turkish_name"] + ")",
                        font=("Consolas", 8), fg=self.colors["ghost"], bg=self.colors["bg_card"],
                        anchor="w").pack(fill="x", padx=2, pady=1)
                evp = [EVIDENCE_TYPES[e]["icon"] for e in g["evidence"]]
                agg = "A:" + str(int(g["aggression"]*10))
                tk.Label(fr, text="    " + " ".join(evp) + "  " + agg,
                        font=("Consolas", 7), fg=self.colors["text_dim"], bg=self.colors["bg_card"],
                        anchor="w").pack(fill="x", padx=2)

    # =========================================================================
    # ARAÇ & EŞYA
    # =========================================================================
    def use_tool(self, et):
        ei = EVIDENCE_TYPES[et]
        self.game.log_event("")
        self.game.log_event("=" * 50)
        self.game.log_event("[TOOL] " + ei["tool"] + " kullaniliyor...")
        self.game.log_event("[TOOL] " + ei["detail"])
        self.game.log_event("=" * 50)
        self.game.sanity -= random.uniform(0.3, 1.0)

        def scan():
            result = self.game.scan_evidence(et)
            self.root.after(0, lambda: self._update_evidence_status(et, result))
        threading.Thread(target=scan, daemon=True).start()

    def _update_evidence_status(self, et, result):
        try:
            if et in self.evidence_status_labels and self.evidence_status_labels[et].winfo_exists():
                if result:
                    self.evidence_status_labels[et].configure(text="[VAR]", fg="#00ff00")
                else:
                    self.evidence_status_labels[et].configure(text="[YOK]", fg="#ff0000")
        except Exception:
            pass
        if self.game.found_evidence:
            parts = ["  " + EVIDENCE_TYPES[e]["icon"] + " " + EVIDENCE_TYPES[e]["name"]
                     for e in self.game.found_evidence]
            try:
                self.found_evidence_text.configure(text="\n".join(parts), fg=self.colors["text_bright"])
            except Exception:
                pass

    def use_item_gui(self, ik):
        threading.Thread(target=lambda: self._use_item_thread(ik), daemon=True).start()

    def _use_item_thread(self, ik):
        self.game.use_protective_item(ik)
        self.root.after(0, self._update_item_display)

    def _update_item_display(self):
        for ik, iv in self.game.inventory.items():
            try:
                if ik in self.item_status_labels and self.item_status_labels[ik].winfo_exists():
                    t = "x" + str(iv["count"])
                    if iv["active"]:
                        t += " [" + str(iv["timer"]) + "s]"
                    self.item_status_labels[ik].configure(text=t)
            except Exception:
                pass

    # =========================================================================
    # ELEME & TAHMİN
    # =========================================================================
    def eliminate_ghosts_gui(self, et, has_it):
        ei = EVIDENCE_TYPES[et]
        self.game.log_event("")
        self.game.log_event("-" * 50)
        self.game.log_event("[ELEME] " + ei["name"] + " -> " + ("VAR" if has_it else "YOK"))
        self.game.log_event("-" * 50)
        self.game.eliminate_by_evidence(et, has_it)
        self.root.after(100, self.populate_ghost_list)
        if len(self.game.remaining_ghosts) == 1:
            self.game.log_event("")
            self.game.log_event("=" * 50)
            gn = self.game.remaining_ghosts[0]
            g = GHOST_DATABASE[gn]
            self.game.log_event("[!!!] TEK SUPHELI KALDI: " + gn + " (" + g["turkish_name"] + ")")
            self.game.log_event("[!!!] Yetenek: " + g.get("ability_description", ""))
            self.game.log_event("[!!!] Zayiflik: " + g.get("weakness", ""))
            self.game.log_event("=" * 50)
        elif len(self.game.remaining_ghosts) == 0:
            self.game.log_event("[HATA] Tum hayaletler elendi! Sifirlanıyor...")
            self.game.remaining_ghosts = list(GHOST_DATABASE.keys())
            self.game.eliminated_ghosts = []
            self.root.after(100, self.populate_ghost_list)

    def open_guess_window(self):
        gw = tk.Toplevel(self.root)
        gw.title("Hayalet Turunu Tahmin Et")
        gw.geometry("700x780")
        gw.configure(bg=self.colors["bg"])
        gw.transient(self.root)
        gw.grab_set()

        tk.Label(gw, text="[?] HANGI HAYALET?", font=("Consolas", 16, "bold"),
                fg=self.colors["accent"], bg=self.colors["bg"]).pack(pady=8)
        tk.Label(gw, text="Kalan: " + str(len(self.game.remaining_ghosts)) + " / 27",
                font=("Consolas", 10), fg=self.colors["text"], bg=self.colors["bg"]).pack()

        if self.game.found_evidence:
            evp = [EVIDENCE_TYPES[e]["icon"] for e in self.game.found_evidence]
            tk.Label(gw, text="Kanitlar: " + " ".join(evp), font=("Consolas", 10),
                    fg=self.colors["info"], bg=self.colors["bg"]).pack()

        tk.Label(gw, text="!! Yanlis tahmin = -20 Akil Sagligi!", font=("Consolas", 10),
                fg=self.colors["danger"], bg=self.colors["bg"]).pack(pady=4)

        c = tk.Canvas(gw, bg=self.colors["bg"], highlightthickness=0)
        sb = tk.Scrollbar(gw, orient="vertical", command=c.yview)
        bf = tk.Frame(c, bg=self.colors["bg"])
        bf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0, 0), window=bf, anchor="nw")
        c.configure(yscrollcommand=sb.set)
        c.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        sb.pack(side="right", fill="y")
        c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Kalan hayaletleri önce göster
        for gn in sorted(GHOST_DATABASE.keys(), key=lambda x: (x in self.game.eliminated_ghosts, x)):
            g = GHOST_DATABASE[gn]
            elim = gn in self.game.eliminated_ghosts
            if elim:
                tk.Button(bf, text="  [X] " + gn + " (" + g["turkish_name"] + ") - ELENDI",
                         font=("Consolas", 9, "overstrike"), fg="#440000", bg="#110000",
                         relief="flat", anchor="w", state="disabled", padx=8, pady=2).pack(fill="x", pady=1, padx=4)
            else:
                evp = [EVIDENCE_TYPES[e]["icon"] for e in g["evidence"]]
                txt = "  [>] " + gn + " (" + g["turkish_name"] + ") " + " ".join(evp)
                tk.Button(bf, text=txt, font=("Consolas", 9), fg=self.colors["ghost"],
                         bg=self.colors["bg_card"], activebackground=self.colors["accent"],
                         activeforeground="#ffffff", relief="ridge", anchor="w", cursor="hand2",
                         padx=8, pady=2,
                         command=lambda n=gn, w=gw, cv=c: self.make_guess(n, w, cv)).pack(fill="x", pady=1, padx=4)

        def close_g():
            c.unbind_all("<MouseWheel>")
            gw.destroy()
        gw.protocol("WM_DELETE_WINDOW", close_g)

    def make_guess(self, gn, win, canvas):
        canvas.unbind_all("<MouseWheel>")
        win.destroy()
        if self.game.check_guess(gn):
            self.show_victory(gn)
        else:
            self.game.log_event("")
            self.game.log_event("=" * 50)
            self.game.log_event("[X] YANLIS! " + gn + " degil! (-20 Akil Sagligi)")
            self.game.log_event("=" * 50)
            if gn in self.game.remaining_ghosts:
                self.game.remaining_ghosts.remove(gn)
                self.game.eliminated_ghosts.append(gn)
            self.populate_ghost_list()
            if self.game.sanity <= 0:
                self.show_game_over()

    # =========================================================================
    # KAZANMA / KAYBETME
    # =========================================================================
    def show_victory(self, gn):
        self.game.game_active = False
        g = GHOST_DATABASE[gn]

        vw = tk.Toplevel(self.root)
        vw.title("KAZANDINIZ!")
        vw.geometry("700x700")
        vw.configure(bg="#001a00")
        vw.transient(self.root)

        tk.Label(vw, text="<<< SORUSTURMA TAMAMLANDI >>>", font=("Consolas", 18, "bold"),
                fg="#00ff00", bg="#001a00").pack(pady=12)
        tk.Label(vw, text=g.get("ascii_art", ""), font=("Consolas", 10),
                fg=self.colors["ghost"], bg="#001a00").pack()

        m = self.game.investigation_time // 60
        s = self.game.investigation_time % 60
        ds = "!" * g["danger_level"]
        score = max(0, 2000 - self.game.investigation_time * 2) + int(self.game.sanity * 15) + \
                len(self.game.found_evidence) * 300 + len(self.game.tools_used) * 50 + \
                self.game.special_events_triggered * 25 + self.game.close_calls * 100

        items_used = [PROTECTIVE_ITEMS[k]["turkish_name"] + " x" + str(v["total_used"])
                     for k, v in self.game.inventory.items() if v["total_used"] > 0]

        txt = (
            "\nHayalet: " + gn + " (" + g["turkish_name"] + ")\n"
            "Tehlike: " + ds + " | Zayiflik: " + g.get("weakness", "?") + "\n"
            "Yetenek: " + g.get("ability_description", "") + "\n\n"
            + g["description"] + "\n"
            + g.get("lore", "") + "\n\n"
            "================================\n"
            "Sure: " + str(m) + ":" + str(s).zfill(2) + "\n"
            "Kalan Akil: %" + str(int(self.game.sanity)) + "\n"
            "Arac: " + str(len(self.game.tools_used)) + "/7 | Kanit: " + str(len(self.game.found_evidence)) + "/3\n"
            "Av Sayisi: " + str(self.game.hunt_count) + " | Ucuz Kurtulus: " + str(self.game.close_calls) + "\n"
            "Ozel Olay: " + str(self.game.special_events_triggered) + "\n"
            "Esyalar: " + (", ".join(items_used) if items_used else "Hicbiri") + "\n"
            "================================\n"
            "SKOR: " + str(score) + "\n"
            "================================"
        )
        tk.Label(vw, text=txt, font=("Consolas", 9), fg="#00ff00", bg="#001a00",
                justify="center").pack(pady=8)
        tk.Button(vw, text="[OK] Temizle ve Kapat", font=("Consolas", 12, "bold"),
                 fg="#ffffff", bg="#004400", activebackground="#006600", relief="ridge",
                 padx=18, pady=8, command=lambda: [vw.destroy(), self.end_game()]).pack(pady=8)

    def show_game_over(self):
        self.game.game_active = False
        g = GHOST_DATABASE[self.game.current_ghost_name]

        gow = tk.Toplevel(self.root)
        gow.title("OYUN BITTI")
        gow.geometry("650x550")
        gow.configure(bg="#1a0000")
        gow.transient(self.root)

        tk.Label(gow, text="!!! AKIL SAGLIGINIZ SIFIRA DUSTU !!!", font=("Consolas", 16, "bold"),
                fg="#ff0000", bg="#1a0000").pack(pady=12)
        tk.Label(gow, text=g.get("ascii_art", ""), font=("Consolas", 12),
                fg="#ff0000", bg="#1a0000").pack()

        m = self.game.investigation_time // 60
        s = self.game.investigation_time % 60
        txt = (
            "\nHayalet sizi ele gecirdi...\n\n"
            "Gercek: " + self.game.current_ghost_name + " (" + g["turkish_name"] + ")\n"
            "Yetenek: " + g.get("ability_description", "") + "\n"
            "Zayiflik: " + g.get("weakness", "?") + "\n\n"
            "\"" + g["description"] + "\"\n\n"
            "Sure: " + str(m) + ":" + str(s).zfill(2) + " | Kanit: " + str(len(self.game.found_evidence)) + "/3\n"
            "Av Sayisi: " + str(self.game.hunt_count)
        )
        tk.Label(gow, text=txt, font=("Consolas", 10), fg="#ff6666", bg="#1a0000",
                justify="center").pack(pady=8)
        tk.Button(gow, text="[OK] Temizle ve Kapat", font=("Consolas", 12, "bold"),
                 fg="#ffffff", bg="#440000", activebackground="#660000", relief="ridge",
                 padx=18, pady=8, command=lambda: [gow.destroy(), self.end_game()]).pack(pady=8)

    def end_game(self):
        self.game.game_active = False
        self.game.running = False
        time.sleep(0.3)
        self.game.cleanup()
        self.root.after(1000, self.create_main_menu)

    # =========================================================================
    # GÜNCELLEME
    # =========================================================================
    def update_loop(self):
        if self.game.game_active:
            try:
                san = max(0, self.game.sanity)
                clr = "#00ff00" if san > 50 else ("#ffaa00" if san > 25 else "#ff0000")

                if hasattr(self, "sanity_label") and self.sanity_label.winfo_exists():
                    self.sanity_label.configure(text="AKIL: " + str(int(san)) + "%", fg=clr)
                if hasattr(self, "sanity_bar_fill") and self.sanity_bar_fill.winfo_exists():
                    self.sanity_bar_fill.configure(bg=clr)
                    self.sanity_bar_fill.place(x=0, y=0, relwidth=max(0, san/100), relheight=1.0)

                m = self.game.investigation_time // 60
                s = self.game.investigation_time % 60
                if hasattr(self, "time_label") and self.time_label.winfo_exists():
                    self.time_label.configure(text="SURE: " + str(m).zfill(2) + ":" + str(s).zfill(2))

                if hasattr(self, "temp_label") and self.temp_label.winfo_exists():
                    t = round(self.game.room_temperature, 1)
                    tc = self.colors["warning"] if t >= 5 else ("#00ccff" if t >= 0 else "#0088ff")
                    self.temp_label.configure(text="SICAK: " + str(t) + "C", fg=tc)

                if hasattr(self, "emf_label") and self.emf_label.winfo_exists():
                    e = self.game.emf_level
                    ec = self.colors["text_dim"] if e < 3 else (self.colors["warning"] if e < 5 else self.colors["danger"])
                    bars = "|" * e + "." * (5 - e)
                    self.emf_label.configure(text="EMF:[" + bars + "]", fg=ec)

                if hasattr(self, "remaining_label") and self.remaining_label.winfo_exists():
                    self.remaining_label.configure(text="KALAN:" + str(len(self.game.remaining_ghosts)))

                if hasattr(self, "power_label") and self.power_label.winfo_exists():
                    pw = self.game.ghost_power
                    if pw != 1.0:
                        pt = "GUC:" + str(round(pw, 2))
                        self.power_label.configure(text=pt, fg="#ff0000" if pw > 1 else "#00ff00")
                    else:
                        self.power_label.configure(text="")

                if hasattr(self, "hunt_label") and self.hunt_label.winfo_exists():
                    if self.game.hunt_mode:
                        self.hunt_label.configure(text="!!! AV MODU !!!", fg="#ff0000")
                    elif self.game.ghost_stunned_timer > 0:
                        self.hunt_label.configure(text="[SERSEM " + str(self.game.ghost_stunned_timer) + "s]",
                                                 fg=self.colors["holy_water"])
                    elif self.game.ghost_banished_timer > 0:
                        self.hunt_label.configure(text="[UZAKTA " + str(self.game.ghost_banished_timer) + "s]",
                                                 fg=self.colors["incense"])
                    else:
                        self.hunt_label.configure(text="")

                self._update_item_display()

                if hasattr(self, "active_items_label") and self.active_items_label.winfo_exists():
                    ap = []
                    for ik, iv in self.game.inventory.items():
                        if iv["active"]:
                            ap.append(PROTECTIVE_ITEMS[ik]["icon"] + str(iv["timer"]) + "s")
                    self.active_items_label.configure(text="Aktif: " + " ".join(ap) if ap else "")

                self._update_log()

                if san <= 0 and not self.game.game_over:
                    self.game.game_over = True
                    self.show_game_over()
            except Exception:
                pass

        self.root.after(200, self.update_loop)

    def _update_log(self):
        if not hasattr(self, "log_text"):
            return
        try:
            if not self.log_text.winfo_exists():
                return
        except Exception:
            return

        cl = len(self.game.events_log)
        if cl > self.last_log_index:
            self.log_text.configure(state="normal")
            for i in range(self.last_log_index, cl):
                msg = self.game.events_log[i]
                if msg.strip() == "":
                    self.log_text.insert("end", "\n")
                    continue
                tag = "system"
                if "AV MODU" in msg or "!!! " in msg:
                    tag = "hunt"
                elif ">>>" in msg:
                    tag = "danger"
                elif "WHISPER" in msg:
                    tag = "whisper"
                elif "TESPIT" in msg or "[VAR]" in msg or "[OK]" in msg or "TAMAMLANDI" in msg:
                    tag = "success"
                elif "[YOK]" in msg or "elendi" in msg or "YANLIS" in msg:
                    tag = "warning"
                elif "[TOOL]" in msg:
                    tag = "ghost"
                elif "[ITEM]" in msg:
                    tag = "item"
                elif "[~]" in msg:
                    tag = "ambient"
                elif "[EYE]" in msg or "[SIG]" in msg or "[EMF]" in msg or "[TMP]" in msg or "[WRT]" in msg or "[FLD]" in msg or "[PRC]" in msg:
                    tag = "info"
                elif "[!!]" in msg:
                    tag = "danger"
                self.log_text.insert("end", msg + "\n", tag)
            self.log_text.configure(state="disabled")
            self.log_text.see("end")
            self.last_log_index = cl

    def on_close(self):
        if self.game.game_active:
            if not messagebox.askyesno("Cikis", "Sorusturma devam ediyor!\nTemizleyip cikilsin mi?"):
                return
        self.game.game_active = False
        self.game.running = False
        time.sleep(0.3)
        self.game.cleanup()
        self.root.destroy()
        sys.exit(0)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("================================================================")
    print("  WINDOWS PARANORMAL INVESTIGATOR v6.6.6")
    print("  27 Hayalet | 7 Arac | 6 Koruyucu Esya")
    print("================================================================")
    app = GhostHunterGUI()
    app.run()