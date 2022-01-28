import unittest
from datasets.dict_to_xml import dict_to_xml, MetadataError
import copy

dict = {
    'identifier': 'IDENTIFIER', 
    'title': 'TITLE', 
    'publisher': 'PUBLISHER', 
    'publication_year': 2022, 
    'resource_type': 'Text', 
    'subjects': ['SUBJECT'], 
    'creators': [{'givenname': 'CreatorGName', 'familyname': 'CreatorFName', 'affiliation': 'AFFILIATION'}]
}

subjectdict = {
    'identifier': 'IDENTIFIER', 
    'title': 'TITLE', 
    'publisher': 'PUBLISHER', 
    'publication_year': 2022, 
    'resource_type': 'Text', 
    'creators': [{'givenname': 'CreatorGName', 'familyname': 'CreatorFName', 'affiliation': 'AFFILIATION'}]
}

affiliationdict = {
    'identifier': 'IDENTIFIER', 
    'title': 'TITLE', 
    'publisher': 'PUBLISHER', 
    'publication_year': 2022, 
    'resource_type': 'Text',
    'subjects': ['SUBJECT'], 
    'creators': [{'givenname': 'CreatorGName', 'familyname': 'CreatorFName'}]
}

class TestDictToXml(unittest.TestCase):
    def test_mandatory(self):
        res = dict_to_xml(dict)

        self.assertIn('<identifier identifierType="DOI">IDENTIFIER</identifier>', res)
        self.assertIn('<titles><title>TITLE</title></titles>', res)
        self.assertIn('<publisher>PUBLISHER</publisher>', res)
        self.assertIn('<publicationYear>2022</publicationYear>', res)
        self.assertIn('<resourceType resourceTypeGeneral="Text">Text</resourceType>', res)
        self.assertIn('<creator><creatorName nameType="Personal">CreatorFName, CreatorGName</creatorName><givenName>CreatorGName</givenName><familyName>CreatorFName</familyName><affiliation>AFFILIATION</affiliation></creator>', res)
    
    def test_missing_identifier(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['identifier']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)

    def test_missing_title(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['title']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)

    def test_missing_publisher(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['publisher']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_publication_year(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['publication_year']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_resource_type(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['resource_type']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_creators(self):
        dictcopy = copy.deepcopy(dict)
        del dictcopy['creators']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_subject(self):
        dictcopy= copy.deepcopy(subjectdict)
        dictcopy['subjects'] = ["SUBJECT"]
        res = dict_to_xml(dictcopy)
        self.assertIn('<subject>SUBJECT</subject>', res)
    
    def test_missing_affiliation(self):
        dictcopy = copy.deepcopy(affiliationdict)
        dictcopy['creators'][0]['affiliation'] = "AFFILIATION"
        res = dict_to_xml(dictcopy)
        self.assertIn('<affiliation>AFFILIATION</affiliation>', res)
        

if __name__ == '__main__':
    unittest.main()