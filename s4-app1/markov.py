import argparse
import codecs
import glob
import os
import time
from random import random

PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]


class Node:
    def __init__(self, word, prob):
        self.word = word
        self.probability = prob


class Author:
    def __init__(self, name, unigram_dict, unigram_sorted, bigram_dict, bigram_sorted):
        self.name = name
        self.unigram_dict = unigram_dict
        self.unigram_sorted = unigram_sorted
        self.bigram_dict = bigram_dict
        self.bigram_sorted = bigram_sorted


def merge_sort_dict(list_init):
    ldl = []
    for num in list_init:
        ldl.append([num])

    while True:
        for i in range(int(len(ldl) / 2)):
            gauche = ldl[i]
            droite = ldl[i + 1]
            merged = []
            ldl.pop(i)
            ldl.pop(i)
            i_gauche = 0
            l_gauche = len(gauche)
            i_droite = 0
            l_droite = len(droite)

            is_merged = False
            while not is_merged:

                if i_gauche >= l_gauche and i_droite >= l_droite:
                    is_merged = True

                elif i_gauche >= l_gauche:
                    merged.append(droite[i_droite])
                    i_droite += 1

                elif i_droite >= l_droite:
                    merged.append(gauche[i_gauche])
                    i_gauche += 1

                elif gauche[i_gauche][next(iter(gauche[i_gauche]))] >= droite[i_droite][next(iter(droite[i_droite]))]:
                    merged.append(gauche[i_gauche])
                    i_gauche += 1

                else:
                    merged.append(droite[i_droite])
                    i_droite += 1

            ldl.insert(i, merged)
            if len(ldl) == 1:
                return ldl[0]


def scrape_folder_init(path, author_list, save_to_txt, remove_ponc):
    for author in os.listdir(path):
        if author != ".DS_Store":
            tm = time.time()
            print(author)
            author_path = path + "/" + author
            gram_dict_list = [None, {}, {}]
            sorted_gram_list = [None, [], []]
            word_count = 0
            for text in os.listdir(author_path):
                if text != ".DS_Store":
                    print(text)
                    text_path = author_path + "/" + text
                    word_list = read_word_list_from_text(text_path, remove_ponc)
                    word_count += len(word_list)

                    for i in range(1, 3):
                        get_n_gram_from_word_list(word_list, i, gram_dict_list[i])

            inv_word_count = 1 / word_count
            for i in range(1, 3):

                unsorted_gram = []
                for key in gram_dict_list[i]:
                    gram_dict_list[i][key] *= inv_word_count
                    unsorted_gram.append({key: gram_dict_list[i][key]})
                sorted_gram_list[i] = merge_sort_dict(unsorted_gram)

            if save_to_txt:
                with codecs.open("./sorted/" + author + "/unigram_sorted.txt", "w+", encoding="utf-8",
                                 errors="ignore") as f:
                    for dict in sorted_gram_list[1]:
                        key = next(iter(dict))
                        f.write(key + " " + str(dict[key]))
                        f.write("\n")

                with codecs.open("./sorted/" + author + "/bigram_sorted.txt", "w+", encoding="utf-8",
                                 errors="ignore") as f:
                    for dict in sorted_gram_list[2]:
                        key = next(iter(dict))
                        f.write(key + " " + str(dict[key]))
                        f.write("\n")

            author_list.append(
                Author(author, gram_dict_list[1], sorted_gram_list[1], gram_dict_list[2], sorted_gram_list[2]))


