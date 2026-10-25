"""
Inject image + audio markup into the Twine SugarCube story.
Re-runnable: it removes any previously-injected block first.
"""
import re, html, sys, pathlib

STORY = pathlib.Path(__file__).resolve().parent.parent / "story.html"
START = "<!-- ASSETS-INJECTED-START -->"
END   = "<!-- ASSETS-INJECTED-END -->"

# Set to False to wrap all <<cacheaudio>>/<<audio>> calls in /* AUDIO-OFF ... */
# so the story still runs when mp3 files are missing.
AUDIO_ENABLED = True

def _audio(block: str) -> str:
    """Wrap audio macros in <<silently>> so they emit no whitespace.
    When AUDIO_ENABLED is False, wrap the whole thing in /* AUDIO-OFF */.
    The block is collapsed to a single line — SugarCube's newline-to-br
    rule otherwise inserts visible blank space between the image and <h1>.
    """
    inner = block.replace("\n", "")
    if AUDIO_ENABLED:
        return f"<<silently>>{inner}<</silently>>"
    return "/* AUDIO-OFF: 删掉本注释的开闭符即可启用音频\n" + block + "\n*/"

# (passage_name, raw_block_to_prepend) — raw block uses normal HTML / SC syntax;
# we'll entity-encode it once before insertion since passage bodies are encoded.
INJECTIONS = {
    # --- StoryInit: register all audio --------------------------------------
    "StoryInit": _audio("""<<cacheaudio "bgm-prologue" "assets/audio/bgm-prologue.mp3">>
<<cacheaudio "bgm-act1"     "assets/audio/bgm-act1.mp3">>
<<cacheaudio "bgm-act2"     "assets/audio/bgm-act2.mp3">>
<<cacheaudio "bgm-act3"     "assets/audio/bgm-act3.mp3">>
<<cacheaudio "sfx-alarm"    "assets/audio/sfx-alarm.mp3">>
<<cacheaudio "sfx-message"  "assets/audio/sfx-message.mp3">>
<<createaudiogroup ":bgm">>
    <<track "bgm-prologue">>
    <<track "bgm-act1">>
    <<track "bgm-act2">>
    <<track "bgm-act3">>
<</createaudiogroup>>"""),

    # --- 序幕 ---------------------------------------------------------------
    "序幕": '<img src="assets/img/prologue.jpg" alt="序幕" class="scene-img">\n'
            + _audio('<<audio ":bgm" stop>><<audio "bgm-prologue" volume 0.4 loop play>>\n'
                     '<<audio "sfx-alarm" volume 0.7 play>>'),

    # --- 第一幕 -------------------------------------------------------------
    "第一幕": '<img src="assets/img/act1-work.jpg" alt="第一幕" class="scene-img">\n'
              + _audio('<<audio ":bgm" stop>><<audio "bgm-act1" volume 0.4 loop play>>'),

    # --- 第二幕 -------------------------------------------------------------
    "第二幕": '<img src="assets/img/act2-social.jpg" alt="第二幕" class="scene-img">\n'
              + _audio('<<audio ":bgm" stop>><<audio "bgm-act2" volume 0.4 loop play>>\n'
                       '<<audio "sfx-message" volume 0.8 play>>'),

    # --- 第三幕 -------------------------------------------------------------
    "第三幕": '<img src="assets/img/act3-night.jpg" alt="第三幕" class="scene-img">\n'
              + _audio('<<audio ":bgm" stop>><<audio "bgm-act3" volume 0.35 loop play>>'),

    # --- 5 个结局（沿用 act3 的 BGM，不再切）---------------------------------
    "结局一": '<img src="assets/img/ending-1-shutdown.jpg" alt="结局一 · 断电关机" class="scene-img">',
    "结局二": '<img src="assets/img/ending-2-helpless.jpg" alt="结局二 · 习得性无助" class="scene-img">',
    "结局三": '<img src="assets/img/ending-3-lowpower.jpg" alt="结局三 · 低能量续航" class="scene-img">',
    "结局四": '<img src="assets/img/ending-4-reconcile.jpg" alt="结局四 · 自我和解" class="scene-img">',
    "结局五": '<img src="assets/img/ending-5-warrior.jpg" alt="结局五 · 反内耗战士" class="scene-img">',

    # --- 全剧终 -------------------------------------------------------------
    "全剧终": '<img src="assets/img/finale.jpg" alt="全剧终" class="scene-img">\n'
              + _audio('<<audio ":bgm" fadeoverto 4 0>>'),
}

EXTRA_CSS = """/* === scene image styling (auto-injected) === */
.scene-img{
    display:block;
    max-width:100%;
    height:auto;
    margin:0 auto 0.6em;
    border-radius:8px;
    box-shadow:0 4px 18px rgba(0,0,0,.5);
}
.scene-img + h1,
.scene-img + br + h1{
    margin-top:0.2em;
}
"""

def main():
    src = STORY.read_text(encoding="utf-8")

    # 1) Inject into each named passage --------------------------------------
    for name, raw_block in INJECTIONS.items():
        # Collapse the injected block to a single line. SugarCube turns each
        # newline in passage source into <br>, so multi-line injections leave
        # visible vertical gaps before the <h1>. Trailing "\" on each line is
        # SugarCube's line-continuation; combined with single-line we add it
        # to the END marker so the gap to the next line (the original passage
        # body) is also eaten.
        inline_block = raw_block.replace("\n", "")
        encoded_block = html.escape(inline_block, quote=True)
        wrapped = f"{START}{encoded_block}{END}\\\n"

        # Find <tw-passagedata ... name="<name>" ...>BODY</tw-passagedata>
        pattern = re.compile(
            r'(<tw-passagedata\b[^>]*\bname="' + re.escape(name) + r'"[^>]*>)(.*?)(</tw-passagedata>)',
            re.DOTALL,
        )
        m = pattern.search(src)
        if not m:
            print(f"!! passage not found: {name}", file=sys.stderr)
            sys.exit(1)

        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        # Strip any previous injection so script is idempotent
        body = re.sub(
            re.escape(START) + r".*?" + re.escape(END) + r"\n?",
            "", body, flags=re.DOTALL,
        )
        new_body = wrapped + body
        src = src[:m.start()] + open_tag + new_body + close_tag + src[m.end():]
        print(f"[ok] injected into: {name}")

    # 2) (Re)append CSS to the user stylesheet block (idempotent) ------------
    css_marker = "/* === scene image styling (auto-injected) === */"
    css_end    = "/* === /scene image styling === */"
    css_block  = EXTRA_CSS.rstrip() + "\n" + css_end + "\n"
    # Remove any prior auto-injected CSS so we can update it
    src = re.sub(
        re.escape(css_marker) + r".*?" + re.escape(css_end) + r"\n?",
        "", src, flags=re.DOTALL,
    )
    src = re.sub(
        r'(<style role="stylesheet"[^>]*>)',
        r'\1' + css_block,
        src, count=1,
    )
    print("[ok] (re)wrote scene-img CSS")

    STORY.write_text(src, encoding="utf-8")
    print(f"\nWrote {STORY}")

if __name__ == "__main__":
    main()
