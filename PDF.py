from pypdf import PdfReader


class PDF:
    def __init__(self, path):
        self.path = path
        self.pdf = PdfReader(self.path)

    def get_outline(self):
        outline = self.pdf.named_destinations
        return outline

    def get_text(self):
        text = self.pdf.pages[0].extract_text()
        return text

if __name__ == '__main__':
    pdf = PDF('contract2.pdf')
    print(pdf.get_text())
    