def scrape_author_folder(path, save_to_txt, remove_ponc):
    author_list = []
    for author in os.listdir(path):
        if author != ".DS_Store":
            print(author)
            author_path = path + "/" + author
            gram_dict_list = [None, {}, {}]
            sorted_gram_list = [None, [], []]
            word_count = 0
            for text in os.listdir(author_path):
                if text != ".DS_Store":
                    print(text)
                    text_path = author_path + "/" + text
                    word_list = read_word_list_from_text(text_path, remove_ponc)
                    word_count += len(word_list)

                    for i in range(1, 3):
                        get_n_gram_from_word_list(word_list, i, gram_dict_list[i])

            inv_word_count = 1 / word_count
            for i in range(1, 3):

                unsorted_gram = []
                for key in gram_dict_list[i]:
                    gram_dict_list[i][key] *= inv_word_count
                    unsorted_gram.append({key: gram_dict_list[i][key]})
                sorted_gram_list[i] = merge_sort_dict(unsorted_gram)

            if save_to_txt:
                with codecs.open("./sorted/" + author + "/unigram_sorted.txt", "w+", encoding="utf-8",
                                 errors="ignore") as f:
                    for dict in sorted_gram_list[1]:
                        key = next(iter(dict))
                        f.write(key + " " + str(dict[key]))
                        f.write("\n")

                with codecs.open("./sorted/" + author + "/bigram_sorted.txt", "w+", encoding="utf-8",
                                 errors="ignore") as f:
                    for dict in sorted_gram_list[2]:
                        key = next(iter(dict))
                        f.write(key + " " + str(dict[key]))
                        f.write("\n")

            author_list.append(
                Author(author, gram_dict_list[1], sorted_gram_list[1], gram_dict_list[2], sorted_gram_list[2]))
    return author_list


def scrape_single_author(path, author_name, remove_ponc):
    author_path = path + "/" + author_name
    gram_dict_list = [None, {}, {}]
    sorted_gram_list = [None, [], []]
    word_count = 0
    for text in os.listdir(author_path):
        if text != ".DS_Store":
            print(text)
            text_path = author_path + "/" + text
            word_list = read_word_list_from_text(text_path, remove_ponc)
            word_count += len(word_list)

            for i in range(1, 3):
                get_n_gram_from_word_list(word_list, i, gram_dict_list[i])

    inv_word_count = 1 / word_count
    for i in range(1, 3):

        unsorted_gram = []
        for key in gram_dict_list[i]:
            gram_dict_list[i][key] *= inv_word_count
            unsorted_gram.append({key: gram_dict_list[i][key]})
        sorted_gram_list[i] = merge_sort_dict(unsorted_gram)

    return [Author(author_name, gram_dict_list[1], sorted_gram_list[1], gram_dict_list[2], sorted_gram_list[2])]


def scrape_mystery_file_old(path, remove_ponc):
    gram_dict_list = [None, {}, {}]
    sorted_gram_list = [None, [], []]
    word_count = 0

    word_list = read_word_list_from_text(path, remove_ponc)
    word_count += len(word_list)

    for i in range(1, 3):
        get_n_gram_from_word_list(word_list, i, gram_dict_list[i])

    inv_word_count = 1 / word_count
    for i in range(1, 3):

        unsorted_gram = []
        for key in gram_dict_list[i]:
            gram_dict_list[i][key] *= inv_word_count
            unsorted_gram.append({key: gram_dict_list[i][key]})
        sorted_gram_list[i] = merge_sort_dict(unsorted_gram)

    return Author("Mystery", gram_dict_list[1], sorted_gram_list[1], gram_dict_list[2], sorted_gram_list[2])


def scrape_mystery_file(path, remove_ponc):
    gram_dict_list = [{}, {}]
    sorted_gram_list = [[], []]

    word_list = read_word_list_from_text(path, remove_ponc)
    word_count = len(word_list)

    get_n_gram_from_word_list(word_list, 1, gram_dict_list[0])
    get_n_gram_from_word_list(word_list, 2, gram_dict_list[1])

    inv_word_count = 1 / word_count
    for i in range(0, 2):

        unsorted_gram = []
        for key in gram_dict_list[i]:
            gram_dict_list[i][key] *= inv_word_count
            unsorted_gram.append({key: gram_dict_list[i][key]})
        sorted_gram_list[i] = merge_sort_dict(unsorted_gram)

    return Author("Mystery", gram_dict_list[0], sorted_gram_list[0], gram_dict_list[1], sorted_gram_list[1])


