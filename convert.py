import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' #Mute TF messages

import pyautogui
import numpy as np
import PIL
import cv2

def get_prediction(tiles, sess, probabilities, prediction, x, keep_prob):

    #Reshape tileset into format used by NN
    validation_set = np.swapaxes(np.reshape(tiles, [32*32, 64]),0,1)

    #Run NN
    guess_prob, guessed = sess.run(
        [probabilities, prediction], 
        feed_dict={x: validation_set, keep_prob: 1.0})
    a = np.array(list(map(lambda x: x[0][x[1]], zip(guess_prob, guessed))))
    # tile_probablities = a.reshape([8,8])[::-1,:]

    #Convert Guesses into FEN
    labelIndex2Name = lambda label_index: ' KQRBNPkqrbnp'[label_index]
    pieceNames = list(map(lambda k: '1' if k == 0 else labelIndex2Name(k), guessed)) #Convert " " to "1" (format used in FEN)
    fen = '/'.join([''.join(pieceNames[i*8:(i+1)*8]) for i in reversed(range(8))])

    return fen

def get_fen(region, sess, probabilities, prediction, x, keep_prob, reverse_fen, compressed=True):

    grayscale_img = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_BGR2GRAY)
    processed_gray_img = np.asarray(PIL.Image.fromarray(grayscale_img).resize([257,257], PIL.Image.BILINEAR), dtype=np.uint8) / 255.0
    #By resizing to 257 instead of 256 - it gives for a little more room for the edge pieces

    #Generate tiles for NN
    tiles = np.zeros([32,32,64], dtype=np.float32)
    for rank in range(8): # rows (numbers)
        for file in range(8): # columns (letters)
            tiles[:,:,(rank*8+file)] = processed_gray_img[(7-rank)*32:((7-rank)+1)*32,file*32:(file+1)*32]
    
    fen = get_prediction(tiles, sess, probabilities, prediction, x, keep_prob)

    #make compressed fen (/11111111/ --> /8/)
    if compressed:
        for length in reversed(range(2, 9)):
            fen = fen.replace(length * "1", str(length))

    #Reverese FEN if black
    if reverse_fen:
        return "/".join(fen.split("/")[::-1])
    return fen