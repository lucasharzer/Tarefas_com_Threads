import pandas as pd


class Spreadsheet:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = pd.read_excel(filename)

    def get_data(self):
        return self.data

    def save(self, data, filename: str):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)