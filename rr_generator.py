import sys

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

def main(filepath: str):
    participants: list = []
    with open(filepath, 'r') as reader:
        for line in reader:
            participants.append(line.split("\n")[0])

    if len(participants) % 2 == 1:
        participants.append("DUMMY")

    print(participants)
    schedule: str = ""
    
    for round_, matches in enumerate(round_robin_scheudle[len(participants)]):
        schedule += f"Round {round_ + 1}:\n"
        for match in matches:
            pairing = f"\t{participants[match[0]]} - {participants[match[1]]}\n"
            if "DUMMY" in pairing:
                continue
            schedule += pairing


    print(schedule)

if __name__ == "__main__":
    filepath = "./example.txt"
    if len(sys.argv) == 2:
        filepath = sys.argv[1]

    main(filepath)
