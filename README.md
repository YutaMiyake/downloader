# downloader.py

## Description
Download all the accessible files of a particular extention in a web page. Specifically, downloader.py searches through 'href' in html tag 'a' for whatever ends at the given extention. Then, it downloads only accessible files into your destination.

## Dependencies
A downloader.py requires BeautifulSoup4 and requests modules as well as basic modules.

## Usage
```bash
$ python downloader.py [url] [ext] [dist='./']
```

Example: download every pdf files in a mit online course into pdfs folder
```bash
$ python downloader.py http://ocw.mit.edu/courses/brain-and-cognitive-sciences/9-66j-computational-cognitive-science-fall-2004/lecture-notes/ pdf pdfs
```