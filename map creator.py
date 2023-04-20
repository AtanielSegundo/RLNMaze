from colordict import ColorDict
import os
import random
import numpy as np
import pygame as pg
from screeninfo import get_monitors

# MAP DESIGN CREATOR 1.0
Modo = input("E - Editar / C - Criar \n").strip().upper()

if Modo == "E":
    NOME = input("Nome do mapa: ")
    MAPA = np.load("./Mapas/"+NOME+".npy")
    LINHAS = len(MAPA)
    COLUNAS = len(MAPA[:])
else:
    MAPA = None
    LINHAS =  int(input("LINHAS = "))
    COLUNAS = int(input("COLUNAS = "))
#______________________________________________________________________________


cores = ColorDict() 

#proposito corretivo
def limitador(maze : object , l : int , c : int) -> tuple: 
    correct = False
    X = l
    Y = c
    if l >= maze.linhas  :
        X = maze.linhas - 1
        correct = True
    if c >= maze.linhas  :
        Y = maze.colunas - 1    
        correct = True
    if correct == True:
        return X,Y
    return l,c
#proposito estetico
def quitecheck(test) -> bool :
    for event in test:
        if event.type == pg.QUIT:
            return True
    return False 
        

# Classe que armazena o labirinto
class maze:
      
     def __init__(self,linhas : int ,colunas : int,MODE : str, MAPA : list):
         self.linhas  :int  = linhas
         self.colunas :int  = colunas
         if MODE == 'E':
             self.mapa = MAPA
         else:
             self.mapa    :list = self.DMC()
             
         self.livre ,self.parede = self.countwalls()  
     
     
     def countwalls(self):
         columns = self.colunas
         lines =   self.linhas
         livre = columns*lines
         parede = 0
         for i in range(self.linhas):
          for j in range(self.colunas):
              if self.mapa[i][j] == 1:
                  parede+=1
                  livre-=1
         return livre,parede
     
     #Gera o labirinto utilizando o algoritmo de prim aleatorio
     def DMC(self):
         def surroundingCells(rand_wall):
         	s_cells = 0
         	if (maze[rand_wall[0]-1][rand_wall[1]] == 0):
         		s_cells += 1
         	if (maze[rand_wall[0]+1][rand_wall[1]] == 0):
         		s_cells += 1
         	if (maze[rand_wall[0]][rand_wall[1]-1] == 0):
         		s_cells +=1
         	if (maze[rand_wall[0]][rand_wall[1]+1] == 0):
         		s_cells += 1

         	return s_cells
         
         wall = 1
         cell = 0
         unvisited = 'u'
         height = self.linhas
         width =  self.colunas
         maze = []
         
         for i in range(0, height):
         	line = []
         	for j in range(0, width):
         		line.append(unvisited)
         	maze.append(line)
          
         starting_height = int(random.random()*height)
         starting_width = int(random.random()*width)
         
         if (starting_height == 0):
         	starting_height += 1
         if (starting_height == height-1):
         	starting_height -= 1
         if (starting_width == 0):
         	starting_width += 1
         if (starting_width == width-1):
         	starting_width -= 1
         
         maze[starting_height][starting_width] = cell
         walls = []
         walls.append([starting_height - 1, starting_width])
         walls.append([starting_height, starting_width - 1])
         walls.append([starting_height, starting_width + 1])
         walls.append([starting_height + 1, starting_width])
         
         maze[starting_height-1][starting_width] = 1
         maze[starting_height][starting_width - 1] = 1
         maze[starting_height][starting_width + 1] = 1
         maze[starting_height + 1][starting_width] = 1
         
         while (walls):
         	# Pick a random wall
         	rand_wall = walls[int(random.random()*len(walls))-1]

         	# Check if it is a left wall
         	if (rand_wall[1] != 0):
         		if (maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == 0):
         			# Find the number of surrounding cells
         			s_cells = surroundingCells(rand_wall)

         			if (s_cells < 2):
         				# Denote the new path
         				maze[rand_wall[0]][rand_wall[1]] = 0

         				# Mark the new walls
         				# Upper cell
         				if (rand_wall[0] != 0):
         					if (maze[rand_wall[0]-1][rand_wall[1]] != 0):
         						maze[rand_wall[0]-1][rand_wall[1]] = 1
         					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]-1, rand_wall[1]])


         				# Bottom cell
         				if (rand_wall[0] != height-1):
         					if (maze[rand_wall[0]+1][rand_wall[1]] != 0):
         						maze[rand_wall[0]+1][rand_wall[1]] = 1
         					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]+1, rand_wall[1]])

         				# Leftmost cell
         				if (rand_wall[1] != 0):	
         					if (maze[rand_wall[0]][rand_wall[1]-1] != 0):
         						maze[rand_wall[0]][rand_wall[1]-1] = 1
         					if ([rand_wall[0], rand_wall[1]-1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]-1])
         			

         			# Delete wall
         			for wall in walls:
         				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
         					walls.remove(wall)

         			continue

         	# Check if it is an upper wall
         	if (rand_wall[0] != 0):
         		if (maze[rand_wall[0]-1][rand_wall[1]] == 'u' and maze[rand_wall[0]+1][rand_wall[1]] == 0):

         			s_cells = surroundingCells(rand_wall)
         			if (s_cells < 2):
         				# Denote the new path
         				maze[rand_wall[0]][rand_wall[1]] = 0

         				# Mark the new walls
         				# Upper cell
         				if (rand_wall[0] != 0):
         					if (maze[rand_wall[0]-1][rand_wall[1]] != 0):
         						maze[rand_wall[0]-1][rand_wall[1]] = 1
         					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]-1, rand_wall[1]])

         				# Leftmost cell
         				if (rand_wall[1] != 0):
         					if (maze[rand_wall[0]][rand_wall[1]-1] != 0):
         						maze[rand_wall[0]][rand_wall[1]-1] = 1
         					if ([rand_wall[0], rand_wall[1]-1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]-1])

         				# Rightmost cell
         				if (rand_wall[1] != width-1):
         					if (maze[rand_wall[0]][rand_wall[1]+1] != 0):
         						maze[rand_wall[0]][rand_wall[1]+1] = 1
         					if ([rand_wall[0], rand_wall[1]+1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]+1])

         			# Delete wall
         			for wall in walls:
         				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
         					walls.remove(wall)

         			continue

         	# Check the bottom wall
         	if (rand_wall[0] != height-1):
         		if (maze[rand_wall[0]+1][rand_wall[1]] == 'u' and maze[rand_wall[0]-1][rand_wall[1]] == 0):

         			s_cells = surroundingCells(rand_wall)
         			if (s_cells < 2):
         				# Denote the new path
         				maze[rand_wall[0]][rand_wall[1]] = 0

         				# Mark the new walls
         				if (rand_wall[0] != height-1):
         					if (maze[rand_wall[0]+1][rand_wall[1]] != 0):
         						maze[rand_wall[0]+1][rand_wall[1]] = 1
         					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]+1, rand_wall[1]])
         				if (rand_wall[1] != 0):
         					if (maze[rand_wall[0]][rand_wall[1]-1] != 0):
         						maze[rand_wall[0]][rand_wall[1]-1] = 1
         					if ([rand_wall[0], rand_wall[1]-1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]-1])
         				if (rand_wall[1] != width-1):
         					if (maze[rand_wall[0]][rand_wall[1]+1] != 0):
         						maze[rand_wall[0]][rand_wall[1]+1] = 1
         					if ([rand_wall[0], rand_wall[1]+1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]+1])

         			# Delete wall
         			for wall in walls:
         				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
         					walls.remove(wall)


         			continue

         	# Check the right wall
         	if (rand_wall[1] != width-1):
         		if (maze[rand_wall[0]][rand_wall[1]+1] == 'u' and maze[rand_wall[0]][rand_wall[1]-1] == 0):

         			s_cells = surroundingCells(rand_wall)
         			if (s_cells < 2):
         				# Denote the new path
         				maze[rand_wall[0]][rand_wall[1]] = 0

         				# Mark the new walls
         				if (rand_wall[1] != width-1):
         					if (maze[rand_wall[0]][rand_wall[1]+1] != 0):
         						maze[rand_wall[0]][rand_wall[1]+1] = 1
         					if ([rand_wall[0], rand_wall[1]+1] not in walls):
         						walls.append([rand_wall[0], rand_wall[1]+1])
         				if (rand_wall[0] != height-1):
         					if (maze[rand_wall[0]+1][rand_wall[1]] != 0):
         						maze[rand_wall[0]+1][rand_wall[1]] = 1
         					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]+1, rand_wall[1]])
         				if (rand_wall[0] != 0):	
         					if (maze[rand_wall[0]-1][rand_wall[1]] != 0):
         						maze[rand_wall[0]-1][rand_wall[1]] = 1
         					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
         						walls.append([rand_wall[0]-1, rand_wall[1]])

         			# Delete wall
         			for wall in walls:
         				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
         					walls.remove(wall)

         			continue

         	# Delete the wall from the list anyway
         	for wall in walls:
         		if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
         			walls.remove(wall)
                     
         for i in range(0, height):
         	for j in range(0, width):
         		if (maze[i][j] == 'u'):
         			maze[i][j] = 1

         # Set entrance and exit
         for i in range(0, width):
         	if (maze[1][i] == 0):
         		maze[0][i] = 0
         		break

         for i in range(width-1, 0, -1):
         	if (maze[height-2][i] == 0):
         		maze[height-1][i] = 0
         		break
             
         return maze

         
     def outmap(self) -> object : 
         return self.mapa 
     
     def insert(self,alter : tuple ):
         valor = alter[0]
         self.mapa[alter[1]][alter[2]] = valor
         
         if valor == 1: 
             self.parede+=1
             self.livre -=1
         else: 
             self.livre+=1  
             self.parede-=1
             
