import requests

BASE_URL = "http://localhost:8000/game"


def print_field(matrix):
    symbols = {0: " ", 1: "X", 2: "O"}
    print("-------------")
    for row in matrix:
        print("| " + " | ".join(symbols[val] for val in row) + " |")
        print("-------------")


def create_game():
    response = requests.post(BASE_URL)
    return response.json()["game_id"]


def get_state(game_id):
    data = requests.get(f"{BASE_URL}/{game_id}").json()
    return data["field"]["matrix"], data["is_game_over"], data.get("winner")


def make_move(game_id, matrix):
    payload = {"game_id": game_id, "field": {"matrix": matrix}}
    return requests.post(f"{BASE_URL}/{game_id}", json=payload).json()


def main():
    game_id = create_game()
    matrix, game_over, winner = get_state(game_id)
    print_field(matrix)

    while not game_over:
        row, col = map(int, input().split())
        matrix[row][col] = 1
        result = make_move(game_id, matrix)
        matrix = result["field"]["matrix"]
        print_field(matrix)
        game_over, winner = result["is_game_over"], result.get("winner")

    if winner == 1:
        print("Победа X!")
    elif winner == 2:
        print("Победа O!")
    else:
        print("Ничья!")


if __name__ == "__main__":
    main()
