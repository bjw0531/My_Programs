from ctypes import *
import time

print("Load DD!")

dd_dll = windll.LoadLibrary('./DDHID64.dll')

st = dd_dll.DD_btn(0)  # DD Initialize
if st == 1:
    print("OK")
else:
    print("Error")
    exit(101)
