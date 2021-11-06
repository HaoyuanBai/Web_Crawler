import logging
import re
from urllib.parse import urlparse, urldefrag,urljoin

import urllib.request
from collections import defaultdict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus
        self.history = defaultdict(int)
        self.num = 0
        self.subdomain=  []
        self.length={}



    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched,
                        len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)


    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form).

        Suggested library: lxml
        """
        outputLinks = list()
        pattern = ('[A-Za-z0-9]')
        url = url_data["url"]  # based
        contentt = url_data["content"]
        urlresponse = url_data['http_code']

        parsed = urlparse(url)
        domain = "http://" + parsed.netloc
        wordtoken = []
        # writing urls into .txt files
        with open("url.txt", 'a+') as file, open("word.txt", 'a+') as contentfile, open("length.txt", 'a+') as longestfile ,  open("subdomain.txt", 'a+') as subdomainfile:

            #            if self.is_valid(url) is True:
            if urlresponse != 404:  # 404 if the url does not exist in the corpus
                try:
                    soup = BeautifulSoup(contentt, 'html.parser')  # BeautifulSoup to parse
                    soupcontent = soup.get_text()#get the text
                    asoup = soup.find_all('a')  # find the url star with the tad "<a...... and store in varibale soup"
                    file.write('this is url \n')
                    file.write(url + "\n")
                    for t in soupcontent.split():
#                        print('aa',t)
                        #                        for i in t:
                        #                            print(123123,i)
                        #                            if f"'{i}'" == ascii(i) :#O(1)
                        #                                print('t',t)
                        #                                wordtoken.append(t)
                        #                    wordtoken = set(wordtoken)
                        #                        print('t',t)
                        check =t.isalnum()
                        if check:
                                wordtoken.append(t)
                    for i in asoup:
                        try:
                            if i != None:
                                relativeURL = i.get('href')
                                absoluteURL = urljoin(url, relativeURL,allow_fragments=True)  # Construct a absolute URL with base url and another url
                                absolute = urllib.parse.urljoin(domain, relativeURL)
    #                            print(absolute, 'absolute')
                                if '//' in absolute:  # make sure it's absolute form
                                    outputLinks.append(absolute)
                                    new =absolute.split('://')
                                    newww=new[1]
                                    sub =newww.split('/')
                                    subbb= sub[0]
                                    self.subdomain.append(subbb)
                                    for k in url_data.keys():
                                        if url_data['is_redirected'] is True:
                                            outputLinks.append(url_data["final_url"])
                                    file.write(absolute)
                                    self.num += 1
                        except:
                            pass

                    wordtoken= set(wordtoken)
                    subdomainfile.write( str(self.subdomain ))
                    self.length[url] = len(wordtoken)
                    contentfile.write(str(wordtoken)+'\n' )
                    file.write('this is longest \n')
                    longestfile.write( str(self.length[url]+'\n'))
                    stop = ['a','about''above',
'after','again','against''all','am','an','and','any','are','as','at','be','because','been','before','being','below','between','both','but','by','can\'t','cannot']
                    print( '123', max(set(wordtoken), key = list.count) )
            

                except:
                    print(1)
                    pass

#        print('qwq', self.num)
        return outputLinks



        '''
        Additionally crawler traps include history based trap detection where based on your practice runs you will
        determine if there are sites that you have crawled that are traps, continuously repeating sub-directories
        and very long URLs. '''


    def is_valid(self,url):
        try:

            parsed = urlparse(url)

            if parsed.scheme.lower() not in set(["http", "https","ftp", b"http", b"https",b"ftp"]):
                return False


            if parsed[:6]=="mailto":
                return False

            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())



        except TypeError:
            print("TypeError for ", parsed)
            return False

