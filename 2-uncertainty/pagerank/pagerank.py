import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
ITERATIVE_MAX_DIFFERENCE_THRESHOLD = 0.001


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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if page not in corpus:
        raise ValueError("Page not in corpus")

    prob_distribution = {}
    corpus_length = len(corpus)
    page_links = corpus[page]

    if corpus[page]:
        # Case where page has links
        # Calculate damping factor additional prob
        random_prob = (1 - damping_factor) / corpus_length

        # Calculate prob for each link in page
        link_prob = damping_factor / len(page_links)

        for corpus_page in corpus:
            if corpus_page in page_links:
                prob_distribution[corpus_page] = link_prob + random_prob
            else:
                prob_distribution[corpus_page] = random_prob

    else:
        # Case where page does not have any links
        # Return dictionary with equal probability for all pages in corpus
        equal_prob = 1 / corpus_length
        for corpus_page in corpus:
            prob_distribution[corpus_page] = equal_prob

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise tracker
    page_rank_dict = {}
    for page in corpus:
        page_rank_dict[page] = 0

    # Initially randomnly select a page
    random_page = random.choice(list(corpus.keys()))

    # For range(n) randomnly select a page to go to based on the transition_model
    for i in range(n):
        prob_distribution = transition_model(corpus, random_page, damping_factor)
        random_page = random.choices(
            population=list(prob_distribution.keys()),
            weights=list(prob_distribution.values()),
            k=1,
        )[0]
        page_rank_dict[random_page] += 1 / n

    return page_rank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise page_rank values to 1 / N
    corpus_length = len(corpus)
    page_ranks = {}
    for page in corpus:
        page_ranks[page] = 1 / corpus_length

    # Continue looping until threshold is met
    new_page_ranks = {}
    max_difference = float('inf')
    while (max_difference >= ITERATIVE_MAX_DIFFERENCE_THRESHOLD):
        if new_page_ranks:
            page_ranks = new_page_ranks

        new_page_ranks = {}

        for page in page_ranks:
            # Calculate iterative portion of formula
            iteration_result = 0
            for p in page_ranks:

                p_links = corpus[p]
                if not p_links: # If no links treat as 1 link for every page in corpus
                    p_links = corpus.keys()

                if page in p_links:
                    p_num_links = len(p_links)
                    p_page_rank = page_ranks[p]
                    iteration_result += p_page_rank / p_num_links

            # Iterative formula
            new_page_rank = (1 - damping_factor) / corpus_length + damping_factor * iteration_result
            new_page_ranks[page] = new_page_rank
        
        # Compare new_page_ranks to previous to establish max difference
        max_difference = 0
        for page in page_ranks:
            difference = abs(page_ranks[page] - new_page_ranks[page])
            if difference > max_difference:
                max_difference = difference

    return new_page_ranks


if __name__ == "__main__":
    main()
