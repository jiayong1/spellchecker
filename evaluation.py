# Authors: Jiayong Lin, Hengduo Li


import argparse

from tqdm import tqdm
import pandas as pd

from align import Aligner
from checker_backend import SpellChecker


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--topn', type=int, dest='n', default=1000, help='Ramdomly test on n words.')
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
    n = opts.n
    checker = SpellChecker(Aligner(opts.sigma, opts.bayes))
    #f = open("data/testdata.txt", "r")
    top1=top2=top3 = 0
    allpairs = 0


    data = pd.read_csv('data/testdata.txt', sep=" ", header=None)
    data.columns = ["correct", "mis"]
    subdata = data.sample(n = n) 

    for index, row in tqdm(subdata.iterrows()):
        allpairs += 1
        fs = checker.give_suggestions(row["mis"], opts.topk)
        if fs is not None:
            resultlist = [row[0] for row in fs]
            if row["correct"].strip() == resultlist[0]:
                top1 += 1 
                top2 += 1
                top3 += 1
            elif len(resultlist) >= 2 and row["correct"].strip() == resultlist[1] :
                top2 += 1
                top3 += 1
            elif len(resultlist) == 3 and row["correct"].strip() == resultlist[2] :
                top3 += 1



    print("Top 1 precision: ", top1 / allpairs)
    print("Top 2 precision: ", top2 / allpairs)
    print("Top 3 precision: ", top3 / allpairs)
    print("-----------------------------------------")



if __name__ == '__main__':
    main()
