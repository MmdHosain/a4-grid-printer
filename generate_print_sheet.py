#!/usr/bin/env python3
"""
A4 Grid Print Sheet Generator
==============================
Generates print-ready A4 sheets with tiled squares of any image with zero quality loss.
Ideal for printing stickers, badges, photo tiles, or QR codes on glossy photo paper.

Author: MmdHosain
License: MIT
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


def create_pdf_seamless(image_path, output_path, cols=7, rows=10, sq_size_cm=2.7, with_cutlines=False):
    """
    Creates an exact vector-dimensioned A4 PDF with contiguous squares (0 gap).
    Includes professional margin crop marks outside the printable artwork.
    If with_cutlines is True, also draws subtle hairline grid lines.
    """
    page_w, page_h = A4
    sq_size = sq_size_cm * cm
    grid_w = cols * sq_size
    grid_h = rows * sq_size

    if grid_w > page_w or grid_h > page_h:
        raise ValueError(
            f"Grid size ({grid_w/cm:.1f}x{grid_h/cm:.1f} cm) exceeds A4 page ({page_w/cm:.1f}x{page_h/cm:.1f} cm)!"
        )

    margin_x = (page_w - grid_w) / 2.0
    margin_y = (page_h - grid_h) / 2.0

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"A4 Print Sheet - {cols*rows}x {sq_size_cm}cm Squares")
    c.setAuthor("A4 Grid Print Sheet Generator")

    reader = ImageReader(image_path)

    # Place images (PDF coordinates: (0,0) is bottom-left)
    for r in range(rows):
        y = margin_y + (rows - 1 - r) * sq_size
        for col in range(cols):
            x = margin_x + col * sq_size
            c.drawImage(reader, x, y, width=sq_size, height=sq_size)

    # Optional hairline cut guides directly on grid lines
    if with_cutlines:
        c.setStrokeColor(colors.HexColor('#999999'))
        c.setLineWidth(0.25)
        for col_idx in range(cols + 1):
            x = margin_x + col_idx * sq_size
            c.line(x, margin_y, x, margin_y + grid_h)
        for row_idx in range(rows + 1):
            y = margin_y + row_idx * sq_size
            c.line(margin_x, y, margin_x + grid_w, y)

    # Professional outer margin crop marks (ticks)
    mark_len = 6.0 * mm
    mark_gap = 2.5 * mm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.4)

    # Vertical boundary crop marks (top and bottom margins)
    for col_idx in range(cols + 1):
        x = margin_x + col_idx * sq_size
        c.line(x, margin_y - mark_gap, x, margin_y - mark_gap - mark_len)
        c.line(x, margin_y + grid_h + mark_gap, x, margin_y + grid_h + mark_gap + mark_len)

    # Horizontal boundary crop marks (left and right margins)
    for row_idx in range(rows + 1):
        y = margin_y + row_idx * sq_size
        c.line(margin_x - mark_gap, y, margin_x - mark_gap - mark_len, y)
        c.line(margin_x + grid_w + mark_gap, y, margin_x + grid_w + mark_gap + mark_len, y)

    # Technical print info in margin
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#777777'))
    info = f"A4 Sheet | {cols*rows} Squares ({cols}x{rows}) | {sq_size_cm:.2f} x {sq_size_cm:.2f} cm | Scale: 100% Actual Size"
    c.drawString(margin_x, margin_y + grid_h + mark_gap + mark_len + 1.5 * mm, info)

    c.showPage()
    c.save()
    print(f"  [+] Created PDF: {output_path}")


def create_pdf_spaced(image_path, output_path, cols=7, rows=10, sq_size_cm=2.7, gap_mm=1.5):
    """
    Creates an A4 PDF with specified spacing between squares and a thin cut outline.
    Best suited for die-cutters or craft square punches.
    """
    page_w, page_h = A4
    sq_size = sq_size_cm * cm
    gap = gap_mm * mm
    grid_w = cols * sq_size + (cols - 1) * gap
    grid_h = rows * sq_size + (rows - 1) * gap

    if grid_w > page_w or grid_h > page_h:
        raise ValueError(
            f"Spaced grid size exceeds A4 page dimensions! Reduce spacing or square size."
        )

    margin_x = (page_w - grid_w) / 2.0
    margin_y = (page_h - grid_h) / 2.0

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"A4 Print Sheet - {cols*rows}x {sq_size_cm}cm Squares ({gap_mm}mm Spacing)")
    c.setAuthor("A4 Grid Print Sheet Generator")

    reader = ImageReader(image_path)
    c.setStrokeColor(colors.HexColor('#aaaaaa'))
    c.setLineWidth(0.25)

    for r in range(rows):
        y = margin_y + (rows - 1 - r) * (sq_size + gap)
        for col in range(cols):
            x = margin_x + col * (sq_size + gap)
            c.drawImage(reader, x, y, width=sq_size, height=sq_size)
            c.rect(x, y, sq_size, sq_size)

    # Technical print info
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#777777'))
    info = f"A4 Sheet | {cols*rows} Squares ({cols}x{rows}) | {sq_size_cm:.2f} cm | {gap_mm}mm Gap | Scale: 100% Actual Size"
    c.drawString(margin_x, margin_y + grid_h + 3.0 * mm, info)

    c.showPage()
    c.save()
    print(f"  [+] Created PDF (Spaced): {output_path}")


def create_raster_image(image_path, output_path, cols=7, rows=10, sq_size_cm=2.7, dpi=300):
    """
    Renders the A4 grid sheet into a high-resolution raster image (PNG) at specified DPI.
    """
    px_w = int(round(210.0 / 25.4 * dpi))
    px_h = int(round(297.0 / 25.4 * dpi))
    sq_px = int(round(sq_size_cm * 10.0 / 25.4 * dpi))

    grid_w = cols * sq_px
    grid_h = rows * sq_px

    margin_x = (px_w - grid_w) // 2
    margin_y = (px_h - grid_h) // 2

    img_sheet = Image.new("RGB", (px_w, px_h), (255, 255, 255))
    src = Image.open(image_path).convert("RGB")
    tile = src.resize((sq_px, sq_px), Image.Resampling.LANCZOS)

    for r in range(rows):
        y = margin_y + r * sq_px
        for col in range(cols):
            x = margin_x + col * sq_px
            img_sheet.paste(tile, (x, y))

    draw = ImageDraw.Draw(img_sheet)
    guide_color = (180, 180, 180)
    line_w = max(1, int(round(dpi / 300)))

    for c_idx in range(cols + 1):
        x = margin_x + c_idx * sq_px
        draw.line([(x, margin_y), (x, margin_y + grid_h)], fill=guide_color, width=line_w)
        mark_len = int(round(6.0 / 25.4 * dpi))
        mark_gap = int(round(2.5 / 25.4 * dpi))
        draw.line([(x, margin_y - mark_gap), (x, margin_y - mark_gap - mark_len)], fill=(0, 0, 0), width=line_w)
        draw.line([(x, margin_y + grid_h + mark_gap), (x, margin_y + grid_h + mark_gap + mark_len)], fill=(0, 0, 0), width=line_w)

    for r_idx in range(rows + 1):
        y = margin_y + r_idx * sq_px
        draw.line([(margin_x, y), (margin_x + grid_w, y)], fill=guide_color, width=line_w)
        mark_len = int(round(6.0 / 25.4 * dpi))
        mark_gap = int(round(2.5 / 25.4 * dpi))
        draw.line([(margin_x - mark_gap, y), (margin_x - mark_gap - mark_len, y)], fill=(0, 0, 0), width=line_w)
        draw.line([(margin_x + grid_w + mark_gap, y), (margin_x + grid_w + mark_gap + mark_len, y)], fill=(0, 0, 0), width=line_w)

    img_sheet.save(output_path, dpi=(dpi, dpi), quality=98)
    print(f"  [+] Created Image ({dpi} DPI): {output_path} ({px_w}x{px_h})")


def main():
    parser = argparse.ArgumentParser(
        description="Generate print-ready A4 sheets with 70 (or configurable) square image copies."
    )
    parser.add_argument(
        "image",
        nargs="?",
        default="sample.jpg",
        help="Path to source image file (default: sample.jpg)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="output",
        help="Output directory for generated files (default: output)",
    )
    parser.add_argument(
        "-s", "--size",
        type=float,
        default=2.7,
        help="Square tile size in centimeters (default: 2.7)",
    )
    parser.add_argument(
        "-c", "--cols",
        type=int,
        default=7,
        help="Number of columns (default: 7)",
    )
    parser.add_argument(
        "-r", "--rows",
        type=int,
        default=10,
        help="Number of rows (default: 10)",
    )
    parser.add_argument(
        "-g", "--gap",
        type=float,
        default=1.5,
        help="Gap in millimeters for spaced layout (default: 1.5)",
    )
    parser.add_argument(
        "--no-raster",
        action="store_true",
        help="Skip generating PNG raster images (generate PDFs only)",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print(f"Error: Input image file '{args.image}' not found.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    total_count = args.cols * args.rows

    print(f"Generating print sheets for '{args.image}':")
    print(f"  - Layout: {args.cols} cols x {args.rows} rows = {total_count} squares")
    print(f"  - Tile Size: {args.size} x {args.size} cm")
    print(f"  - Output Directory: {args.output_dir}\n")

    prefix = f"A4_{total_count}x_{args.size:.1f}cm"

    # 1. Seamless with outer margin crop marks (Recommended for guillotine / ruler)
    pdf_clean = os.path.join(args.output_dir, f"{prefix}_Clean_CropMarks.pdf")
    create_pdf_seamless(args.image, pdf_clean, cols=args.cols, rows=args.rows, sq_size_cm=args.size, with_cutlines=False)

    # 2. Seamless with subtle cut guide lines (Recommended for scissors)
    pdf_guides = os.path.join(args.output_dir, f"{prefix}_With_CutGuides.pdf")
    create_pdf_seamless(args.image, pdf_guides, cols=args.cols, rows=args.rows, sq_size_cm=args.size, with_cutlines=True)

    # 3. Spaced layout with individual borders
    pdf_spaced = os.path.join(args.output_dir, f"{prefix}_Spaced_{args.gap:.1f}mm.pdf")
    create_pdf_spaced(args.image, pdf_spaced, cols=args.cols, rows=args.rows, sq_size_cm=args.size, gap_mm=args.gap)

    # 4 & 5. High-res raster images
    if not args.no_raster:
        png_300 = os.path.join(args.output_dir, f"{prefix}_PrintReady_300DPI.png")
        create_raster_image(args.image, png_300, cols=args.cols, rows=args.rows, sq_size_cm=args.size, dpi=300)

        png_600 = os.path.join(args.output_dir, f"{prefix}_PrintReady_600DPI.png")
        create_raster_image(args.image, png_600, cols=args.cols, rows=args.rows, sq_size_cm=args.size, dpi=600)

    print("\n[Done] All print-ready sheets successfully generated!")


if __name__ == "__main__":
    main()
