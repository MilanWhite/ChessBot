<h1 align="center">Chess Bot</h1>
<p align="center"><i>A chess bot that plays chess for you</i></p>

This repository is a personal project of a chess bot that is meant to play chess for you on any chess site: Chess.com, Lichess.com, Chess24.com, etc.

<h3>Breakdown:</h3>

  <p>1) Board Detection</p>
  Board detection is achieved through the use of image manipulation with <a href="https://opencv.org/">OpenCV.</a> Using <code>cv2.Canny()</code> filters the edges of the image - 
  allowing for later use of <code>cv2.getStructuringElement()</code> and <code>cv2.erode()</code> to extract horizontal/vertical lines only. A next step is to combine the two filtered images into one with <code>cv2.maximum(img1, img2)</code>. 
  The resultant image now contains only straight and horizontal lines, allowing for contour detection around the vertices of the squares within the image. <br><br>
