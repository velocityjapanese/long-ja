"""
Velocity Japanese - YouTube Long-Form Video Automation
Generates 10-minute videos (120 phrases) with AI thumbnails
Publishes 1x daily to YouTube
"""

import os, sys, json, random, asyncio, subprocess, time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")
if not AI_MODEL:
    raise ValueError("AI_MODEL not set!")

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
HISTORY_DIR = OUTPUT_DIR / "history"
LONGFORM_DIR = OUTPUT_DIR / "longform_videos"

for d in [OUTPUT_DIR, HISTORY_DIR, LONGFORM_DIR]:
    d.mkdir(exist_ok=True)

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
TARGET_PHRASES = 120
PHRASES_PER_BATCH = 30

LANGUAGES = {
    "Japanese": {"voice": "ja-JP-NanamiNeural", "label": "Japanese"},
}

ENGLISH_VOICE = "en-US-GuyNeural"

CATEGORIES = [
    "Motivation", "Love", "Success", "Wisdom", "Happiness",
    "Self Improvement", "Gratitude", "Friendship", "Hope", "Creativity",
    "Inner Peace", "Confidence", "Perseverance", "Inspiration", "Positive Life",
    "Courage", "Kindness", "Patience", "Forgiveness", "Strength",
    "Joy", "Balance", "Growth", "Purpose", "Mindfulness",
    "Greetings", "Basic Phrases", "Travel", "Food", "Daily Life",
]

CATEGORIES_JA = {
    "Motivation": "モチベーション", "Love": "愛", "Success": "成功",
    "Wisdom": "知恵", "Happiness": "幸せ", "Self Improvement": "自己啓発",
    "Gratitude": "感謝", "Friendship": "友情", "Hope": "希望",
    "Creativity": "創造性", "Inner Peace": "内なる平和", "Confidence": "自信",
    "Perseverance": "忍耐", "Inspiration": "インスピレーション", "Positive Life": "ポジティブな人生",
    "Courage": "勇気", "Kindness": "親切", "Patience": "忍耐強さ",
    "Forgiveness": "許し", "Strength": "強さ", "Joy": "喜び",
    "Balance": "バランス", "Growth": "成長", "Purpose": "目的",
    "Mindfulness": "マインドフルネス", "Greetings": "挨拶", "Basic Phrases": "基本フレーズ",
    "Travel": "旅行", "Food": "食べ物", "Daily Life": "日常生活",
}

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"
MAX_RECENT_CATEGORIES = 15

CATEGORY_HISTORY_FILE = HISTORY_DIR / "used_categories.json"


