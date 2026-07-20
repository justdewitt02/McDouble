"""
Checks whether the Chattanooga Lookouts hit a double in their most recent
HOME game (checked the day after), and sends a push notification via
ntfy.sh if they did -- meaning it's a $1 McDouble day.

Runs for free on a schedule via GitHub Actions (see .github/workflows/).
"""
import datetime
import os
import sys
import requests

STATS_API = "https://statsapi.mlb.com/api/v1"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")  # set as a GitHub Actions secret


def find_team_id():
    """Find the Lookouts' team ID for the Double-A sport (sportId=12)."""
    resp = requests.get(f"{STATS_API}/teams", params={"sportId": 12, "activeStatus": "Y"})
    resp.raise_for_status()
    for team in resp.json().get("teams", []):
        if "Chattanooga" in team.get("name", ""):
            return team["id"], team["name"]
    raise RuntimeError("Could not find Chattanooga Lookouts in team list")


def get_recent_home_games(team_id, days_back=2):
    """Get completed home games in the last `days_back` days."""
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days_back)
    resp = requests.get(
        f"{STATS_API}/schedule",
        params={
            "sportId": 12,
            "teamId": team_id,
            "startDate": start.isoformat(),
            "endDate": today.isoformat(),
        },
    )
    resp.raise_for_status()
    games = []
    for date_entry in resp.json().get("dates", []):
        for game in date_entry.get("games", []):
            if (
                game["status"]["abstractGameState"] == "Final"
                and game["teams"]["home"]["team"]["id"] == team_id
            ):
                games.append(game)
    return games


def game_had_double(game_pk, team_id):
    """Check the boxscore for whether the home team hit any doubles."""
    resp = requests.get(f"{STATS_API}/game/{game_pk}/boxscore")
    resp.raise_for_status()
    data = resp.json()
    home_team = data["teams"]["home"]
    if home_team["team"]["id"] != team_id:
        return False, 0
    doubles = home_team["teamStats"]["batting"].get("doubles", 0)
    return doubles > 0, doubles


def send_notification(title, message):
    if not NTFY_TOPIC:
        print("NTFY_TOPIC not set -- skipping push, printing instead.")
        print(title, "-", message)
        return
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": title, "Priority": "high", "Tags": "baseball,hamburger"},
    )


def main():
    team_id, team_name = find_team_id()
    games = get_recent_home_games(team_id)

    if not games:
        print(f"No recent completed home games found for {team_name}.")
        return

    any_double = False
    for game in games:
        had_double, count = game_had_double(game["gamePk"], team_id)
        game_date = game["officialDate"]
        if had_double:
            any_double = True
            print(f"{game_date}: {team_name} hit {count} double(s) at home!")
            send_notification(
                "McDouble Day! 🍔",
                f"The Lookouts hit {count} double(s) in their {game_date} home game. "
                f"$1 McDouble is on today!",
            )
        else:
            print(f"{game_date}: no doubles at home.")

    if not any_double:
        print("No doubles in recent home games -- no McDouble deal today.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
