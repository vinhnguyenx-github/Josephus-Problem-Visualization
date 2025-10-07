import json

K_PRIMARY = 3
K_FALLBACK = 2

def josephus_elimination_hybrid(n):
    people = list(range(1, n + 1))
    steps = []
    idx = 0
    while len(people) > 1:
        # dynamic k
        k = K_PRIMARY if len(people) >= 3 else K_FALLBACK
        idx = (idx + k - 1) % len(people)
        eliminated = people.pop(idx)
        steps.append({
            "eliminated": eliminated,
            "remaining": people.copy(),
            "k_used": k
        })
    return {
        "n": n,
        "winner": people[0] if people else None,
        "rounds": steps
    }

def generate_table(max_n=30):
    data = {}
    for n in range(1, max_n + 1):
        data[f"n={n}"] = josephus_elimination_hybrid(n)
    return data

def save_to_json(filename="josephus_table.json", winner_file="josephus_winners.json"):
    table = generate_table()
    with open(filename, "w") as f:
        json.dump(table, f, indent=4)

    winners = {str(n): table[f"n={n}"]["winner"] for n in range(1, 31)}
    with open(winner_file, "w") as f:
        json.dump(winners, f, indent=4)

    print(f"Saved full table to {filename}")
    print(f"Saved winners-only data to {winner_file}")

if __name__ == "__main__":
    save_to_json()