from pynput.keyboard import Key, Listener
from ctypes import *
import time
import os

# thisdirpath = os.path.dirname(os.path.realpath(__file__))
# classdd = windll.LoadLibrary(f"{thisdirpath}/DDHID64.dll")
# time.sleep(2)
# st = classdd.DD_btn(0)  # DD Initialize

# if st == 1:
#     print("OK")
# else:
#     print("Error")
#     exit(101)

keydict = {
    "Key.esc": 100,
    "Key.f1": 101,
    "Key.f2": 102,
    "Key.f3": 103,
    "Key.f4": 104,
    "Key.f5": 105,
    "Key.f6": 106,
    "Key.f7": 107,
    "Key.f8": 108,
    "Key.f9": 109,
    "Key.f10": 110,
    "Key.f11": 111,
    "Key.f12": 112,
    "Key.print_screen": 700,
    "Key.scroll_lock": 701,
    "Key.pause": 702,
    "'`'": 200,
    "'1'": 201,
    "'2'": 202,
    "'3'": 203,
    "'4'": 204,
    "'5'": 205,
    "'6'": 206,
    "'7'": 207,
    "'8'": 208,
    "'9'": 209,
    "'0'": 210,
    "'-'": 211,
    "'='": 212,
    "Key.backspace": 214,
    "Key.tab": 300,
    "'q'": 301,
    "'w'": 302,
    "'e'": 303,
    "'r'": 304,
    "'t'": 305,
    "'y'": 306,
    "'u'": 307,
    "'i'": 308,
    "'o'": 309,
    "'p'": 310,
    "'['": 311,
    "']'": 312,
    "'\\'": 213,
    "Key.caps_lock": 400,
    "'a'": 401,
    "'s'": 402,
    "'d'": 403,
    "'f'": 404,
    "'g'": 405,
    "'h'": 406,
    "'j'": 407,
    "'k'": 408,
    "'l'": 409,
    "';'": 410,
    "\"'\"": 411,
    "Key.enter": 313,
    "Key.shift": 500,
    "'z'": 501,
    "'x'": 502,
    "'c'": 503,
    "'v'": 504,
    "'b'": 505,
    "'n'": 506,
    "'m'": 507,
    "','": 508,
    "'.'": 509,
    "'/'": 510,
    "Key.shift_r": 511,
    "Key.ctrl_l": 600,
    "Key.cmd": 601,
    "Key.alt_l": 602,
    "Key.space": 603,
    "Key.left": 710,
    "Key.up": 709,
    "Key.down": 711,
    "Key.right": 712,
    "Key.insert": 703,
    "Key.home": 704,
    "Key.page_up": 705,
    "Key.delete": 706,
    "Key.end": 707,
    "Key.page_down": 708,
    "Key.num_lock": 810,
    "'/'": 811,
    "'*'": 812,
    "'-'": 813,
    "'+'": 814,
    "<96>": 800,
    "<97>": 801,
    "<98>": 802,
    "<99>": 803,
    "<100>": 804,
    "<101>": 805,
    "<102>": 806,
    "<103>": 807,
    "<104>": 808,
    "<105>": 809,
    "<110>": 816,
    "<21>":  604
}


def keyConvert(key):
    if key == "'\\x01'":
        return
    return keydict[key]

# print(keyConvert("'d'"))

# f = open(f'{thisdirpath}/macros/2022.12.21.11.36.48.txt','r')

# line = 0
# while line != '':
#     line = f.readline()
#     if line == '':
#         break

#     if line[0] == 'p':
#         tmp = keyConvert(line[1:-1])
#         print(tmp)
#         classdd.DD_key(tmp,1)
#     if line[0] == 'r':
#         tmp = keyConvert(line[1:-1])
#         print(tmp)
#         classdd.DD_key(tmp,2)
#     if line[0] == 'w':
#         time.sleep(float(line[1:-1]))

