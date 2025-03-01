import xml.etree.ElementTree as ET
import pandas as pd
import sys

def get_text(element):
    """Extracts text content from an XML element."""
    return "".join(element.itertext()).strip()

def search_xml(file_path, search_term, case_sensitive):
    """Searches for a term in the XML file and extracts relevant table data with cell IDs."""
    # Load the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespace mapping for parsing
    ns = {
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    }

    formatted_results = []
    search_term_cmp = search_term if case_sensitive else search_term.lower()

    # Iterate through all tables and their rows
    for table in root.findall('.//table:table', ns):
        table_name = table.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name', 'Unknown')
        for row_idx, row in enumerate(table.findall('.//table:table-row', ns), start=1):
            for col_idx, cell in enumerate(row.findall('.//table:table-cell', ns), start=1):
                cell_text = get_text(cell)
                cell_text_cmp = cell_text if case_sensitive else cell_text.lower()
                
                if search_term_cmp in cell_text_cmp:  # Search for the term in the content
                    cell_id = f"{chr(64 + col_idx)}{row_idx}"  # Convert column index to letter (A, B, C...)
                    formatted_results.append((cell_text, table_name, cell_id))

    # Convert results to DataFrame and display
    df = pd.DataFrame(formatted_results, columns=["Found Text", "In Table", "Cell ID"])
    print(df.to_string(index=False))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file.xml> <search_term> <case_sensitive: yes/no>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    search_term = sys.argv[2]
    case_sensitive = sys.argv[3].lower() == 'yes'
    
    search_xml(file_path, search_term, case_sensitive)
