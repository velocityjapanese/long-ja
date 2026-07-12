import os, io, base64, random
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SCENIC_STYLES = [
    "beautiful Japanese woman in traditional kimono standing in a serene Japanese garden with cherry blossoms, soft sunlight filtering through petals, peaceful atmosphere, cinematic 8K quality",
    "elegant Japanese woman in modern fashion walking through neon-lit Tokyo street at dusk with Mount Fuji in background, vibrant colors, cinematic lighting",
    "Japanese woman in red kimono holding a paper umbrella by a tranquil bamboo forest stream, morning mist, ethereal atmosphere, highly detailed",
    "portrait of a Japanese woman with serene expression in front of a torii gate during golden hour, warm sunlight, cherry blossom petals floating, cinematic",
    "Japanese woman dressed in elegant kimono overlooking a traditional Japanese temple at sunset, dramatic sky, wisteria flowers, ultra realistic",
    "beautiful Japanese woman in casual modern outfit at Shibuya crossing, dynamic cityscape, night neon lights reflecting on wet ground, cinematic mood",
    "Japanese woman in traditional attire meditating by a still lake with snow-capped Mount Fuji reflection, zen garden foreground, peaceful, high detail",
    "elegant Japanese woman in yukata at summer festival with fireworks illuminating the night sky, traditional lanterns, joyful atmosphere, vibrant colors",
]

FONT_PATHS = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/noto/NotoSans-Bold.ttf",
]

JAPANESE_FONT_PATHS = [
    "C:/Windows/Fonts/msgothic.ttc",
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/Meiryo.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]


def generate_scenic_image(category_english: str, category_japanese: str, output_path: str):
    if not OPENAI_API_KEY:
        return None

    style = random.choice(SCENIC_STYLES)
    prompt = (
        f"YouTube thumbnail for '{category_english}' Japanese language learning video. "
        f"{style}. "
        f"16:9 landscape aspect ratio. High contrast, vibrant colors suitable for YouTube thumbnail. "
        f"No text in the image."
    )

    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size="1792x1024",
            quality="high",
            n=1,
        )
        raw = None
        if resp.data[0].url:
            import requests
            raw = requests.get(resp.data[0].url, timeout=60).content
        elif resp.data[0].b64_json:
            raw = base64.b64decode(resp.data[0].b64_json)
        else:
            return None

        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img = img.resize((1920, 1080), Image.LANCZOS)
        overlay_text_on_thumbnail(img, category_english, category_japanese, output_path)
        return output_path
    except Exception as e:
        return None


def load_font(font_paths, size):
    for font_path in font_paths:
        if Path(font_path).exists():
            try: return ImageFont.truetype(font_path, size)
            except: continue
    return ImageFont.load_default()


def overlay_text_on_thumbnail(img, category_english, category_japanese, output_path):
    draw = ImageDraw.Draw(img)
    w, h = img.size

    font_hero = load_font(FONT_PATHS, 110)
    font_sub = load_font(FONT_PATHS, 64)
    font_cat_en = load_font(FONT_PATHS, 48)
    font_cat_ja = load_font(JAPANESE_FONT_PATHS, 56)
    font_brand = load_font(FONT_PATHS, 40)
    font_count = load_font(FONT_PATHS, 130)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.rectangle([(0, 0), (w, 180)], fill=(0, 0, 0, 160))
    overlay_draw.rectangle([(0, h - 120), (w, h)], fill=(0, 0, 0, 160))

    brand_text = "VELOCITY JAPANESE"
    bb = overlay_draw.textbbox((0, 0), brand_text, font=font_brand)
    overlay_draw.text(((w - (bb[2] - bb[0])) // 2, h - 85), brand_text, fill=(255, 210, 0), font=font_brand)

    count_text = "120 PHRASES"
    bb = overlay_draw.textbbox((0, 0), count_text, font=font_count)
    cx = (w - (bb[2] - bb[0])) // 2
    overlay_draw.rounded_rectangle(
        [cx - 30, 15, cx + (bb[2] - bb[0]) + 30, 155], radius=20, fill=(0, 0, 0, 200)
    )
    overlay_draw.text((cx + (bb[2] - bb[0]) // 2, 85), count_text, fill=(255, 210, 0), font=font_count, anchor="mm")

    cat_line = f"{category_english.upper()} | {category_japanese}"
    bb = overlay_draw.textbbox((0, 0), cat_line, font=font_cat_en)
    cx = (w - (bb[2] - bb[0])) // 2
    overlay_draw.rounded_rectangle(
        [cx - 25, h - 200 - 5, cx + (bb[2] - bb[0]) + 25, h - 200 + 65], radius=15, fill=(120, 40, 200, 220)
    )
    overlay_draw.text((cx + (bb[2] - bb[0]) // 2, h - 200 + 28), cat_line, fill=(255, 255, 255), font=font_cat_en, anchor="mm")

    sub_text = "Learn Japanese - 10 Minute Lesson"
    bb = overlay_draw.textbbox((0, 0), sub_text, font=font_sub)
    cx2 = (w - (bb[2] - bb[0])) // 2
    overlay_draw.text((cx2 + (bb[2] - bb[0]) // 2, h - 130), sub_text, fill=(200, 200, 200), font=font_sub, anchor="mm")

    background_overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(background_overlay)
    bg_draw.rectangle([(0, 0), (w, 15)], fill=(0, 0, 0, 0))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    thumb_bytes = io.BytesIO()
    quality = 85
    img.save(thumb_bytes, format="JPEG", quality=quality)
    while thumb_bytes.tell() > 2097152 and quality > 10:
        quality -= 10
        thumb_bytes = io.BytesIO()
        img.save(thumb_bytes, format="JPEG", quality=quality)
    thumb_bytes.seek(0)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(thumb_bytes.read())

    return output_path
