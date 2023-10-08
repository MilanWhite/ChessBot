import tensorflow as tf
from time import sleep

#Animation (Remove if not needed)
import itertools
import threading
import os
import sys


#Chess
import chess
import chess.engine

from detect import locate
from convert import get_fen
from autogui import make_dicts
from autogui import move_pieces

def get_castle_str(fen, k_num):
    #A castle string informs the engine whether castling is possible or not
    split_fen = fen.split("/")
    castle_str = ""
    #If the king is in their original place, and a rook is also unmoved --> castling is possible
    #Done for both white and black
    if (split_fen[-1][k_num] == 'K'):
        if split_fen[-1][-1] == 'R':
            castle_str += "K"
        if split_fen[-1][0] == 'R':
            castle_str += "Q"
    if (split_fen[0][k_num] == 'k'):
        if split_fen[0][0] == 'r':
            castle_str += "k"
        if split_fen[0][-1] == 'r':
            castle_str += "q"
    return castle_str #KQkq

def get_color(fen):
    #First king in FEN determines color
    for i in fen:
        if i == "K": return "b"
        elif i == "k": return "w"

def set_move(fen):
    #Get engine --> Set board --> get best move --> update board
    over = False
    try:
        engine = chess.engine.SimpleEngine.popen_uci("./weights/stockfish_12_win_x64_avx2/stockfish_20090216_x64_avx2.exe")

        board = chess.Board(fen)
        limit = chess.engine.Limit(time=5.0)
        move = str(engine.play(board, limit).move)
        move_uci = chess.Move.from_uci(move)
        board.push(move_uci)
        brd_fen = board.fen().split(' ')[0]

        if board.is_game_over():
            over = True

        engine.quit()
        return move, brd_fen, over, board

    except chess.engine.EngineTerminatedError:
        print('engine died lol, fen:', fen)

def load_weights(weightsPath):
    #Load Tensorflow weights
    print("Loading weights...")
    with tf.io.gfile.GFile(weightsPath, "rb") as f:
        weight_def = tf.compat.v1.GraphDef()
        weight_def.ParseFromString(f.read())
    with tf.Graph().as_default() as weights:
        tf.import_graph_def(weight_def, name="tcb")
    return weights


def main():
    #Locate the board
    region, pps = locate()
    #Load TF graph
    weights = load_weights("./weights/model.pb")
    sess, x, keep_prob, prediction, probabilities = tf.compat.v1.Session(graph=weights), weights.get_tensor_by_name('tcb/Input:0'), \
        weights.get_tensor_by_name('tcb/KeepProb:0'), weights.get_tensor_by_name('tcb/prediction:0'), weights.get_tensor_by_name('tcb/probabilities:0')
    
    # Determine the king number, color, and FEN formatting
    fen = get_fen(region, sess, probabilities, prediction, x, keep_prob, False, False)
    k_num = 4 #Default king in 4th position for white
    color = get_color(fen)
    reverse_fen = False
    if color == "b":
        fen = "/".join(fen.split("/")[::-1]) #rewrite fen as black first (b/w)
        k_num = 3 #King position when black
        reverse_fen = True

    #Determine castling parameters
    castle_str = get_castle_str(fen, k_num)

    #MAIN GAME
    let, num = make_dicts(pps, color) #make dictionaries that link coords on board(a-h, 1-8) to pixels on screen
    active = True
    while active:
        #Get FEN --> get best move --> play best move --> wait for response
        fen = get_fen(region, sess, probabilities, prediction, x, keep_prob, reverse_fen)
        move, brd_fen, over, board = set_move(f"{fen} {color} {castle_str}")
        move_pieces(let, num, region[0], region[1], move, pps, k_num)

        if over:
            print('Good Game')
            active = False

        #OUTPUT (Disable if not needed)
        os.system("cls")
        print(f"{board}\nMove: {move}\n")
        waiting = True
        def animate_waiting():
            for c in itertools.cycle(["|", "/", "-", "\\"]):
                if not waiting:
                    break
                sys.stdout.write("\rWaiting for Response " + c)
                sys.stdout.flush()
                sleep(0.1)
            sys.stdout.write("\rDone" + " "*20)
        t = threading.Thread(target=animate_waiting)
        t.start()

        while waiting:
            sleep(0.75)
            wait_fen = get_fen(region, sess, probabilities, prediction, x, keep_prob, reverse_fen)
            if wait_fen != brd_fen: #Compare a new FEN to old FEN to determine whether a move has been played
                sleep(0.75) #Delay is to ensure the move animation has been played out before continuation
                waiting = False

if __name__ == "__main__":
    main()