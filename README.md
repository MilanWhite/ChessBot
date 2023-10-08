# Chess Bot
*A chess bot that plays chess games for you*
This repository is a personal project of a chess bot that is meant to play top engine moves for you on any chess site: Chess.com, Lichess.com, Chess24.com, etc.

https://github.com/MilanWhite/ChessBot/assets/69779040/a9f45f77-e01b-4ed0-8d45-84a76db4585c


## Usage
```
pip install -r requirements.txt
```
Run Chess_Bot.py
```
python Chess_Bot.py
```
## Breakdown
### Board Detection:
Board detection is done through [OpenCV](https://opencv.org/) and Computer Vision. Check out my [ChessBoardDetection](https://github.com/MilanWhite/ChessBoardDetection) repo.
### Piece Recognition
Piece recognition is done through a trained TensorFlow Neural Network. Check out my [ChessPieceRecognition](https://github.com/MilanWhite/TFChessPieceRecognition) repo.
