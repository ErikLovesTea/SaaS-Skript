# Erik ....., TA-25A, viimane tõsine muudatus ~2023-07-06

import ctypes
import json
import os
import pickle
import random
import re
import shutil
import subprocess
import sys
import time
import tkinter as tk
import datetime
from getpass import getuser
from threading import Thread
from tkinter import filedialog
import win32gui
from cryptography.fernet import Fernet
import bson
import dearpygui.dearpygui as dpg
import requests
import win32api
import win32con
import win32event
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from pymongo.mongo_client import MongoClient
import pyautogui

MB_OK = 0x0
MB_ICONERROR = 0x10
MB_ICONINFORMATION = 0x40


def show_error_message(message):
    ctypes.windll.user32.MessageBoxW(0, str(message), "Error", MB_OK | MB_ICONERROR)


def show_info_message(message):
    ctypes.windll.user32.MessageBoxW(0, str(message), "Info", MB_OK | MB_ICONINFORMATION)


def check_internet_connection():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as exception:
        show_error_message("No internet connection")
        sys.exit()


check_internet_connection()
CONFIG = {
    "linear": {
        "dx": 0,
        "dy": 0,
        "delay": 0.0
    },
    "nonlinear": {
        "horizontal": {
            "dx": 0,
            "dy": 0,
            "delay": 0.0
        },
        "vertical": {
            "dx": 0,
            "dy": 0,
            "delay": 0.0
        },
    }
}

SLEEP = True
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)
script_path = sys.argv[0]
script_name = os.path.basename(script_path)
file_to_encrypt = script_name
field_value11 = None
field_value15 = None
serial_number = ""
remaining_days = 0
remaining_hours = 0
KEY_ID = 0
SAVE_FILE_LOCATION = str(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil\\savedlogin.dmt")
DEFAULT_USER = ""
DEFAULT_PASS = ""
SAVED_LOGIN = []
URI = "XXX" # Demo build, ära nuta.
USERNAME = ""
PASSWORD = ""
VIEWPORT_NAME = "SiegeMP recoil"
VIEWPORT_WIDTH = 500
VIEWPORT_HEIGHT = 500
VIEWPORT_ON_TOP = True

FLOAT_PRECISION = "%0.3f"  # "%0.2f" "%0.3f" "%0.4f"
SPEED_DRAG_FLOAT = 0.01  # 0.01 0.001 0.0001
LINEAR_DX_MIN = -32
LINEAR_DX_MAX = 32
LINEAR_DY_MIN = -32
LINEAR_DY_MAX = 32
LINEAR_DELAY_MIN = 0.0
LINEAR_DELAY_MAX = 128.0

NONLINEAR_H_DX_MIN = -32
NONLINEAR_H_DX_MAX = 32
NONLINEAR_H_DY_MIN = -32
NONLINEAR_H_DY_MAX = 32
NONLINEAR_H_DELAY_MIN = 0.0
NONLINEAR_H_DELAY_MAX = 128.0  # 8.0 16.0 32.0 64.0 128.0

NONLINEAR_V_DX_MIN = -32
NONLINEAR_V_DX_MAX = 32
NONLINEAR_V_DY_MIN = -32
NONLINEAR_V_DY_MAX = 32
NONLINEAR_V_DELAY_MIN = 0.0
NONLINEAR_V_DELAY_MAX = 128.0  # 8.0 16.0 32.0 64.0 128.0

ACTIVATE_MACRO_BTN = win32con.VK_F1
SELECT_MACRO_BTN = win32con.VK_F2
AIM_BTN = win32con.VK_RBUTTON
SHOOT_BTN = win32con.VK_LBUTTON

EXIT = False
INIT_TIME = 0.0
TIME = 0.0
CURSOR_POS = [0, 0]
MACRO_INIT_TIME = 0.0
MACRO_EXECUTION_TIME = 0.0
LINEAR_MACRO_RUNNING = False
NONLINEAR_MACRO_RUNNING = False
ACTIVATE_MACRO = True
RUN_LINEAR_MACRO = False
RUN_NONLINEAR_MACRO = True
EVENT_ACTIVATE_MACRO_BTN = win32event.CreateEvent(None, 1, 0, None)
EVENT_SELECT_MACRO_BTN = win32event.CreateEvent(None, 1, 0, None)


def encrypt_the_program():
    with open(file_to_encrypt, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(file_to_encrypt, 'wb') as file:
        file.write(encrypted_data)

    current_file = script_name
    new_file = f'{random.randint(a=10000, b=10000000)}.exe'
    os.rename(script_path, new_file)


def check_connection_to_db():
    try:
        client = MongoClient(URI)
        database = client["Cluster0"]
        collection = database["Status"]
        result = collection.find_one({})

        array_field = result["Status"]
        python_array = list(array_field)

        if python_array[0]:
            pass
        else:
            show_info_message("program is disabled")
            encrypt_the_program()
            sys.exit()
        if python_array[1] != 5:
            encrypt_the_program()
            show_error_message("This program is outdated, please reinstall")
            sys.exit()

    except ConnectionFailure as err:
        show_error_message(f"TLS error, fix is in discord | A = {err}")
        sys.exit()
    except Exception as err:
        show_error_message(err)
        sys.exit()


check_connection_to_db()

try:
    with open(SAVE_FILE_LOCATION, "rb") as bs:
        loaded_login = pickle.load(bs)
        SAVED_LOGIN = loaded_login
        DEFAULT_USER = SAVED_LOGIN[0]
        DEFAULT_PASS = SAVED_LOGIN[1]
except:
    pass


def init():
    global INIT_TIME
    INIT_TIME = time.time()
    return


def is_aimbtn_pressed():
    global SLEEP

    while not EXIT:
        if abs(win32api.GetKeyState(AIM_BTN)) > 1:
            SLEEP = False
        else:
            SLEEP = True
        time.sleep(0.01)

    return


colordata = [(0, 0, 0), (255, 255, 255)]


def changetextcolor():
    colordata[1] = dpg.get_value("cp")
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, colordata[1], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, colordata[0], category=dpg.mvThemeCat_Core)

            dpg.bind_theme(global_theme)


def changetabcolor():
    colordata[0] = dpg.get_value("cp")
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, colordata[1], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colordata[0], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, colordata[0], category=dpg.mvThemeCat_Core)

            dpg.bind_theme(global_theme)


