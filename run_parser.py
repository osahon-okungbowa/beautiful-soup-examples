""" file is the main entry point for running the parser script.
This is for test purposes ONLY """

import parsers.parser_utility as utility
import parsers.main_parser as parser


if __name__ == "__main__":
    
    # cache the provided web pages
    utility.cache_web_page([
    'https://ocrdata.ed.gov/StateNationalEstimations/Estimations_2013_14',
    'https://ocrdata.ed.gov/StateNationalEstimations/Estimations_2011_12',
    'https://ocrdata.ed.gov/StateNationalEstimations/Projections_2009_10',
    'https://ocrdata.ed.gov/StateNationalEstimations/Projections_2006',
    'https://ocrdata.ed.gov/StateNationalEstimations/Projections_2004',
    'https://ocrdata.ed.gov/StateNationalEstimations/Projections_2000'])
    
    page_counter = 1

    for content in utility.load_web_cache():
        result = parser.parse(content)
        if result is None:
            print("NO RESOURCE FOUND")
        else:
            """ json.dump(result,
                      open(f'./index{page_counter}.json', 'w'), indent=4)
            yaml.dump(result,
                      open(f'./index{page_counter}.yaml', 'w'), indent=4,
                      default_flow_style=False) """
        page_counter += 1
