#!/usr/bin/python

class Field():

    WIDTH = 10
    HEIGHT = 22
    
    def __init__(self):
        self.state = [[' ' for cols in range(WIDTH)] for rows in range(HEIGHT)]

    def drop(self, tetromino):
        pass
        
if __name__ == '__main__':
