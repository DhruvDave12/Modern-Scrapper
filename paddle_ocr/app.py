import json
import numpy as np
from paddleocr import PaddleOCR, PPStructure
from bs4 import BeautifulSoup

class Document:
    
    def __init__(self):
        self._pages = {}
        self._doc_meta = {
            "ip_doc_path": "",
            "ip_doc_name": "",
            "ip_doc_type": ""
        }

    def create_obj(self, pages, doc_meta):
        self._pages = pages
        self._doc_meta = doc_meta

    def __str__(self):
        s = "\nDocument\n==========\n"

        for p_no, p_content in self._pages.items():
            s = s + "\nPage Number: {}\n==========\n".format(p_no)
            s = s + str(p_content) + "\n\n"
        return s

    @property
    def pages(self):
        return self._pages

    @property
    def doc_meta(self):
        return self._doc_meta

class Page:
    
    def __init__(self):
        self._text = ""
        self._lines = []
        self._tables = []
        self._kv_pairs = []
        self._qa_pairs = []
        self._id = ""
        self._bbox = BoundingBox(0, 0, 0, 0)

    def create_obj(self, id, bbox, text, lines, tables, kv_pairs, qa_pairs):
        self._id = id
        self._bbox = bbox
        self._text = text
        self._lines = lines
        self._tables = tables
        self._kv_pairs = kv_pairs
        self._qa_pairs = qa_pairs

    def __str__(self):
        s = "Page\n==========\n"
        for line in self._lines:
            s = s + str(line) + "\n"

        s = s + "\nTables\n==========\n"
        for table in self._tables:
            s = s + str(table) + "\n"

        s = s + "\nKey Value Pairs\n==========\n"
        for kv in self._kv_pairs:
            s = s + str(kv) + "\n\n"

        s = s + "\nQuestion Answer Pairs\n==========\n"
        for query in self._qa_pairs:
            s = s + str(query) + "\n\n"

        return s

    @property
    def text(self):
        return self._text

    @property
    def lines(self):
        return self._lines

    @property
    def tables(self):
        return self._tables

    @property
    def kv_pairs(self):
        return self._kv_pairs

    @property
    def qa_pairs(self):
        return self._qa_pairs

    @property
    def bbox(self):
        return self._bbox

    @property
    def id(self):
        return self._id
    
class Row:
    
    def __init__(self):
        self._cells = []

    def create_obj(self, cells):
        self._cells = cells

    def __str__(self):
        s = ""
        for cell in self._cells:
            s = s + "[{}]".format(str(cell))
        return s

    @property
    def cells(self):
        return self._cells


class Table:

    def __init__(self):
        self._rows = []
        self._header_row = None
        self._merged_cells = []
        self._id = ""
        self._confidence = None
        self._bbox = BoundingBox(0, 0, 0, 0)

    def create_obj(self, id, bbox, rows, header_row, merged_cells, confidence):
        self._rows = rows
        self._header_row = header_row
        self._merged_cells = merged_cells
        self._id = id
        self._bbox = bbox
        self._confidence = confidence

    def __str__(self):
        s = "Table\n==========\n"
        for row in self._rows:
            s = s + "Row\n==========\n"
            s = s + str(row) + "\n"

        s = s + "\nHeader Row\n==========\n"
        s = s + str(self._header_row) + "\n"

        s = s + "\nMerged Cells Info\n==========\n"
        for mc in self._merged_cells:
            s = s + str(mc) + "\n"

        return s

    @property
    def id(self):
        return self._id

    @property
    def rows(self):
        return self._rows

    @property
    def merged_cells(self):
        return self._merged_cells

    @property
    def header_row(self):
        return self._header_row

    @property
    def bbox(self):
        return self._bbox

    @property
    def confidence(self):
        return self._confidence

