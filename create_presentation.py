#!/usr/bin/env python3
"""
Generate a PDF presentation for the wooden pocket mirror product.
Pure Python — no external dependencies.

This creates a valid PDF file with:
- Product title and description
- Dimensions table
- Features list
- Pricing info
- Contact/order section
"""

import struct
import time
import math


class SimplePDF:
    """Minimal PDF generator — no dependencies."""

    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_page_content = []
        self.page_width = 595.28  # A4 width in points
        self.page_height = 841.89  # A4 height in points
        self.margin = 50
        self.y = self.page_height - self.margin
        self.font_size = 12
        self.fonts_used = set()

    def _escape(self, text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    def set_font_size(self, size):
        self.font_size = size
        self.current_page_content.append(f'/F1 {size} Tf')

    def add_text(self, text, x=None, size=None, bold=False):
        if x is None:
            x = self.margin
        if size:
            self.set_font_size(size)

        font = '/F2' if bold else '/F1'
        self.current_page_content.append(f'{font} {self.font_size} Tf')
        self.current_page_content.append(f'BT {x} {self.y} Td ({self._escape(text)}) Tj ET')
        self.y -= self.font_size * 1.4

    def add_line(self, x1, y1, x2, y2, width=0.5):
        self.current_page_content.append(f'{width} w {x1} {y1} m {x2} {y2} l S')

    def add_rect(self, x, y, w, h, fill=False, stroke=True, gray=0.9):
        ops = ''
        if fill:
            ops += f'{gray} g {x} {y} {w} {h} re f '
        if stroke:
            ops += f'0 g {x} {y} {w} {h} re S'
        self.current_page_content.append(ops)

    def newline(self, lines=1):
        self.y -= self.font_size * 1.4 * lines

    def new_page(self):
        if self.current_page_content:
            self.pages.append(self.current_page_content)
        self.current_page_content = []
        self.y = self.page_height - self.margin

    def check_page_break(self, needed=100):
        if self.y < self.margin + needed:
            self.new_page()

    def save(self, filename):
        self.pages.append(self.current_page_content)

        pdf_content = b'%PDF-1.4\n'
        offsets = []

        obj_num = 1

        # Object 1: Catalog
        offsets.append(len(pdf_content))
        pdf_content += f'{obj_num} 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'.encode('latin-1')
        obj_num += 1

        # Object 2: Pages
        page_obj_start = 3 + 2  # catalog + pages + 2 fonts
        page_refs = ' '.join(f'{page_obj_start + i*2} 0 R' for i in range(len(self.pages)))
        offsets.append(len(pdf_content))
        pdf_content += f'{obj_num} 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(self.pages)} >>\nendobj\n'.encode('latin-1')
        obj_num += 1

        # Object 3: Font (Helvetica)
        offsets.append(len(pdf_content))
        pdf_content += f'{obj_num} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n'.encode('latin-1')
        obj_num += 1

        # Object 4: Font Bold (Helvetica-Bold)
        offsets.append(len(pdf_content))
        pdf_content += f'{obj_num} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n'.encode('latin-1')
        obj_num += 1

        # Pages and their content streams
        for page_content in self.pages:
            stream_text = '\n'.join(page_content)
            stream_bytes = stream_text.encode('latin-1', errors='replace')
            stream_len = len(stream_bytes)

            # Page object
            offsets.append(len(pdf_content))
            pdf_content += (
                f'{obj_num} 0 obj\n'
                f'<< /Type /Page /Parent 2 0 R '
                f'/MediaBox [0 0 {self.page_width} {self.page_height}] '
                f'/Contents {obj_num+1} 0 R '
                f'/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> '
                f'>>\nendobj\n'
            ).encode('latin-1')
            obj_num += 1

            # Content stream
            offsets.append(len(pdf_content))
            pdf_content += f'{obj_num} 0 obj\n<< /Length {stream_len} >>\nstream\n'.encode('latin-1')
            pdf_content += stream_bytes
            pdf_content += b'\nendstream\nendobj\n'
            obj_num += 1

        # Cross-reference table
        xref_offset = len(pdf_content)
        pdf_content += b'xref\n'
        pdf_content += f'0 {obj_num}\n'.encode('latin-1')
        pdf_content += b'0000000000 65535 f \n'
        for offset in offsets:
            pdf_content += f'{offset:010d} 00000 n \n'.encode('latin-1')

        # Trailer
        pdf_content += (
            f'trailer\n<< /Size {obj_num} /Root 1 0 R >>\n'
            f'startxref\n{xref_offset}\n%%EOF\n'
        ).encode('latin-1')

        with open(filename, 'wb') as f:
            f.write(pdf_content)
        print(f'PDF saved: {filename} ({len(pdf_content)} bytes, {len(self.pages)} pages)')


def create_presentation():
    pdf = SimplePDF()

    # === PAGE 1: Title ===
    pdf.newline(2)

    # Header background
    pdf.add_rect(0, pdf.page_height - 200, pdf.page_width, 200, fill=True, gray=0.15)

    pdf.y = pdf.page_height - 80
    # Title (white on dark - simulated with font)
    pdf.current_page_content.append('1 g')  # white color
    pdf.add_text('POCKET MIRROR', x=50, size=36, bold=True)
    pdf.add_text('Handcrafted Wooden Compact Mirror', x=50, size=16)
    pdf.newline(1)
    pdf.add_text('Premium Gift | CNC Manufactured | Natural Walnut', x=50, size=12)
    pdf.current_page_content.append('0 g')  # back to black

    pdf.y = pdf.page_height - 250

    # Product description
    pdf.add_text('PRODUCT OVERVIEW', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 200, pdf.y + 10, 1)
    pdf.newline(1)

    pdf.add_text('Elegant round pocket mirror crafted from solid walnut wood.', size=12)
    pdf.add_text('Two halves connected by a brass barrel hinge with magnetic closure.', size=12)
    pdf.add_text('Inside: real glass mirror + personalized photo under acrylic.', size=12)
    pdf.newline(1)
    pdf.add_text('Perfect as:', size=12, bold=True)
    pdf.add_text('  - Premium gift for women (birthday, anniversary)', size=11)
    pdf.add_text('  - Wedding favors / bridesmaid gifts', size=11)
    pdf.add_text('  - Corporate branded gifts (with laser engraving)', size=11)
    pdf.add_text('  - Personalized keepsake with photo inside', size=11)

    pdf.newline(2)

    # Dimensions box
    pdf.add_text('DIMENSIONS', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 200, pdf.y + 10, 1)
    pdf.newline(1)

    dims = [
        ('Diameter', '70 mm'),
        ('Height (closed)', '16 mm'),
        ('Height (open)', '~85 mm'),
        ('Weight', '~45 g'),
        ('Mirror diameter', '58 mm'),
        ('Material', 'Solid Walnut'),
        ('Hinge', 'Brass barrel hinge'),
        ('Closure', 'Neodymium magnets'),
    ]

    col1_x = 60
    col2_x = 300
    for label, value in dims:
        pdf.add_text(label, x=col1_x, size=11)
        pdf.y += 11 * 1.4  # go back up
        pdf.add_text(value, x=col2_x, size=11, bold=True)

    # === PAGE 2: Features & Customization ===
    pdf.new_page()
    pdf.newline(1)
    pdf.add_text('FEATURES & QUALITY', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 250, pdf.y + 10, 1)
    pdf.newline(1)

    features = [
        'Solid walnut wood (not veneer, not plastic)',
        'CNC precision machined (tolerance +/- 0.1 mm)',
        'Hand-sanded to 400 grit smoothness',
        'Food-safe Danish oil finish',
        'Real glass mirror (not plastic film)',
        'Brass hardware (hinge + pin) — will patina beautifully',
        'Strong neodymium magnets — satisfying snap closure',
        'Fits in pocket, purse, or clutch',
        'Each piece is unique (natural wood grain)',
    ]

    for f in features:
        pdf.add_text(f'  + {f}', size=11)

    pdf.newline(2)
    pdf.add_text('CUSTOMIZATION OPTIONS', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 280, pdf.y + 10, 1)
    pdf.newline(1)

    customs = [
        ('Engraving on lid', 'Name, date, logo, monogram (laser or CNC)'),
        ('Photo inside', 'Customer provides image, printed on metal/paper'),
        ('Wood species', 'Walnut (dark), Oak (light), Cherry (warm)'),
        ('Mirror options', 'Regular mirror or magnifying (2x/5x)'),
        ('Gift box', 'Kraft box with ribbon, or premium wooden box'),
        ('Bulk branding', 'Company logo engraved for corporate orders'),
    ]

    for title, desc in customs:
        pdf.add_text(f'  {title}:', size=11, bold=True)
        pdf.add_text(f'      {desc}', size=10)
        pdf.newline(0.3)

    # === PAGE 3: Pricing & Order ===
    pdf.new_page()
    pdf.newline(1)
    pdf.add_text('PRICING', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 150, pdf.y + 10, 1)
    pdf.newline(1)

    pdf.add_text('Unit pricing (depends on quantity):', size=12)
    pdf.newline(1)

    # Price table
    prices = [
        ('Quantity', 'Price/unit', 'Engraving', 'Total example'),
        ('1-5 pcs', '$35-40', '+$5', '$40-45/pc'),
        ('10-25 pcs', '$28-32', '+$3', '$31-35/pc'),
        ('50-100 pcs', '$22-25', 'included', '$22-25/pc'),
        ('100+ pcs', '$18-20', 'included', '$18-20/pc'),
    ]

    col_xs = [60, 180, 300, 410]
    for row_idx, row in enumerate(prices):
        is_header = row_idx == 0
        for col_idx, cell in enumerate(row):
            pdf.add_text(cell, x=col_xs[col_idx], size=10 if not is_header else 10, bold=is_header)
            if col_idx < len(row) - 1:
                pdf.y += 10 * 1.4
        if is_header:
            pdf.add_line(50, pdf.y + 8, 530, pdf.y + 8, 0.5)
            pdf.newline(0.3)

    pdf.newline(1)
    pdf.add_text('* Prices include: material, CNC machining, finishing, hardware, assembly', size=9)
    pdf.add_text('* Shipping and packaging quoted separately', size=9)
    pdf.add_text('* Lead time: 5-7 days (1-25 pcs), 10-14 days (50+ pcs)', size=9)

    pdf.newline(2)
    pdf.add_text('COMPARISON WITH ALTERNATIVES', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 330, pdf.y + 10, 1)
    pdf.newline(1)

    comparisons = [
        ('Plastic compact (mass market)', '$3-8', 'Cheap feel, no personalization'),
        ('Metal compact (mid-range)', '$10-20', 'Cold, generic, no wood warmth'),
        ('THIS: Wood compact (premium)', '$25-40', 'Warm, unique, personalizable'),
        ('Luxury brand compact (Chanel etc)', '$80-200', 'Brand tax, not handcrafted'),
    ]

    for name, price, note in comparisons:
        pdf.add_text(f'  {name}', size=10, bold=True)
        pdf.y += 10 * 1.4
        pdf.add_text(f'{price}', x=350, size=10)
        pdf.add_text(f'      {note}', size=9)
        pdf.newline(0.3)

    pdf.newline(2)
    pdf.add_text('NEXT STEPS', size=18, bold=True)
    pdf.newline(0.5)
    pdf.add_line(50, pdf.y + 10, 180, pdf.y + 10, 1)
    pdf.newline(1)

    steps = [
        '1. Approve design and dimensions',
        '2. Choose wood species and finish',
        '3. Provide engraving artwork (if needed)',
        '4. Confirm quantity and delivery date',
        '5. Production starts (prototype in 2-3 days)',
    ]
    for s in steps:
        pdf.add_text(f'  {s}', size=11)

    pdf.newline(3)
    pdf.add_rect(40, pdf.y - 10, pdf.page_width - 80, 60, fill=True, gray=0.93)
    pdf.y += 35
    pdf.add_text('Ready to order? Contact us for a sample or custom quote.', x=60, size=12, bold=True)

    pdf.save('pocket_mirror_presentation.pdf')


if __name__ == '__main__':
    create_presentation()
