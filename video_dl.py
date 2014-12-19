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
        self.page_links_list = page_links_list

        return page_links_list

    def get_video_links(self):
        video_links_list = []
        for page_link in self.page_links_list:
            req = urllib2.Request(page_link, headers=hdr)
            response = urllib2.urlopen(req)
            html = response.read()
            print html
            pattern_vid = "\'file\'\,\'\S*\'\)"
            pattern_seccode = "\'seccode\'\,\'\S*\'\)"
            pattern_max_vid = "\'max_vid\'\,\'\S*\'\)"
            vid = re.findall(pattern_vid, html)[0]
            seccode = re.findall(pattern_seccode, html)[0]
            max_vid = re.findall(pattern_max_vid, html)[0]
            print vid, seccode, max_vid
            get_file_link = self.domain + "/getfile.php?VID="+vid+\
                    "&mp4=1&seccode="+seccode+"&max_vid="+max_vid
            print get_file_link
            ##req = urllib2.Request(get_file_link, headers=hdr)
            ##response = urllib2.urlopen(req)
            ##video_link = response.read()
        return 
         
            

    def download(self):
        for url in self.video_links_list:
            file_name = url.split('/')[-1]
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)
            
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
            
                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,
            
            f.close()

    def main(self):
        self.get_page_links()
        self.get_video_links()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please add a domain"
    else:
        domain = sys.argv[1]
        video_dl = VideoDl(domain)
        video_dl.main()
