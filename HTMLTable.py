DEFAULT_TABLE_STYLE = {
    'font-family': 'Microsoft YaHei',
    'border-collapse': 'collapse'
}

def style_to_css(style_sheet):
    text = ''.join([f'{key}: {value};' for key, value in style_sheet.items()])
    return f'style="{text}"'

class TableCell(object):
    def __init__(self, text, x, y, set_header=False, style_sheet={}) -> None:
        self.text = text
        self.x, self.y = x, y
        self.cell_type = 'th' if (x == 0 and set_header) else 'td'
        assert isinstance(style_sheet, dict)
        self.style_sheet = style_sheet
    
    def set_style(self, key, value):
        self.style_sheet[key] = value

    def get_style(self, key):
        return self.style_sheet[key]

    def set_style_sheet(self, style_sheet):
        assert isinstance(style_sheet, dict)
        self.style_sheet = style_sheet

    def get_style_sheet(self):
        return self.style_sheet.copy()

    def clear_style_sheet(self):
        self.style_sheet = {}

    def style_to_css(self):
        return style_to_css(self.style_sheet)
    
    def text_to_str(self):
        #TODO: data type handling
        return str(self.text)
    
    def to_html(self):
        return f'\t<{self.cell_type}{" " + self.style_to_css() if self.style_sheet else ""}>' + \
            f'{self.text_to_str()}</{self.cell_type}>\n'

    def __str__(self) -> str:
        return f'{super().__str__()}\n' + \
            f'Cell: ({self.x}, {self.y})\n' + \
            f'Content: {self.text}\n' + \
            f'Style sheet: {self.style_sheet}'

class Table(object):
    def __init__(self, data, set_header=False, caption='', caption_style_sheet={}) -> None:
        assert isinstance(data, list)
        
        self.cells = []
        self.caption = caption
        self.caption_style_sheet = caption_style_sheet
        self.n_row, self.n_col = len(data), None
        
        for i, row in enumerate(data):
            assert isinstance(row, list)
            self.cells.append([TableCell(cell, i, j, set_header) for j, cell in enumerate(row)])
            if self.n_col is None:
                self.n_col = len(row)
            else:
                assert self.n_col == len(row)

    def get_cell(self, x, y):
        return self.cells[x][y]

    def set_style(self, key, value):
        for row in self.cells:
            for cell in row:
                cell.set_style(key, value)

    def set_style_sheet(self, style_sheet):
        for row in self.cells:
            for cell in row:
                cell.set_style_sheet(style_sheet)

    def set_row_style(self, row, key, value):
        for cell in self.cells[row]:
            cell.set_style(key, value)

    def set_row_style_sheet(self, row, style_sheet):
        for cell in self.cells[row]:
            cell.set_style_sheet(style_sheet)

    def set_col_style(self, col, key, value):
        for i in range(self.n_row):
            self.cells[i][col].set_style(key, value)

    def set_col_style_sheet(self, col, style_sheet):
        for i in range(self.n_row):
            self.cells[i][col].set_style_sheet(style_sheet)

    def clear_style_sheet(self):
        for row in self.cells:
            for cell in row:
                cell.clear_style_sheet()
    
    def to_html(self, table_style_sheet=None):
        text = f'<table {style_to_css(DEFAULT_TABLE_STYLE) if not table_style_sheet else table_style_sheet}>\n'
        text += '<tbody>\n'
        for row in self.cells:
            row_text = ''.join([cell.to_html() for cell in row])
            text += f'<tr>\n{row_text}</tr>\n'
        text += '</tbody>\n</table>\n'
        
        return text

    def to_svg(self, width, height):
        return '<svg xmlns="http://www.w3.org/2000/svg">' + \
            f'<foreignObject width="{width}" height="{height}">' + \
            '<body xmlns="http://www.w3.org/1999/xhtml">' + \
            self.to_html() + \
            '</body>' + \
            '</foreignObject>' + \
            '</svg>'

    def __str__(self) -> str:
        return f'{super().__str__()}\n' + \
            f'Table: {self.n_row} x {self.n_col}'

class Style(object):
    @staticmethod
    def apply(table: Table):
        pass

class GridStyle(Style):
    @staticmethod
    def apply(table: Table, w=1):
        style_sheet = {
            'border-top': f'solid {w}px',
            'border-bottom': f'solid {w}px',
            'border-left': f'solid {w}px',
            'border-right': f'solid {w}px',
        }
        table.set_style_sheet(style_sheet)

class APAStyle(Style):
    @staticmethod
    def apply(table: Table, w1=2, w2=1):
        table.set_row_style_sheet(0, {
            'border-top': f'solid {w1}px',
            'text-align': 'center',
            'font-weight': 'bold'
        })
        table.set_row_style_sheet(1, {'border-top': f'solid {w2}px'})
        table.set_row_style_sheet(table.n_row - 1, {'border-bottom': f'solid {w1}px'})
        table.set_style('padding-right', '6px')

"""
Example of usage:

from HTMLTable import Table, APAStyle
data = [['name', 'ad'], ['aa', 'ddd'], ['ff', 'ddd']]
t = Table(data)
APAStyle.apply(t)
print(t.to_html())
"""