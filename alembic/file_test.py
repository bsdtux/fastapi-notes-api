import os
import sys

current_path = os.path.dirname(__file__)
root_path = os.path.join(current_path, "../api/models")
sys.path.append(root_path)
print(sys.path)