def ispressed():
    key = win32api.GetKeyState(0x02)

    if key < 0:
        return key < 0


def click():
    sleepTime = datetime.timedelta(milliseconds=10)

    start_time = datetime.datetime.now()
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    while start_time + sleepTime > datetime.datetime.now():
        pass

    start_time = datetime.datetime.now()
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    while start_time + sleepTime > datetime.datetime.now():
        pass


def request_send_encrypt():
    client1 = MongoClient(URI)
    db1 = client1["Cluster0"]
    collection191 = db1["Accounts"]

    user_value = str(dpg.get_value("encreq_user"))
    documents = collection191.find({"Username": user_value})

    for document in documents:
        found_value = document['_id']
        filter_a = {'_id': found_value}
        update = {'$set': {'EncReq': True}}
        collection191.update_one(filter_a, update)


def hwid_ban():
    grabbed_user1 = dpg.get_value("hwid_ban_user")
    if str(grabbed_user1) == "Admin":
        show_error_message("Request declined")
        return
    client1 = MongoClient(URI)
    db1 = client1["Cluster0"]
    collection191 = db1["Accounts"]

    user_value = str(grabbed_user1)
    documents = collection191.find({"Username": user_value})

    for document in documents:
        found_value = document['hwid']
        client2 = MongoClient(URI)
        database2 = client2['Cluster0']
        collection2 = database2['banned']
        doc2 = {f"{str(random.randint(a=1, b=1000))}": str(found_value)}
        collection2.insert_one(doc2)

    filter233 = {"Username": user_value}
    documents12 = collection191.find(filter233)

    for document in documents12:
        document_id11 = document["_id"]
        filter_a = {'_id': bson.ObjectId(document_id11)}
        update = {'$set': {'Banned': True}}
        # noinspection PyShadowingNames
        collection191.update_one(filter_a, update)


def hwid_reset():
    grabbed_user1 = dpg.get_value("hwid_reset_user")

    if str(grabbed_user1) == "Admin":
        show_error_message("Request declined")
        return

    client1 = MongoClient(URI)
    db1 = client1["Cluster0"]
    collection191 = db1["Accounts"]

    user_value = str(grabbed_user1)
    documents = collection191.find({"Username": user_value})

    for document in documents:
        found_value = document['_id']
        filter_a = {'_id': found_value}
        update = {'$set': {'hwid': None}}
        collection191.update_one(filter_a, update)


def linearRecoil():
    global EXIT, AIM_BTN, SHOOT_BTN, RUN_LINEAR_MACRO, LINEAR_MACRO_RUNNING, ACTIVATE_MACRO, CONFIG

    while not EXIT:
        if SLEEP:
            time.sleep(0.1)
            continue
        if not ACTIVATE_MACRO:
            time.sleep(0.1)
            continue
        if win32api.GetKeyState(AIM_BTN) < 0 and win32api.GetKeyState(
                SHOOT_BTN) < 0 and RUN_LINEAR_MACRO and ACTIVATE_MACRO:
            LINEAR_MACRO_RUNNING = True
            print("HI")
            dx = int(CONFIG["linear"]["dx"])
            dy = int(CONFIG["linear"]["dy"])
            CONFIG["linear"]["delay"] = dpg.get_value("drag_float_linear_delay")
            msdelay = CONFIG["linear"]["delay"] / 1000.000
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, dy, 0, 0)
            time.sleep(msdelay)
        else:
            LINEAR_MACRO_RUNNING = False

    return


def nonlinearRecoilHorizontal():
    global EXIT, AIM_BTN, SHOOT_BTN, RUN_NONLINEAR_MACRO, NONLINEAR_MACRO_RUNNING, ACTIVATE_MACRO, CONFIG

    while not EXIT:
        if SLEEP:
            time.sleep(0.1)
            continue
        if not ACTIVATE_MACRO:
            time.sleep(0.1)
            continue
        if win32api.GetKeyState(AIM_BTN) < 0 and win32api.GetKeyState(
                SHOOT_BTN) < 0 and RUN_NONLINEAR_MACRO and ACTIVATE_MACRO:
            NONLINEAR_MACRO_RUNNING = True
            dx = int(CONFIG["nonlinear"]["horizontal"]["dx"])
            dy = int(CONFIG["nonlinear"]["horizontal"]["dy"])
            msdelay = CONFIG["nonlinear"]["horizontal"]["delay"] / 1000.000
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, dy, 0, 0)
            time.sleep(msdelay)
        else:
            NONLINEAR_MACRO_RUNNING = False
    return


# noinspection PyShadowingNames
def find_user_by_key():
    global field_value11
    grabbed_user = dpg.get_value("find_key_user")
    # noinspection PyShadowingNames
    client = MongoClient(URI)
    db = client["Cluster0"]
    collection19 = db["Accounts"]

    key_value = str(grabbed_user)
    documents = collection19.find({"Key": key_value})

    for document in documents:
        field_value11 = document['Username']


def nonlinearRecoilVertical():
    global EXIT, AIM_BTN, SHOOT_BTN, RUN_NONLINEAR_MACRO, ACTIVATE_MACRO, CONFIG

    while not EXIT:
        if SLEEP:
            time.sleep(0.1)
            continue
        if not ACTIVATE_MACRO:
            time.sleep(0.1)
            continue
        if win32api.GetKeyState(AIM_BTN) < 0 and win32api.GetKeyState(
                SHOOT_BTN) < 0 and RUN_NONLINEAR_MACRO and ACTIVATE_MACRO:
            dx = int(CONFIG["nonlinear"]["vertical"]["dx"])
            dy = int(CONFIG["nonlinear"]["vertical"]["dy"])
            msdelay = CONFIG["nonlinear"]["vertical"]["delay"] / 1000.000
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, dy, 0, 0)
            time.sleep(msdelay)

    return


