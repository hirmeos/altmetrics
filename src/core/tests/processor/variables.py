from collections import namedtuple


wiki_json = {  # example of wiki API call output
    'batchcomplete': '',
    'query': {
        'normalized': [
            {
                'from': 'The_battle_for_open',
                'to': 'The battle for open'
            }
        ],
        'pages': {
            '1950647': {
                'pageid': 1950647,
                'ns': 0,
                'title': 'The battle for open',
                'extlinks': [
                    {'*': 'http://dx.doi.org/10.5334/bam'},
                    {'*': 'http://creativecommons.org/licenses/by/3.0/'}
                ]
            }
        }
    }
}


WikiReference = namedtuple('WikiReference', ('doi', 'references'))

wiki_reference_simple = WikiReference(
    doi='10.16993/bbc',
    references=[
        'http://socialarchive.iath.virginia.edu/ark:/99166/w6zs3qwx',
        'http://data.bnf.fr/ark:/12148/cb12336493z',
        'http://doi.org/10.16993/bbc',
        'http://isni.org/isni/0000000081111546',
        'http://www.worldcat.org/oclc/54929440',
        'https://digitalcommons.hope.edu/anchor_1988/23',
    ]
)

wiki_reference_encoded = WikiReference(
    doi='10.16993/bak',
    references=[
        'http://jimandnancyforest.com/',
        'http://doi.org/10.16993%2Fbak',
        'http://www.peace.mennolink.org/cgi-bin/m.pl?a=134',
        'http://orthodoxwiki.org/Jim_Forest',
        'http://www.worldcat.org/issn/0002-7049',
        'https://www.wikidata.org/wiki/Q6195030',
    ]
)


class MockUri:
    def __init__(self, raw):
        self.raw = raw


class MockEvent:
    def __init__(self, subject_id, uri):
        self.subject_id = subject_id
        self.uri = uri


class MockWikipediaPage:
    def __init__(self, references):
        self.references = references