def load_json(path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_phrase_history():
    return load_json(PHRASE_HISTORY_FILE, {"phrases": [], "last_updated": None})


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    save_json(PHRASE_HISTORY_FILE, data)


def is_phrase_used(english_text):
    history = load_phrase_history()
    eng_lower = english_text.lower().strip()
    for p in history.get("phrases", []):
        if p.get("english", "").lower().strip() == eng_lower:
            return True
    return False


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    for p in phrases:
        history["phrases"].append({
            "english": p["english"], "japanese": p["japanese"],
            "category": category, "generated_at": datetime.now().isoformat()
        })
    save_phrase_history(history)
    print(f"[history] Added {len(phrases)} phrases (total: {len(history['phrases'])})")


def get_available_category():
    used = load_json(CATEGORY_HISTORY_FILE, {"categories": []})
    used_list = used.get("categories", [])

    remaining = [c for c in CATEGORIES if c not in used_list]
    if not remaining:
        used_list = []
        remaining = list(CATEGORIES)

    selected = random.choice(remaining)
    used_list.append(selected)
    save_json(CATEGORY_HISTORY_FILE, {"categories": used_list})
    return selected


def generate_phrases(category_english, num_phrases):
    category_japanese = CATEGORIES_JA[category_english]
    history = load_phrase_history()
    used_texts = [p.get("english", "") for p in history.get("phrases", [])]

    all_phrases = []
    batch_size = PHRASES_PER_BATCH
    max_attempts = 5
    ai_models = [AI_MODEL, "openai", "mistral", "llama"]
    viral_styles = [
        "surprising fact", "common mistake", "quick tip", "must-know",
        "cultural insight", "daily use", "travel essential", "fun expression"
    ]

    num_batches = (num_phrases + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        remaining = num_phrases - len(all_phrases)
        current_batch = min(batch_size, remaining)
        if current_batch <= 0:
            break

        style = random.choice(viral_styles)
        exclusion = ""
        if used_texts:
            recent = used_texts[-30:] if len(used_texts) > 30 else used_texts
            exclusion = f"\n\nAVOID these phrases: {recent}"

        acquired = False
        for attempt in range(max_attempts):
            if acquired:
                break
            for model in ai_models:
                if acquired:
                    break
                try:
                    import requests
                    url = "https://gen.pollinations.ai/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    prompt = f"""Create {current_batch * 2} unique {category_english} Japanese learning phrases.

Style: Make each feel like a {style}.

RULES:
1. SHORT phrases (5-12 words per language)
2. Natural pauses with commas
3. Speakable in 3-5 seconds
4. Simple, practical vocabulary
5. Vary sentence structure

Return JSON array: [{{"english": "...", "japanese": "...", "romaji": "..."}}]{exclusion}"""

                    resp = requests.post(url, json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a Japanese teacher creating viral YouTube content."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.9
                    }, headers=headers, timeout=90)

                    if resp.status_code != 200:
                        continue

                    content = resp.json()["choices"][0]["message"]["content"].strip()
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()

                    phrases = json.loads(content)
                    for p in phrases:
                        if len(all_phrases) >= num_phrases:
                            break
                        eng = p.get("english", "")
                        if len(eng.split()) <= 15 and not is_phrase_used(eng):
                            all_phrases.append(p)

                    if len(all_phrases) >= num_phrases:
                        acquired = True
                        print(f"[content] Batch {batch_num+1} via {model}")

                except Exception as e:
                    continue

            if not acquired:
                time.sleep(1)

    final = all_phrases[:num_phrases]
    if final:
        add_phrases_to_history(final, category_english)
    print(f"[content] Generated {len(final)} phrases")
    return final


async def generate_audio(text, voice, output_path):
    try:
        import edge_tts
        await edge_tts.Communicate(text, voice).save(output_path)
        return True
    except:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "2", output_path], capture_output=True)
        return False


def get_audio_duration(path):
    if not Path(path).exists():
        return 2.0
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 2.0


def generate_all_audio(phrases, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_files = []

    for i, p in enumerate(phrases):
        en_file = output_dir / f"en_{i}.mp3"
        ja_file = output_dir / f"ja_{i}.mp3"
        combined = output_dir / f"c_{i}.mp3"

        asyncio.run(generate_audio(p["english"], ENGLISH_VOICE, str(en_file)))
        asyncio.run(generate_audio(p["japanese"], "ja-JP-NanamiNeural", str(ja_file)))

        en_dur = get_audio_duration(str(en_file))
        ja_dur = get_audio_duration(str(ja_file))

        subprocess.run(["ffmpeg", "-y", "-i", str(en_file), "-i", str(ja_file),
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]", "-map", "[out]", str(combined)], capture_output=True)

        actual_dur = get_audio_duration(str(combined))
        audio_files.append({
            "index": i, "combined": str(combined), "duration": actual_dur,
            "en_duration": en_dur, "ja_duration": ja_dur
        })

        if (i + 1) % 20 == 0:
            print(f"  Audio {i+1}/{len(phrases)}...")

    return audio_files


def create_narration(audio_files, output_file):
    concat_file = Path(output_file).parent / "narration_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for a in audio_files:
            p = Path(a["combined"]).resolve().as_posix()
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c:a", "copy", output_file], capture_output=True)
    if concat_file.exists():
        concat_file.unlink()
    if Path(output_file).exists():
        print(f"[audio] Narration: {Path(output_file).name}")


def create_video(phrases, audio_files, final_audio, output_file, category):
    temp_clips = []
    for i, (p, a) in enumerate(zip(phrases, audio_files)):
        dur = a["duration"]
        temp = Path(output_file).parent / f"clip_{i:04d}.mp4"
        temp_clips.append(temp)

        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"color=c=0x2D2341:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d={dur}:r={FPS}",
            "-i", a["combined"],
            "-vf",
            f"drawtext=text='{p['english']}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-80:"
            f"fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':box=1:boxcolor=black@0.6:boxborderw=15,"
            f"drawtext=text='{p['japanese']}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2+40:"
            f"fontfile='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc':box=1:boxcolor=black@0.6:boxborderw=15",
            "-c:v", "libx264", "-c:a", "aac", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-shortest", str(temp)
        ]
        subprocess.run(cmd, capture_output=True)

        if (i + 1) % 20 == 0:
            print(f"  Video clip {i+1}/{len(phrases)}...")

    concat_file = Path(output_file).parent / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for clip in temp_clips:
            f.write(f"file '{clip.resolve().as_posix()}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", output_file], check=True, capture_output=True)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    video_dur = get_audio_duration(str(output_file))
    print(f"[video] Created: {Path(output_file).name} ({video_dur:.1f}s)")
    return video_dur


def generate_title_desc(category_en, category_ja, phrases, duration_min):
    title = f"Learn Japanese: 120 Essential {category_en} Phrases in 10 Minutes! ({category_ja})"
    if len(title) > 100:
        title = f"120 Japanese {category_en} Phrases - 10 Min Lesson ({category_ja})"

    description = f"""🇯🇵 Learn Japanese with Velocity Japanese! 🇯🇵

In this video, you'll learn 120 essential {category_en} ({category_ja}) phrases.
Perfect for beginners and intermediate learners!

📚 WHAT YOU'LL LEARN:
• 120 practical {category_en} phrases
• Correct pronunciation with Romaji
• Natural speaking practice

PHRASES IN THIS VIDEO:
"""
    for i, p in enumerate(phrases, 1):
        description += f"\n{i}. {p['english']}\n   → {p['japanese']} [{p.get('romaji', '')}]"

    description += """

📌 TIPS:
1. Repeat each phrase out loud
2. Practice daily
3. Use the natural pauses to speak along

🔔 Subscribe for more Japanese lessons!
👍 Like if you found this helpful!
💬 Comment your favorite phrase!

#LearnJapanese #Japanese #JapanesePhrases #JapaneseLesson #LanguageLearning #JapaneseVocabulary #JLPT #日本語 #StudyingJapanese
"""
    if len(description) > 4900:
        description = description[:4900] + "\n\n#LearnJapanese #Japanese #LanguageLearning"

    tags = [
        "Learn Japanese", "Japanese Phrases", "Japanese", category_en,
        "Japanese Lesson", "Japanese for Beginners", "Language Learning",
        "Japanese Vocabulary", "Velocity Japanese", "Speak Japanese", "JLPT", "日本語"
    ]

    return title, description, tags


def generate_longform_video():
    os.makedirs("output", exist_ok=True)

    category_en = get_available_category()
    category_ja = CATEGORIES_JA[category_en]
    print(f"\n{'='*80}")
    print(f"Category: {category_en} ({category_ja})")
    print(f"Target: {TARGET_PHRASES} phrases")
    print(f"{'='*80}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_dir = LONGFORM_DIR / f"{category_en}_{timestamp}"
    video_dir.mkdir(exist_ok=True)

    print("[1/5] Generating phrases...")
    phrases = generate_phrases(category_en, TARGET_PHRASES)
    if not phrases:
        raise Exception("Failed to generate phrases")

    print("[2/5] Generating audio...")
    audio_files = generate_all_audio(phrases, video_dir)
    final_audio = video_dir / "narration.mp3"
    create_narration(audio_files, str(final_audio))

    total_dur = sum(a["duration"] for a in audio_files)
    print(f"Total duration: {total_dur:.1f}s ({total_dur/60:.1f} min)")

    print("[3/5] Creating video...")
    output_video = video_dir / "final_video.mp4"
    video_dur = create_video(phrases, audio_files, str(final_audio), str(output_video), category_en)

    print("[4/5] Generating thumbnail...")
    try:
        from generate_thumbnail import generate_scenic_image
        thumbnail_path = video_dir / "thumbnail.jpg"
        generate_scenic_image(category_en, category_ja, str(thumbnail_path))
        print(f"Thumbnail generated: {thumbnail_path}")
    except Exception as e:
        print(f"Thumbnail generation skipped: {e}")

    print("[5/5] Generating metadata...")
    title, description, tags = generate_title_desc(category_en, category_ja, phrases, video_dur / 60)

    meta = {
        "title": title,
        "description": description,
        "tags": tags,
        "category_english": category_en,
        "category_japanese": category_ja,
        "phrases_count": len(phrases),
        "duration_seconds": video_dur,
        "duration_minutes": video_dur / 60,
        "video_path": str(output_video),
        "thumbnail_path": str(thumbnail_path),
        "phrases": phrases,
        "generated_at": datetime.now().isoformat(),
    }
    save_json(video_dir / "video_metadata.json", meta)

    save_json(BASE_DIR / "output" / "latest_video.json", meta)
    save_json(BASE_DIR / "output" / "latest_upload_info.json", {
        "title": title, "description": description, "tags": tags,
        "category": category_en, "phrases_count": len(phrases)
    })

    print(f"\n{'='*80}")
    print(f"COMPLETE!")
    print(f"  {output_video}")
    print(f"  {thumbnail_path}")
    print(f"  Duration: {video_dur/60:.1f} min")
    print(f"  Phrases: {len(phrases)}")
    print(f"{'='*80}\n")

    return meta


if __name__ == "__main__":
    generate_longform_video()