def isMacroActivated():
    global EVENT_ACTIVATE_MACRO_BTN, ACTIVATE_MACRO_BTN, ACTIVATE_MACRO
    keystate = win32api.GetKeyState(ACTIVATE_MACRO_BTN)

    if keystate < 0:
        if win32event.WaitForSingleObject(EVENT_ACTIVATE_MACRO_BTN, 0) == win32event.WAIT_TIMEOUT:
            value = dpg.get_value("checkbox_activate_macro")
            win32event.SetEvent(EVENT_ACTIVATE_MACRO_BTN)
            if value:
                dpg.set_value("checkbox_activate_macro", False)
            else:
                dpg.set_value("checkbox_activate_macro", True)
    else:
        win32event.ResetEvent(EVENT_ACTIVATE_MACRO_BTN)

    return


def isMacroSelected():
    global SELECT_MACRO_BTN, EVENT_SELECT_MACRO_BTN
    keystate = win32api.GetKeyState(SELECT_MACRO_BTN)

    if keystate < 0:
        if win32event.WaitForSingleObject(EVENT_SELECT_MACRO_BTN, 0) == win32event.WAIT_TIMEOUT:
            value = dpg.get_value("macro_tab")
            win32event.SetEvent(EVENT_SELECT_MACRO_BTN)
            if value == "linear_tab":
                dpg.set_value("macro_tab", "nonlinear_tab")
            else:
                dpg.set_value("macro_tab", "linear_tab")
    else:
        win32event.ResetEvent(EVENT_SELECT_MACRO_BTN)


def selectCurrentMacro():
    global RUN_LINEAR_MACRO, RUN_NONLINEAR_MACRO
    tabvalue = str(dpg.get_value("macro_tab"))
    print(tabvalue)

    if RUN_LINEAR_MACRO == RUN_NONLINEAR_MACRO:
        RUN_LINEAR_MACRO = True
        RUN_NONLINEAR_MACRO = False
        return

    if tabvalue == "55":
        RUN_LINEAR_MACRO = True
        RUN_NONLINEAR_MACRO = False

    else:
        RUN_LINEAR_MACRO = False
        RUN_NONLINEAR_MACRO = True

    return


def listenInput():
    isMacroActivated()
    isMacroSelected()
    selectCurrentMacro()
    return


def updateWindowProportion():
    id = ["config_panel"]
    heightMargen = 18.0
    # widthMainWindow = dpg.get_item_width("main_window")
    heightMainWindow = dpg.get_item_height("main_window") - heightMargen
    heightPanel1 = 0
    heightPanel2 = 0
    heightPanel1 = heightMainWindow - heightPanel2
    dpg.set_item_height(id[0], int(heightPanel1))
    dpg.set_primary_window("main_window", True)

    return


def updateMetrics():
    global INIT_TIME, TIME, CURSOR_POS, MACRO_INIT_TIME, MACRO_EXECUTION_TIME
    global LINEAR_MACRO_RUNNING, NONLINEAR_MACRO_RUNNING

    TIME = time.time() - INIT_TIME

    try:
        CURSOR_POS = win32api.GetCursorPos()
    except Exception:
        pass

    if LINEAR_MACRO_RUNNING or NONLINEAR_MACRO_RUNNING:
        MACRO_EXECUTION_TIME = time.time() - MACRO_INIT_TIME
    else:
        MACRO_EXECUTION_TIME = 0.000
        MACRO_INIT_TIME = time.time()

    str0 = "Cursor: " + str(CURSOR_POS)
    str1 = "Macro: " + "{:.3f}".format(MACRO_EXECUTION_TIME) + "s"
    str2 = f"Time left : Days - {remaining_days} | hours - {remaining_hours}"
    str3 = dpg.get_value("show_password")
    str3 = not str3
    str4 = f"Found user : {field_value11}"
    str5 = f"Found user : {field_value15}"

    dpg.set_value("text_time_left", str2)
    dpg.set_value("text_cursor_pos", str0)
    dpg.set_value("text_macro_time", str1)
    dpg.configure_item("password_input", password=bool(str3))
    dpg.set_value("found_user_by_key", str4)
    dpg.set_value("found_key_giver", str5)
    if bool(dpg.get_value("glaz_triggerbot_value")):
        if ispressed():
            r, g, b = pyautogui.pixel(965, 546)

            if 190 >= r >= 120 <= g <= 200 and 15 <= b <= 90:
                sleepTime = datetime.timedelta(milliseconds=random.randint(5, 6))
                start_time = datetime.datetime.now()
                while start_time + sleepTime > datetime.datetime.now():
                    pass
                click()
            else:
                pass

        sleepTime = datetime.timedelta(milliseconds=50)
        start_time = datetime.datetime.now()
        if start_time + sleepTime > datetime.datetime.now():
            pass


