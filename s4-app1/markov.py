import random


def get_markov_from_unigram(gram_list, length):
    text = ""

    for i in range(length):
        prob = random.random()
        # print("prob =", prob)
        prob_tot = 0
        for j in range(len(gram_list)):
            gram = next(iter(gram_list[j]))
            # print("gram =", gram)
            prob_tot += gram_list[j][gram]
            # print("prob_tot=", prob_tot)
            if prob_tot > prob:
                text += gram + " "
                break

    return text


class Node:
    def __init__(self, word, prob):
        self.word = word
        self.probability = prob


def get_graph_from_bigram(bigram_list):
    graph_dict = {}
    for bigram_dict in bigram_list:
        bigram = next(iter(bigram_dict))
        first_word = bigram.split()[0]
        second_word = bigram.split()[1]
        # print(bigram)
        node = Node(second_word, bigram_dict[bigram])
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


def get_markov_from_bigram_graph(graph_dict, length):
    text = ""
    first_word = next(iter(graph_dict))

    next_word = first_word
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

    return text
