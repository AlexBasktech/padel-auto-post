from PIL import Image, ImageDraw, ImageFont
import sys

W, H = 1080, 1350
NAVY = (3, 6, 23)
LIME = (180, 255, 62)
WHITE = (245, 248, 240)
GREY = (140, 150, 170)
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
import os
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-padel.png")


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


def make(out, kicker, big, sub, footer="padelautourdemoi.fr"):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # faint court illustration, right side
    court(d, 660, 90, 330, 600, (30, 44, 66), 6)
    # ball
    d.ellipse([905, 610, 965, 670], fill=LIME)
    # logo top-left
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, (70, 70))
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
    d.text((105, H - 305), "TU GÈRES UN CLUB ?", font=font(BLACK, 38), fill=LIME)
    d.text((105, H - 252), "Passe Premium dès 29 €/mois → /pro", font=font(MED, 40), fill=WHITE)
    # footer bar
    d.rectangle([0, H - 140, W, H], fill=LIME)
    d.text((70, H - 102), footer, font=font(BLACK, 54), fill=NAVY)
    im.save(out, quality=95)


if __name__ == "__main__":
    make(*sys.argv[1:5])
