import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # check if page is None
    if corpus[page] == None:
        # add empty dict
        num = {i:0 for i in corpus.keys()}
        # iterate over 
        for key in corpus.keys():
            num[key] += damping_factor / (len(corpus.keys()))
            
    # if corpus is Not None
    if corpus[page] != None:
        # create dict with initial values 
        num = {i:0 + round((1-damping_factor) / len(corpus.keys()), 3) for i in corpus.keys()}
        # iterate over keys, check if page and add distribution 
        for key, value in num.items():
            if key != page:
                num[key] += damping_factor / (len(corpus.keys()) - 1)
    return num 

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # create empty dict
    num = {i:0 for i in corpus.keys()}
    # randomly select first page
    page = random.choice(list(corpus.keys()))
    # iterate over n samples
    for i in range(1, n):
        # get the distribution 
        model = transition_model(corpus, page, damping_factor)
        # iterate over empty dict 
        for g in num:
            # add values with prodived formula
            num[g] = ((i-1) * num[g] + model[g]) / i
        # update randomly pages   
        page = random.choices(list(num.keys()), list(num.values()), k=1)[0]

    return num

import math

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    old = {i:(1 / len(corpus.keys())) for i in corpus.keys()}
    new = {i: math.inf for i in corpus.keys()}
    lenth = len(corpus)
    
    while any(g > 0.001 for g in new.values()):
        for page in old.keys():
            proba = 0
            for keys, pages in corpus.items():
                
                if not pages:
                    
                    pages = corpus.keys()
                    
                if page in pages:
                    
                    proba += old[keys] / len(pages)
                    
            new_rank = ((1 - damping_factor) / lenth) + (damping_factor * proba)
            
            new[page] = abs(new_rank - old[page])
            
            old[page] = new_rank
            
    return old

if __name__ == "__main__":
    main()