class BoundingBox:
    def __init__(self, width, height, left, top):
        self._width = width
        self._height = height
        self._left = left
        self._top = top

    def __str__(self):
        return "width: {}, height: {}, left: {}, top: {}".format(self._width,
                                                                 self._height,
                                                                 self._left,
                                                                 self._top)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top


class Word:

    def __init__(self):
        self._id = ""
        self._text = ""
        self._text_type = None
        self._confidence = None
        self._bbox = BoundingBox(0, 0, 0, 0)

    def create_obj(self, id, bbox, text, text_type, confidence):
        self._id = id
        self._bbox = bbox
        self._text = text
        self._text_type = text_type
        self._confidence = confidence

    def __str__(self):
        return self._text

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def text_type(self):
        return self._text_type

    @property
    def bbox(self):
        return self._bbox

    @property
    def confidence(self):
        return self._confidence


class Line:

    def __init__(self):
        self._id = ""
        self._text = ""
        self._words = []
        self._confidence = None
        self._bbox = BoundingBox(0, 0, 0, 0)

    def create_obj(self, id, bbox, text, words, confidence):
        self._id = id
        self._bbox = bbox
        self._text = text
        self._words = words
        self._confidence = confidence

    def __str__(self):
        s = "Line\n==========\n"
        s = s + self._text + "\n"
        s = s + "Words\n----------\n"
        for word in self._words:
            s = s + "[{}]".format(str(word))
        return s

    @property
    def id(self):
        return self._id

    @property
    def words(self):
        return self._words

    @property
    def text(self):
        return self._text

    @property
    def bbox(self):
        return self._bbox

    @property
    def confidence(self):
        return self._confidence


class Cell:

    def __init__(self):
        self._row_index = -1
        self._column_index = -1
        self._bbox = BoundingBox(0, 0, 0, 0)
        self._id = ""
        self._text = ""
        self._confidence = None

    def create_obj(self, id, text, bbox, row_index, column_index, confidence):
        self._row_index = row_index
        self._column_index = column_index
        self._bbox = bbox
        self._id = id
        self._text = text
        self._confidence = confidence

    def __str__(self):
        return self._text

    @property
    def row_index(self):
        return self._row_index

    @property
    def column_index(self):
        return self._column_index

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def bbox(self):
        return self._bbox

    @property
    def confidence(self):
        return self._confidence



# Confirmed from here
# https://github.com/PaddlePaddle/PaddleOCR/blob/44316ac7fded076889e6b916b39a9b984c719c74/ppstructure/kie/tools/eval_with_label_end2end.py#LL100C3-L100C3
def __populateBoundingBox(bbox):
    return BoundingBox(bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[3])

def __populateBoundingPolygon(bbox):
    # ACCEPTS A LIST OF 8 ELEMENTS
    return BoundingBox(abs(bbox[0]-bbox[2]), abs(bbox[5]-bbox[3]), bbox[0], bbox[7])

def __extract_words_from_line(line, wordid):
    words = []
    print("LINE: ", line)
    bhards = line[1][0].split(" ")
    print("BHARDS: ", bhards)
    for word in bhards:
        print("W: ",word)
        word_obj = Word()
        word_obj._id = wordid
        word_obj._text = word
        words.append(word_obj)
        wordid += 1
    print("\n\n")
    return words

