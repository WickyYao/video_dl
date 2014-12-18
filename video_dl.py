import sys

import urllib2
import re


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


class VideoDl(object):

    def __init__(self, domain):
        self.domain = domain

    def get_page_links(self):
        page_links_list = []
        for i in range(1, 2):
            req = urllib2.Request(self.domain+'/video.php?category=rf&page='+str(i), headers=hdr)
            response = urllib2.urlopen(req)
            page = response.read()
            pattern = self.domain+'/view_video.php\S*viewtype=basic&category=rf'
            page_links = re.findall(pattern, page)
            for page_link in page_links:
                if page_link not in page_links_list:
                    page_links_list.append(page_link)
        return page_links_list

    def main(self):
        self.get_page_links()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please add a domain"
    else:
        domain = sys.argv[1]
        video_dl = VideoDl(domain)
        video_dl.main()
