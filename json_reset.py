from jsonFunctions import *


def main():

    league_name = call_league()

    team_stats = league_path(league_name) + "team_stats.json"
    recent_form = league_path(league_name) + "recent_form.json"

    message = f"Stats for {league_name} have been created/reset."

    if os.path.exists(team_stats):
        os.remove(team_stats)

    if os.path.exists(recent_form):
        os.remove(recent_form)

    create_dictionary(league_name)
    create_recent_form_list(league_name)
    log(message)


if __name__ == "__main__":
    main()