def __extract_table_from_page(image_layout, tableid):
    tables = []
    for components in image_layout:
        print(components)
        if(components['type'] == 'table'):
            table = Table()
            table._id = tableid
            tableid += 1
            # TODO -> DISCUSS THIS VERSION OF BOUNDING BOX
            table._bbox = __populateBoundingBox(components['bbox'])
            rows = []
            print("REC RES: ", len(components['res']['rec_res']))
            print("CELL_BBOX: ", len(components['res']['cell_bbox']))
            print("REC RES: ", components['res']['rec_res'])
            
            # total occurence of pattern <tr> in html string
            total_rows = components['res']['html'].count('<tr>')
            total_cells = components['res']['html'].count('<td>')
            print("Total Rows: ", total_rows)
            print("Total Cells: ", total_cells)
            total_cells_in_row = int(total_cells / total_rows)
            cellid = 0
            
            for rowidx in range(total_rows):
                row = Row()
                cells = []
                for cellidx in range(total_cells_in_row):
                    cell = Cell()
                    cell._id = cellid
                    cell._bbox = __populateBoundingPolygon(components['res']['cell_bbox'][cellid])
                    cell._column_index = cellidx
                    cell._row_index = rowidx
                    cell._confidence = components['res']['rec_res'][cellid][1]
                    cell._text = components['res']['rec_res'][cellid][0]
                    cells.append(cell)
                    cellid += 1
                
                row._cells = cells
                rows.append(row)
            
            table._rows = rows
            # header row is the row where the html contains <thead> tag
            is_header_in_table = components['res']['html'].find('<thead>') != -1
            if is_header_in_table:
                table._header_row = rows[0]
        
            tables.append(table)
    
    return tables  


def map_html_to_table(html: str, rec_res: list[tuple[str, float]], cell_bbox: list[list[int]]):
    print("HTML: ", html)
    soup = BeautifulSoup(html)
    table = soup.find('table')
    data = []
    # getting the header rows
    index = 0
    temp_rec_res = rec_res
    for header_row in table.find('thead').find_all('tr'):
        obj = {
            'type': 'header_row',
            'row_index': index,
            'data': []
        }
        index += 1
        cell_idx = 0
        for header_cell_content in header_row.find_all('td'):
            if(header_cell_content.text.strip() == ''): continue
            cell_obj = {
                'type': 'header_cell',
                'column_index': cell_idx,
                'row_index': index,
                'cell_content': header_cell_content.text.strip()
            }
            cell_idx += 1
            # find the match in rec_res
            found_direct_match = False
            for idx in range(len(temp_rec_res)):
                if(temp_rec_res[idx][0] == header_cell_content.text.strip()):
                    cell_obj['confidence'] = temp_rec_res[idx][1]
                    cell_obj['bbox'] = cell_bbox[idx]
                    found_direct_match = True
                    temp_rec_res[idx] = ('', 0)
                    break
                
            # TODO -> HANDLE THIS CASE WHEN WE DONT HAVE A DIRECT MATCH
            if found_direct_match == False:
                # means we dont have bbox and confidence 
                cell_obj['confidence'] = 0
                cell_obj['bbox'] = None    

            obj["data"].append(cell_obj)
        
        data.append(obj)
    
    index = 0
    
    print("REC RES: ", rec_res)
    # now we will get the rows simillarly
    table_body = table.find('tbody')
    for row in table_body.find_all('tr'):
        obj = {
            'type': 'row',
            'row_index': index,
            'data': []
        }
        index += 1
        cell_idx = 0
        for cell_content in row.find_all('td'):
            if(cell_content.text.strip() == ''): continue
            
            # TODO -> HANDLE THIS CASE WHEN WE HAVE SPAN ATTIIBUTE IN HTML FOR A CELL
            # if cell_content.has_attr('rowspan') or cell_content.has_attr('colspan'):
                
            cell_obj = {
                'type': 'cell',
                'cell_content': cell_content.text.strip(),
                'column_index': cell_idx,
                'row_index': index, 
            }
            found_direct_match = False
            for idx in range(len(temp_rec_res)):
                if(temp_rec_res[idx][0] == cell_content.text.strip()):
                    cell_obj['confidence'] = temp_rec_res[idx][1]
                    cell_obj['bbox'] = cell_bbox[idx]
                    found_direct_match = True
                    temp_rec_res[idx] = ('', 0)
                    break
            
            if found_direct_match is False:
                # means we dont have bbox and confidence 
                cell_obj['confidence'] = 0
                cell_obj['bbox'] = None    

            obj["data"].append(cell_obj)
        data.append(obj)
    
    return data

