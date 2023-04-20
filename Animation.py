from time import sleep
from colordict import ColorDict
import numpy  as np
import pygame as pg
from screeninfo import get_monitors
monitors = get_monitors()
largura,altura = monitors[0].width,monitors[0].height 

#função que move o agente segundo a tabela Q
def agente(TabelaQ: object , estado : tuple):
    l,c = ((estado[0]+1)*EscalaR)-EscalaR/2,((estado[1]+1)*EscalaC)-EscalaC/2
    pg.draw.circle(janela, cor['yellow'],(c,l), (EscalaC+EscalaR)//10)
    Imax = np.argmax(TabelaQ[estado[0]][estado[1]])
    Amax = ACOES[Imax]
    aux = list(estado)
    new = list()
    for i in range(len(estado)):
     new.append(aux[i] + Amax[i])
    return tuple(new)
    
#função que pega a escala adequada para tela
def scale(dimensao : int , maximo : int):
    escala = 1
    aux = result = dimensao
    while result < maximo - 100:
        escala += 1
        result = escala*aux
    return escala

#função que define a posição inicial do agente no ambiente
def Ainicio(mapa : list, linhas :int , colunas: int) -> tuple:  
    inicio = (0,0)
    for linha in range(0,linhas):
        for coluna in range(0,colunas):
            if mapa[linha][coluna] == 9:   inicio = (linha,coluna)
    return inicio

#função que desenha a grade 
def draw(mapa:list,janela:object,escalaR,escalaC,linhas:int,colunas:int):
    janela.fill(cor['black'])
    for i in range(0,linhas*escalaR,escalaR):
        for j in range(0,colunas*escalaC,escalaC):
            COR = Numtocolor[mapa[i//escalaR][j//escalaC]]
            pg.draw.rect(janela,COR,(j+1,i+1,escalaC-1,escalaR-1))
    

#função com proposito estetico
def quitecheck(test : object) -> bool :
    for event in test:
        if event.type == pg.QUIT:
            return True
    return False 

#Variaveis iniciais
cor = ColorDict()
Numtocolor = {
              1 : cor['red'],
              0 : cor['white'],
              2 : cor['green'],
              9 : cor['blue']
                }
NOME = input("Nome do mapa: ")
Mapa = np.load("./Mapas/" + NOME + ".npy" )
LINHAS  = len(Mapa)
COLUNAS = len(Mapa[:]) 
QNOME = NOME + "Qtable.npy"
TabelaQ = np.load("./TabelasQ/"+QNOME)

#variaveis de referência
ACOES = [
[1, 0],     #Frente
[0, 1],     #Direita 
[-1,0],     #Atrás
[0,-1],     #Esquerda
[0, 0]      #parado
]
NACOES = len(ACOES)
Estado = INICIO = Ainicio(Mapa , LINHAS , COLUNAS)

#variaveis da animação
EscalaR = scale(LINHAS ,altura) 
EscalaC = scale(COLUNAS,largura) 
pg.init()
janela = pg.display.set_mode((COLUNAS*EscalaC,LINHAS*EscalaR))
pg.display.set_caption("Animação")

while True:
    sleep(0.35)
    if quitecheck(pg.event.get()) == True : 
        pg.quit()
        break
    draw(Mapa,janela,EscalaR,EscalaC,LINHAS,COLUNAS)
    Estado = agente(TabelaQ,Estado)
    pg.display.flip()
    