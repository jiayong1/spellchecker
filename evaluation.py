# Authors: Jiayong Lin, Hengduo Li

import argparse

from tqdm import tqdm

from align import Aligner
from checker_backend import SpellChecker


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--topk', type=int, default=3, help='return top k canditates to pick')
    parser.add_argument('-s', '--sigma', type=int, default=5, help='gap score used in global alognment')
    parser.add_argument('--noBayes', action='store_false', dest='bayes',
                        default=True,
                        help='don\'t apply Bayes rule.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        default=False,
                        help='verbose')
    return parser



def main():
    opts = get_parser().parse_args()
    checker = SpellChecker(Aligner(opts.sigma, opts.bayes))
    alphabet = set('abcdefghijklmnopqrstuvwxyz')

    f = open("data/testdata.txt", "r")
    top1=top2=top3 = 0
    allpairs = 0
    for i in tqdm(f):
        correct = i.strip().split(" ")[0]
        mis =  i.strip().split(" ")[1]


        allpairs += 1
        fs = checker.give_suggestions(mis, opts.topk)
        if fs is not None:
            resultlist = [row[0] for row in fs]
            if correct.strip() == resultlist[0]:
                top1 += 1 
                top2 += 1
                top3 += 1
            elif len(resultlist) >= 2 and correct.strip() == resultlist[1] :
                top2 += 1
                top3 += 1
            elif len(resultlist) == 3 and correct.strip() == resultlist[2] :
                top3 += 1



    print(top1 / allpairs)
    print(top2 / allpairs)
    print(top3 / allpairs)
    print("--------------------")





if __name__ == '__main__':
    main()