def _extract_table_from_page(image_layout, tableid):
    tables = []
    
    for components in image_layout:
        if(components['type'] == 'table'):
            table = Table()
            table._id = tableid
            tableid += 1
            table._bbox = __populateBoundingBox(components['bbox'])
            rows = []
            header_rows = []
            
            table_html = components['res']['html']
            rec_res = components['res']['rec_res']
            boxes = components['res']['boxes']
            cell_bbox = components['res']['cell_bbox']
            
            row_wise_data = map_html_to_table(table_html, rec_res, boxes)

            for row in row_wise_data:
                required_row_format = Row()
                cells_in_row = []
                for cell in row.get('data'):
                    required_cell_format = Cell()
                    required_cell_format._text = cell.get('cell_content')
                    required_cell_format._confidence = cell.get('confidence')
                    if cell.get('bbox') is not None:
                        required_cell_format._bbox = __populateBoundingBox(cell.get('bbox'))
                    required_cell_format._row_index = cell.get('row_index')
                    required_cell_format._column_index = cell.get('column_index')
                    cells_in_row.append(required_cell_format)
                
                required_row_format._cells = cells_in_row
                if row.get('type') == 'header_row':
                    header_rows.append(required_row_format)
                else: 
                    rows.append(required_row_format)
            
            table._rows = rows
            table._header_row = header_rows
            tables.append(table)
    
    return tables
                        
ocr_model = PaddleOCR(use_angle_cls=True, lang="en")
pp_structure_model = PPStructure(show_log=True)

# MAIN FUNCTION THAT USES PADDLEOCR TO EXTRACT USEFUL DATA FROM THE IMAGE
def get_machine_readable_document(img_path):
    machine_document = Document()
    pages = []
    page = Page()
    lineid = 1
    wordid = 1
    tableid = 1
    
 
    result = ocr_model.ocr(img_path, cls=True)
    print("RESULT: ", result)
    image_layout = pp_structure_model(img_path,return_ocr_result_in_table=True)
    
    # TODO -> MAKE IT WORD LEVEL
    for idx in range(len(result)):
        lines = []
        res = result[idx]
        for line in res:
            print(line[1][0])
            line_obj = Line()
            line_obj._id = lineid
            words_in_line = __extract_words_from_line(line, wordid)
            # print("WORDS IN LINE: ", words_in_line)
            line_obj._confidence = line[1][1]
            list_of_coords = []
            for coord in line[0]:
                list_of_coords.append(coord[0])
                list_of_coords.append(coord[1])
            line_obj._bbox = __populateBoundingPolygon(list_of_coords)
            line_obj._text = line[1][0]
            line_obj._words = words_in_line
            lines.append(line_obj)
            lineid += 1
        page._lines = lines
        
    tables = _extract_table_from_page(image_layout, tableid)
    # __extract_table_paddle(image_layout, tableid)
    # tables_in_page = __extract_table_from_page(image_layout, tableid)
    page._tables = tables
    pages.append(page)    
    
    # TODO -> READ MORE ABOUT HOW WE CAN USE KIE TO EXTRACT KEY VALUE PAIRS
    # run the kie to get key value pairs    
    
    machine_document._pages = pages
    return machine_document
                    

# MAIN EXECUTION CALL FOR THE PADDLE OCR SCRIPT
if __name__ == "__main__":
    # CURRENTLY SUPPORTS ONLY STRUCTURED DATA I.E., TABLE EXTRACTION
    
    # image_bytes = open('test_image_semi.png', 'rb').read()
    image_bytes = open('tester.png', 'rb').read()
    
    machine_document = get_machine_readable_document(image_bytes)

    # Printing linewise data
    for page in machine_document.pages:
        for line in page.lines:
            print(line.text, end=" ")
            print(line.confidence)
            
    print("\n\n")
    
    
    # PRINTING THE TABLE FROM THIS DOCUMENT
    for page in machine_document.pages:
        print(page)
                
                
                
