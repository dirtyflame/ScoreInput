from tkinter import *
from jsonFunctions import *


def clear_stack():  # Empties the current stack and creates a new line on the input screen if necessary

    global teams_stack
    global score_stack
    global display_text
    global stackUpdateTick
    global display_called

    if teams_stack:
        teams_stack = []

        display_called += 1  #stops creating new line constantly if button is spammed

        failed = Label(root, text="Cleared")
        failed.grid(row=display_called, column=3)

    score_stack = []

    display_text = ""
    stackUpdateTick = 0


def submit_stack():  # Checks stack is full and then submits data to file

    global teams_stack
    global score_stack
    global display_text
    global stackUpdateTick
    global display_called
    global league

    if len(score_stack) == 2 and len(teams_stack) == 2:

        # Home Team
        stat_update(league, teams_stack[0], "Played Home", 1)
        stat_update(league, teams_stack[0], "Scored Home", score_stack[0])
        stat_update(league, teams_stack[0], "Conceded Home", score_stack[1])

        # Away Team
        stat_update(league, teams_stack[1], "Played Away", 1)
        stat_update(league, teams_stack[1], "Scored Away", score_stack[1])
        stat_update(league, teams_stack[1], "Conceded Away", score_stack[0])

        # Update recent form for both teams
        update_recent_form(league, teams_stack[0], teams_stack[1], score_stack[0], score_stack[1])

        log(f"Submitted {teams_stack[0]} {score_stack[0]} - {score_stack[1]} {teams_stack[1]}.")

        teams_stack = []
        score_stack = []

        display_called += 1  # stops creating new line constantly if button is spammed

        failed = Label(root, text="Submitted")
        failed.grid(row=display_called, column=3)

        score_stack = []

        display_text = ""
        stackUpdateTick = 0


def change_display_text():  # Changes the text which shows up on the UI

    global display_text

    display_text = ""

    if not score_stack:

        if len(teams_stack) == 1:
            display_text = teams_stack[0]

        if len(teams_stack) == 2:
            display_text = f"{teams_stack[0]} v {teams_stack[1]}"

    if len(score_stack) == 1:
        display_text = f"{teams_stack[0]} {score_stack[0]} -   {teams_stack[1]}"

    if len(score_stack) == 2:
        display_text = f"{teams_stack[0]} {score_stack[0]} - {score_stack[1]} {teams_stack[1]}"


def show_display_text():  # Creates labels to display input

    global display_text
    global display_called
    global stackUpdateTick

    if stackUpdateTick == 3:
        display_called += 1
        stackUpdateTick = 0

    displayLabel = Label(root, text=display_text, padx=5, pady=0)
    displayLabel.grid(row=display_called + 1, column=2)


def add_team_to_stack(team):  # Adds team to stack if applicable and then calls the display function

    global teams_stack
    global display_text
    global stackUpdateTick

    if len(teams_stack) < 2 and team not in teams_stack:

        teams_stack.append(team)
        change_display_text()
        stackUpdateTick += 1

    show_display_text()


def add_score_to_stack(num):  # Adds score to stack if applicable and then calls the display function

    global score_stack
    global teams_stack

    if len(score_stack) < 2 and len(teams_stack) == 2:
        score_stack.append(num)

    change_display_text()
    show_display_text()


def create_team_buttons(team_list):  # Creates the team buttons in rows of 2

    columnNum = 0
    rowNum = 0

    colour_count = 1
    button_colour = "#F0F0F0"

    for j in team_list:

        if colour_count == 2 and button_colour == "#F0F0F0":
            button_colour = "#DBDBDB"
            colour_count = 0

        if colour_count == 2 and button_colour == "#DBDBDB":
            button_colour = "#F0F0F0"
            colour_count = 0

        if columnNum == 2:
            columnNum = 0
            rowNum += 1

        teamButton = Button(root, text=j, width=10, background = button_colour, command=lambda name=j: add_team_to_stack(name))
        teamButton.grid(row=rowNum, column=columnNum)
        columnNum += 1
        colour_count += 1


def create_clear_button(team_list):  # Adds clear button at the bottom of the team buttons

    row_position = round(len(team_list)/2) + 1

    clearButton = Button(root, text="Clear", width=22, background="#FF4248", command=clear_stack)
    clearButton.grid(row=row_position, column=0, columnspan=2)


def create_number_buttons():  # Self-explanatory

    columnNum = 0
    rowNum = 0

    zeroButton = Button(root, text="0", width=18, command=lambda: add_score_to_stack(0))
    zeroButton.grid(row=0, column=4, columnspan=3)

    for i in range(1, 10):

        if columnNum == 3:
            columnNum = 0
            rowNum += 1

        numberButton = Button(root, text=i, width=5, command=lambda num=i: add_score_to_stack(num))
        numberButton.grid(row=rowNum + 1, column=columnNum + 4)

        columnNum += 1


def create_submit_button():  # Self-explanatory

    submitButton = Button(root, text="Submit to JSON", width=18, background="#FFF13A", command=submit_stack)
    submitButton.grid(row=4, column=4, columnspan=3)


def create_excel_submit_button():

    excelButton = Button(root, text="Submit to Excel", width=18, background="#20FF14", command=lambda: add_data_to_excel(league))
    excelButton.grid(row=5, column=4, columnspan=3)


def add_titles():  # Just adds the titles at the top

    scores = Label(root, text="Input", font=("Helvetica", 11, "bold"))
    scores.grid(row=0, column=2)

    status = Label(root, text="Status", font=("Helvetica", 11, "bold"))
    status.grid(row=0, column=3)


league = call_league()

root = Tk()

root.title("Score Input")
root.iconbitmap(get_bitmap())  # Doesn't actually work but cba removing it

# Variables that are called here since pretty much every function uses them
teams_stack = []
score_stack = []
# "Stack" is what I call the lists which store the two team names and two scores
display_text = ""
display_called = 0
stackUpdateTick = 0

Teams = load_teams(league)

create_team_buttons(Teams)
create_clear_button(Teams)
add_titles()
create_number_buttons()
create_submit_button()
create_excel_submit_button()
log("------------------------------------------------------")
log(f"{league} selected and program initialised...")


root.mainloop()
