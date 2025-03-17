import sys
import numpy as np

from excel_reader import extract_leagues

round_robin_scheudle: dict = {
        4: (
            ((0,3),(1,2)),
            ((3,2),(0,1)),
            ((1,3), (2,0))
            ),
        6: (
            ((0,5),(1,4),(2,3)),
            ((5,3),(4,2),(0,1)),
            ((1,5),(2,0),(3,4)),
            ((5,4),(0,3),(1,2)),
            ((2,5),(3,1),(4,0))
            )
        }

def round_robin(participants: list[str]) -> None:
    odd_participants = False
    if len(participants) % 2 == 1:
        odd_participants = True
        participants.append("")
    matches = int(len(participants)/2)


    A = np.array([x for x in range(matches)])
    B = np.array([x for x in range(2*matches-1, matches-1, -1)])
    B0 = len(participants) - 1
    for round_ in range(len(participants) - 1):
        match_schedule = f"Rnd. {round_ + 1}: "
        for match in range(matches):
            # skip first match, as match against highest indexed participant is skipped in this case
            if match == 0:
                if odd_participants:
                    continue

                if round_ % 2 == 1:
                    match_schedule = match_schedule + f"| {participants[B[match]]} - {participants[A[match]]} "
                    continue
            match_schedule = match_schedule + f"| {participants[A[match]]} - {participants[B[match]]} "

        print(match_schedule)
        B = B + matches + 1
        B[B>len(participants)- 1] -= len(participants) - 1
        B -= 1
        B[0] = B0
        A = A + matches + 1
        A[A > len(participants) - 1] -= len(participants) - 1
        A -= 1

def main(filepath: str):
    # participants: list = []
    # with open(filepath, 'r') as reader:
    #     for line in reader:
    #         participants.append(line.split("\n")[0])

    leagues = extract_leagues(filepath)

    for league in leagues:

        # if len(league.participants) % 2 == 1:
        #     league.participants.append("DUMMY")

        print(f"{league.name} ({len(league.participants)} players)\n")
        round_robin(league.participants)
        print("\n")

        # if len(league.participants) < 4 or len(league.participants) > 6:
        #     continue
        #
        # for round_, matches in enumerate(round_robin_scheudle[len(league.participants)]):
        #     schedule += f"Round {round_ + 1}:\n"
        #     for match in matches:
        #         pairing = f"\t{league.participants[match[0]]} - {league.participants[match[1]]}\n"
        #         if "DUMMY" in pairing:
        #             continue
        #         schedule += pairing
        #
        #
        # print(schedule)

if __name__ == "__main__":
    filepath = "./example.txt"
    if len(sys.argv) == 2:
        filepath = sys.argv[1]

    main(filepath)