def scrape_folder(path, author_list):
    for author in os.listdir(path):
        if author != ".DS_Store":
            print(author)
            author_path = path + "/" + author
            gram_dict_list = [None, {}, {}]
            sorted_gram_list = [None, [], []]
            sorted_gram_list[1] = read_from_sorted_list(author_path + "/unigram_sorted.txt")
            for dict in sorted_gram_list[1]:
                gram_dict_list[1].update(dict)
            sorted_gram_list[2] = read_from_sorted_list(author_path + "/bigram_sorted.txt")
            for dict in sorted_gram_list[2]:
                gram_dict_list[2].update(dict)

            author_list.append(
                Author(author, gram_dict_list[1], sorted_gram_list[1], gram_dict_list[2], sorted_gram_list[2]))


def read_from_sorted_list(path):
    sorted_list = []
    with codecs.open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            words = line.split()
            if len(words) > 2:
                sorted_list.append({words[0] + " " + words[1]: float(words[2])})
            else:
                sorted_list.append({words[0]: float(words[1])})

    return sorted_list


def read_word_list_from_text(path, remove_ponc):
    word_list = []
    with codecs.open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for word in line.split():
                word = word.lower()
                if remove_ponc:
                    remixed_word = ""
                    for letter in word:
                        if letter not in PONC:
                            remixed_word += letter
                else:
                    remixed_word = word
                word_list.append(remixed_word)
    return word_list


def get_n_gram_from_word_list(word_list, n, gram_dict):
    for i in range(len(word_list) - n + 1):
        gram = ""
        for j in range(i, i + n):
            gram += word_list[j] + " "
        if gram not in gram_dict.keys():
            gram_dict[gram] = 1
        else:
            gram_dict[gram] += 1


def get_distance_between_n_gram(sm_gram, xl_gram):
    distance = 0
    common_words = 0
    for key in sm_gram:
        word = key
        xl_value = 0
        if word in xl_gram.keys():
            common_words += 1
            xl_value = xl_gram[word]
        distance += abs(sm_gram[key] - xl_value) / (sm_gram[key] + xl_value)
    return distance / common_words


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
        node = Node(second_word, bigram_dict[bigram_key])
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


def main():
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A', help='Use all authors')
    args = parser.parse_args()

    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = glob.glob(rep_aut + "/*")

    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

    if args.d:
        author_path = "./" + args.d
    else:
        author_path = "./" + "TextesPourEtudiants"

    # author_path = rep_aut
    author_name = "Voltaire"
    find_mystery_author = False
    mystery_text_name = ""
    generate_text_markov = False
    markov_length = 0
    markov_file_name = ""
    use_unigrams = True
    print_n_element_in_list = False
    list_index = 0

    if args.a:
        author_name = args.a
        analyse_all_authors = False
    else:
        analyse_all_authors = True

    if args.f:
        find_mystery_author = True
        mystery_text_name = args.f

    if args.m:
        use_unigrams = (args.m == 1)

    if args.F or args.F == 0:
        print_n_element_in_list = True
        list_index = args.F

    if args.G:
        generate_text_markov = True
        markov_length = args.G

    if analyse_all_authors:
        author_list = scrape_author_folder(author_path, False, remove_ponc)
    else:
        author_list = scrape_single_author(author_path, author_name, remove_ponc)

    if find_mystery_author:
        mystery_author = scrape_mystery_file(mystery_text_name + ".txt", remove_ponc)
        minimum = 10000000000
        found_author = "???"
        for author in author_list:
            distance = get_distance_between_n_gram(mystery_author.unigram_dict, author.unigram_dict)
            if distance < minimum:
                minimum = distance
                found_author = author.name
            print(found_author, " ", minimum)

    if print_n_element_in_list:
        for author in author_list:
            print(author.name)
            if use_unigrams:
                if list_index < len(author.unigram_sorted):
                    print(author.unigram_sorted[list_index])
                else:
                    print("index is way too high you need to cut it")
            else:
                if list_index < len(author.bigram_sorted):
                    print(author.bigram_sorted[list_index])
                else:
                    print("index is way too high you need to cut it")

    if generate_text_markov:
        for author in author_list:
            if use_unigrams:
                text = get_markov_from_unigram(author, markov_length)
            else:
                text = get_markov_from_bigram_graph(author, markov_length)

            print(text)


if __name__ == "__main__":
    main()
