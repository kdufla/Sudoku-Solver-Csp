import sys
from multiprocessing import Pool


'''
helper methods for trivial operations
'''

def get_input_as_list(inp):
	ls = []
	for i in range(9):
		ls.append([0] * 9)
	for x in range(9):
		for y in range(9):
			if(inp[9*x+y]!='.'):
				ls[x][y]=int(inp[9*x+y])
	return ls

def get_output(ls):
	st=''
	for x in ls:
		for i in x:
			st+=str(i)
	
	return st+'\n'

def is_in_row(i,n,ls,z):
	for x in range(9):
		if ls[i][x]==n and x!=z:
			return True
	return False

def is_in_col(i,n,ls,z):
	for x in range(9):
		if ls[x][i]==n and x!=z:
			return True
	return False

def get_box_borders(x,y):
	if x<3:
		sx=0
		ex=3
	elif x>5:
		sx=6
		ex=9
	else:
		sx=3
		ex=6

	if y<3:
		sy=0
		ey=3
	elif y>5:
		sy=6
		ey=9
	else:
		sy=3
		ey=6

	return (sx,ex,sy,ey)

def in_box(x,y,n,ls):
	sx,ex,sy,ey=get_box_borders(x,y)
	for xx in range(sx,ex):
		for yy in range(sy,ey):
			if ls[xx][yy]==n and xx!=x and yy!=y:
				return True
	return False


# check if putting domain n in variable (x,y) satisfies constraints
def satisfies_constraint(x,y,n,board):
	return not (is_in_row(x,n,board,y) or is_in_col(y,n,board,x) or in_box(x,y,n,board))

# forward checking: update lists of domains after chooseing n for variable (x,y)
# and return records for reverseing changes (backtracking)
def update_neighbours(x,y,n,domain):
	record=[]
	for i in range(9):
		if (x,i) in domain and n in domain[(x,i)]:
			domain[(x,i)].remove(n)
			record.append((x,i))
		if (i,y) in domain and n in domain[(i,y)]:
			domain[(i,y)].remove(n)
			record.append((i,y))

	sx,ex,sy,ey=get_box_borders(x,y)
	for xx in range(sx,ex):
		for yy in range(sy,ey):
			if (xx,yy) in domain and n in domain[(xx,yy)]:
				domain[(xx,yy)].remove(n)
				record.append((xx,yy))
	
	#print(n,record)
	return record

# backtracking: reverse changes after seeing that choosen subtree was wrong one 
def reverse_update(value,record,domain):
	for index in record:
		domain[index].append(value)

# builds list of domains for every variable
def build_domains(board): 
	domain={}
	for xx in range(9):
		for yy in range(9):
			if board[xx][yy]==0:
				domain[(xx,yy)]=[z for z in range(1,9+1) if satisfies_constraint(xx,yy,z,board)]
	return domain

'''
Recursive Backtracking Search:

base case:
	board is filled

chooses variable to fill (MRV) and checks every value
'''
def rec_back(ls,domain):
	if not domain:
		return True

	x,y=min(domain,key=lambda x:len(domain[x]))
	values=domain[(x,y)]
	
	for value in values:
		# update board and domain
		ls[x][y]=value
		del domain[(x,y)]
		record=update_neighbours(x,y,value,domain)


		res=rec_back(ls,domain)
		
		if(res):
			return True
		else:
			ls[x][y]=0
			domain[(x,y)]=values
			reverse_update(value,record,domain)
	return False

def solve_csp(sudoku):
	ls=get_input_as_list(sudoku)
	domain=build_domains(ls)
	rec_back(ls,domain)
	return get_output(ls)

def main():
	a=open(sys.argv[1],'r')
	b=open(sys.argv[2],'w')


	sudokus=[]

	sudoku=a.readline()
	while sudoku:
		sudokus.append(sudoku)
		sudoku=a.readline()

	p=Pool(8)
	sudokus=p.map(solve_csp,sudokus)

	for x in sudokus:
		b.write(x)
		
	a.close()
	b.close()

if __name__ == "__main__": main()