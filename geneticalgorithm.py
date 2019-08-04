import random
import datetime
import matplotlib.pyplot as plt

def geneticalgorithm(func,variables_matrix,restrictions = [],tipo='maximize',permutacao = 50,len_populacao = 4,mutacao = 5,qntd_repeticoes = 1000):
	populacao = [] 
	#Cria a população inicial
	while len(populacao) < len_populacao:
		try:
			tryout = [variables_matrix[i][random.randint(0,len(variables_matrix[i])*10000)%len(variables_matrix[i])] for i in range(len(variables_matrix))]
			for j in restrictions:
				assert j(tryout)
			populacao.append(tryout)
		except:
			pass
		#verifica se as restrições permitem a solução gerada
	genes = []
	#Popula uma lista de dicionários como população
	for i in range(len(populacao)):
		genes.append(dict(valor = func(populacao[i]),nome = str(chr(65+i)),caracteristicas = populacao[i]))

	melhor = dict()
	for i in range(qntd_repeticoes):
		#Ordena os valores da lista populacional baseada no valor da função objetivo
		genes = sortpopulation(genes,tipo)
		if i == 0:
			melhor['valor'] = genes[0]['valor']
			melhor['nome'] = genes[0]['nome']
			melhor['caracteristicas'] = list(genes[0]['caracteristicas'])
		elif melhor['valor'] < genes[0]['valor'] and (tipo == 'max' or tipo == 'maximize'):
			melhor['valor'] = genes[0]['valor']
			melhor['nome'] = genes[0]['nome']
			melhor['caracteristicas'] = list(genes[0]['caracteristicas'])
		elif melhor['valor'] > genes[0]['valor'] and (tipo == 'min' or tipo == 'minimize'):
			melhor['valor'] = genes[0]['valor']
			melhor['nome'] = genes[0]['nome']
			melhor['caracteristicas'] = list(genes[0]['caracteristicas'])
			#print(melhor)
			#define o melhor valor
		#Efetua a seleção natural, um elemento dos 50% melhores e outro dos 50% piores
		parents = selection(genes,permutacao)

		#realiza o crossover, gerando os filhos da população
		correct_cross = False
		while correct_cross == False:
			try:
				cross = crossover(parents)
				for i in cross:
					for j in restrictions:
						assert j(i['caracteristicas'])
					i['valor'] = func(i['caracteristicas'])
				correct_cross = True
			except:
				correct_cross = False

		#verifica se ocorre mutação
		correct_cross = True
		mutation_rate = random.randint(0,100)
		if mutation_rate <= mutacao:
			correct_cross = False
		while correct_cross == False:
			try:
				cross = mutation(cross,variables_matrix)
				for i in cross:
					for j in restrictions:
						assert j(i['caracteristicas'])
					i['valor'] = func(i['caracteristicas'])
				correct_cross = True
			except:
				correct_cross = False

		#realoca os filhos no lugar dos pais
		for i in range(len(genes)):
			for j in range(len(cross)):
				if genes[i]['nome'] == cross[j]['nome']:
					genes[i] = cross[j]
	return melhor

def mutation(genes,variables_matrix):
	#escolhe o filho com um número randômico
	filho = random.randint(0,len(genes)*10000)%len(genes)
	#escolhe o gene a ser mutado
	gene = random.randint(0,len(variables_matrix)*10000)%len(variables_matrix)
	#escolhe o valor para substituir o gene
	valor = random.randint(0,len(genes[filho])*10000)%len(genes[filho])
	#altera o valor
	genes[filho]['caracteristicas'][gene] = variables_matrix[gene][valor]
	return genes

def crossover(genes):
	aux = list(genes)
	len_caracteristicas = len(aux[0]['caracteristicas'])
	#escolhe o gene para ser trocado randomicamente
	posicao = random.randint(0,len_caracteristicas*10000)%len_caracteristicas
	for i in range(int(len(aux)/2)):
		#troca dos genes
		aux[i]['caracteristicas'][posicao],aux[int((i+(len(aux)/2))-1)]['caracteristicas'][posicao] = aux[int((i+(len(aux)/2))-1)]['caracteristicas'][posicao],aux[i]['caracteristicas'][posicao]
	return aux

def selection(genes,permutacao):
	best = []
	best_fo = 0
	worse = []
	worse_fo = 0
	#percorre os 50% melhores elementos da população
	for i in range(int(len(genes)/2)):
		best.append(genes[i])
		best_fo = best_fo + genes[i]['valor']
	#percorre os 50% piores elementos da população
	for i in range(int(len(genes)/2),len(genes)):
		worse.append(genes[i])
		worse_fo = worse_fo + genes[i]['valor']
	parentB = []
	parentW = []
	aux = int(len(best)*permutacao/100)
	for i in range(aux):
		parentB.append(random.randint(0,int(best_fo*10000))%oneifzero(best_fo))
		parentW.append(random.randint(0,int(worse_fo*10000))%oneifzero(worse_fo))
	#cria valores randomicos baseado na qualidade da função objetivo dos melhores e piores
	somaA = 0
	somaB = 0
	parents = []
	for i in parentB:
		parents.append(position(best,i))
	for i in parentW:
		parents.append(position(worse,i))
	return parents

def oneifzero(val):
	if val == 0:
		return 1
	return val

def sortpopulation(genes,tipo):
	#ordena a população baseada no valor
	if tipo == 'maximize' or tipo == 'max':
		aux = list(genes)
		for i in range(len(aux)):
			for j in range(len(aux)):
				if aux[i]['valor'] > aux[j]['valor']:
					aux[i],aux[j] = aux[j],aux[i]
		return aux
	elif tipo == 'minimize' or tipo == 'min':
		aux = list(genes)
		for i in range(len(aux)):
			for j in range(len(aux)):
				if aux[i]['valor'] < aux[j]['valor']:
					aux[i],aux[j] = aux[j],aux[i]
		return aux

#Retorna a posição do elemento baseado no valor gerado para a soma da função objetivo
def position(genes,val):
	soma_genes = 0
	for i in genes:
		soma_genes = soma_genes + i['valor']
		if val <= soma_genes:
			return dict(i)

#função objetivo
def main(vector):
	return 6*vector[0]+5*vector[1]

#restrição 1
def restriction1(vector):
	return vector[0] + vector[1] <= 5

#restrição 2
def restriction2(vector):
	return 3*vector[0] + 2*vector[1] <= 12


if __name__ == '__main__':
	vect = [[i for i in range(100)] for j in range(2)]
	a = geneticalgorithm(main,vect,[restriction1,restriction2],tipo='max',len_populacao=50)
	print(a)




