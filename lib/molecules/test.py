import os
import sys


print(os.environ['PATH'])
print(sys.path)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
print(sys.path)

from PyChem import molecules

current_directory = os.path.dirname(__file__)
parent_dir = os.path.split(current_directory)[0]
DATA_FILE = parent_dir + 'files/elements.json'

print(DATA_FILE)
