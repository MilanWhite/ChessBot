import time
import win32api
import win32con
import pyautogui

#Piece move functions
def click_drag(x, y, x2, y2):
    x, y = int(x), int(y)
    x2, y2 = int(x2), int(y2)
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x2, y2, 0.1)
    pyautogui.mouseUp(button='left')

def click(x, y):
    x, y = int(x), int(y)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#Create dictionaries to link engine output (e2e4) to on-screen coordinates for quick access
def make_dicts(pps, color):

    half_pps = pps / 2

    letter = {
        'a' : half_pps,
        'b' : half_pps + pps,
        'c' : half_pps + (pps * 2),
        'd' : half_pps + (pps * 3),
        'e' : half_pps + (pps * 4),
        'f' : half_pps + (pps * 5),
        'g' : half_pps + (pps * 6),
        'h' : half_pps + (pps * 7),
    }

    if color == 'w':
        number = {
            '8' : half_pps,
            '7' : half_pps + pps,
            '6' : half_pps + (pps * 2),
            '5' : half_pps + (pps * 3),
            '4' : half_pps + (pps * 4),
            '3' : half_pps + (pps * 5),
            '2' : half_pps + (pps * 6),
            '1' : half_pps + (pps * 7),
        }
    else:
        number = {
            '1' : half_pps,
            '2' : half_pps + pps,
            '3' : half_pps + (pps * 2),
            '4' : half_pps + (pps * 3),
            '5' : half_pps + (pps * 4),
            '6' : half_pps + (pps * 5),
            '7' : half_pps + (pps * 6),
            '8' : half_pps + (pps * 7),
        }

    return letter, number


def move_pieces(letter, number, startX, startY, code, pps, k_num):

    if code != '0-0' or '0-0-0':
        list_code = list(code)

        click_drag(letter[list_code[0]] + startX, number[list_code[1]] + startY, letter[list_code[2]] + startX, number[list_code[3]] + startY)

        #Promotion of pieces
        if len(list_code) > 4:
            if list_code[-1] == 'q':
                click(letter[list_code[2]] + startX, number[list_code[3]] + startY)
            elif list_code[-1] == 'n':
                click(letter[list_code[2]] + startX, (number[list_code[3]] + startY) - pps)
            elif list_code[-1] == 'r':
                click(letter[list_code[2]] + startX, (number[list_code[3]] + startY) - (pps * 2))
            elif list_code[-1] == 'b':
                click(letter[list_code[2]] + startX, (number[list_code[3]] + startY) - (pps * 3))
    #Castling
    else:
        if code == '0-0':
            click_drag(letter['h'], number[str(k_num)], letter['h'], number[str(k_num)] - (pps * 2))

        if code == '0-0-0':
            click_drag(letter['h'], number[str(k_num)], letter['h'], number[str(k_num)] + (pps * 2))