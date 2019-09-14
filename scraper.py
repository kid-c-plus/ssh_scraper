import getopt
import sys
from collections import Counter

from bs4 import BeautifulSoup
import requests

class ScrapedSite:
    def __init__(self, rooturl, recursive=True, local=True, transform=(lambda x: x.lower()), *args, **kwargs):
        self.rooturl = rooturl.lower()
        try:
            if local:
                self.roottext = open(self.rooturl).read()
            else:
                self.roottext = requests.get().text
        except Exception as e:
            print("HTML Read Error: %s" % e)
        soup = BeautifulSoup(self.roottext)
        self.wordlist = Counter([transform(word) for word in soup.get_text().split(" ")])
        
        if recursive:
            hrefs = [self.rooturl] + [link.get('href').lower() for link in soup.find_all("a") if link.get('href').lower() != self.rooturl]
            counter = 0
            while counter < len(hrefs):
                href = hrefs[counter]
                subsoup = BeautifulSoup(href)
                self.wordlist.update([transform(word) for word in subsoup.get_text().split(" ")])
                hrefs += [link.get('href').lower() for link in subsoup.find_all("a") if link.get('href').lower() not in hrefs]
                counter += 1

def main():


if __name__ == "__main__":
    main()