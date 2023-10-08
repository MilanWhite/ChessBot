# Chess Bot
*A chess bot that plays chess games for you*
This repository is a personal project of a chess bot that is meant to play top engine moves for you on any chess site: Chess.com, Lichess.com, Chess24.com, etc.

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
