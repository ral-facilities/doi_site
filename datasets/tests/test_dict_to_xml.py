import unittest
from datasets.dict_to_xml import dict_to_xml, MetadataError
import copy

test_dict = {
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
        res = dict_to_xml(test_dict)

        self.assertIn('<identifier identifierType="DOI">IDENTIFIER</identifier>', res)
        self.assertIn('<titles><title>TITLE</title></titles>', res)
        self.assertIn('<publisher>PUBLISHER</publisher>', res)
        self.assertIn('<publicationYear>2022</publicationYear>', res)
        self.assertIn('<resourceType resourceTypeGeneral="Text">Text</resourceType>', res)
        self.assertIn('<creator><creatorName nameType="Personal">CreatorFName, CreatorGName</creatorName><givenName>CreatorGName</givenName><familyName>CreatorFName</familyName></creator>', res)
    
    def test_missing_identifier(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['identifier']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)

    def test_missing_title(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['title']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)

    def test_missing_publisher(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['publisher']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_publication_year(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['publication_year']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_resource_type(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['resource_type']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_creators(self):
        dictcopy = copy.deepcopy(test_dict)
        del dictcopy['creators']
        with self.assertRaises(MetadataError):
            res = dict_to_xml(dictcopy)
    
    def test_missing_subject(self):
        dictcopy= copy.deepcopy(test_dict)
        dictcopy['subjects'] = ["SUBJECT"]
        res = dict_to_xml(dictcopy)
        self.assertIn('<subject>SUBJECT</subject>', res)
    
    def test_missing_affiliation(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['creators'][0]['affiliation'] = "AFFILIATION"
        res = dict_to_xml(dictcopy)
        self.assertIn('<affiliation>AFFILIATION</affiliation>', res)
    
    def test_missing_orcid(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['creators'][0]['orcid'] = "CREATORORCID"
        res = dict_to_xml(dictcopy)
        self.assertIn('<nameIdentifier schemeURI="https://orcid.org/" nameIdentifierScheme="ORCID">CREATORORCID</nameIdentifier>', res)
    
    def test_missing_description(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['abstract'] = "ABSTRACT"
        res = dict_to_xml(dictcopy)
        self.assertIn('<descriptions><description descriptionType="Abstract">ABSTRACT</description></descriptions>', res)
    
    def test_missing_resource_type_text(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['resource_type_text'] = "RESOURCE TYPE TEXT"
        res = dict_to_xml(dictcopy)
        self.assertIn('<resourceType resourceTypeGeneral="Text">RESOURCE TYPE TEXT</resourceType>', res)
        
    def test_missing_version(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['version'] = "0.0.0"
        res = dict_to_xml(dictcopy)
        self.assertIn('<version>0.0.0</version>', res)
    
    def test_missing_funder_name(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['funders']= [{'funder_name':"Stfc", 'funder_identifier':""}]
        res = dict_to_xml(dictcopy)
        self.assertIn('<funderName>Stfc</funderName>', res)
    
    def test_missing_funder_identifier(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['funders']= [{'funder_name':"", 'funder_identifier':"999"}]
        res = dict_to_xml(dictcopy)
        self.assertIn('<funderIdentifier funderIdentifierType="Crossref Funder ID">999</funderIdentifier>', res)
    
    def test_missing_award_number(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['funders']= [{'funder_name':"", 'funder_identifier':"", 'award_number':"666"}]
        res = dict_to_xml(dictcopy)
        self.assertIn('<awardNumber>666</awardNumber>', res)
    
    def test_missing_award_title(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['funders']= [{'funder_name':"", 'funder_identifier':"", 'award_title':"AWARD TITLE"}]
        res = dict_to_xml(dictcopy)
        self.assertIn('<awardTitle>AWARD TITLE</awardTitle>', res)
    
    def test_missing_date(self):
        dictcopy = copy.deepcopy(test_dict)
        dictcopy['dates'] = [{'date': '2022-02-22', 'date_type': 'Updated', 'date_text': 'Updated with 4.4 properties'}]
        res = dict_to_xml(dictcopy)
        self.assertIn('<dates><date dateType="Updated" dateInformation="Updated with 4.4 properties">2022-02-22</date></dates>', res)

    def test_missing_related_identifier(self):
            dictcopy= copy.deepcopy(test_dict)
            dictcopy['related_identifiers'] = [{'related_identifier':"www.site-url.com", 'related_identifier_type':"URL", 'related_identifier_relation_type':"Cites" }]
            res = dict_to_xml(dictcopy)
            self.assertIn('<relatedIdentifier relatedIdentifierType="URL" relationType="Cites">www.site-url.com</relatedIdentifier>', res)
if __name__ == '__main__':
    unittest.main()