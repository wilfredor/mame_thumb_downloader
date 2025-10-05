#!/usr/bin/env python3
import os, sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET

# Config
TYPES = ["Named_Boxarts", "Named_Titles", "Named_Snaps"]
BASES = [
    "https://thumbnails.libretro.com/MAME%202003-Plus",
    "https://thumbnails.libretro.com/MAME",
]
OUT_BASE = os.path.join(os.getcwd(), "thumbnails", "MAME")

# Util
def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return None

def sanitize_title(t:str)->str:
    for ch in ("®","™","©"):
        t = t.replace(ch,"")
    t = t.replace(":", " - ").replace("/", "-").replace("\\"," - ")
    t = t.replace("’","'").replace("“",'"').replace("”",'"')
    # compacta espacios
    return " ".join(t.split())

def urlq(s:str)->str:
    return urllib.parse.quote(s, safe="~._-")

# 1) ROMs en carpeta actual
roms = [f for f in os.listdir(".") if f.lower().endswith(".zip")]
if not roms:
    print("No hay .zip aquí.")
    sys.exit(1)

# 2) crea estructura de salida
for t in TYPES:
    os.makedirs(os.path.join(OUT_BASE, t), exist_ok=True)

# 3) descarga y construye mapa shortname -> título (mame2003-plus)
xml_url = "https://raw.githubusercontent.com/libretro/mame2003-plus-libretro/master/metadata/mame2003-plus.xml"
data = fetch(xml_url)
if not data:
    print("No pude descargar el mapa mame2003-plus.")
    sys.exit(1)

root = ET.fromstring(data)
short2title = {}
for g in root.findall(".//game"):
    k = g.attrib.get("name")
    d = g.findtext("description") or ""
    if k and d:
        short2title[k] = d

# 4) loop con progreso
total = len(roms) * len(TYPES)
done = 0

def show_progress():
    p = int(done * 100 / total) if total else 100
    print(f"Progreso: {p:3d}%", end="\r", flush=True)

found = 0

for rom in roms:
    short = os.path.splitext(rom)[0]
    for t in TYPES:
        dest = os.path.join(OUT_BASE, t, f"{short}.png")
        if os.path.exists(dest):
            done += 1
            show_progress()
            continue

        ok = False

        # A) intenta shortname directo en MAME 2003-Plus
        url = f"{BASES[0]}/{t}/{short}.png"
        blob = fetch(url)
        if blob:
            with open(dest, "wb") as f: f.write(blob)
            ok = True
        else:
            # B) por título en 2003-Plus y MAME (png/jpg)
            title = short2title.get(short, "")
            if title:
                clean = sanitize_title(title)
                enc = urlq(clean)
                for base in BASES:
                    if ok: break
                    for ext in ("png","jpg"):
                        url2 = f"{base}/{t}/{enc}.{ext}"
                        blob2 = fetch(url2)
                        if blob2:
                            with open(dest, "wb") as f: f.write(blob2)
                            ok = True
                            break

        if ok: found += 1
        done += 1
        show_progress()

# 5) resumen
print()  # salto de línea después del progreso
print(f"Descargadas: {found} de {total} posibles.")
print("Guardado en:")
for t in TYPES:
    print("  " + os.path.join(OUT_BASE, t))
