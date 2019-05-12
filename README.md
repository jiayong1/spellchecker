# spellchecker

- Authors: Hengduo Li, Jiayong Lin, Hanyu Wang.

![image](https://github.com/henrylee2570/701_spellchecker/raw/master/method.png)

`cli_checker.py` provides an interactive command line interface for users to check their words.

`checker_backend.py` implements the spellchecker backend `SpellChecker` that can be used in other python programs.
## Usage

Usage of the interactive command line interface:

```
python cli_checker.py [-h] [-k TOPK] [-s SIGMA] [--noBayes] [--onlyBayes] [-v]

optional arguments:
  -h, --help                show this help message and exit
  -k TOPK, --topk TOPK      return top k canditates to pick
  -s SIGMA, --sigma SIGMA   gap score used in global alignment
  --noBayes                 don't apply Bayes rule.
  --onlyBayes               only ues Bayes rule(no global alignment).
  -v, --verbose             verbose mode on
```

## Example

Start an interactive command line interface that returns 5 candidates:

```
python cli_checker.py -k 5
```

You may see:

```
Please input your word:
> 
```

You mistakenly input "gename":

```
Please input your word:
> gename
```

You'll get the results immediately:

```
Please input your word:
> gename
Possible word(s):
genome, rename, senate, renamed, became
```

where the first candidate `genome` is exactly what you want.
