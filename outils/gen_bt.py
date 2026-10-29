from PIL import Image, ImageDraw, ImageFont
import sys

W, H = 1080, 1350
NAVY = (247, 247, 242)
LIME = (28, 130, 58)
WHITE = (20, 30, 25)
GREY = (140, 150, 170)
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
import os
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-basktech.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def court(d, x, y, w, h, col, width=4):
    """Padel court seen from above: outline, net, service lines, center line."""
    d.rectangle([x, y, x + w, y + h], outline=col, width=width)
    d.line([x, y + h / 2, x + w, y + h / 2], fill=col, width=width + 2)  # net
    sy = h * 0.15
    d.line([x, y + sy, x + w, y + sy], fill=col, width=width)
    d.line([x, y + h - sy, x + w, y + h - sy], fill=col, width=width)
    d.line([x + w / 2, y + sy, x + w / 2, y + h - sy], fill=col, width=width)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def make(out, kicker, big, sub, footer="basktech.eus"):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # faint court illustration, right side
    d.rectangle([0, 0, W, 18], fill=(226, 30, 38))
    # ball

    # logo top-left
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((240, 240), Image.LANCZOS)
    m = Image.new('L', (240, 240), 0); ImageDraw.Draw(m).ellipse((4, 4, 236, 236), fill=255)
    im.paste(lg, (70, 70), m)
    # kicker
    d.text((70, 360), kicker.upper(), font=font(MED, 34), fill=LIME)
    # big text
    fb = font(BLACK, 150 if len(big) < 10 else 110)
    y = 420
    for line in big.split("\n"):
        d.text((66, y), line, font=fb, fill=WHITE)
        y += fb.size + 10
    # sub text
    fs = font(MED, 46)
    y = max(y + 30, 740)
    for line in wrap(d, sub, fs, 900):
        d.text((70, y), line, font=fs, fill=WHITE)
        y += 62
    # premium club offer, on every post
    d.rounded_rectangle([70, H - 330, W - 70, H - 180], radius=24, outline=LIME, width=4)
    d.text((105, H - 305), "TON SITE EST-IL VISIBLE PAR L’IA ?", font=font(BLACK, 38), fill=LIME)
    d.text((105, H - 252), "Teste-le sur basktech.eus", font=font(MED, 40), fill=WHITE)
    # footer bar
    d.rectangle([0, H - 140, W, H], fill=LIME)
    d.text((70, H - 102), footer, font=font(BLACK, 54), fill=(255, 255, 255))
    im.save(out, quality=95)


if __name__ == "__main__":
    make(*sys.argv[1:5])
