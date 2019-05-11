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

    while True:
        print('Please input your word:')
        word = str(input('>')).strip().lower()
        if set(word) - alphabet:
            print('Error: your word contains invalid characters.')
        else:
            # feed freq_dict into final_suggestions() to enable Bayes optimization
            fs = checker.give_suggestions(word, opts.topk)
            print('Possible word(s):')
            if opts.verbose:
                print(fs)
            else:    
                print(', '.join(x[0] for x in fs))


if __name__ == '__main__':
    main()
