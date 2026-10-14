# Sprint 1 Local Sample Dataset
games = [
    {
        "name": "Portal 2",
        "rating": 4.6,
        "genre": "Puzzle",
        "platform": "PC",
    },
    {
        "name": "The Witcher 3",
        "rating": 4.8,
        "genre": "RPG",
        "platform": "PC",
    },
    {
        "name": "Minecraft",
        "rating": 4.5,
        "genre": "Sandbox",
        "platform": "Multi-platform",
    },
    {
        "name": "Hades",
        "rating": 4.7,
        "genre": "Action",
        "platform": "Nintendo Switch",
    },
    {
        "name": "God of War",
        "rating": 4.7,
        "genre": "Action",
        "platform": "PlayStation",
    },
    {
        "name": "Stardew Valley",
        "rating": 4.4,
        "genre": "Simulation",
        "platform": "PC",
    },
    {
        "name": "Mario Kart 8 Deluxe",
        "rating": 4.5,
        "genre": "Racing",
        "platform": "Nintendo Switch",
    },
    {
        "name": "Baldur's Gate 3",
        "rating": 4.9,
        "genre": "RPG",
        "platform": "PC",
    },
]


def display_welcome_message():
    """Display the application title in a readable banner."""
    print("=" * 60)
    print("             GAMING STATISTICS DASHBOARD")
    print("=" * 60)


def display_main_menu():
    """Display the available menu options."""
    print("\n1. View Games")
    print("2. Search Game")
    print("3. View Statistics")
    print("4. View Genres")
    print("5. View Top Rated Games")
    print("0. Exit")


def get_menu_choice():
    """Read and validate a menu choice from 0 to 5."""
    user_input = input("\nSelect an option: ").strip()

    if not user_input:
        print("Warning: Please enter a menu option from 0 to 5.")
        return None

    try:
        choice = int(user_input)
    except ValueError:
        print("Warning: Menu choice must be a number from 0 to 5.")
        return None

    if choice < 0 or choice > 5:
        print("Warning: Please select a menu option from 0 to 5.")
        return None

    return choice


def view_games():
    """Display every game in the local sample dataset."""
    print("\nGAMES")
    print("-" * 72)

    for number, game in enumerate(games, start=1):
        print(
            f"{number}. {game['name']} | "
            f"Rating: {game['rating']:.1f} | "
            f"Genre: {game['genre']} | "
            f"Platform: {game['platform']}"
        )


def search_game():
    """Search for games using a case-insensitive partial name."""
    search_term = input("\nEnter game name: ").strip()

    if not search_term:
        print("Warning: Search term cannot be blank.")
        return

    matching_games = [
        game
        for game in games
        if search_term.lower() in game["name"].lower()
    ]

    if not matching_games:
        print(f'Game not found: "{search_term}"')
        return

    print("\nSEARCH RESULTS")
    print("-" * 72)

    for number, game in enumerate(matching_games, start=1):
        print(
            f"{number}. {game['name']} | "
            f"Rating: {game['rating']:.1f} | "
            f"Genre: {game['genre']} | "
            f"Platform: {game['platform']}"
        )


def view_statistics():
    """Calculate and display statistics from the local dataset."""
    total_games = len(games)
    total_rating = sum(game["rating"] for game in games)
    average_rating = total_rating / total_games if total_games else 0
    highest_rating = max(
        (game["rating"] for game in games),
        default=0,
    )

    print("\nGAME STATISTICS")
    print("-" * 40)
    print(f"Total Games: {total_games}")
    print(f"Average Rating: {average_rating:.2f}")
    print(f"Highest Rating: {highest_rating:.1f}")
    print(
        "Note: These statistics come from the "
        "Sprint 1 local sample dataset."
    )


def view_genres():
    """Count and display the number of games in each genre."""
    genre_counts = {}

    for game in games:
        genre = game["genre"]
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    print("\nGAME GENRES")
    print("-" * 40)

    for genre in sorted(genre_counts):
        print(f"{genre}: {genre_counts[genre]} game(s)")


def view_top_games():
    """Display games sorted from highest to lowest rating."""
    sorted_games = sorted(
        games,
        key=lambda game: game["rating"],
        reverse=True,
    )

    print("\nTOP RATED GAMES")
    print("-" * 40)

    for number, game in enumerate(sorted_games, start=1):
        print(f"{number}. {game['name']} - {game['rating']:.1f}")


def main():
    """Run the Gaming Statistics Dashboard menu loop."""
    display_welcome_message()

    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice is None:
            continue

        if choice == 1:
            view_games()
        elif choice == 2:
            search_game()
        elif choice == 3:
            view_statistics()
        elif choice == 4:
            view_genres()
        elif choice == 5:
            view_top_games()
        elif choice == 0:
            print("\nThank you for using Gaming Statistics Dashboard.")
            print("Goodbye!")
            break

main()