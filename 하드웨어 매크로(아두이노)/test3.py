import os


with open(f'./macros/2023.1.7.15.32.33.txt', 'r+') as f:
    f.seek(0, os.SEEK_END)
    pos = f.tell() - 1
    while pos > 0 and f.read(1) != "\n":
        pos -= 1
        f.seek(pos, os.SEEK_SET)

    if pos > 0:
        f.seek(pos, os.SEEK_SET)
        f.truncate()