#Obtendo as informações da tela
monitors = get_monitors()
largura,altura = monitors[0].width,monitors[0].height 
centro  = (largura/2,altura/2)

#gerando o mapa  a ser alterado
mapa = maze(LINHAS,COLUNAS,Modo,MAPA)
Trow = int(altura/mapa.linhas)
Tcol = int(largura/mapa.colunas)

#iniciando o pygame
pg.init()
ajuste = 1
janela = pg.display.set_mode((ajuste*largura,ajuste*altura))
pg.display.set_caption("Map Creator")
janela.fill(cores['black'])
#icone = pg.image.load("./Logos/mapcreator.png")
#pg.display.set_icon(icone)

def scale(dimensao : int , maximo : int):
    escala = 1
    aux = result = dimensao
    while result < maximo - 10 :
        escala += 1
        result = escala*aux
    return escala

Numtocolor = {
              1 : cores['red'],
              0 : cores['white'],
              2 : cores['green'],
              9 : cores['blue']
                }

def draw(mapa:list,janela:object,escalaR,escalaC,linhas:int,colunas:int):
    janela.fill(cores['black'])
    for i in range(0,linhas*escalaR,escalaR):
        for j in range(0,colunas*escalaC,escalaC):
            COR = Numtocolor[mapa[i//escalaR][j//escalaC]]
            pg.draw.rect(janela,COR,(j+1,i+1,escalaC-1,escalaR-1))
            
def DRAW (maze,mapa) :
   NTrow = int(Trow*ajuste)
   NTcol = int(Tcol*ajuste)
   for i in range(0,int(altura*ajuste),NTrow+1):
       for j in range(0,int(largura*ajuste),NTcol+1):
        pg.draw.rect( janela ,cores['black'],(j ,i , NTcol , NTrow))
        Ncor = cores['red']
        l,c = limitador(maze,int(i/(Trow)),int(j/(Tcol)))
        if mapa[l][c] == 0:
            Ncor = cores['white']
        if mapa[l][c] == 2:
            Ncor = cores['green']
        if mapa[l][c] == 9:
            Ncor = cores['blue']
        pg.draw.rect( janela ,Ncor, (j+1,i+1,NTcol-NTcol/20,NTrow-NTrow/20))


EscalaR = scale(LINHAS  , altura) 
EscalaC = scale(COLUNAS , largura) 

#laço principal
while True:
    if quitecheck(pg.event.get()) == True : 
        pg.quit()
        break
    
    draw(mapa.outmap(),janela,EscalaR,EscalaC,LINHAS,COLUNAS)
    Mouse = pg.mouse.get_pressed(3)
    clicado = (999,999)
    if Mouse[0] == True and clicado[0]!= pg.mouse.get_pos()[0] and clicado[1]!= pg.mouse.get_pos()[1] :
        posicao = clicado = pg.mouse.get_pos()
        linha,coluna = limitador(mapa,int(posicao[1]/(Trow)),int(posicao[0]/(Tcol)))
        test = mapa.mapa[linha][coluna]
        Changed = int(0)
        if test == 0:
            Changed = 1
        mapa.insert((Changed,linha,coluna))
    if Mouse[2] == True and clicado[0]!= pg.mouse.get_pos()[0] and clicado[1]!= pg.mouse.get_pos()[1] :
       posicao = clicado = pg.mouse.get_pos()
       linha,coluna = limitador(mapa,int(posicao[1]/(Trow)),int(posicao[0]/(Tcol)))
       test = mapa.mapa[linha][coluna]
       Changed = 2
       if test == 2:
           Changed = 9 
       mapa.insert((Changed,linha,coluna))
       
    pg.display.update()
try:
    os.mkdir("./Mapas")
except:
    pass
if Modo == "E":
    print(f"Mapa {NOME} Salvo")
    np.save("./Mapas/"+NOME+".npy",mapa.mapa)
else:
    NOME = str(input("Nome do arquivo = ")).strip() + ".npy"
    np.save("./Mapas/"+NOME,mapa.mapa)
