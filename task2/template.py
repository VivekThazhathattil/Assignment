from pylatex import Document, Package, Section,\
    Subsection, Command, Head, Foot, PageStyle, LargeText,\
    simple_page_number, UnsafeCommand, Tabular, Tabu, MiniPage, Figure
from pylatex.utils import NoEscape, italic 
from pylatex.base_classes import CommandBase, Arguments

def set_preamble(doc):
    doc.documentclass = Command(
            'documentclass',
            options=['12pt', 'landscape'],
            arguments=['article'],
    )
    doc.packages.append(Package('geometry', options=['a4paper','hmargin=0.5cm','bottom=25mm','height=180mm','includehead']))
    doc.packages.append(Package('noto', options=['sfdefault']))
    doc.packages.append(Package('graphicx'))

def set_header_and_footer(doc):
    header = PageStyle('header', header_thickness=1, footer_thickness=1)
    with header.create(Head('C')):
        header.append('Learn Basics LaTeX Training')
    with header.create(Foot('C')):
        header.append('Learn Basics LaTeX Training')
    with header.create(Foot('R')):
        header.append('08-06-2022')
    doc.preamble.append(header)
    doc.change_document_style('header')
    doc.append(NoEscape(
        r"""
        \lhead{\includegraphics[width=1.2cm]{logo_learn_basics.png}}
        """
    ))

class Table_All_Border(CommandBase):
    _latex_name = 'tableAllBorder'
    packages = [Package('tabularray')]

class Table_Big_Mid(CommandBase):
    _latex_name = 'tableBigMid'
    packages = [Package('tabularray')]

class Table_H_Border(CommandBase):
    _latex_name = 'tableHBorder'
    packages = [Package('tabularray')]

class Table_V_Border(CommandBase):
    _latex_name = 'tableVBorder'
    packages = [Package('tabularray')]

def add_table_templates(doc):
    table_data = [
        [
            '\\tableAllBorder',
            r"""
            \begin{tblr}
            {
                vlines,
                hlines,
                rows = {1.5cm, m},
                columns={3cm, c},
                row{1} = {1.5cm, h, rowsep=5pt},
                row{3} = {1.5cm, f, rowsep=5pt},
                column{1} = {3cm, l, colsep=5pt},
                column{3} = {3cm, r, colsep=5pt},
                stretch = 0,
            }
            {#1} & {#2} & {#3} \\ 
            {#4} & {#5} & {#6} \\
            {#7} & {#8} & {#9} \\ 
            \end{tblr}
            """
        ],
        [
            '\\tableBigMid',
            r"""
            \begin{tblr}
            {
                vlines,
                hlines,
                rows = {1.5cm, m},
                columns={7cm, c},
                row{1} = {1.5cm, h, rowsep=5pt},
                row{3} = {1.5cm, f, rowsep=5pt},
                column{1} = {1cm, l, colsep=5pt},
                column{3} = {1cm, r, colsep=5pt},
                stretch = 0,
            }
            {#1} & {#2} & {#3} \\ 
            {#4} & {#5} & {#6} \\
            {#7} & {#8} & {#9} \\ 
            \end{tblr}
            """
        ],
        [
            '\\tableVBorder',
            r"""
            \begin{tblr}
            {
                vline{2,3},
                rows = {1.5cm, m},
                columns={7cm, c},
                row{1} = {1.5cm, h, rowsep=5pt},
                row{3} = {1.5cm, f, rowsep=5pt},
                column{1} = {1cm, l, colsep=5pt},
                column{3} = {1cm, r, colsep=5pt},
                stretch = 0,
            }
            {#1} & {#2} & {#3} \\ 
            {#4} & {#5} & {#6} \\
            {#7} & {#8} & {#9} \\ 
            \end{tblr}
            """
        ],
        [
            '\\tableHBorder',
            r"""
            \begin{tblr}
            {
                hlines,
                rows = {1.5cm, m},
                columns={3cm, c},
                row{1} = {1.5cm, h, rowsep=5pt},
                row{3} = {1.5cm, f, rowsep=5pt},
                column{1} = {3cm, l, colsep=5pt},
                column{3} = {3cm, r, colsep=5pt},
                stretch = 0,
            }
            {#1} & {#2} & {#3} \\ 
            {#4} & {#5} & {#6} \\
            {#7} & {#8} & {#9} \\ 
            \end{tblr}
            """
        ],
    ]

    for table in table_data:            
        new_table_command = UnsafeCommand('newcommand', table[0], options=9, extra_arguments= NoEscape(table[1]))
        doc.append(new_table_command)

if __name__ == '__main__':
    doc = Document('basic')
    set_preamble(doc)
    set_header_and_footer(doc)
    add_table_templates(doc)

    sample_data = [str(j) + "x" + str(i) for j in range(1,4) for i in range(1,4)]
    tables_to_append = [
        Table_All_Border(arguments=Arguments(sample_data)),
        Table_H_Border(arguments=Arguments(sample_data)),
        Table_Big_Mid(arguments=Arguments(sample_data)),
        Table_V_Border(arguments=Arguments(sample_data)),
    ]

    hrule_inserted = False

    for i in range(2):
        with doc.create(MiniPage(width=r'0.9\textwidth')):
            for j in range(2):
                doc.append(NoEscape(r'\vspace{1cm}'))
                with doc.create(MiniPage(width=r'0.4\textwidth', height=r'0.35\textheight', pos='t', content_pos='c')):
                    doc.append(tables_to_append[2*i + j])
                doc.append(NoEscape(r'\hfill'))
        if not hrule_inserted:
            doc.append(NoEscape(r'\hrule'))
            hrule_inserted = True
    doc.generate_pdf('test_pylatex', clean_tex=False)
    doc.generate_tex()
