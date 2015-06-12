# Author: Yuta Miyake
# File: downloader.py

from BeautifulSoup import BeautifulSoup as bs
import urllib2, requests, os, re, sys

def downloadFile(path,ext,dst):
    """Download all the files of a particular extention in a web page

        Usage: "python downloader.py [url] [ext] [dst]"
    """
    soup = bs(urllib2.urlopen(path))

    filenames = []
    for link in soup.findAll('a',href=re.compile(".+\."+ext)):
      filenames.append(link.get('href'))  # tag.get('attr')

    if not os.path.exists(dst):
       print dst+" is not found"
       return

    sizes = []
    total = 0
    founds = []
    for name in filenames:
        url = os.path.join(path,name)
        try:
            site = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print e.reason +": "+ url
        else:
            print "Found : " + url
            size = int(site.headers['content-length'])
            sizes.append(size)
            total += size
            founds.append(name)
    if len(founds) <= 0:
        print "\nThere is no %s file that can be accessible." %(ext) 
        return

    print "\nTotal size is " + getReadableFileSize(total)
    if raw_input("Are you sure you want to download all the files? [y/n]: ") != "y":
        return
    
    sys.stdout.write("\n")
    ctr = 0
    for name in founds:
        url = os.path.join(path,name)
        size = sizes[ctr]
        ctr = ctr + 1
        print "\rDownloading %s ..." % (url)

        # get filename
        index = name.rfind('/')
        if index != -1:
            name = name[index+1:]

        localpath = os.path.join(dst,name)
        response = requests.get(url, stream=True) 

        with open(localpath, "wb") as f:
            if size is None:
                f.write(response.content)
            else:
                dl = 0
                for chunk in response.iter_content(chunk_size=1024):
                   dl += len(chunk)
                   f.write(chunk)
                   done = int(50 * dl / size)
                   sys.stdout.write("\r%d%% [%s%s] %d" % (float(dl)/size*100,'=' * done, ' ' * (50-done),size))
                   sys.stdout.flush()

def getReadableFileSize(bytes):
        if bytes < 1000:
            return str(bytes) + 'B'
        
        units = ['kB','MB','GB','TB','PB','EB','ZB','YB']
        u = -1

        while bytes >= 1000:
            bytes /= 1000
            u = u + 1
        return str(bytes) + units[u]
  

if __name__=='__main__':
    if len(sys.argv) == 4:
        downloadFile(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print "Usage python downloader.py [url] [ext] [dst]"