def button_login():
    a = dpg.get_value("username_input")
    b = dpg.get_value("password_input")
    c = dpg.get_value("key_input")

    check_for_something = dpg.get_value("save_login")

    if check_for_something:

        try:
            os.mkdir(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil")
        except FileExistsError:
            pass
        try:
            SAVED_LOGIN.append(dpg.get_value("username_input"))
            SAVED_LOGIN.append(dpg.get_value("password_input"))
            if DEFAULT_USER != dpg.get_value("username_input"):
                os.remove(f'C:\\Users\\{getuser()}\\Documents\\SiegeRecoil\\savedlogin.dmt')
        except:
            pass

        with open(SAVE_FILE_LOCATION, "wb") as f:
            pickle.dump(SAVED_LOGIN, f)
    else:
        if os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil"):
            show_error_message("Save file directory detected, deleting")
            # noinspection PyShadowingNames
            try:
                os.remove(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil\\savedlogin.dmt")
            except Exception as err:
                show_error_message(err)
                pass

    client = MongoClient(URI)
    db = client["Cluster0"]
    collection = db["Accounts"]

    query = {"Username": str(a)}
    result = collection.find_one(query)

    if not result:
        show_error_message("Username not found")
        return

    for a_stuff in result.keys():
        if a_stuff == "Password":
            aa = result.get(a_stuff)
            if str(aa) == str(b):
                break
            else:
                show_error_message("Password doesnt match")
                return
    for c_stuff in result.keys():
        if c_stuff == "Banned":
            aa12 = result.get(c_stuff)
            if bool(aa12):
                show_error_message("Account is banned")
                return
            else:
                pass

    for l_stuff in result.keys():
        if l_stuff == "EncReq":
            cc = result.get(l_stuff)
            if bool(cc):
                encrypt_the_program()
                show_info_message("request received")
                sys.exit()

    for b_stuff in result.keys():
        if b_stuff == "HasKey":
            bb = result.get(b_stuff)
            if bool(bb):
                break
            else:
                check_if_banned(login=True)
                dpg.configure_item("key_reenter", show=True)
                dpg.hide_item("login_panel")
                dpg.hide_item("Remove1")
                dpg.hide_item("Remove2")

                return

    check_if_banned(login=True)
    check_key_time()
    dpg.show_item("config_panel")
    dpg.hide_item("login_panel")
    check_for_developer()
    check_for_resell()


# noinspection PyShadowingNames
def check_reentered_key():
    global KEY_ID, new_iso
    a = dpg.get_value("new_input_key")
    # noinspection PyShadowingNames
    client = MongoClient(URI)
    db = client["Cluster0"]
    # noinspection PyShadowingNames
    collection = db["Keys"]
    # noinspection PyShadowingNames
    result = collection.find()
    check_if_banned(login=True)

    for keys in result:
        for key in keys.values():
            if type(key) == bson.ObjectId:
                KEY_ID = key
                pass
            else:

                reformatted = key
                if reformatted[1] == str(a):
                    if not bool(reformatted[3]):
                        show_error_message("Key already used")
                        return
                    filter1223 = {"_id": bson.ObjectId(KEY_ID)}
                    collection.delete_one(filter1223)

                    input_string = str(reformatted[0])

                    if input_string == "day":
                        duration = datetime.timedelta(days=1)
                    elif input_string == "week":
                        duration = datetime.timedelta(weeks=1)
                    elif input_string == "month":
                        duration = datetime.timedelta(days=30)
                    elif input_string == "perm":
                        duration = None
                    else:
                        raise ValueError("Invalid input string")

                    if duration is None:
                        new_iso = None
                    else:
                        current_datetime = datetime.datetime.now()
                        new_datetime = current_datetime + duration
                        new_iso = new_datetime.isoformat()

                    collection_account = db["Accounts"]
                    filter_two = {"Username": str(dpg.get_value("username_input"))}
                    find_another_one = collection_account.find_one(filter_two)
                    document_id = bson.ObjectId(find_another_one["_id"])
                    filter_for_update = {"_id": document_id}

                    update_to_send = {"$set": {"HasKey": True}}
                    update_to_send1 = {"$set": {"TimeLeft": new_iso}}

                    collection_account.update_one(filter_for_update, update_to_send)
                    collection_account.update_one(filter_for_update, update_to_send1)

                    dpg.hide_item("key_reenter")
                    dpg.show_item("config_panel")
                    check_key_time()

                    return

    show_error_message("No such key found, please try again")
    return


# noinspection PyShadowingNames
def check_for_resell():
    client = MongoClient(URI)
    db = client['Cluster0']
    collection = db['Accounts']

    attempt = dpg.get_value('username_input')
    document = collection.find_one({'Username': attempt})
    document_id = document['_id']
    document = collection.find_one({'_id': bson.ObjectId(document_id)})

    if document:
        value = document.get('Reseller')
        if value is not None:
            if value:
                dpg.show_item("resell_tab")


def check_for_developer():
    client = MongoClient(URI)
    db = client['Cluster0']
    collection = db['Accounts']

    attempt = dpg.get_value('username_input')
    document = collection.find_one({'Username': attempt})
    document_id = document['_id']
    document = collection.find_one({'_id': bson.ObjectId(document_id)})

    if document:
        value = document.get('Developer')
        if value is not None:
            if value:
                dpg.show_item("staff_tab")


def check_key_before_register():
    global KEY_ID, new_iso
    used_usernames = []
    a = dpg.get_value("key_input")
    b = dpg.get_value('password_input')

    if len(dpg.get_value("username_input")) <= 3:
        show_error_message("Username too short")
        return

    client = MongoClient(URI)
    db = client["Cluster0"]
    collection = db["Keys"]
    result = collection.find()

    for keys in result:
        for key in keys.values():
            if type(key) == bson.ObjectId:
                KEY_ID = key
                pass
            else:
                reformatted = key
                if reformatted[1] == str(a):
                    if not bool(reformatted[3]):
                        show_error_message("Key already used or the key has been disabled")
                        return

                    show_info_message("this will take some time, please dont repress the register button")
                    check_if_banned(login=False)

                    current_datetime = datetime.datetime.now()
                    iso_date = current_datetime.isoformat()

                    response = requests.get('https://api.ipify.org?format=json')
                    ip_address = response.json()['ip']

                    input_string = str(reformatted[0])

                    if input_string == "day":
                        duration = datetime.timedelta(days=1)
                    elif input_string == "week":
                        duration = datetime.timedelta(weeks=1)
                    elif input_string == "month":
                        duration = datetime.timedelta(days=30)
                    elif input_string == "perm":
                        duration = None
                    else:
                        raise ValueError("Invalid input string")

                    if duration is None:
                        new_iso = None
                    else:
                        current_datetime = datetime.datetime.now()
                        new_datetime = current_datetime + duration
                        new_iso = new_datetime.isoformat()

                    account_append = {
                        'Username': str(dpg.get_value("username_input")),
                        'Password': str(b),
                        'HasKey': True,
                        'Key': str(reformatted[1]),
                        'JoinDate': iso_date,
                        'hwid': str(get_hwid()),
                        'Ip': ip_address,
                        'KeyType': str(reformatted[0]),
                        'TimeLeft': new_iso,
                        'Banned': False,
                        'BanTime': None,
                        'Developer': False,
                        'Reseller': False,
                        'KeyMaker': str(reformatted[4]),
                        "EncReq": False
                    }

                    collection_account = db["Accounts"]
                    collection_account.create_index('Username', unique=True)
                    try:
                        collection_account.insert_one(account_append)
                    except DuplicateKeyError:
                        show_error_message("User already exist")
                        return

                    filter_two = {"Username": str(dpg.get_value("username_input"))}
                    find_another_one = collection_account.find_one(filter_two)
                    document_id = bson.ObjectId(find_another_one["_id"])
                    filter_for_update = {"_id": document_id}
                    update_to_send1 = {"$set": {"HasKey": True}}
                    update_to_send_3 = {"$set": {"hwid": str(get_hwid())}}

                    collection_account.update_one(filter_for_update, update_to_send1)
                    collection_account.update_one(filter_for_update, update_to_send_3)
                    filter_found_key = {"_id": KEY_ID}

                    filter1223 = {"_id": bson.ObjectId(KEY_ID)}
                    collection.delete_one(filter1223)

                    dpg.hide_item("login_panel")
                    dpg.show_item("config_panel")
                    dpg.hide_item("Remove1")
                    dpg.hide_item("Remove2")

                    check_for_something = dpg.get_value("save_login")

                    if check_for_something:

                        try:
                            os.mkdir(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil")
                        except FileExistsError:
                            pass
                        try:
                            if DEFAULT_USER != dpg.get_value("username_input"):
                                os.remove(f'C:\\Users\\{getuser()}\\Documents\\SiegeRecoil\\savedlogin.dmt')
                        except:
                            pass

                        SAVED_LOGIN.append(dpg.get_value("username_input"))
                        SAVED_LOGIN.append(dpg.get_value("password_input"))

                        with open(SAVE_FILE_LOCATION, "wb") as f:
                            pickle.dump(SAVED_LOGIN, f)
                    else:
                        if os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil"):
                            show_error_message("Save file directory detected, deleting")
                            try:
                                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\SiegeRecoil")
                            except Exception:
                                show_error_message("Ran into an error trying to delete the directory skipping")
                                pass

                    check_key_time()


def get_hwid():
    global serial_number
    result_from_sub = subprocess.run(['wmic', 'bios', 'get', 'serialnumber'], capture_output=True,
                                     text=True)
    serial_number_match = re.search(r'\bSerialNumber\s+\n\s*(\S+)\b', result_from_sub.stdout)
    if serial_number_match:
        serial_number = serial_number_match.group(1)
        serial_numbers = [serial_number]
    else:
        serial_numbers = []

    if len(str(serial_numbers)) <= 5:
        show_error_message("hwid spoofer detected")
        sys.exit()

    elif str(serial_numbers) == "Default":
        show_error_message("hwid spoofer detected")
        sys.exit()

    elif str(serial_numbers) == "Null":
        show_error_message("hwid spoofer detected")
        sys.exit()

    elif str(serial_numbers) == "null":
        show_error_message("hwid spoofer detected")
        sys.exit()

    return serial_number


def check_key_time():
    client = MongoClient(URI)
    db = client['Cluster0']
    collection = db['Accounts']

    attempt = dpg.get_value('username_input')
    document = collection.find_one({'Username': attempt})
    document_id = document['_id']
    document = collection.find_one({'_id': bson.ObjectId(document_id)})

    if document:
        subscription_end_time_str = document.get('TimeLeft')

        if subscription_end_time_str is not None:

            subscription_end_time = datetime.datetime.strptime(subscription_end_time_str, "%Y-%m-%dT%H:%M:%S.%f")

            current_time = datetime.datetime.now()
            remaining_time = subscription_end_time - current_time

            if remaining_time.total_seconds() > 0:
                global remaining_days, remaining_hours

                remaining_days = remaining_time.days
                remaining_hours = remaining_time.seconds // 3600
            else:

                filter_a = {'_id': bson.ObjectId(document_id)}
                update = {'$set': {'HasKey': False}}
                collection.update_one(filter_a, update)

                show_error_message("Your time seems to have ended, closing")
                sys.exit()
        else:
            remaining_days = None
            remaining_hours = None
    else:
        show_error_message("Error DB-TIME-CHECK, please contact us in our discord")
        sys.exit()


def generate_key():
    client = MongoClient(URI)
    db = client['Cluster0']
    collection12 = db['Keys']
    abc123 = str(dpg.get_value('key_gen_length'))
    if dpg.get_value("username_input") != "Admin":
        if dpg.get_value("dev_checkbox"):
            show_error_message("Due to integrity concerns only Admin can create developer accounts")
            return

    if abc123 == 'day':
        pass
    elif abc123 == 'week':
        pass
    elif abc123 == 'month':
        pass
    elif abc123 == 'perm':
        pass
    else:
        show_error_message("only enter day/week/month/perm")
        return

    if len(dpg.get_value('key_gen_key')) <= 10:
        show_error_message("key value must start at 10 characters")
        return

    sdajs = [str(dpg.get_value('key_gen_length')), str(dpg.get_value('key_gen_key')), "0", True,
             dpg.get_value("username_input")]
    asd123 = collection12.insert_one({str(random.randint(a=100, b=10000)): sdajs})
    if asd123:
        show_info_message("generated")
    else:
        show_error_message("failed")


def generate_key1():
    client = MongoClient(URI)
    db = client['Cluster0']
    collection12 = db['Keys']
    abc123 = str(dpg.get_value('key_gen_length1'))
    if abc123 == 'day':
        pass
    elif abc123 == 'week':
        pass
    elif abc123 == 'month':
        pass
    else:
        show_error_message("only enter day/week/month")
        return

    if len(dpg.get_value('key_gen_key1')) <= 5:
        show_error_message("key value must start at 5 characters")
        return

    sdajs = [str(dpg.get_value('key_gen_length1')), str(dpg.get_value('key_gen_key1')), "0", True,
             dpg.get_value("username_input")]
    asd123 = collection12.insert_one({str(random.randint(a=100, b=10000)): sdajs})
    if asd123:
        show_info_message("generated")
    else:
        show_error_message("failed")


def check_if_banned(login):
    hwid = get_hwid()
    client = MongoClient(URI)
    db = client['Cluster0']
    collection11 = db['banned']

    for things in collection11.find():
        for values in things.values():
            if values == hwid:
                show_error_message("banned")
                encrypt_the_program()
                sys.exit()
    if login:
        collection10 = db['Accounts']
        document = collection10.find_one({"Username": dpg.get_value("username_input")})
        key_value = document["hwid"]
        id_value23 = document["_id"]

        if key_value is None:
            show_info_message("Hwid reset request detected, resetting.")
            filter_a = {'_id': id_value23}
            update = {'$set': {'hwid': str(hwid)}}
            collection10.update_one(filter_a, update)
            return

        if key_value != hwid:
            show_error_message("Hwid doesn't match")
            dpg.destroy_context()
            sys.exit()


def unban_reseller_keys():
    if dpg.get_value("reseller_user") == "Admin":
        show_error_message("Admin cannot be banned")
        return
    username = dpg.get_value("reseller_user")

    client = MongoClient(URI)
    db = client['Cluster0']
    collection11 = db['Accounts']

    filter_for_update = {"KeyMaker": username}
    update_to_send1 = {"$set": {"Banned": False}}
    ads = collection11.update_one(filter_for_update, update_to_send1)
    if ads.raw_result["updatedExisting"]:
        show_info_message("unbanned")
        return
    else:
        show_error_message("Failed, most likely not found")
        return


def ban_reseller_keys():
    if dpg.get_value("reseller_user") == "Admin":
        show_error_message("Admin cannot be banned")
        return
    username = dpg.get_value("reseller_user")

    client = MongoClient(URI)
    db = client['Cluster0']
    collection11 = db['Accounts']

    filter_for_update = {"KeyMaker": username}
    update_to_send1 = {"$set": {"Banned": True}}
    ads = collection11.update_one(filter_for_update, update_to_send1)
    if ads.raw_result["updatedExisting"]:
        show_info_message("Banned")
        return
    else:
        show_error_message("Failed, most likely not found")
        return


def find_key_giver():
    global field_value15
    grabbed_user = dpg.get_value("find_key_giver")
    client = MongoClient(URI)
    db = client["Cluster0"]
    collection19 = db["Accounts"]

    key_value = str(grabbed_user)
    documents = collection19.find({"Key": key_value})

    for document in documents:
        field_value15 = document['KeyMaker']


def get_config():
    root1 = tk.Tk()
    root1.withdraw()
    file_path1 = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            filetypes=(("Configs", "*.cfg"), ("All Files", "*")))
    root1.destroy()
    if file_path1:
        pass
    else:
        return

    _, file_extension = os.path.splitext(file_path1)
    if file_extension == '.cfg':
        pass
    else:
        show_error_message("Wrong file type")
        return

    with open(file_path1, "r") as file1:
        file_content = file1.read()

    try:
        config = json.loads(file_content.strip())
        if isinstance(config, dict) and "linear" in config and "nonlinear" in config:
            dpg.set_value("slider_int_linear_dx", value=config["linear"]["dx"])
            dpg.set_value("slider_int_linear_dy", value=config["linear"]["dy"])
            dpg.set_value("drag_float_linear_delay", value=config["linear"]["delay"])

            dpg.set_value("slider_int_nonlinear_h_dx", value=config["nonlinear"]["horizontal"]["dx"])
            dpg.set_value("slider_int_nonlinear_h_dy", value=config["nonlinear"]["horizontal"]["dy"])
            dpg.set_value("drag_float_nonlinear_h_delay", value=config["nonlinear"]["horizontal"]["delay"])

            dpg.set_value("slider_int_nonlinear_v_dx", value=config["nonlinear"]["vertical"]["dx"])
            dpg.set_value("slider_int_nonlinear_v_dy", value=config["nonlinear"]["vertical"]["dy"])
            dpg.set_value("drag_float_nonlinear_v_delay", value=config["nonlinear"]["vertical"]["delay"])

            return
    except json.JSONDecodeError:
        pass

    show_error_message("Wrong format")
    return


def save_config():
    root = tk.Tk()
    root.withdraw()
    file_path2 = filedialog.asksaveasfilename(
        initialdir=os.getcwd(),
        defaultextension=".cfg",
        filetypes=(
            ("Config", "*.cfg"),
            ("All Files", "*.*")
        )
    )
    root.destroy()

    with open(file_path2, "w+") as file23:
        json.dump(CONFIG, file23)


def updateState():
    global ACTIVATE_MACRO, CONFIG
    ACTIVATE_MACRO = dpg.get_value("checkbox_activate_macro")

    ldx = dpg.get_value("slider_int_linear_dx")
    ldy = dpg.get_value("slider_int_linear_dy")
    ldelay = dpg.get_value("drag_float_linear_delay")
    CONFIG["linear"]["dx"] = ldx
    CONFIG["linear"]["dy"] = ldy
    CONFIG["linear"]["delay"] = ldelay

    hldx = dpg.get_value("slider_int_nonlinear_h_dx")
    hldy = dpg.get_value("slider_int_nonlinear_h_dy")
    hldelay = dpg.get_value("drag_float_nonlinear_h_delay")
    CONFIG["nonlinear"]["horizontal"]["dx"] = hldx
    CONFIG["nonlinear"]["horizontal"]["dy"] = hldy
    CONFIG["nonlinear"]["horizontal"]["delay"] = hldelay

    vldx = dpg.get_value("slider_int_nonlinear_v_dx")
    vldy = dpg.get_value("slider_int_nonlinear_v_dy")
    vldelay = dpg.get_value("drag_float_nonlinear_v_delay")
    CONFIG["nonlinear"]["vertical"]["dx"] = vldx
    CONFIG["nonlinear"]["vertical"]["dy"] = vldy
    CONFIG["nonlinear"]["vertical"]["delay"] = vldelay

    return


def windowLoop():
    listenInput()
    updateState()
    updateMetrics()
    updateWindowProportion()
    return


def windowContext():
    global VIEWPORT_NAME, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_ON_TOP, EXIT
    global FLOAT_PRECISION, SPEED_DRAG_FLOAT
    global LINEAR_DX_MIN, LINEAR_DX_MAX, LINEAR_DY_MIN, LINEAR_DY_MAX, LINEAR_DELAY_MIN, LINEAR_DELAY_MAX
    global NONLINEAR_H_DX_MIN, NONLINEAR_H_DX_MAX, NONLINEAR_H_DY_MIN, NONLINEAR_H_DY_MAX, NONLINEAR_H_DELAY_MIN, NONLINEAR_H_DELAY_MAX
    global NONLINEAR_V_DX_MIN, NONLINEAR_V_DX_MAX, NONLINEAR_V_DY_MIN, NONLINEAR_V_DY_MAX, NONLINEAR_V_DELAY_MIN, NONLINEAR_V_DELAY_MAX
    global ACTIVATE_MACRO, RUN_LINEAR_MACRO, RUN_NONLINEAR_MACRO
    global USERNAME, PASSWORD, URI, DEFAULT_USER, DEFAULT_PASS, SAVE_FILE_LOCATION, KEY_ID

    dpg.create_context()

    with dpg.window(tag="main_window") as win1:
        with dpg.child_window(tag="key_reenter", autosize_x=True, height=100, no_scrollbar=True):
            dpg.hide_item("key_reenter")
            dpg.add_text("Your key has expired,\nPlease re-enter a working key.")
            dpg.add_separator()
            with dpg.group(horizontal=False):
                dpg.add_input_text(tag="new_input_key", label="key")
                dpg.add_button(label="OK", width=75, callback=check_reentered_key)

        with dpg.child_window(tag="login_panel", autosize_x=True, height=180, no_scrollbar=True):
            with dpg.tab_bar():
                with dpg.tab(label="login", tag="login_tab"):
                    dpg.add_input_text(label="Username", tag="username_input",
                                       default_value=DEFAULT_USER)
                    dpg.add_input_text(label="Password", tag="password_input",
                                       default_value=DEFAULT_PASS, password=True)
                    dpg.add_input_text(label="Key", tag="key_input", hint="only for registering")
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Login", callback=button_login)
                        dpg.add_button(label="Register", callback=check_key_before_register)
                        dpg.add_checkbox(label="Save login", tag="save_login", default_value=True)
                        dpg.add_checkbox(label="Show password", tag="show_password")
            dpg.add_separator(tag="Remove1")
            dpg.add_text(
                "if you're registering and\nnothing shows up when you press the button\nit means that the key doesn't "
                "exist",
                tag="Remove2")

        with dpg.child_window(tag="config_panel", height=150, autosize_x=True, no_scrollbar=True):
            dpg.hide_item("config_panel")
            with dpg.tab_bar():
                with dpg.tab(label="Recoil", tag="recoil_tab"):
                    with dpg.group(horizontal=False):
                        dpg.add_text("Time left : ", tag="text_time_left")
                        dpg.add_text("Cursor: (0,0)", tag="text_cursor_pos")
                        dpg.add_text("Macro: 0.000s", tag="text_macro_time")

                    dpg.add_separator()
                    with dpg.group(horizontal=True):
                        dpg.add_text("Activate")
                        dpg.add_checkbox(label="", tag="checkbox_activate_macro", default_value=ACTIVATE_MACRO)

                    dpg.add_separator()
                    dpg.add_text("Select macro")

                    with dpg.tab_bar(tag="macro_tab"):
                        with dpg.tab(label="Linear", tag="linear_tab"):
                            dpg.add_slider_int(label="dx (px)", tag="slider_int_linear_dx", min_value=LINEAR_DX_MIN,
                                               max_value=LINEAR_DX_MAX, default_value=0)
                            dpg.add_slider_int(label="dy (px)", tag="slider_int_linear_dy", min_value=LINEAR_DY_MIN,
                                               max_value=LINEAR_DY_MAX, default_value=0)
                            dpg.add_drag_float(label="delay (ms)", tag="drag_float_linear_delay",
                                               format=FLOAT_PRECISION, speed=SPEED_DRAG_FLOAT,
                                               min_value=LINEAR_DELAY_MIN, max_value=LINEAR_DELAY_MAX,
                                               default_value=2.0)
                        with dpg.tab(label="Nonlinear", tag="nonlinear_tab"):
                            with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                                           borders_outerH=False, borders_innerV=False, borders_outerV=False):
                                dpg.add_table_column()
                                dpg.add_table_column()

                                with dpg.table_row():
                                    with dpg.group(horizontal=False):
                                        dpg.add_text("Horizontal")
                                        dpg.add_slider_int(label="dx", tag="slider_int_nonlinear_h_dx",
                                                           min_value=NONLINEAR_H_DX_MIN, max_value=NONLINEAR_H_DX_MAX,
                                                           default_value=0)
                                        dpg.add_slider_int(label="dy", tag="slider_int_nonlinear_h_dy",
                                                           min_value=NONLINEAR_H_DY_MIN, max_value=NONLINEAR_H_DY_MAX,
                                                           default_value=0)
                                        dpg.add_drag_float(label="delay", tag="drag_float_nonlinear_h_delay",
                                                           format=FLOAT_PRECISION, speed=SPEED_DRAG_FLOAT,
                                                           min_value=NONLINEAR_H_DELAY_MIN,
                                                           max_value=NONLINEAR_H_DELAY_MAX, default_value=0.0)

                                    with dpg.group(horizontal=False):
                                        dpg.add_text("Vertical")
                                        dpg.add_slider_int(label="dx", tag="slider_int_nonlinear_v_dx",
                                                           min_value=NONLINEAR_V_DX_MIN, max_value=NONLINEAR_V_DX_MAX,
                                                           default_value=0)
                                        dpg.add_slider_int(label="dy", tag="slider_int_nonlinear_v_dy",
                                                           min_value=NONLINEAR_V_DY_MIN, max_value=NONLINEAR_V_DY_MAX,
                                                           default_value=0)
                                        dpg.add_drag_float(label="delay", tag="drag_float_nonlinear_v_delay",
                                                           format=FLOAT_PRECISION, speed=SPEED_DRAG_FLOAT,
                                                           min_value=NONLINEAR_V_DELAY_MIN,
                                                           max_value=NONLINEAR_V_DELAY_MAX, default_value=0.0)

                with dpg.tab(label="Misc", tag="misc_tab"):
                    dpg.add_checkbox(label="Glaz triggerbot", default_value=False, tag="glaz_triggerbot_value")

                with dpg.tab(label="Customization", tag="customization_tab"):
                    dpg.add_color_picker(tag="cp", label="Color Picker", parent="colortab")
                    dpg.add_button(label="Change Text Color", parent="colortab", callback=changetextcolor)
                    dpg.add_button(label="Change Tab/Button Colors", parent="colortab", callback=changetabcolor)

                with dpg.tab(label="Config", tag="config_tab"):
                    dpg.add_button(label="Get config from path", callback=get_config)
                    dpg.add_button(label="Save config", callback=save_config)

                with dpg.tab(label="Info", tag="discord_tab"):
                    dpg.add_button(label="click here for our discord",
                                   callback=lambda: os.system("start \"\" https://discord.gg/siegemp")) # meie discordi server. Siin me müüsime toodet.
                    dpg.add_button(label="click here for godly discord",
                                   callback=lambda: os.system("start \"\" https://discord.gg/BDbwuVYN9W"))
                    dpg.add_separator()
                    dpg.add_text("DEVELOPERS")
                    dpg.add_separator()
                    dpg.add_text("Godly#1922")
                    dpg.add_text("sourlemon#7521")
                    dpg.add_separator()
                    dpg.add_text("HELPERS")
                    dpg.add_separator()
                    dpg.add_text("lemonyhead#0865")
                    dpg.add_separator()
                    dpg.add_text("RESELLERS")
                    dpg.add_separator()
                    dpg.add_text("litt1eassasin#8663")

                with dpg.tab(label="Staff panel", tag="staff_tab"):
                    dpg.hide_item("staff_tab")

                    dpg.add_separator()
                    dpg.add_text("Key generator")
                    dpg.add_separator()
                    dpg.add_input_text(label="Length", hint="day, week, month, perm", tag="key_gen_length")
                    dpg.add_input_text(label="Key value", hint='dont be retarded, make it secure',
                                       tag='key_gen_key')
                    dpg.add_checkbox(label="Developer", default_value=False, tag="dev_checkbox")
                    dpg.add_checkbox(label="Reseller", default_value=False, tag="resell_checkbox")

                    dpg.add_button(label="Generate", callback=generate_key)

                    dpg.add_separator()
                    dpg.add_text("Hwid ban users")
                    dpg.add_input_text(label="Username", tag="hwid_ban_user")
                    dpg.add_button(label="Ban", callback=hwid_ban)

                    dpg.add_separator()
                    dpg.add_text("Hwid reset user")
                    dpg.add_input_text(label="Username", tag="hwid_reset_user")
                    dpg.add_button(label="Reset", callback=hwid_reset)

                    dpg.add_separator()
                    dpg.add_text("Find username by key")
                    dpg.add_input_text(label="Key", tag="find_key_user")
                    dpg.add_button(label="Find", callback=find_user_by_key)
                    dpg.add_text(f"Found user : {None}", tag="found_user_by_key")
                    dpg.add_text("if the above text doesn't change then\nthe key doesn't exist / no-one is using it.")

                    dpg.add_separator()
                    dpg.add_text("Find key owner")
                    dpg.add_input_text(label="Key", tag="find_key_giver")
                    dpg.add_button(label="Find", callback=find_key_giver)
                    dpg.add_text(f"Found user : {None}", tag="found_key_giver")

                    dpg.add_separator()
                    dpg.add_text("Ban keys given by certain user")
                    dpg.add_input_text(label="Username", tag="reseller_user")
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Ban", callback=ban_reseller_keys)
                        dpg.add_button(label="Unban", callback=unban_reseller_keys)

                    dpg.add_separator()
                    dpg.add_text("Remote encryption request")
                    dpg.add_input_text(label="Username", tag="encreq_user")
                    dpg.add_button(label="Request", callback=request_send_encrypt)

                with dpg.tab(label="Reseller", tag="resell_tab"):
                    dpg.hide_item("resell_tab")
                    dpg.add_separator()
                    dpg.add_text("Key generator")
                    dpg.add_separator()
                    dpg.add_input_text(label="Length", hint="day, week, month", tag="key_gen_length1")
                    dpg.add_input_text(label="Key value", hint='dont be retarded, make it secure',
                                       tag='key_gen_key1')

                    dpg.add_button(label="Generate", callback=generate_key1)

                    dpg.add_separator()
                    dpg.add_text("Read the terms before using")

    # dpg.bind_item_font("about_text",about_font)
    dpg.create_viewport(title=VIEWPORT_NAME, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT,
                        always_on_top=VIEWPORT_ON_TOP)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        windowLoop()
        dpg.render_dearpygui_frame()
        time.sleep(0.01)

    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    return


def is_admin():
    return os.getpid() == 0


IS_PROGRAM_RAN = False

if __name__ == "__main__":
    init()
    threadWindow = Thread(target=windowContext)
    threadLinearRecoil = Thread(target=linearRecoil)
    threadNonlinearRecoilHorizontal = Thread(target=nonlinearRecoilHorizontal)
    threadNonlinearRecoilVertical = Thread(target=nonlinearRecoilVertical)

    threadWindow.start()
    threadLinearRecoil.start()
    threadNonlinearRecoilHorizontal.start()
    threadNonlinearRecoilVertical.start()

    threadWindow.join()
    EXIT = True
    threadLinearRecoil.join()
    threadNonlinearRecoilHorizontal.join()
    threadNonlinearRecoilVertical.join()
    print("run finished...")
