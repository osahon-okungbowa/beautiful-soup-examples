""" File contains simple script showiing the power of BeautifulSoup"""

import bs4 # pip install beautifulsoup4

def print_html(file: str) -> str:
    """ Return the contents of the specified file as html string """

    with open(file, mode='r') as html_file:

        soup = bs4.BeautifulSoup(html_file, 'html5lib')
    return soup.prettify()

def find_anchor(file: str) -> str:
    """ Replace the contents of all anchor tags in the specified
    file with a particular string """
    # open the html file in read mode
    with open(file, mode='r') as html_file:
        # create the Soup DOM object from the html file
        soup = bs4.BeautifulSoup(html_file, 'html5lib')
    # for all the anchor tags in the document...
    for anchor in soup.find_all('a'):
        # replace the content of the anchor with this
        anchor.string.replace_with('Osahon Link')
     # open the html file for writing
    with open(file, mode='w') as html_file:
        # writing the contents of the updated html file
        html_file.write(soup.prettify())

if __name__ == "__main__":
    print(print_html('example-html.html'))
    find_anchor('example-html.html')
