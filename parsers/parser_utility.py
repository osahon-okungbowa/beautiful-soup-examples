""" utility functions for parsers """

import os.path
import os
import json

import requests # pip install requests
import yaml # pip install PyYAML


def dump_dataset(dataset, add_yaml=False):
    """ function dumps the returned dataset as json format
    if 'add_yaml' is True, then a yaml dump is also done.
    File dumps use the name of the dataset.
    Files are dumped in '.dataset_dumps' directory"""

    if not os.path.exists('./.dataset_dumps'): # the dumps directory does not exist
        # create directory
        os.mkdir('./.dataset_dumps')

    # dump the json
    json.dump(dataset,
              open(f'./.dataset_dumps/{dataset["name"]}.json', 'w'), 
              indent=4)
    if add_yaml: # dump yaml
        yaml.dump(dataset,
                  open(f'./.dataset_dumps/{dataset["name"]}.yaml', 'w'),
                  indent=4,
                  default_flow_style=False)


def cache_web_page(urls: [str]):
    """ function caches the specified web page in .web_caches directory """
    
    if not os.path.exists('./.web_caches'): # the cache directory does not exist
        # create directory
        os.mkdir('./.web_caches')
    # cache the urls provided
    for url in urls:
        if url.endswith('.html'):
            with open('./.web_caches/{0}'.\
                    format(url[url.rfind('/')+1:]), 'wt') as html_file:
                html_file.write(requests.get(url, verify=False).text)
        else:
            with open('./.web_caches/{0}'.\
                    format(url[url.rfind('/')+1:] + ".html"), 'wt') as\
                     html_file:
                html_file.write(requests.get(url, verify=False).text)

def load_web_cache():
    """ function loads the contents of each cached
    web page. The function returns a generator.
    The generator returns the content of each page when iterated."""
    
    # get the web pages in the web_caches folder
    with os.scandir('./.web_caches') as scanned_dir:
        for web_page in scanned_dir:
            with open('./.web_caches/{}'.format(web_page.name), 'rt') as html_file:
                # add page content to list
                yield html_file.read()
