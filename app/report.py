import pandas as pd

from app import db
from app.events import get_event
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate


def generate_report(eid, columns, filter_by, filter_by_eq, sort_by, order):
    column_names = {'KSUID': 'student.KSUID AS "KSU ID"', 'LastName': 'student.LastName AS "Last Name"',
                    'FirstName': 'student.FirstName AS "First Name"', 'EmailAddress': 'student.EmailAddress AS "Email"',
                    'ClassRank': 'student.ClassRank AS "Class Rank"', 'MajorName': 'major.MajorName AS "Major"',
                    'Department': 'major.Department'}

    event = get_event(eid).first()
    what = ', '.join([column_names[column] for column in columns])
    sort = column_names[sort_by].split(' ')[0]

    sql = "SELECT "+what+" FROM attendance INNER JOIN student ON attendance.KSUID = student.KSUID " \
          "LEFT JOIN major ON student.MajorID = major.MajorID WHERE attendance.EventID = "+str(eid)+" "

    if filter_by:
        col = column_names[filter_by].split(' ')[0]
        sql += "AND "+col+(" LIKE '"+filter_by_eq+"%' " if filter_by_eq else " IS NULL ")

    sql += "ORDER BY "+sort+" "+order+";"

    df = pd.read_sql_query(sql, db.engine)
    rows = len(df.index)
    df.loc[rows] = ['']*(len(df.columns)-1) + ['Count: '+str(rows)]

    generate_html(df, event)
    generate_excel(df, event)
    generate_pdf(df, event)


# HTML table view
def generate_html(df, event):
    html = '<h5>'+event.event_name+' ('+event.get_date()+')<br>Event Attendance Report</h5>'
    html += df.to_html(classes='table table-striped table-bordered', index=False)
    out = ''
    for line in html.split('\r'):
        out += line.replace('<td>None</td>', '<td>-----</td>')+'\r'
    with open('app/reports/report.html', 'w') as f:
        f.write(out)


# Excel view
def generate_excel(df, event):
    writer = pd.ExcelWriter('app/reports/report.xlsx', engine='xlsxwriter')
    sheet_name = 'Attendance Report'
    df.to_excel(writer, sheet_name=sheet_name, index=False, startcol=0, startrow=3)
    worksheet = writer.sheets[sheet_name]

    widths = [max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])] + \
             [max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns]

    for i, width in enumerate(widths):
        worksheet.set_column(i-1, i-1, width+5)

    worksheet.write(1, 0, event.event_name+' ('+event.get_date()+') Event Attendance Report')
    writer.save()


# PDF view
def generate_pdf(df, event):
    doc = SimpleDocTemplate('app/reports/report.pdf', pagesize=landscape(letter))

    elements = []
    styles = getSampleStyleSheet()
    data = [df.columns.to_list()]
    for value in df.values:
        data.append([Paragraph(x, styles['Normal']) if x else Paragraph('-----', styles['Normal']) for x in value])

    cell_size = 22.86*cm/len(df.columns)
    table = Table(data, [cell_size, cell_size], repeatRows=1)
    table.hAlign = 'LEFT'
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    elements.append(Paragraph(event.event_name+' ('+event.get_date()+') Event Attendance Report', styles['Heading2']))
    elements.append(Paragraph('', styles['Normal']))
    elements.append(table)
    doc.build(elements)
