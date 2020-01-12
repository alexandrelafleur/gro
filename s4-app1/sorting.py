import time
import random


def merge_sort_dict_old(list_init):
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

            is_merged = False
            while not is_merged:

                if not gauche and not droite:
                    is_merged = True

                elif not gauche:
                    merged.append(droite[0])
                    droite.pop(0)

                elif not droite:
                    merged.append(gauche[0])
                    gauche.pop(0)

                elif gauche[0][next(iter(gauche[0]))] >= droite[0][next(iter(droite[0]))]:
                    merged.append(gauche[0])
                    gauche.pop(0)

                else:
                    merged.append(droite[0])
                    droite.pop(0)

            ldl.insert(i, merged)
            if len(ldl) == 1:
                return ldl[0]


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


def quick_sort_dict(list_init):
    ldl = [list_init]
    not_sorted = True

    while not_sorted:
        index = 0
        not_sorted = False

        for i in range(len(ldl)):
            if len(ldl[i]) > 1:
                index = i
                not_sorted = True
                break

        if not_sorted:
            liste = ldl.pop(index)
            pivot_dict = liste[0]
            pivot = pivot_dict[next(iter(pivot_dict))]
            liste.pop(0)
            gauche = []
            droite = []

            for dict in liste:
                num = dict[next(iter(dict))]
                if num < pivot:
                    droite.append(dict)
                else:
                    gauche.append(dict)

            ldl.insert(index, droite)
            ldl.insert(index, [pivot_dict])
            ldl.insert(index, gauche)

    sorted_list = []
    for liste in ldl:
        if liste:
            sorted_list.append(liste[0])

    return sorted_list


def get_n_gram_from_word_list(word_list, n, gram_dict):
    for i in range(len(word_list) - n + 1):
        gram = ""
        for j in range(i, i + n):
            gram += word_list[j] + " "
        if gram not in gram_dict.keys():
            gram_dict[gram] = 1
        else:
            gram_dict[gram] += 1


def main():
    mots = [{"allo": 2}, {"bye": 4}, {"chow": 1}, {"ala": 6}, {"nye": 5}, {"chaud": 3}]
    total = 0
    for gram in mots:
        total += gram[next(iter(gram))]
    print(total)
    for gram in mots:
        gram[next(iter(gram))] /= total
    total = 0
    for gram in mots:
        total += gram[next(iter(gram))]
    print(total)

    # mots = quick_sort_dict(mots)
    # print(mots)
    # list_init = [3, 1, 2, 6, 5, 4]
    sorted_list = (merge_sort_dict(mots))
    # word_list = ["allo", "bye", "fuck", "toi", "rue"]
    # gram_dict = {}
    # get_n_gram_from_word_list(word_list, 2, gram_dict)
    # for gram in gram_dict:
    #     print(gram)
    # markov(sorted_list, 10)

    list_bigram = [{"allo toi": 2}, {"bye bye": 4}, {"chow bye": 1}, {"ala 2": 6}, {"bill nye": 5}, {"chien chaud": 3}]


if __name__ == "__main__":
    main()
