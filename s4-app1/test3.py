import copy
import os
import time
import codecs
import math
from sorting import quick_sort_dict, merge_sort_dict
from markov import get_graph_from_bigram, get_markov_from_bigram_graph, get_markov_from_unigram


class Author:
    def __init__(self, name, unigram_dict, unigram_sorted, bigram_dict, bigram_sorted):
        self.name = name
        self.unigram_dict = unigram_dict
        self.unigram_sorted = unigram_sorted
        self.bigram_dict = bigram_dict
        self.bigram_sorted = bigram_sorted


def scrape_folder_init(path, author_list, save_to_txt):
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
                    word_list = read_word_list_from_text(text_path)
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

            print(time.time() - tm)

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


def scrape_folder(path, author_list):
    for author in os.listdir(path):
        if author != ".DS_Store":
            tm = time.time()
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
            print(time.time() - tm)

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


def read_word_list_from_text(path):
    word_list = []
    with codecs.open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for word in line.split():
                word = word.lower()
                word_list.append(word)
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
        word = key.rstrip()
        xl_value = 0
        if word in xl_gram.keys():
            common_words += 1
            xl_value = xl_gram[word]
            #print(sm_gram[key] , " ", xl_value)
        distance += abs(sm_gram[key] - xl_value) / (sm_gram[key] + xl_value)
    #print("common_words = ", common_words)
    return distance / common_words


def main():
    path = "./sorted"
    init_path = "./TextesPourEtudiants"
    validation_path = "./TextesPourAutoValidation"

    # ------------------ authors --------------------------
    print("---------------------parsing mystery texts")
    mystery_author_list = []
    scrape_folder_init(validation_path, mystery_author_list, False)

    print("-------------------parsing author texts")
    author_list = []
    scrape_folder(path, author_list)

    # print("---------------------markov chain")
    # for author in author_list:
    #     print(author.name, " ----")
    #     print("markov unigram")
    #     text = get_markov_from_unigram(author.unigram_sorted, 20)
    #     print(text)
    #     print("markov bigram")
    #     graph = get_graph_from_bigram(author.bigram_sorted)
    #     text = get_markov_from_bigram_graph(graph, 20)
    #     print(text)

    for i in range(len(mystery_author_list)):
        print("finding author of mystery text", mystery_author_list[i].name)
        #print("small dict length =", len(mystery_author_list[i].unigram_dict))
        minimum = 10000000000
        mystery_author = "???"
        for author in author_list:

            distance = get_distance_between_n_gram(mystery_author_list[i].unigram_dict, author.unigram_dict)
            # print(author.name, " ----")
            # print(distance)
            if distance < minimum:
                minimum = distance
                mystery_author = author.name
        print(mystery_author)
        print(minimum)

if __name__ == "__main__":
    main()
