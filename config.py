"""VELOCITY LONGFORM - 16:9 chapter lesson, brand and motion constants."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_DIR = BASE_DIR / "output"
LESSONS_DIR = OUTPUT_DIR / "lessons"
HISTORY_DIR = OUTPUT_DIR / "history"
SCENE_DIR = BASE_DIR / "scene"

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30

TARGET_CHAPTERS = 8
PHRASES_PER_CHAPTER = 7
TARGET_PHRASES = TARGET_CHAPTERS * PHRASES_PER_CHAPTER

# ---------------------------------------------------------------- brand

BRAND = "VELOCITY JAPANESE"
BRAND_LOCKUP_TOP = "VELOCITY"
BRAND_LOCKUP_BOTTOM = "JAPANESE"
HANDLE = "@velocityjapanese"
MASCOT_NAME = "Velo"

# ==== LANGUAGE PACK START ====
LANGUAGE = {'code': 'ja',
 'name': 'Japanese',
 'native_name': '日本語',
 'history_key': 'japanese',
 'english_voice': 'en-US-AvaNeural',
 'english_fallback_voice': 'en-US-GuyNeural',
 'native_voice': 'ja-JP-NanamiNeural',
 'native_fallback_voice': 'ja-JP-KeitaNeural',
 'native_engine': 'edge',
 'native_lang_code': 'ja',
 'english_rate': '-4%',
 'native_rate': '-10%',
 'english_pitch': '+0Hz',
 'native_pitch': '+0Hz',
 'native_label': '日本語',
 'translit_label': 'ROMAJI',
 'flag': 'jp',
 'greeting': 'こんにちは!',
 'encouragement': 'すごい!',
 'rtl': False,
 'char_tiles': True,
 'script_font': 'Script.ttf',
 'glyphs': 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'}
# ==== LANGUAGE PACK END ====

# ==== CATEGORIES START ====
CATEGORIES = {'Motivation': 'モチベーション',
 'Love': '愛',
 'Success': '成功',
 'Wisdom': '知恵',
 'Happiness': '幸せ',
 'Self Improvement': '自己啓発',
 'Gratitude': '感謝',
 'Friendship': '友情',
 'Hope': '希望',
 'Creativity': '創造性',
 'Inner Peace': '心の平和',
 'Confidence': '自信',
 'Perseverance': '忍耐',
 'Inspiration': 'インスピレーション',
 'Positive Life': 'ポジティブな人生',
 'Courage': '勇気',
 'Kindness': '親切',
 'Patience': '忍耐',
 'Forgiveness': '許し',
 'Strength': '強さ',
 'Joy': '喜び',
 'Balance': 'バランス',
 'Growth': '成長',
 'Purpose': '目的',
 'Mindfulness': 'マインドフルネス',
 'Travel & Airport': '旅行と空港',
 'Ordering Food & Dining': '食事の注文と外食',
 'Shopping & Prices': '買い物と値段',
 'Asking for Directions': '道を聞く',
 'Hotel & Accommodation': 'ホテルと宿泊',
 'Daily Routine': '日々のルーティン',
 'Meeting People & Greetings': '人と会う・挨拶',
 'Emergency & Health': '緊急事態と健康',
 'Public Transportation': '公共交通機関',
 'Work & Office': '仕事とオフィス',
 'Weather & Small Talk': '天気と雑談',
 'Coffee Shop & Bakery': 'カフェとパン屋',
 'Family & Home': '家族と家庭',
 'Hobbies & Free Time': '趣味と自由時間',
 'Dating & Romance': 'デートと恋愛',
 'Phone Calls & Messages': '電話とメッセージ',
 'Banking & Money': '銀行と金銭',
 'Doctor & Pharmacy': '医者と薬局',
 'Sports & Fitness': 'スポーツとフィットネス',
 'Celebrations & Parties': 'お祝いとパーティー',
 'Feelings & Emotions': '感情',
 'Agreeing & Disagreeing': '賛成と反対',
 'Making Plans': '計画を立てる',
 'Common Native Slang': '一般的なネイティブスラング',
 'Cultural Traditions': '文化的な伝統'}
# ==== CATEGORIES END ====

CATEGORY_NAMES = list(CATEGORIES.keys())

AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-5.4-nano")
AI_FALLBACK_MODEL = os.getenv("AI_FALLBACK_MODEL", "gemini-fast")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

# ---------------------------------------------------------------- timing (seconds)

INTRO_DURATION = 7.2
CHAPTER_INTRO_DURATION = 4.4
OUTRO_DURATION = 13.0

EN_CARD_IN = 0.70
GAP_EN_NATIVE = 0.60
NATIVE_CARD_LEAD = 0.40
GAP_BEFORE_REPEAT = 1.00
TAIL_HOLD = 1.30

# ---------------------------------------------------------------- palette

INK = "#30303A"
MUTED = "#8A8A8A"
CREAM = "#FFF8E7"
GREEN = "#58CC02"
GREEN_DARK = "#46A302"
GREEN_DEEP = "#3D8F00"
BLUE = "#1CB0F6"
PURPLE = "#7C5CFF"
ORANGE = "#FF7A00"
RED = "#FF4B4B"
YELLOW = "#F5A700"
TEAL = "#00A889"
PINK = "#E056A0"

# ==== HASHTAGS START ====
HASHTAGS = ['#learnjapanese',
 '#japaneselessons',
 '#japaneseforbeginners',
 '#languagelearning',
 '#japanesevocabulary',
 '#velocityjapanese',
 '#dailyjapanese',
 '#japanese',
 '#learnlanguages',
 '#speakjapanese']
# ==== HASHTAGS END ====
