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
        xml_publication_year.text = str(d['publication_year'])
    except KeyError:
        raise MetadataError('Missing mandatory metadata identifier')

    xml_resource_type = ET.SubElement(xml_resource, 'resourceType')
    try:
        xml_resource_type.attrib['resourceTypeGeneral'] = d['resource_type']
    except KeyError:
        raise MetadataError('Missing mandatory metadata resource type')
    xml_resource_type.text = d.get("resource_type_text") or d["resource_type"]
    
    try:
        subjects = d["subjects"]
    except KeyError:
        subjects = []
    if subjects:
        xml_subjects = ET.SubElement(xml_resource, 'subjects')
        for subject in subjects:
            xml_subject = ET.SubElement(xml_subjects, 'subject')
            xml_subject.text = subject
    
    try:
        relatedIdentifiers = d["related_identifiers"]
    except KeyError:
        relatedIdentifiers = []
    if relatedIdentifiers:
        xml_related_identifiers = ET.SubElement(xml_resource, 'relatedIdentifiers')
        for relatedIdentifier in relatedIdentifiers:
            if relatedIdentifier['related_identifier']:
                xml_related_identifier = ET.SubElement(xml_related_identifiers, 'relatedIdentifier')
                xml_related_identifier.text = relatedIdentifier['related_identifier']
                xml_related_identifier.attrib['relatedIdentifierType'] = relatedIdentifier['related_identifier_type']
                xml_related_identifier.attrib['relationType'] = relatedIdentifier['related_identifier_relation_type']

    xml_creators = ET.SubElement(xml_resource, 'creators')
    try:
        creators = d['creators']
    except KeyError:
            raise MetadataError('Missing mandatory metadata creators')
    if creators:
        for creator in creators:
            xml_creator = ET.SubElement(xml_creators, 'creator')
            xml_creator_name = ET.SubElement(xml_creator, 'creatorName')
            xml_creator_name.text = creator['familyname'] + ', ' + creator['givenname']
            xml_creator_name.attrib['nameType'] = 'Personal'
            xml_creator_given_name = ET.SubElement(xml_creator, 'givenName')
            xml_creator_given_name.text = creator['givenname']
            xml_creator_family_name = ET.SubElement(xml_creator, 'familyName')
            xml_creator_family_name.text = creator['familyname']
            try:
                orcid = creator['orcid']
            except KeyError:
                orcid = None
            if orcid:
                xml_creator_name_identifier = ET.SubElement(xml_creator, 'nameIdentifier')
                xml_creator_name_identifier.attrib['schemeURI'] = 'https://orcid.org/'
                xml_creator_name_identifier.attrib['nameIdentifierScheme'] = 'ORCID'
                xml_creator_name_identifier.text = creator['orcid']
            try: 
                affiliation = creator['affiliation']
            except KeyError:
                affiliation = None
            if affiliation:
                xml_creator_affiliation = ET.SubElement(xml_creator, 'affiliation')
                xml_creator_affiliation.text = creator['affiliation']
    
    xml_funders = ET.SubElement(xml_resource, 'fundingReferences')
    try:
        funders = d['funders']
    except KeyError:
        funders = None
    if funders:
        for funder in funders:
            xml_funder = ET.SubElement(xml_funders, 'fundingReference')
            xml_funder_name = ET.SubElement(xml_funder, 'funderName')
            xml_funder_name.text = funder['funder_name'] 
            xml_funder_identifier = ET.SubElement(xml_funder, 'funderIdentifier')
            xml_funder_identifier.text = funder['funder_identifier']
            xml_funder_identifier.attrib['funderIdentifierType'] = 'Crossref Funder ID'
            try:
                awardNumber = funder['award_number']
            except KeyError:
                awardNumber = None
            if awardNumber:
                xml_funder_award_number = ET.SubElement(xml_funder, 'awardNumber')
                xml_funder_award_number.text = funder['award_number']
            try: 
                awardTitle = funder['award_title']
            except KeyError:
                awardTitle = None
            if awardTitle:
                xml_award_title = ET.SubElement(xml_funder, 'awardTitle')
                xml_award_title.text = funder['award_title']

    try:
        abstract = d['abstract']
    except KeyError:
        abstract = None
    if abstract:
        xml_descriptions = ET.SubElement(xml_resource, 'descriptions')
        xml_description = ET.SubElement(xml_descriptions, 'description')
        xml_description.attrib['descriptionType'] = 'Abstract'
        xml_description.text = d['abstract']
    
    try:
        version = d['version']
    except KeyError:
        version = None
    if version:
        xml_version = ET.SubElement(xml_resource, 'version')
        xml_version.text = d['version']
    
    try:
        dates = d['dates']
    except KeyError:
        dates = []
    if dates:
        xml_dates = ET.SubElement(xml_resource, 'dates')
        for date in dates:
            if date['date']:
                xml_date  = ET.SubElement(xml_dates, 'date')
                xml_date.attrib['dateType'] = date['date_type']
                xml_date.attrib['dateInformation'] = date['date_text']
                xml_date.text = date['date']

    
    return '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + ET.tostring(xml_resource, encoding='unicode')