from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver import ActionChains
import random, string, chess, chess.engine, time

from plyer import notification  # NOT NEEDED

alphabet = string.ascii_lowercase
PATH = r"PATH TO CHROMEDRIVER"
driver = webdriver.Chrome(PATH)


def check_pos(fen):
    tim = 0.25
    engine = chess.engine.SimpleEngine.popen_uci(r"Path to stockfish executable")

    board = chess.Board(fen)
    print()
    try:
        if int(driver.find_element(By.CLASS_NAME, "sidebar-play-solved").text) > 60:
            tim = 1
    except:
        ...
    info = engine.analyse(board, chess.engine.Limit(tim))["pv"][0]
    engine.close()
    return info


def click(x, y):
    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(x, y)
    action.perform()
    ActionChains(driver).click(None).perform()  # context_click is rightclick


# NUMBERS VARY BASED ON SCREEN SIZE
mice = {
    "letters": {
        "a": 257,
        "b": 360,
        "c": 490,
        "d": 572,
        "e": 692,
        "f": 810,
        "g": 976,
        "h": 1058,
    },
    "numbers": {
        "1": 910,
        "2": 837,
        "3": 740,
        "4": 520,
        "5": 424,
        "6": 275,
        "7": 167,
        "8": 63,
    },
    "lettersg": {
        "a": 360,
        "b": 450,
        "c": 572,
        "d": 692,
        "e": 784,
        "f": 810,
        "g": 976,
        "h": 1058,
    },
    "numbersg": {
        "1": 837,
        "2": 770,
        "3": 620,
        "4": 520,
        "5": 424,
        "6": 348,
        "7": 250,
        "8": 164,
    },
}

# PUZZLE
# a is 257, b is 360, c is 490, d is 572, e is 692, f is 810 g is 976, h is 1058
# '1' : 837, '2' : 713, '3' : 665, '4' : 520, '5' : 424, '6' : 275, '7' : 135 '8' : 63
# GAME
# 'a' : 360,'b': 450,'c': 572,'d': 692,'e': 784,'f': 810,'g': 976,'h': 1058
# '1' : 837,'2': 698,'3': 665,'4': 520,'5': 424,'6': 348,'7': 275,'8':164

# FINDS BOARD PIECE COORDINATES, AND PLAYS BEST MOVE
def get_board(g):
    if g == "p":
        color = 0
        while color not in ["w", "b"]:
            color = driver.find_element(By.CLASS_NAME, "section-heading-title").text
            color = color[0].lower()
    else:
        color = g
    # Position Notation:
    fen = ""

    copyy = [[0 for _ in range(8)] for z in range(8)]

    lst = driver.find_elements(By.CLASS_NAME, "piece")

    newlst = [sorted(x.get_attribute("class").split(), key=len) for x in lst]

    for x in newlst:
        try:
            coords = [int(x[2].split("-")[1][0]), int(x[2].split("-")[1][1])]
            copyy[coords[1] - 1][coords[0] - 1] = x[0]
        except:
            return
    if color == "b":
        copyy = [list(reversed(x)) for x in copyy]
    for x in reversed(copyy):
        num = 0
        for i, tile in enumerate(x):
            if tile == 0:
                num += 1
                if i == 7:
                    fen += str(num)

            else:
                if num != 0:
                    fen += str(num)
                    num = 0
                if tile[0] == "w":
                    fen += tile[1].upper()
                else:
                    fen += tile[1]
        fen += "/"

    fen = fen[:-1] + f" {color}"
    # FINDS BEST MOVE
    move = str(check_pos(fen))
    if color == "b":
        move = move[0] + str(9 - int(move[1])) + move[2] + str(9 - int(move[3]))

    print(move)
    if g == "p":  # PUZZLE MODE
        click(mice["letters"][move[0]], mice["numbers"][move[1]])
        click(mice["letters"][move[2]], mice["numbers"][move[3]])
    else:  # GAME MODE
        click(mice["lettersg"][move[0]], mice["numbersg"][move[1]])
        click(mice["lettersg"][move[2]], mice["numbersg"][move[3]])
    ActionChains(driver).click(None).perform()
    ActionChains(driver).click(None).perform()


# CREATES ALT ACCOUNT (BAN POSSIBLE)
driver.get("https://www.chess.com/register")
driver.maximize_window()
lst = driver.find_elements(By.CLASS_NAME, "ui_v5-input-component")

for _ in range(7):
    lst[0].send_keys(random.choice(alphabet))
for _ in range(7):
    lst[1].send_keys(random.choice(alphabet))
lst[1].send_keys("@gmail.com")
lst[2].send_keys("asdf12UOB@U")

while True:
    # ANSWER INPUT AFTER YOU ARE IN PUZZLE RUSH or AFTER A FEW MOVES IN A GAME
    # w = white, b = black, p = puzzle
    x = input("Game (w/b) or puzzle(p)? - (w/b/p)").lower()

    if x == "p":
        while True:
            try:
                get_board("p")
                time.sleep(1.5)
            # OPTIONAL####### STOCKFISH DOES CRASH OCCASIONALLY, this will notify you
            except Exception as e:
                notification.notify(
                    title="RIP Stockfish",
                    message=str(e),
                    app_icon=r"PATH TO .ico FILE",
                    app_name="Stockfish",
                    timeout=3,
                )
                time.sleep(3)
            #################
    else:
        while True:
            try:
                black = int(
                    driver.find_elements(By.CLASS_NAME, "black")[-1].get_attribute(
                        "data-ply"
                    )
                )
                white = int(
                    driver.find_elements(By.CLASS_NAME, "white")[-1].get_attribute(
                        "data-ply"
                    )
                )
                if x == "w" and white == black:
                    get_board(x)
                elif x == "b" and black < white:
                    get_board(x)
                time.sleep(1)
            except TypeError:
                # GAME ENDED
                break
