import sys
import pandas as pd
from datetime import datetime 

print(sys.argv)

file_name = sys.argv[0]  # Name of the file

try:
    day = sys.argv[1]  # Whatever we pass via CLI
except IndexError:
    day = datetime.today().strftime('%Y-%m-%d')

# Fancy stuff with pandas

print(f'Job finished successfully on {day}, from file {file_name}')