# {
# 'type': 'table', 
# 'bbox': [49, 316, 644, 390], -> BOUDING BOX CORRESPONDING TO BOTTOM LEFT AND TOP RIGHT COORDINATES
# 'img': array([[[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255]],

#        [[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255]],

#        [[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255]],

#        ...,

#        [[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255]],

#        [[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255]],

#        [[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...,
#         [255, 255, 255],
#         [255, 255, 255],
        # [255, 255, 255]]], 
        # dtype=uint8), 
        
# 'res': {'cell_bbox': [
                        # [134.73117065429688, 4.547006607055664, 176.3472137451172, 4.637653827667236, 175.59619140625, 17.164764404296875, 132.33419799804688, 17.014131546020508], 
                        # [392.7130432128906, 4.050057888031006, 469.4200134277344, 4.085495471954346, 467.6061096191406, 17.242145538330078, 390.98626708984375, 17.31422996520996], 
                        # [175.4239959716797, 21.830659866333008, 166.6536102294922, 21.697250366210938, 166.81759643554688, 34.193885803222656, 173.4441375732422, 34.37847137451172], 
                        # [440.2635803222656, 21.45237159729004, 452.3863525390625, 21.376155853271484, 450.8210144042969, 34.97297286987305, 438.17120361328125, 35.10542297363281], 
                        # [170.8258819580078, 36.483482360839844, 173.2439727783203, 36.7409782409668, 172.18856811523438, 49.48451232910156, 169.79640197753906, 49.23167419433594], 
                        # [442.6731872558594, 37.41398620605469, 449.9951171875, 37.48476791381836, 450.18328857421875, 50.453758239746094, 442.3849792480469, 50.411415100097656], 
                        # [162.6781463623047, 54.95498275756836, 174.8602752685547, 55.128082275390625, 176.51622009277344, 68.08387756347656, 163.97372436523438, 67.96549987792969], 
                        # [432.8999328613281, 55.21455383300781, 452.54071044921875, 55.405723571777344, 449.9870910644531, 68.24555969238281, 430.4668884277344, 68.16956329345703]
                    # ], 
        # 'boxes': [
                    # [124.0, 4.0, 182.0, 22.0], 
                    # [410.0, 4.0, 471.0, 22.0], 
                    # [147.0, 20.0, 161.0, 41.0], 
                    # [433.0, 20.0, 447.0, 40.0], 
                    # [146.0, 36.0, 161.0, 57.0], 
                    # [433.0, 35.0, 447.0, 57.0], 
                    # [147.0, 53.0, 161.0, 74.0], 
                    # [433.0, 52.0, 446.0, 74.0]
                  # ], 
        # 'rec_res': [
                # ('Column 1', 0.9186647534370422), 
                # ('Column 2', 0.9403901696205139), 
                # ('A', 0.9735663533210754), 
                # ('D', 0.9364280700683594), 
                # ('B', 0.9187546968460083), 
                # ('E', 0.39264994859695435), 
                # ('C', 0.5448295474052429), 
                # ('F', 0.9723163843154907)
            # ], 
        # 'html': '<html><body><table><thead><tr><td>Column 1</td><td>Column 2</td></tr></thead><tbody><tr><td>A</td><td>D</td></tr><tr><td>B</td><td>E</td></tr><tr><td>C</td><td>F</td></tr></tbody></table></body></html>'}, 
        # 'img_idx': 0}
        
        
        
# TODO -> 1. HANDLE THE MERGED CELL SCENARIO WHERE IN DIRECT MATCH IS NOT AVAILABLE
# TODO -> 2. IF NEEDED THEN REMOVE THE TABLE BBOX FROM THE LINES WE EXTRACT
# TODO -> 3. WORD LEVEL BBOX, CURRENT VERSION HAS LINE LEVEL BBOX


# CURRENT VERSION

# 1. Line Level Detection i.e., we dont have bounding box for each word.
# 2. We have done only table extraction where in the merged cell i.e., direct match not found case is not handled percisely.