import datetime
from dataclasses import dataclass
from openpyxl import load_workbook

@dataclass
class League:
    name: str
    participants: list[str]

def extract_leagues(filepath: str) -> list[League]:
    workbook = load_workbook(filename=filepath, data_only=True)
    # print(workbook.sheetnames)
    leagues_sheet = workbook["Leagues"]
    leagues_: list[League] = []
    for row in leagues_sheet.iter_cols(values_only=True):
        if any(map(lambda x: x is not None, row)):
            for idx, item in enumerate(row):
                if item is None:
                    continue

                leagues_.append(League(item, [x for x in row[idx+1:] if x is not None]))
                break

    return leagues_

if __name__ == "__main__":
    leagues = extract_leagues("./excel_test.xlsx")

    for league in leagues:
        print(f"{league.name}:\n\t {league.participants}")
