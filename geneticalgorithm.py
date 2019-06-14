import random
import datetime
import multiprocessing as mp
import matplotlib.pyplot as plt

def ga(func,restrictions,variables_matrix,workers = 100,tipo='maximize',qntd_repeticoes=10000,mutacao = 10,len_populacao=4):
	antes = datetime.datetime.now()
	trabalhadores = [mp.Process(target = geneticalgorithm,args=(func,restrictions,variables_matrix,tipo,len_populacao,mutacao,qntd_repeticoes)) for i in range(workers)]
	for p in trabalhadores: p.start()
	for p in trabalhadores: p.join()
	depoisthread = datetime.datetime.now()
	lista = []
	for i in range(workers):
		lista.append(geneticalgorithm(func,restrictions,variables_matrix,tipo=tipo,qntd_repeticoes = qntd_repeticoes,mutacao = mutacao))
	depoisserie = datetime.datetime.now()
	return((depoisserie-depoisthread).total_seconds(),(depoisthread-antes).total_seconds())

def geneticalgorithm(func,restrictions,variables_matrix,tipo='maximize',len_populacao = 4,mutacao = 10,qntd_repeticoes = 10000):
	populacao = [] 
	#Cria a população inicial
	while len(populacao) < len_populacao:
		try:
			tryout = [variables_matrix[i][random.randint(0,len(variables_matrix[i])*10000)%len(variables_matrix[i])] for i in range(len(variables_matrix))]
			for j in restrictions:
				assert j(tryout)
			#verifica se as restrições permitem a solução gerada
			populacao.append(tryout)
		except:
			pass
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
		parents = selection(genes)

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
	#troca dos genes
	aux[1]['caracteristicas'][posicao],aux[0]['caracteristicas'][posicao] = aux[0]['caracteristicas'][posicao],aux[1]['caracteristicas'][posicao]
	return aux

def selection(genes):
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
	parentA = random.randint(0,best_fo*10000)%best_fo
	parentB = random.randint(0,worse_fo*10000)%worse_fo
	#cria valores randomicos baseado na qualidade da função objetivo dos melhores e piores
	somaA = 0
	somaB = 0
	parents = []
	#escolhe o valor para os pais
	for i in range(len(best)-1,-1,-1):
		if somaA + best[i]['valor'] >= parentA:
			parents.append(best[i])
			break
		somaA = somaA + best[i]['valor']
	for i in range(len(worse)-1,-1,-1):
		if somaB + worse[i]['valor'] >= parentB:
			parents.append(worse[i])
			break
		somaB = somaB + worse[i]['valor']
	return parents

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
#função objetivo
def main(vector):
	x = 0
	for i in vector:
		x = x + i
	return x

#restrição 1
def restriction1(vector):
	return vector[0] >= 2

#restrição 2
def restriction2(vector):
	return vector[2] < 7


if __name__ == '__main__':
	mult = []
	normal = []
	for i in range(10):
		(a,b) = ga(main,[restriction1,restriction2],[[1,2,3,4],[5,6,7],[4,1,2]],tipo='max',len_populacao=4,workers=i*10)
		mult.append(b)
		normal.append(a)
	plt.plot(normal,label='Série')
	plt.plot(mult,label = 'MultiProcessamento')
	plt.ylabel('some numbers')
	plt.show()

