from detect import locate

def main():
    #Get the location of the board(x, y, dimx, dimy) and the pixels per square of this board
    region, pps = locate()

    print(region, pps)

    # PLAN -->
    #find board
    
    #loop
        #convert to FEN

        #find best move

        #play best move

        #wait for response

if __name__ == "__main__":
    main()