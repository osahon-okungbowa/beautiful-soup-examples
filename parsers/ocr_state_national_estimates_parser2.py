""" parser for ocr state/national estimates 2009/10,
2006,2004,2002 """

import re

import bs4 # pip install beautifulsoup4

from parsers import parser_utility as utility
import parsers


def parse(content: str) -> dict:
    """ function parses content to create a dataset model """

    # create parser object
    soup_parser = bs4.BeautifulSoup(content, 'html5lib')
    # define a variable that is the dataset
    dataset = None

    dataset_containers = soup_parser.body.find_all(id='maincontent',
                                                   recursive=True)
    for container in dataset_containers:
        # create dataset model dict
        dataset = dict()
        dataset['source_url'] = ''
        # get the first available div element
        dataset['title'] = str(container.find(name='div').\
                            string).strip()
        # replace all non-word characters (e.g. ?/) with '-'
        dataset['name'] = re.sub(r'[\W]', '-', dataset['title']).lower()
        dataset['publisher'] = ''
        if container.select_one('p') is not None:
            # get the first available p element
            dataset['description'] = str(container.select_one('p').string).\
                                  strip()
        else:
            # get the 2nd div element
            dataset['description'] = str(container.\
                                    select_one('p, div:nth-child(2)').\
                                    string).strip()
        dataset['tags'] = ''
        dataset['date'] = ''
        dataset['contact_person_name'] = ""
        dataset['contact_person_email'] = ""

        # by default, define empty resources for dataset
        dataset['resources'] = list()

        # add  resources from the 'container' to the dataset
        page_resource_links = container.find_all(name='a',
                                                 href=parsers.parser.resource_checker,
                                                 recursive=True)
        for resource_link in page_resource_links:
            resource_obj = {'source_url': '',
                            'url': resource_link['href'],
                            'name': str(resource_link.string).strip()
                           }
            # get the format of the resource from the file extension of the link
            resource_format = resource_link['href']\
                            [resource_link['href'].rfind('.') + 1:]
            resource_obj['format'] = resource_format
            # add the resource_obj to collection of resources
            dataset['resources'].append(resource_obj)

        # if this dataset alread has data resource files look for
        # document resource files
        if len(dataset['resources']) > 0:
            # add  documents from the 'container' to the dataset
            page_document_links = container.find_all(name='a',
                                                    href=parsers.parser.document_checker,
                                                    recursive=True)
            for resource_link in page_document_links:
                resource_obj = {'source_url': '',
                                'url': resource_link['href'],
                                'name': str(resource_link.string).strip()
                               }
                # get the format of the resource from the file extension of the link
                resource_format = resource_link['href']\
                                [resource_link['href'].rfind('.') + 1:]
                resource_obj['format'] = resource_format
                # add the resource_obj to collection of resources
                dataset['resources'].append(resource_obj)
        # TODO dump file
        utility.dump_dataset(dataset, False)

    return dataset
