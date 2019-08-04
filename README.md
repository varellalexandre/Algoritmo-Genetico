# Otimização

Os problemas de otimização possuem diversas correntes de solução. Problemas de Programação Linear, Inteira e Inteira mista podem ser solucionados pelo Simplex, um algoritmo que utiliza operações matriciais para encontrar a solução que tem melhor qualidade para a função objetivo do problema. 
No entanto, as soluções exatas de problemas de otimização com o uso do simplex, podem ser muito demoradas e tornarem do tipo NP, para esses casos são usados mecanismos de solução que podem encontrar Minimos/Máximos globais porém que focam em encontrar Minimos/Máximos locais.
Nesse tipo de solução se enquadram as meta-heurísticas e as heurísticas, um exemplo de meta-heurística é o algoritmo genético e de heuristica a solução do problema do K-means.

## Algoritmo Genético

Nessa função criada nesse repositório, é possível realizar o processo de otimização por algoritmo genético. 

![alt desc](https://images.slideplayer.com/16/5034354/slides/slide_1.jpg)
Imagem retirada de https://images.slideplayer.com/16/5034354/slides/slide_1.jpg 

### Fases

#### Seleção

A seleção é realizada, escolhendo os melhores e piores de uma população de soluções. Na função é passada o percentual de permutação que deve acontecer na seleção. São escolhidos uma quantidade X de elementos dos melhores elementos e dos piores elementos.

#### Crossover

O crossover permite permultar características dos pais escolhidos na seleção, e em seguida criar filhos com a alternancia dessas características.

#### Mutação

A mutação é o fenômeno que permite que um indivíduo tenha uma característica própria alterada. Com isso é possível que uma população varie não só internamente.

## Exemplo
Um exemplo pode ser demonstrado para a função 

MAX 6X+5Y
st.
X+Y<=5
3X+2Y<=12

X>=0
Y>=0
(X,Y) Contidos nos Inteiros

problema retirado de 
https://www.analyticsvidhya.com/blog/2017/02/lintroductory-guide-on-linear-programming-explained-in-simple-english/

### Código
O problema pode ser descrito pelas equações abaixo
```python
#função objetivo
def objetivo(vector):
	return 6*vector[0]+5*vector[1]

#restrição 1
def r1(vector):
	return vector[0] + vector[1] <= 5

#restrição 2
def r2(vector):
	return 3*vector[0] + 2*vector[1] <= 12

```

Agora usando o algoritmo genético para resolve-la, tem-se
```python
if __name__ == '__main__':
	vect = [[i for i in range(100)] for j in range(2)]
	a = geneticalgorithm(objetivo,vect,[r1,r2],tipo='max',len_populacao=50)
	print(a)

```
![alt resposta](https://i.imgsafe.org/69/69472b2e18.png)