"SCRIPT PRINCIPAL PARA CRIAÇÃO DA TABELA Q"
import os 
import numpy as np
from colordict import ColorDict
cor = ColorDict() 
#Definindo entidades do mapa
parede   = 1
livre    = 0
objetivo = 2
parado   = 9  
#Motivos de interface com usuario
AcaoR = {
        1 : "Direita",
        0 : "Frente" ,
        3 : "Esquerda",
        2 : "Atrás",
        4 : "Parado"
        }
#------------------------------------------------------------------------------ 
class ambiente:
     def __init__(self,path : str):
        self.mapa    = np.load("./Mapas/"+path)
        self.linhas  = int(len(self.mapa))
        self.ultimo    = (0,0,0)            #(linha,coluna,entidade) 
        self.colunas = int(len(self.mapa[:]))
        self.recompensa = { livre:   -1, parede:  -100, objetivo: 100,
                            parado:   -1  }
        self.cores      = { livre:    cor['white'], parede: cor['red'],
                            objetivo: cor['green'], parado: cor['white']}   
     def att_mapa(self,linha,coluna,entidade):
        self.ultimo = (linha,coluna,entidade)  
        self.mapa[linha][coluna] = entidade
#------------------------------------------------------------------------------
class agente:
    #Função que determina a posição inicial e o objetivo do agente    
    def Fambient(self, mapa : list, linhas :int , colunas: int) -> [int,int] :  
        inicio = fim = (0,0)
        for linha in range(0,linhas):
            for coluna in range(0,colunas):
                if mapa[linha][coluna] == objetivo: fim    = (linha,coluna)
                if mapa[linha][coluna] == parado:   inicio = (linha,coluna)
        return inicio,fim
    
    #Função que reinicia as variaveis para condição inicial
    def restart(self) -> None:
        self.Nestado = self.estado = self.inicio
        self.condicoes["impacto"]  = False
        self.condicoes["objetivo"] = False
        self.timeon                = 0 
        
    #Função que decai o epsilon:
    def decair(self) -> None:
        epsilon = self.hp["epsilon"]
        epsilon[0] = epsilon[0] - epsilon[2] 
    #Função que verifica o estado no mapa
    def verificar(self,ambiente : object ) -> None:
        Maxrow = ambiente.linhas
        Maxcol = ambiente.colunas    
        if self.Nestado[0] > Maxrow-1 or self.Nestado[0] < 0:
            self.condicoes["impacto"] = True
            return
        if self.Nestado[1] > Maxcol-1 or self.Nestado[1] < 0:
            self.condicoes["impacto"] = True
            return
        if ambiente.mapa[self.Nestado[0]][self.Nestado[1]] == parede:
            self.condicoes["impacto"] = True
        if ambiente.mapa[self.estado[0]][self.estado[1]] == objetivo:
            self.condicoes["objetivo"] = True
            
    #Função que atualiza o estado
    def att_Estado(self , e :tuple):
        meta = list(e)
        for i in range(0,2): 
         meta[i] = meta[i] + self.acoes[self.acao][i]
        return tuple(meta)
    
    #Função que atualiza a tabela Q    
    def att_TabelaQ(self,ambiente : object) -> None :
        Q,s,a = self.TabelaQ,self.estado,self.acao
        alpha = self.hp["alpha"]
        gamma = self.hp["gamma"]
        ns =    self.Nestado
        check = False
        if ns[0] > ambiente.linhas - 1 or ns[1] > ambiente.colunas - 1:
            R = ambiente.recompensa[parede]
            check = True
        if ns[0] < 0 or ns[1] < 0 : 
            check = True
            R = ambiente.recompensa[parede]
        if check == False:
            R = ambiente.recompensa[ambiente.mapa[ns]]
            
        if self.condicoes["impacto"] == True or self.condicoes["objetivo"] == True:        
            Q [ s ][ a ] = (1 - alpha ) * Q [ s ][ a ] + alpha * R
        else:
            Q [ s ][ a ] = (1-alpha)*Q[s][a] + alpha*(R+gamma*np.max( Q[ns]))
    
    #Politica do agente
    def politica(self) -> None:
        #Exploitation
        if np.random.uniform(0,1) > self.hp["epsilon"][0]:
            self.acao  = np.argmax(self.TabelaQ[self.estado])    
        #Exploration
        else:
           self.acao = np.math.ceil(np.random.randint(0,self.Nacoes))
           
    def __init__(self,ambiente : object,alpha : float ,gamma : float):
        self.acoes = [
        [1, 0],     #Frente
        [0, 1],     #Direita 
        [-1,0],     #Atrás
        [0,-1],     #Esquerda
        [0, 0]      #parado
        ]
        self.Nacoes = len(self.acoes)
        self.episodios = (ambiente.linhas * ambiente.colunas*10)*self.Nacoes
        self.hp = {      #hiperparametros
        "alpha": alpha,  #Taxa de aprendizagem
        "gamma": gamma,  #Taxa de desconto
        "epsilon": [1,(1/self.episodios),(1/self.episodios)] #inicio,min,decay
        }
        self.inicio,self.objetivo = self.Fambient(ambiente.mapa,ambiente.linhas,ambiente.colunas)
        ambiente.att_mapa(self.inicio[0],self.inicio[1],0)
        self.estado = self.inicio
        self.timeon = 0
        self.Nestado = self.inicio
        self.TabelaQ = np.zeros((ambiente.linhas,ambiente.colunas,self.Nacoes),float)
        self.condicoes = {
            "impacto" : False,
            "objetivo": False
            }
        self.acao = 4
#------------------------------------------------------------------------------        
#inicializando as variaveis
ARQUIVO = input("Nome do mapa: ")
ambiente = ambiente(ARQUIVO+".npy")
agente   = agente(ambiente,0.95,0.95)
    
#Treinamento
RUN = True
for episodio in range(1,agente.episodios+1):
    while(RUN == True):
        agente.politica()
        #print(AcaoR[agente.acao])
        #Atualizando o Novo estado
        agente.Nestado = agente.att_Estado(agente.Nestado)
        agente.verificar(ambiente)
        agente.att_TabelaQ(ambiente)
        if agente.condicoes["impacto"] == True:
            agente.restart()
            break
        if agente.condicoes["objetivo"] == True:
            agente.restart()
            break
        agente.estado = agente.Nestado
    agente.decair()

#Solução para o erro de estruturaão do TabelaQ
agente.TabelaQ[agente.objetivo[0]][agente.objetivo[1]][4] = ambiente.recompensa[objetivo]
    
print("TREINAMENTO CONCLUIDO, SALVAR TABELA Q?")
opt = input(" Y - sim / N - nao : ").upper()
if opt  == "Y":
    try:
        os.mkdir("./TabelasQ")
    except:
        pass
    np.save("./TabelasQ/" + ARQUIVO +"Qtable.npy",agente.TabelaQ)
    print("ARQUIVO SALVO")