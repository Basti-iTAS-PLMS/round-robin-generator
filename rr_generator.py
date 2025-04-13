import sys
import numpy as np

from excel_reader import extract_leagues

def round_robin(num_participants: int) -> list[list[tuple[int, int]]]:
    odd_participants = False
    if num_participants % 2 == 1:
        odd_participants = True
        num_participants += 1
    matches = int(num_participants / 2)

    pairings: list[list[tuple[int, int]]] = []
    A = np.array([x for x in range(matches)])
    B = np.array([x for x in range(2*matches-1, matches-1, -1)])
    B0 = num_participants - 1
    for round_ in range(num_participants - 1):
        pairings.append([])
        for match in range(matches):
            # skip first match, as match against highest indexed participant is skipped in this case
            if match == 0:
                if odd_participants:
                    continue

                if round_ % 2 == 1:
                    pairings[round_].append((B[match], A[match]))
                    continue
            pairings[round_].append((A[match], B[match]))

        B = B + matches + 1
        B[B > num_participants - 1] -= num_participants - 1
        B -= 1
        B[0] = B0
        A = A + matches + 1
        A[A > num_participants - 1] -= num_participants - 1
        A -= 1

    return pairings

def html_table_header(league: str, round: int) -> str:
    header: str = f"<h3>Pairings - {league} - Round {round} (<from> - <to>)</h3>\n"
    header += f"<table style=\"...\">\n"
    header += f"<tr>\n<th>No.</th>\n<th>White Player</th>\n<th>Result</th>\n"
    header += f"<th>Black Player</th>\n</tr>\n<tr>"

    return header

def html_table_body(round: int, pairings: list[list[tuple[int, int]]], league) -> str:
    pairings_table: str  = ""
    for idx, pairing in enumerate(pairings[round]):
        white_participant = league.participants[pairing[0]]
        black_participant = league.participants[pairing[1]]
        pairings_table += f"<tr>\n\t<th>{idx + 1}.</th>\n"
        pairings_table += f"<td><a href={white_participant.lichess_link}>&#x2654;{white_participant.name}</a></td>\n"
        pairings_table += f"<th> N/A </th>"
        pairings_table += f"<td><a href={black_participant.lichess_link}>&#x265A;{black_participant.name}</a></td>\n"
        pairings_table += f"</tr>\n"

    pairings_table += "</table>\n"
    return pairings_table

def main(filepath_: str):
    leagues = extract_leagues(filepath_)
    pairings_per_league: list[list[list[tuple[int, int]]]] = []
    pairings: list[list[tuple[int, int]]] = []

    # TODO(Basti): below are two variants for thml files. Either remove one or add possibility to choose between them!
    for league in leagues:
        # print(f"{league.name} ({len(league.participants)} players)\n")
        pairings = round_robin(len(league.participants))
        html_table: str = ""
        for idx, round_ in enumerate(pairings):
            html_table += html_table_header(league.name, idx + 1)
            html_table += html_table_body(idx, pairings, league)

        with open(f"{league.name}.html", "w", encoding="utf-8") as f:
                f.write(html_table)

    #     # print(f"{np.array(pairings) + 1}")
    #     pairings_per_league.append(pairings)
    #
    # round_ = 0
    # while (True):
    #     num_of_missing_pairings: int = 0
    #     html_table: str = ""
    #     for pairing, league in zip(pairings_per_league, leagues):
    #         if len(pairing) <= round_:
    #             num_of_missing_pairings += 1
    #             continue
    #
    #         html_table += html_table_header(league.name, round_ + 1)
    #         html_table += html_table_body(round_, pairing, league)
    #
    #     if (num_of_missing_pairings < len(leagues)):
    #         with open(f"./round{round_ + 1}.html", "w", encoding="utf-8") as f:
    #             f.write(html_table)
    #     else:
    #         break
    #
    #     round_ += 1

if __name__ == "__main__":
    filepath = "./example.txt"
    if len(sys.argv) == 2:
        filepath = sys.argv[1]

    main(filepath)
