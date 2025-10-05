A small Python script to **download and name** RetroArch thumbnails for your MAME ROMs **without** running a RetroArch scan.

## What it does

1. Reads every `.zip` (ROM) in the **current folder**.
2. Tries thumbnails by **shortname** from **MAME 2003-Plus**.
3. If not found, maps `shortname → title` using the official `mame2003-plus.xml` and retries by **title** in:
   - **MAME 2003-Plus**
   - **MAME**
   (tries `.png`, then `.jpg`)
4. Saves images as **`<shortname>.png`** under RetroArch-like folders:
├─ Named_Boxarts/
├─ Named_Titles/
└─ Named_Snaps/
5. Shows a **percent progress** and a final **summary**.

## Requirements

- macOS or Linux
- **Python 3** (3.8+)
- **curl**
- Internet access

## Usage

Place `mame_thumbs.py` in the folder with your `.zip` ROMs, then:

```bash
python3 mame_thumbs.py
