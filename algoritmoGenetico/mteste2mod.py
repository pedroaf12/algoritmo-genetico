import random

POP_SIZE = 500                                      #Número de quantos Cromossomos que haverá na população
MUT_RATE = 0.1                                      #Probabilidade de um caractere mudar na mutação
TARGET = 'o rato roeu a roupa do rei'               #Objetivo da 'evolução'        
GENES = ' abcdefghijklmnopqrstuvwxyz'               #Possíveis caracteres que um cromossomo podem ter

def initialize_pop(TARGET):
    population = list()                             #Lista vazia para guardar os cromossomos da população                          
    tar_len = len(TARGET)                           #Tamanho de cada cromossomo vai ter na população           

    for i in range(POP_SIZE):                       #LOOP que executa para cada cromossomo    
        temp = list()                               #Lista temporaria para o cromossomo   
        for j in range(tar_len):                    #LOOP que executa para cada caractere do cromossomo
            temp.append(random.choice(GENES))       #Preenche o cromossomo      
        population.append(temp)                     #Agora guarda o cromossomo que fará parte da população inicial

    return population
#VER AQUI---------------------------------------------------------------------------------------------------------------------------------------------------
def crossover_uniform(selected_chromo, CHROMO_LEN, population):         #Crossover uniforme
    offspring_cross = []                                                #Lista para armazenar os novos decendentes
    for _ in range(POP_SIZE):                                           #loop para gerar a nova popupação de descecndentes
        parent1 = random.choice(selected_chromo)                    #"Pai" da lista dos selecionados
        parent2 = random.choice(population[:int(POP_SIZE*0.5)])     #"Pai" da primeira medade da população

        p1 = parent1[0]                                             #Considera só o cromossomo, sem o fitness
        p2 = parent2[0]                                             #Assim 2 cromossomos são escolhidos


        child = []                                                  #Usa para colocar os descendentes da atual iteração do loop
        for i in range(CHROMO_LEN):
            child.append(random.choice([p1[i], p2[i]]))             #Aleatoriamente, em cada posição do filho um gene de um dos pais 
                                                                    #é selecionado
        offspring_cross.append(child)
    return offspring_cross
#-----------------------------------------------------------------------------------------------------------------------------------------------------------


def crossover(selected_chromo, CHROMO_LEN, population):             #Crossover simples ponto
    offspring_cross = []                                            #Lista para armazenar os novos decendentes
    for i in range(int(POP_SIZE)):
        parent1 = random.choice(selected_chromo)                #"Pai" da lista dos selecionados
        parent2 = random.choice(population[:int(POP_SIZE*50)])  #"Pai" da primeira medade da população

        p1 = parent1[0]                                         #Considera só o cromossomo, sem o fitness
        p2 = parent2[0]                                         #Assim 2 cromossomos são escolhidos

        crossover_point = random.randint(1, CHROMO_LEN-1)       #Escolhe qual ponto do cromossomo sera dividido
        child =  p1[:crossover_point] + p2[crossover_point:]    #"Filho"= metade p1, e metade final de p2
        offspring_cross.extend([child])                         #Add a lista de decendentes
    return offspring_cross
#VER AQUI---------------------------------------------------------------------------------------------------------------------------------------------------
def mutate_invert(offspring, MUT_RATE):                         #Mutação de inversão (Para o mini teste 2)
    mutated_offspring = []                                      #Lista para os descendentes mutados

    for arr in offspring:                                       #Loop para avaliar cada cromossomo da pupolação de descendentes por vez
        if random.random() < MUT_RATE:                          #Se o número gerado aleatoriamente for menor que MUT_RATE haverá mutação no cromossomo    
            start = random.randint(0, len(arr) - 2)             #Seleciona um ponto inicial para inversão, garantindo sobre pelo menos dois 
                                                                #elementos a mais para ser invertido
            end = random.randint(start + 1, len(arr) - 1)       #Seleciona o ponto final da inversão considerando a partir do ponto inicial           
            arr[start:end] = reversed(arr[start:end])           #Inverte a area entre o ponto de inicio e de fim                                         
        mutated_offspring.append(arr)                           #Add o cromossomo mutado ou na na lista da nova população
    return mutated_offspring                 
                   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
