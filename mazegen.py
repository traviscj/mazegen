#!/usr/bin/python
# author: traviscj@traviscj.com		3/28/2013		
# A maze generator using Randomized Prim's algorithm on the cells of the maze
# output format based on: http://robotics.ee.uwa.edu.au/eyebot/doc/sim/maze.html
import random, sys
NORTH, SOUTH, EAST,  WEST   = lambda c: (c[0]-1,c[1]), lambda c: (c[0]+1,c[1]),lambda c: (c[0],c[1]+1), lambda c: (c[0],c[1]-1)
VWALL, HWALL, VBLANK,HBLANK = '|', '_', '_', ' '
class maze(object):
	def __init__(self, rows, cols):
		self.squares_,self.rowset_, self.colset_ = {},range(1,rows+1), range(1,cols+1)
		for row in self.rowset_:
			for col in self.colset_:
				self.squares_[(row,col)] = {'h': HWALL, 'v': VWALL}
		x0,    y0              = random.choice(self.rowset_), random.choice(self.colset_)
		queue, self.reachable_ = {(x0,y0): True},      {(x0,y0): True}
		while len(self.reachable_.keys()) < len(self.squares_.keys()):
			self.neighbors_ = []
			while self.neighbors_ == []:
				fromcell = random.choice(queue.keys())
				self.gen_neighbors(fromcell)
				if self.neighbors_ == []: del queue[fromcell]
			direction = random.choice(self.neighbors_)
			if   direction == SOUTH : self.squares_[          fromcell ]['h'] = HBLANK
			elif direction == EAST  : self.squares_[          fromcell ]['v'] = VBLANK
			elif direction == NORTH : self.squares_[direction(fromcell)]['h'] = HBLANK
			elif direction == WEST  : self.squares_[direction(fromcell)]['v'] = VBLANK
			queue[direction(fromcell)], self.reachable_[direction(fromcell)] = True, True
		self.squares_[(x0,y0)]['h'] = self.squares_[(x0,y0)]['h']=='_' and 'S' or 's'
	def gen_neighbors(self,fromcell):
		# what is criteria for valid wall removal?
		# 1) must be in the list of squares, 2) must not already be reachable, 3) wall must not already be removed.
		good = lambda f,c:  f(c) in self.squares_ and f(c) not in self.reachable_
		if good(NORTH,fromcell) and self.squares_[NORTH(fromcell)]['h'] == HWALL:   self.neighbors_.append( NORTH )
		if good(EAST, fromcell) and self.squares_[     (fromcell)]['v'] == VWALL:   self.neighbors_.append( EAST )
		if good(SOUTH,fromcell) and self.squares_[     (fromcell)]['h'] == HWALL:   self.neighbors_.append( SOUTH )
		if good(WEST, fromcell) and self.squares_[WEST (fromcell)]['v'] == VWALL:   self.neighbors_.append( WEST )
	def printgrid(self):
		print " " + "_"*(2*len(self.colset_)-1)+" "
		for row in self.rowset_:
			print "|"+"".join([self.squares_[(row,col)]['h'] + self.squares_[(row,col)]['v'] for col in self.colset_])	
if __name__ == "__main__":
	if len(sys.argv)<3: print "usage: "+sys.argv[0]+" rows cols"; sys.exit()
	else:               rows,cols = int(sys.argv[1]), int(sys.argv[2])
	g = maze(rows, cols)
	g.printgrid()
