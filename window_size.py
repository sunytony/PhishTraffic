import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Input vector = N x 2

window_size = 20

files = [f for f in pathlib.Path().glob("html/*")]

for file in files:
    

train = pd.read_csv(f"C:\Users\sunyt\OneDrive\바탕 화면\NetLab\phish\phish_win{window_size}.csv")
