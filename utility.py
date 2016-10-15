import fpdf

# ---------------------------- Helper functions --------------------


def check_ace_predefined_words(word):
    predefined_list = ['on', 'off']

    if word is None:
        return 'Null'

    if isinstance(word, basestring):
        word = word.replace(" ", "")

        if word.lower() in predefined_list:
            return 'Data' + uppercase_first_letter(word)

    return uppercase_first_letter(word)


def uppercase_first_letter(s):
    if s is None:
        return 'Null'

    if isinstance(s, basestring) and len(s) > 0:
        return s[0].upper() + s[1:]
    return 'Null'


def clean_str(s):
    index = s.find('}')
    if index > 0:
        s = s[index + 1:]

    index = s.find(':')
    if index > 0:
        s = s[index + 1:]

    return s


class MyPDF(fpdf.FPDF):
    #def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
    #    self.set_font('Arial', 'B', 15)
        # Move to the right
    #    self.cell(80)
        # Title
   #     self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
   #     self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def init_pdf_parser():
    global my_pdf
    my_pdf = MyPDF()
    my_pdf.alias_nb_pages()
    my_pdf.add_page()


def my_pdf_set_report_title(file_name, translation_schema_mode):
    if translation_schema_mode == 1 or translation_schema_mode == 3:
        txt = 'English'
    else:
        txt = 'ACE'

    my_pdf.set_font('Arial', 'B', 15)
    my_pdf.cell(80)
    my_pdf.cell(30, 10, 'Generated report in ' + txt + ' for the AutoFocus3 model', 0, 2, 'C')
    my_pdf.cell(30, 5, file_name, 0, 0, 'C')
    my_pdf.ln(20)


def my_pdf_set_section_title(title):
    my_pdf_line_break(15)
    my_pdf.set_font('Times', 'B', 12)
    my_pdf.cell(50, 8, title, 1, 1, 'C')
    my_pdf.ln(5)


def my_pdf_append_text(text):
    my_pdf.set_font('Times', '', 12)
    if text is None:
        text = 'Invalid'
    #my_pdf.cell(0, 5, text, border=0, ln=1)
    my_pdf.write(5, text)
    my_pdf.ln(5)


def my_pdf_append_text_with_color(text, color):
    my_pdf_set_text_color(color)
    my_pdf.set_font('Times', '', 12)
    if text is None:
        text = 'Invalid'
    #my_pdf.cell(0, 5, text, border=0, ln=1)
    my_pdf.write(5, text)
    my_pdf.ln(5)
    my_pdf_set_text_color()


def my_pdf_export_file(file_name, schema_mode):
    if schema_mode == 1 or schema_mode == 3:
        mode = 'English'
    else:
        mode = 'ACE'

    file_name = file_name.split('.')[0] + '_' + mode + '.pdf'

    my_pdf.output(file_name, 'F')
    return file_name


def my_pdf_line_break(height=5):
    my_pdf.ln(height)


def my_pdf_line_break_with(symbol):
    my_pdf.set_font('Times', '', 12)
    text = ''
    for i in range(1, 30):
        text += symbol
    my_pdf.cell(0, 10, text, 0, 1, 'C')


def my_pdf_end_report(symbol):
    text = ''
    for i in range(1, 20):
        text += symbol
    text += ' End of report '
    for i in range(1, 20):
        text += symbol

    my_pdf.cell(0, 10, text, 0, 1, 'C')


def my_pdf_set_text_color(color='black'):
    if color == 'blue':
        my_pdf.set_text_color(0, 0, 255)
    else:
        my_pdf.set_text_color(0, 0, 0)


def split_name_id(text):
    return text.split(':::')
