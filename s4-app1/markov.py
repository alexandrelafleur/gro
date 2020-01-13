import random


class Node:
    def __init__(self, word, prob):
        self.word = word
        self.probability = prob


def get_markov_from_unigram(author, length):
    text = author.name + " :: Debut:"
    gram_list = author.unigram_sorted
    for i in range(length):
        prob = random.random()
        prob_tot = 0
        for j in range(len(gram_list)):
            gram = next(iter(gram_list[j]))
            prob_tot += gram_list[j][gram]
            if prob_tot > prob:
                text += gram + " "
                break

    return text + author.name + " :: Fin"


def get_graph_from_bigram(bigram_list):
    graph_dict = {}
    for bigram_dict in bigram_list:
        bigram_key = next(iter(bigram_dict))
        first_word = bigram_key.split()[0]
        second_word = bigram_key.split()[1]
        # print(bigram_key)
        node = Node(second_word, bigram_dict[bigram_key])
        # print(node.probability)
        if first_word not in graph_dict.keys():
            graph_dict[first_word] = [node]
        else:
            graph_dict[first_word].append(node)

    for element in graph_dict:
        list_word = graph_dict[element]
        total = 0
        for node in list_word:
            total += node.probability

        for node in list_word:
            node.probability /= total

    return graph_dict


def get_markov_from_bigram_graph(author, length):
    text = author.name + " :: Debut:"
    graph_dict = get_graph_from_bigram(author.bigram_sorted)
    first_word_key = next(iter(graph_dict))

    next_word = first_word_key
    for i in range(length):
        word_list = graph_dict[next_word]
        prob = random.random()
        prob_tot = 0
        for node in word_list:
            prob_tot += node.probability
            if prob_tot > prob:
                text += node.word + " "
                next_word = node.word
                break

    return text + author.name + " :: Fin"
