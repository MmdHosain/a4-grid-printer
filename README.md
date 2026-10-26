# A4 Grid Print Sheet Generator 🖨️📐

A Python utility that tiles images onto an **A4 print sheet** with millimeter precision and **zero quality loss**. Perfect for printing stickers, badges, photo tiles, or QR codes on glossy photo paper.

---

## ✨ Features

- **Zero Quality Loss**: Directly embeds the original JPEG byte stream into the vector PDF without decoding or re-compressing (DCT passthrough).
- **Exact Physical Dimensions**: Vector PDF generation guarantees exact millimeter dimensions ($2.7 \times 2.7\text{ cm}$ default) when printed at 100% scale.
- **Multiple Cutting Styles Generated**:
  1. **Clean + Crop Marks (Recommended)**: Seamless edge-to-edge tiles with professional crop marks in margins (no lines across artwork). Cleanest cut with a ruler & hobby knife.
  2. **With Cut Guides**: Seamless tiles with ultra-fine ($0.25\text{ pt}$) guide lines for easy scissor cutting.
  3. **Spaced Layout**: $1.5\text{ mm}$ spacing between tiles with individual bounding outlines for die-cutters or craft punches.
- **High-Resolution Raster Export**: Generates **300 DPI** and **600 DPI** PNG files for direct use in photo printing software.
- **Fully Configurable**: Tile size, row/column counts, spacing, and output directories can be customized via command-line arguments.

---

## 🚀 Quick Start

### 1. Installation

Ensure you have Python 3.8+ installed, then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Basic Usage

Place your image in the directory as `sample.jpg` and run:

```bash
python generate_print_sheet.py
```

All 5 output files will be saved in the `output/` directory:
- `A4_70x_2.7cm_Clean_CropMarks.pdf`
- `A4_70x_2.7cm_With_CutGuides.pdf`
- `A4_70x_2.7cm_Spaced_1.5mm.pdf`
- `A4_70x_2.7cm_PrintReady_300DPI.png`
- `A4_70x_2.7cm_PrintReady_600DPI.png`

---

## ⚙️ CLI Options & Customization

```bash
python generate_print_sheet.py [image_path] [options]
```

| Option | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `image` | — | `sample.jpg` | Path to source image file |
| `--output-dir` | `-o` | `output` | Directory where generated sheets are saved |
| `--size` | `-s` | `2.7` | Square tile size in centimeters (cm) |
| `--cols` | `-c` | `7` | Number of columns |
| `--rows` | `-r` | `10` | Number of rows |
| `--gap` | `-g` | `1.5` | Gap between tiles in millimeters for spaced PDF |
| `--no-raster` | — | `false` | Skip raster PNG generation (PDFs only) |

### Examples

**Custom image and 3x3 cm squares (6 cols x 8 rows = 48 copies):**
```bash
python generate_print_sheet.py my_art.jpg --size 3.0 --cols 6 --rows 8
```

**Generate only PDFs without high-res raster images:**
```bash
python generate_print_sheet.py logo.png --no-raster
```

---

## 🖨️ Recommended Print Settings

When printing on **glossy photo paper** or **colored paper**:

1. **Scale**: In the print dialog, select **Actual Size** (or **100%**).
   - ⚠️ **Do NOT select "Fit to Printable Area" or "Shrink to Fit"**, or the dimensions will be altered.
2. **Paper Type**: Choose **Glossy Photo Paper** in printer preferences.
3. **Quality**: Set to **High** / **Best**.
4. **Colored Glossy Paper**: Standard desktop printers do not print white ink. White or off-white areas of the artwork will take on the color and glossy sheen of your paper.

---

## 🇮🇷 راهنمای فارسی (Persian Guide)

این ابزار برای چیدن تصاویر در ابعاد دقیق میلی‌متری روی برگ **A4** (به ویژه برای پرینت ۷۰ عدد مربع ۲.۷×۲.۷ سانتیمتر در ۱۰ ردیف و ۷ ستون) بدون افت کیفیت ساخته شده است.

### خروجی‌ها و نحوه برش:
- **`A4_70x_2.7cm_Clean_CropMarks.pdf` (بهترین گزینه):** تصاویر کاملاً به هم چسبیده و بدون خط اضافه هستند؛ نشانه‌های برش فقط در حاشیه کاغذ چاپ می‌شوند. کافی است خط‌کش فلزی را روی علامت‌ها بگذارید و با کاتر برش مستقیم بزنید (با ۱۷ برش تمام ۷۰ قطعه جدا می‌شوند).
- **`A4_70x_2.7cm_With_CutGuides.pdf`:** دارای خطوط راهنمای بسیار نازک بین تصاویر؛ مناسب برای برش با قیچی.
- **`A4_70x_2.7cm_Spaced_1.5mm.pdf`:** دارای فاصله ۱.۵ میلی‌متری بین تصاویر؛ مناسب برای پانچ مربعی یا قالب دایکات.

### تنظیم پرینتر:
- در پنجره پرینت حتماً مقیاس را روی **Actual Size (100%)** بگذارید.
- جنس کاغذ را **Glossy Photo Paper** و کیفیت را **High** قرار دهید.

---

## 📜 License

[MIT License](LICENSE) © 2026 MmdHosain
