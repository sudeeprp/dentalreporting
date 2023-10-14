from docx.shared import RGBColor 
from docxtpl import DocxTemplate

tpl = DocxTemplate ('report_template.docx')

sd = tpl.new_subdoc ()
table = sd.add_table(rows=1, cols=5)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'NO Of Implants'
hdr_cells[1].text = 'Length'
hdr_cells[2].text = 'Head Diameter'
hdr_cells[3].text = 'Aptical Diameter'
hdr_cells[4].text = 'Any Remarks'


recordset = ((1, 50, '4.6', '2.8', 'R1'), (2, 42, '1.6', '3.2', 'Spam,spam, eggs, and ham'), (3, 42,'5','4.6', 'no implants'))
for item in recordset:
    row_cells = table.add_row().cells
    row_cells[0].text = str(item[0])
    row_cells[1].text = str(item[1])
    row_cells[2].text = item[2]
    row_cells[3].text = item[3]
    row_cells[4].text = item[4]

context = {
    'virtual_implant_table': sd,
}

tpl.render(context)
tpl.save('subdoc.docx')