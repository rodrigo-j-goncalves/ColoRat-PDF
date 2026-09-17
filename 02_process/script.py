"""
ColoRat-PDF: splits each PDF in 01_input/ into color-pages / B&W-pages PDFs
plus a summary PDF, all written to 03_output/.

Run directly:
    python script.py

Rodrigo J. Gonçalves

"""

import os

import PyPDF2
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
inputDir = os.path.join(BASE_DIR, '..', '01_input')
outputDir = os.path.join(BASE_DIR, '..', '03_output')
tempDir = os.path.join(BASE_DIR, 'temp')
os.makedirs(tempDir, exist_ok=True)

cant_colors = 256


def is_colored_page(image_path):
  """Determines if a page is colored based on color count."""
  img = Image.open(image_path)
  img = img.convert('RGB')
  # getcolors returns None when unique colors exceed maxcolors, avoiding a full pixel scan
  colors = img.getcolors(maxcolors=cant_colors)
  is_color = colors is None
  print(f'Color page: {is_color}')
  return is_color


def make_summary_pdf(output_path, fields, page_size=(1654, 2339), font_size=30, margin_frac=0.08):
  """Creates a single-page PDF listing top-aligned 'Label: value' fields."""
  width, height = page_size
  img = Image.new('RGB', (width, height), (255, 255, 255))
  draw = ImageDraw.Draw(img)
  try:
    font = ImageFont.load_default(size=font_size)
  except TypeError:
    font = ImageFont.load_default()

  margin = int(width * margin_frac)
  max_width = width - 2 * margin
  line_height = int(font_size * 1.6)
  y = margin

  for label, value in fields:
    text = f'{label}: {value}'
    words = text.split(' ')
    lines, current = [], ''
    for word in words:
      candidate = f'{current} {word}'.strip()
      if draw.textlength(candidate, font=font) <= max_width:
        current = candidate
      else:
        lines.append(current)
        current = word
    lines.append(current)

    for line in lines:
      draw.text((margin, y), line, fill=(0, 0, 0), font=font)
      y += line_height
    y += line_height // 2

  img.save(output_path, format='PDF')


def split_pdf(input_file, output_dir):
  """Splits a PDF into color and B&W pages, plus a summary PDF.

  Writes <name>-summary.pdf always, <name>_color_pages.pdf only if color
  pages were found, and <name>_bw_pages.pdf only if B&W pages were found.
  On a fatal error (e.g. unreadable PDF), only the summary is written, with
  the error recorded in its Notes field.
  """
  filename = os.path.basename(input_file)
  name = os.path.splitext(filename)[0]
  summary_path = os.path.join(output_dir, f'{name}-summary.pdf')
  color_path = os.path.join(output_dir, f'{name}_color_pages.pdf')
  bw_path = os.path.join(output_dir, f'{name}_bw_pages.pdf')

  total_pages = 0
  color_count = 0
  bw_count = 0
  color_written = False
  bw_written = False
  notes = 'No errors, all good.'

  try:
    with open(input_file, 'rb') as f:
      pdf_reader = PyPDF2.PdfReader(f)
      color_writer = PyPDF2.PdfWriter()
      bw_writer = PyPDF2.PdfWriter()

      total_pages = len(pdf_reader.pages)
      num_digits = len(str(total_pages))
      print(f'Number of pages: {total_pages} ({num_digits} digits)')

      for page_num in range(total_pages):
        print(f'\n-------------\nProcessing {input_file}, page {page_num+1}/{total_pages}')

        page = pdf_reader.pages[page_num]
        image_prefix = 'page_num-'

        convert_from_path(input_file,
                          dpi=300,
                          output_folder=tempDir,
                          output_file=image_prefix,
                          first_page=page_num + 1,
                          last_page=page_num + 1,
                          fmt='jpg',
                          paths_only=True)

        print('Conversion done.')

        padded = str(page_num + 1).zfill(num_digits)
        old = os.path.join(tempDir, image_prefix + '0001-' + padded + '.jpg')
        new_image_path = os.path.join(tempDir, f'temp_page_{page_num}.jpg')

        print(f'Rename: {old} --->> {new_image_path}')
        os.rename(old, new_image_path)

        if is_colored_page(new_image_path):
          color_writer.add_page(page)
        else:
          bw_writer.add_page(page)

        os.remove(new_image_path)

      color_count = len(color_writer.pages)
      bw_count = len(bw_writer.pages)

      if color_count > 0:
        with open(color_path, 'wb') as cf:
          color_writer.write(cf)
        color_written = True

      if bw_count > 0:
        with open(bw_path, 'wb') as bf:
          bw_writer.write(bf)
        bw_written = True

  except Exception as e:
    notes = f'Error: {e}'
    print(f'ERROR processing {input_file}: {e}')

  bw_field = str(bw_count) + (f' ({os.path.basename(bw_path)})' if bw_written else '')
  color_field = str(color_count) + (f' ({os.path.basename(color_path)})' if color_written else '')

  make_summary_pdf(summary_path, [
    ('Filename', filename),
    ('Total pages', total_pages),
    ('Black and white pages', bw_field),
    ('Color pages', color_field),
    ('Notes', notes),
  ])


def main():
  # Main

  pdf_files = [f for f in os.listdir(inputDir) if f.endswith('.pdf')]
  print(f'{len(pdf_files)} PDF files in the input directory.\n')

  for pdf in pdf_files:
    input_pdf = os.path.join(inputDir, pdf)
    print(f'\n=============\nProcessing {input_pdf}')
    split_pdf(input_pdf, outputDir)


if __name__ == '__main__':
  main()
