import xml.etree.ElementTree as ET

class MetadataError(Exception):
    pass 

def dict_to_xml(d):
    xml_resource = ET.Element('resource')
    xml_resource.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance' 
    xml_resource.attrib['xmlns'] = 'http://datacite.org/schema/kernel-4' 
    xml_resource.attrib['xsi:schemaLocation'] = 'http://datacite.org/schema/kernel-4 https://schema.datacite.org/meta/kernel-4.4/metadata.xsd' 
    
    xml_identifier = ET.SubElement(xml_resource, 'identifier')
    xml_identifier.attrib['identifierType'] = 'DOI'
    try:
        xml_identifier.text = d['identifier']
    except KeyError:
        raise MetadataError('Missing mandatory metadata identifier')
    
    xml_titles = ET.SubElement(xml_resource, 'titles')
    xml_title = ET.SubElement(xml_titles, 'title')
    try:
        xml_title.text = d['title']
    except KeyError:
            raise MetadataError('Missing mandatory metadata identifier')

    xml_publisher = ET.SubElement(xml_resource, 'publisher')
    try:
        xml_publisher.text = d['publisher']
    except KeyError:
        raise MetadataError('Missing mandatory metadata identifier')

    xml_publication_year = ET.SubElement(xml_resource, 'publicationYear')
    try:
        xml_publication_year.text = d['publication_year']
    except KeyError:
        raise MetadataError('Missing mandatory metadata identifier')

    xml_resource_type = ET.SubElement(xml_resource, 'resourceType')
    try:
        xml_resource_type.attrib['resourceTypeGeneral'] = d['resource_type']
        xml_resource_type.text = d['resource_type']
    except KeyError:
        raise MetadataError('Missing mandatory metadata identifier')

    xml_subjects = ET.SubElement(xml_resource, 'subjects')
    for subject in d['subjects']:
        xml_subject = ET.SubElement(xml_subjects, 'subject')
        xml_subject.text = subject

    xml_creators = ET.SubElement(xml_resource, 'creators')
    try:
        for creator in d['creators']:
            xml_creator = ET.SubElement(xml_creators, 'creator')
            xml_creator_name = ET.SubElement(xml_creator, 'creatorName')
            xml_creator_name.text = creator['familyname'] + ', ' + creator['givenname']
            xml_creator_name.attrib['nameType'] = 'Personal'
            xml_creator_given_name = ET.SubElement(xml_creator, 'givenName')
            xml_creator_given_name.text = creator['givenname']
            xml_creator_family_name = ET.SubElement(xml_creator, 'familyName')
            xml_creator_family_name.text = creator['familyname']
            xml_creator_affiliation = ET.SubElement(xml_creator, 'affiliation')
            xml_creator_affiliation.text = creator['affiliation']
    except KeyError:
                raise MetadataError('Missing mandatory metadata identifier')

    return '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + ET.tostring(xml_resource, encoding='unicode')