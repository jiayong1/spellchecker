import argparse
from checker_backend import SpellChecker
from align import Aligner


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

    f = open("data/misspelling.txt", "r")
    top1=top2=top3 = 0
    allpairs = 0
    for i in f:
        if i[0] =="$":
            correct = i[1:].lower()
        else:
            if not (set(i.lower().strip()) - alphabet) and correct.strip() in double_variants(i.lower().strip()):
                allpairs += 1
                if(i.lower() != correct):
                    fs = checker.give_suggestions(i.lower().strip(), opts.topk)
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