def mutate(offspring, MUT_RATE):                                #Mutação pontual
    mutated_offspring = []                                      #Lista para os descendentes mutados

    for arr in offspring:                                       
        for i in range(len(arr)):
            if random.random() < MUT_RATE:                      #valor aleatório, se menor que mut-rate ocorre mutação
                arr[i] = random.choice(GENES)                   #Substitui o gene mutado por um da lista de genes 
        mutated_offspring.append(arr)                           #Add o cromossomo mutado ou n na lista de mutados  
    return mutated_offspring

#VER AQUI---------------------------------------------------------------------------------------------------------------------------------------------------
def selecao_torneio(populacao, TARGET, k, num_selecionados):
    individuos_selecionados = []
    
    while len(individuos_selecionados) < num_selecionados:
        # o primeiro passo e selecionar k indivíduos da populacao
        torneio = random.sample(populacao, k)
        
        # calula a aptidao de cada cromossomo selecionado para o torneio, criando uma lista de pares
        aptidao_torneio = [fitness_cal(TARGET, cromossomo) for cromossomo in torneio]
        
        # retorna o individuo com a melhor aptidao, ou seja a menor
        vencedor = min(aptidao_torneio, key=lambda x: x[1])
        
        # adiciona o cromossomo do vencedor do torneio aos selecionados
        individuos_selecionados.append(vencedor[0])

        # isso e repetido ate que o numero desejado de individuos seja selecionado

    return individuos_selecionados
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def selection(population, TARGET):                              #Seleção Elitista      
    sorted_chromo_pop = sorted(population, key= lambda x: x[1]) #Ordena a polulação por aptidão de cada cromossomo
    return sorted_chromo_pop[:int(0.5*POP_SIZE)]        #Já que os "melhores" agora tão no começo da lista
                                                        #Divide em dois a lista e retorna só a metade a com os "melhores"
                                                        #Divide pela metade a população

def fitness_cal(TARGET, chromo_from_pop):                       
    difference = 0                                              #Num de diferenças do cromo com alvo                             
    for tar_char, chromo_char in zip(TARGET, chromo_from_pop):  #zip junta os carac deles em pares
        if tar_char != chromo_char:                             #verifica se são diferentes(genes)
            difference+=1                               
    
    return [chromo_from_pop, difference]                    

def replace(new_gen, population):
    for _ in range(len(population)):
        if population[_][1] > new_gen[_][1]:                    #Compara a população inicial com a pupulação mutada 
          population[_][0] = new_gen[_][0]                      #Se a mutada tiver um fitness melhor
          population[_][1] = new_gen[_][1]                      #Vai substituir a população anterior
    return population

def main(POP_SIZE, MUT_RATE, TARGET, GENES):
    # 1) initialize population
    initial_population = initialize_pop(TARGET)    #Cria a primeira população(Inicial)
    found = False                                  #Variável para controle de parada quando encontrar o TARGET
    population = []      #Lista [[cromossomo], fitness]                         
    generation = 1
    k = 5

    # 2) Calculating the fitness for the current population
    for _ in range(len(initial_population)):        #Vai passar cada cromossomos da população pelo "teste" de fitness
        population.append(fitness_cal(TARGET, initial_population[_]))   

    # now population has 2 things, [chromosome, fitness]
    # 3) now we loop until TARGET is found
    while not found:

      # 3.1) select best people from current population
      selected = selecao_torneio(population, TARGET, k, 50)          #Lista selected[[cromossomo], fitness] cromossomos selecionados

      # 3.2) mate parents to make new generation
      population = sorted(population, key= lambda x:x[1])
      crossovered = crossover_uniform(selected, len(TARGET), population)
            
      # 3.3) mutating the childeren to diversfy the new generation
      mutated = mutate_invert(crossovered, MUT_RATE)

      new_gen = []
      for _ in mutated:                             #Será feito o fitness na nova população de descendentes
          new_gen.append(fitness_cal(TARGET, _))

      # 3.4) replacement of bad population with new generation
      # we sort here first to compare the least fit population with the most fit new_gen

      population = replace(new_gen, population)

      
      if (population[0][1] == 0):           #Verifica se o melhor cromossomo é igual ao Target
        print('Target found')
        print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
        break
      print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
      generation+=1

main(POP_SIZE, MUT_RATE, TARGET, GENES)
