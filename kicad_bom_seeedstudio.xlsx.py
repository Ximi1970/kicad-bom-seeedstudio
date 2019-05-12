#!/usr/bin/env python3
import xlsxwriter
import sys
import xml.etree.ElementTree as ET

### Natural key sorting for orders like : C1, C5, C10, C12 ... (instead of C1, C10, C12, C5...)
# http://stackoverflow.com/a/5967539
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]
###

def parse_kicad_xml(input_file):
    """Parse the KiCad XML file and look for the part designators
    as done in the case of the official KiCad Open Parts Library:
    * OPL parts are designated with "SKU" (preferred)
    * other parts are designated with "MPN"
    """
    components = {}
    links = {}
    missing = []

    tree = ET.parse(input_file)
    root = tree.getroot()
    for f in root.findall('./components/'):
        name = f.attrib['ref']
        info = {}
        fields = f.find('fields')
        opl, mpn, link = None, None, None
        if fields is not None:
            for x in fields:
                if x.attrib['name'].upper() == 'SKU':
                    opl = x.text
                elif x.attrib['name'].upper() == 'MPN':
                    mpn = x.text
                if x.attrib['name'].upper() == 'LINK':
                    link = x.text
        if opl:
            components[name] = opl
        elif mpn:
            components[name] = mpn
            components[name] = mpn
        else:
            missing += [name]
            continue
        if link:
            links[name] = link
        else:
            links[name] = ''
    return components, links, missing

def write_bom_seeed(output_file_slug, components, links):
    """How do I prepare the Bill of Materials (BOM) file for Seeed Fusion PCBA Orders:
    http://support.seeedstudio.com/knowledgebase/articles/1886734-how-do-i-prepare-the-bill-of-materials-bom-file
    https://statics3.seeedstudio.com/files/20184/2018.xlsx

    ```
    Designator,MPN/Seeed SKU,Qty,Link
    "C1,C2,C3,C4,C5", "RHA0J471MCN1GS", "5", "https://www.digikey.com.cn/product-detail/zh/nichicon/RHA0J471MCN1GS/493-3771-1-ND/2209480?keywords=RHA0J471MCN1GS"
    "A1,A4", "RH0111-30002", "2", "https://statics3.seeedstudio.com/images/opl/datasheet/318020010.pdf"
    "D1", "CYBLE-014008-00", "1", "https://www.digikey.com.cn/product-detail/zh/cypress-semiconductor-corp/CYBLE-014008-00/428-3600-1-ND/6052585?keywords=CYBLE-014008-00"
    ```

    The output is a CSV file at the `output_file_slug`.csv location.
    """
    parts = {}
    partslink = {}
    for c in components:
        if components[c] not in parts:
            parts[components[c]] = []
            partslink[components[c]] = []
        parts[components[c]] += [c]
        partslink[components[c]] = links[c]

    field_names = ['Designator', 'MPN/Seeed SKU', 'Qty','Link']
    field_sizes = {}
    
    workbook = xlsxwriter.Workbook("{}.xlsx".format(output_file_slug))
    worksheet = workbook.add_worksheet()
    
    cellformats = {}
    for i in range(len(field_names)):
        cellformat = workbook.add_format()
        cellformat.set_center_across()
        cellformats[i] = cellformat
        worksheet.write_string( 0, i, field_names[i], cellformats[i])
        field_sizes[i] = len(field_names[i]) + 10

    row = 1
    for p in sorted(parts.keys()):
        pieces = sorted(parts[p], key=natural_keys)
        designators = ",".join(pieces)
    
        worksheet.write_string( row, 0, designators, cellformats[0])
        worksheet.write_string( row, 1, p, cellformats[1])
        worksheet.write_number( row, 2, len(pieces), cellformats[2])
        worksheet.write_url( row, 3, partslink[p], cellformats[3])

        if len(designators) > field_sizes[0]:
            field_sizes[0] = len(designators)
        if len(p) > field_sizes[1]:
            field_sizes[1] = len(p)
        if len(partslink[p]) > field_sizes[3]:
            field_sizes[3] = len(partslink[p])

        row += 1

    for i in range(len(field_sizes)):
        worksheet.set_column( i, i, field_sizes[i])
        
    workbook.close()
    
    
"""    
    with open("{}.csv".format(output_file_slug), 'w') as csvfile:
        bomwriter = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        bomwriter.writeheader()
        for p in sorted(parts.keys()):
            pieces = sorted(parts[p], key=natural_keys)
            designators = ",".join(pieces)
            bomwriter.writerow({'Designator': designators,
                                'MPN/Seeed SKU': p,
                                'Qty': len(pieces),
                                'Link': partslink[p]})
"""

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    components, links, missing = parse_kicad_xml(input_file)
    write_bom_seeed(output_file, components, links)
    if len(missing) > 0:
        print("** Warning **: there were parts with missing SKU/MPN")
        print(missing)
