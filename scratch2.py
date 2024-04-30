import os

filename = 'map2.txt'

if os.access(filename, os.R_OK):
    print(f"Read access to '{filename}' is granted.")
else:
    print(f"Read access to '{filename}' is denied.")