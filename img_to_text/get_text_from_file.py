import pdfplumber


class TextGetter:

    def __init__(self, path):
        self.path = path

    def extract_table(self, page_num, box=None):
        pdf = pdfplumber.open(self.path)
        table_page = pdf.pages[page_num]
        if box:
            table_page = table_page.crop(box)
        if len(table_page.extract_tables()) > 0:
            return table_page.extract_tables()[0]
        else:
            return None

    def table_converter(self, table):
        table_string = ''

        for row_num in range(len(table)):
            row = table[row_num]
            cleaned_row = row[0]

            print(row)
            table_string += (''.join(cleaned_row))

        table_string = table_string[:-1]

        return table_string
