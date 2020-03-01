""" parser for dept ed web pages"""

import bs4 # pip install beautifulsoup4

# import the individual helper parsers
from parsers import ocr_state_national_estimates_parser1 as estimates_parser1
from parsers import ocr_state_national_estimates_parser2 as estimates_parser2

# extensions for valid resource of a dataset
DATA_EXTENSIONS = {
    'xls': 'Excel',
    'xlsx': 'New Excel',
    'zip': 'ZIP',
    'csv': 'CSV'
}

# extensions for documents that are only valid
# resources IF AND ONLY IF any resource from
# DATA_EXTENSION is present in the dataset
DOCUMENT_EXTENSIONS = {
    '.docx': 'Word document',
    '.doc': 'Word document',
    '.pdf': 'PDF file'
}


def resource_checker(tag_attr: str):
    """ function is used as a filter for BeautifulSoup to
    locate resource (i.e. DATA_EXTENSIONS) files"""

    if tag_attr != '' and tag_attr is not None:
        for extension in DATA_EXTENSIONS.keys():
            if tag_attr.endswith(f'.{extension}'):
                return True
        # if code gets here, no resources found
        return False
    # tag_attr does not match resource required, so return False
    return False

def document_checker(tag_attr: str):
    """ function is used as a filter for BeautifulSoup to
    locate document files (i.e. DOCUMENT_EXTENSIONS) files"""

    if tag_attr != '' and tag_attr is not None:
        for extension in DOCUMENT_EXTENSIONS.keys():
            if tag_attr.endswith(f'.{extension}'):
                return True
        # if code gets here, no resources found
        return False
    # tag_attr does not match resource required, so return False
    return False


def parse(content: str) -> dict:
    """ function parses content to create a dataset model
    or return None if no resource in content"""

    soup_parser = bs4.BeautifulSoup(content, 'html5lib')
    # check if the content contains any of the extensions
    if soup_parser.body.find(name='a', href=resource_checker, 
                             recursive=True) is None:
        # no resource on this page, so return None
        return None

    # if code gets here, at least one resource was found
    
    # check if the parser is working on OCR State & National Estimations (variant 1)
    if soup_parser.body.find(class_='accordiontitle', recursive=True) is not None:
        print("ESTIMATES 1 FOUND")
        # parse the page with the parser and return result
        return estimates_parser1.parse(content)
    # check if the parser is working on OCR State & National Estimations (variant 2)
    if soup_parser.body.select_one('#container #maincontent') is not None:
        print("ESTIMATES 2 FOUND")
        # parse the page with the parser and return result
        return estimates_parser2.parse(content)

