import argparse
import glob
import os

from markov import get_markov_from_unigram, get_markov_from_bigram_graph
from test3 import scrape_author_folder, get_distance_between_n_gram, scrape_mystery_file, scrape_single_author

PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]

if __name__ == "__main__":
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
    print(remove_ponc)
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

    if args.g:
        markov_file_name = args.g

    author_list = []
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
            # with codecs.open(markov_file_name, "w+", encoding="utf-8",
            #                  errors="ignore") as f:
            #     f.write(text)
