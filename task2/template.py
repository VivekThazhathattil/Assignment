from pylatex import Document, Package, Command, Head,\
     Foot, PageStyle, UnsafeCommand, MiniPage
from pylatex.utils import NoEscape, italic 
from pylatex.base_classes import CommandBase, Arguments
from copy import deepcopy

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

def get_escaped_template_string(conf):
    result = r"\begin{tblr}{"

    if conf['vlines'] is not None and conf['vlines']: result += r"vlines,"
    if conf['hlines'] is not None and conf['hlines']: result += r"hlines,"

    def_rows_height_align = "rows={" + conf['rows_default_height'] + ", " + conf['rows_default_align'] + "},"
    result += fr"{def_rows_height_align}"

    def_cols_width_align = "columns={" + conf['cols_default_width'] + ", " + conf['cols_default_align'] + "},"
    result += fr"{def_cols_width_align}"

    if conf['modify_rows'] is not None:
        temp = ""
        for row in conf['modify_rows']:
            temp += "row{" + str(row[0]) + "} = {" + row[1] + "},"
        result += fr"{temp}"

    if conf['modify_cols'] is not None:
        temp = ""
        for col in conf['modify_cols']:
            temp += "column{" + str(col[0]) + "} = {" + col[1] + "},"
        result += fr"{temp}"

    if conf['modify_hlines'] is not None:
        temp = "hline{"
        for entry in conf['modify_hlines']:
            temp += str(entry) + ","
        temp = temp[:-1] + "},"
        result += fr"{temp}"

    if conf['modify_vlines'] is not None:
        temp = "vline{" 
        for entry in conf['modify_vlines']:
            temp += str(entry) + ","
        temp = temp[:-1] + "},"
        result += fr"{temp}"

    if conf['stretch'] is not None:
        temp = "stretch = " + conf['stretch']
        result += fr"{temp}"

    result += r"""}
        {#1} & {#2} & {#3} \\ 
        {#4} & {#5} & {#6} \\
        {#7} & {#8} & {#9} \\ 
        \end{tblr}
    """
    return result

def add_table_templates(doc):
    def_config = {
        'vlines' : True,
        'hlines' : True,
        'rows_default_align' : 'm',
        'rows_default_height' : '1.5cm',
        'cols_default_width' : '3cm',
        'cols_default_align' : 'c',
        'modify_rows' : [
            [1, '1.5cm, h, rowsep=5pt'],
            [3, '1.5cm, f, rowsep=5pt'],
        ],
        'modify_cols' : [
            [1, '3cm, l, colsep=5pt'],
            [3, '3cm, r, colsep=5pt'],
        ],
        'modify_hlines' : None,
        'modify_vlines' : None,
        'stretch' : '0'
    }

    config1 = deepcopy(def_config)

    config2 = deepcopy(def_config)
    config2['cols_default_width'] = '7cm'
    config2['modify_cols'] = [
        [1, '1cm, l, colsep=5pt'],
        [3, '1cm, r, colsep=5pt'],
    ]

    config3 = deepcopy(config2)
    config3['hlines'] = False
    config3['vlines'] = False
    config3['modify_vlines'] = [2,3]

    config4 = deepcopy(def_config)
    config4['vlines'] = False

    table_data = [
        [
            '\\tableAllBorder',
            get_escaped_template_string(config1),
        ],
        [
            '\\tableBigMid',
            get_escaped_template_string(config2),
        ],
        [
            '\\tableVBorder',
            get_escaped_template_string(config3),
        ],
        [
            '\\tableHBorder',
            get_escaped_template_string(config4),
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