# -*- coding: utf-8 -*-
import os
import urllib.request
import time
from supabase import create_client, Client
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# Load from environment variables
SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing environment variables! Create .env.local")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def download_fonts():
    fonts = {
        'DejaVuSans.ttf': 'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf',
        'DejaVuSans-Bold.ttf': 'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf'
    }
    for filename, dl_url in fonts.items():
        if not os.path.exists(filename):
            print(f"Pobieranie fontu {filename}...")
            urllib.request.urlretrieve(dl_url, filename)

def draw_header_footer(c, width, height, page_num):
    c.setFont('DejaVuSans', 9)
    c.setFillColor(HexColor("#64748b"))
    c.drawString(50, 30, f"AquaStart – Premium | Strona {page_num}")

def generate_aquastart_premium():
    download_fonts()
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
    
    timestamp = int(time.time())
    filename = f"AquaStart_Przewodnik_Premium_{timestamp}.pdf"
    
    print(f"📋 Generating PDF: {filename}")
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # PAGE 1: COVER
    c.setFillColor(HexColor("#0284c7"))
    c.rect(0, height - 120, width, 120, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont('DejaVuSans-Bold', 32)
    c.drawString(50, height - 75, "AquaStart")
    c.setFillColor(HexColor("#0f172a"))
    c.setFont('DejaVuSans-Bold', 26)
    c.drawString(50, height - 200, "Przewodnik: Parametry Wody")
    c.setFont('DejaVuSans', 14)
    c.setFillColor(HexColor("#475569"))
    c.drawString(50, height - 240, "Kompleksowe kompendium dla wymagających akwarystów")
    draw_header_footer(c, width, height, 1)
    c.showPage()
    
    # PAGE 2: CONTENT
    c.setFillColor(HexColor("#0f172a"))
    c.setFont('DejaVuSans-Bold', 18)
    c.drawString(50, height - 80, "1. Kluczowe parametry i związki chemiczne")
    c.setFont('DejaVuSans', 11)
    
    text_lines = [
        "W profesjonalnej akwarystyce „Złota zasada" mówi o bezwzględnej równowadze.",
        "Zakresy temperatur optymalnych wynoszą 24°C – 26°C.",
        "Wpływ na florę mają podstawowe gazy i jony → to absolutna podstawa.",
        "",
        "Najważniejsze związki do ciągłego monitorowania:",
        "• Amoniak (NH₃) – wysoce toksyczny w zasadowym pH.",
        "• Dwutlenek węgla (CO₂) – niezbędny do prawidłowego wzrostu roślin.",
        "• Azotyny (NO₂) – skrajnie niebezpieczne dla fauny dennej."
    ]
    
    y = height - 130
    for line in text_lines:
        if line.startswith("•"):
            c.setFont('DejaVuSans-Bold', 11)
            c.setFillColor(HexColor("#0f172a"))
        else:
            c.setFont('DejaVuSans', 11)
            c.setFillColor(HexColor("#334155"))
        c.drawString(50, y, line)
        y -= 22
        
    draw_header_footer(c, width, height, 2)
    c.save()
    print(f"✅ PDF generated: {filename}")
    
    # Upload to Supabase Storage
    print("📤 Uploading to Supabase Storage...")
    try:
        with open(filename, 'rb') as f:
            supabase.storage.from_("publications").upload(
                file=f,
                path=filename,
                file_options={"content-type": "application/pdf"}
            )
        print("✅ Uploaded to Storage")
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return
    
    # Get public URL
    try:
        public_url = supabase.storage.from_("publications").get_public_url(filename)
        print(f"✅ Public URL: {public_url}")
    except Exception as e:
        print(f"❌ URL error: {e}")
        return
    
    # Insert into database
    try:
        supabase.table('pdf_publications').insert({
            "title": "AquaStart Przewodnik Premium",
            "type": "Przewodnik",
            "file_url": public_url
        }).execute()
        print(f"✅ Entry added to pdf_publications")
        print(f"🎊 Done! URL: {public_url}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

if __name__ == "__main__":
    generate_aquastart_premium()
