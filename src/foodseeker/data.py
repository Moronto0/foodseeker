import pandas as pd

# Загрузка данных из CSV файла
file_path = r"..\..\Foods_Data.csv"
df = pd.read_csv(file_path, delimiter=";")
