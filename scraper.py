import getopt
import sys
from collections import Counter

from bs4 import BeautifulSoup
import requests

# ---------------------------------------------------------------- 
# class ScrapedSite - 
# ---------------------------------------------------------------- 
class ScrapedSite:

    # available transforms for words scraped from the site
    transforms = {
        'lower' : lambda x: [x.lower()],
        'upper' : lambda x: [x.upper()],
        'dualcase'  : lambda x: [x[0].upper() + x[1:], x[0].lower() + x[1:]]
    }

    def __init__(self, rooturl, recursive=False, local=False, transform=(lambda x: x.lower()):
        self.rooturl = rooturl.lower()
        try:
            if local:
                self.roottext = open(self.rooturl).read()
            else:
                self.roottext = requests.get().text
        except Exception as e:
            print("HTML Read Error: %s" % e)
        soup = BeautifulSoup(self.roottext)
        self.wordlist = Counter()
        for word in soup.get_text.split(" "):
            self.wordlist.update(transform(word))
        
        if recursive:
            hrefs = [self.rooturl] + [link.get('href').lower() for link in soup.find_all("a") if link.get('href').lower() != self.rooturl]
            counter = 0
            while counter < len(hrefs):
                href = hrefs[counter]
                subsoup = BeautifulSoup(href)
                for word in subsoup.get_text.split(" "):
                    self.wordlist.update(transform(word))
                hrefs += [link.get('href').lower() for link in subsoup.find_all("a") if link.get('href').lower() not in hrefs]
                counter += 1

def main():
    opts, args = getopt.getopt(sys.argv[1:], "hrlt:")
    recursive = False
    local = False
    for o, a in opts:
        if o == "-h":
            print_help()
            exit()
        elif o == "-r":
            recursive = True
        elif o == "-l":
            


def print_help():
    print(open("help.txt"))

if __name__ == "__main__":
    main()
