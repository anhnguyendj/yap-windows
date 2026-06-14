"""
Tạo icon + desktop shortcut cho Yap
Chạy: python make_shortcut.py
"""
import os, sys, math
from pathlib import Path
from PIL import Image, ImageDraw

SCRIPT_DIR = Path(__file__).parent.resolve()

# ── Tạo icon ──────────────────────────────────────────────
def make_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    frames = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        pad = max(1, size // 16)
        r   = size // 5

        # Shadow layer
        for i in range(4):
            o = pad + i
            _rr(d, o, o, size-o, size-o, r+i, (80, 20, 160, 18 - i*4))

        # Main bg — deep purple
        _rr(d, pad, pad, size-pad, size-pad, r, (14, 10, 35, 255))

        # Top gradient tint
        _rr(d, pad+1, pad+1, size-pad-1, size//2+size//8, r, (110, 50, 220, 55))

        # Border
        _rr_outline(d, pad, pad, size-pad, size-pad, r, (160, 90, 255, 160), max(1, size//128+1))

        # Mic icon (centered, proportional)
        cx   = size // 2
        cy   = int(size * 0.47)
        s    = size / 256.0
        mw   = max(4, int(28 * s))
        mh   = max(6, int(40 * s))
        mr   = max(2, int(14 * s))
        col  = (255, 255, 255, 255)

        # Body
        _rr(d, cx - mw//2, cy - mh//2, cx + mw//2, cy + mh//2 - mr, mr, col)
        # Rounded top cap
        d.ellipse([cx - mw//2, cy - mh//2 - mr,
                   cx + mw//2, cy - mh//2 + mr], fill=col)

        # Stand arc (draw as dots)
        sr = max(3, int(22 * s))
        sy = cy + mh // 2
        sw = max(1, int(2.5 * s))
        for angle in range(0, 181, 6):
            rad = math.radians(angle)
            px = int(cx - sr * math.cos(rad))
            py = int(sy + sr * math.sin(rad))
            d.ellipse([px-sw, py-sw, px+sw, py+sw], fill=col)

        # Pole
        pt = sy + sr
        pb = pt + max(2, int(10 * s))
        pw = max(1, int(2 * s))
        d.rectangle([cx-pw, pt, cx+pw, pb], fill=col)

        # Base
        bw = max(2, int(14 * s))
        bh = max(1, int(2 * s))
        d.rectangle([cx-bw, pb, cx+bw, pb+bh*2], fill=col)

        # Green dot — top right
        dr = max(2, int(size * 0.085))
        dx = size - pad - dr - max(1, size // 20)
        dy = pad + dr + max(1, size // 20)
        # Glow
        d.ellipse([dx-dr-2, dy-dr-2, dx+dr+2, dy+dr+2], fill=(30, 180, 80, 80))
        d.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=(45, 220, 110, 255))

        frames.append(img)

    icon_path = SCRIPT_DIR / "yap_icon.ico"
    frames[0].save(
        str(icon_path), format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:]
    )
    print(f"Icon saved: {icon_path}")
    return icon_path


def _rr(draw, x0, y0, x1, y1, r, fill):
    r = min(r, max(1, (x1-x0)//2), max(1, (y1-y0)//2))
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    for cx, cy in [(x0+r, y0+r), (x1-r, y0+r), (x0+r, y1-r), (x1-r, y1-r)]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)


def _rr_outline(draw, x0, y0, x1, y1, r, color, w):
    for i in range(w):
        o = i
        r2 = max(1, r - o)
        x0o, y0o, x1o, y1o = x0+o, y0+o, x1-o, y1-o
        draw.arc([x0o, y0o, x0o+2*r2, y0o+2*r2], 180, 270, fill=color)
        draw.arc([x1o-2*r2, y0o, x1o, y0o+2*r2], 270, 360, fill=color)
        draw.arc([x0o, y1o-2*r2, x0o+2*r2, y1o], 90, 180, fill=color)
        draw.arc([x1o-2*r2, y1o-2*r2, x1o, y1o], 0, 90, fill=color)
        draw.line([x0o+r2, y0o, x1o-r2, y0o], fill=color)
        draw.line([x0o+r2, y1o, x1o-r2, y1o], fill=color)
        draw.line([x0o, y0o+r2, x0o, y1o-r2], fill=color)
        draw.line([x1o, y0o+r2, x1o, y1o-r2], fill=color)


# ── Tạo shortcut ──────────────────────────────────────────
def create_shortcut(icon_path: Path):
    try:
        import win32com.client
    except ImportError:
        print("ERROR: pywin32 not found. Run setup.bat first.")
        input("Press Enter to exit...")
        return

    pythonw = Path(sys.executable).parent / "pythonw.exe"
    if not pythonw.exists():
        pythonw = Path(sys.executable).with_name("pythonw.exe")

    app_py = SCRIPT_DIR / "app.py"

    shell   = win32com.client.Dispatch("WScript.Shell")
    desktop = shell.SpecialFolders("Desktop")
    sc_path = os.path.join(desktop, "Yap.lnk")

    sc = shell.CreateShortcut(sc_path)
    sc.TargetPath     = str(pythonw)
    sc.Arguments      = f'"{app_py}"'
    sc.WorkingDirectory = str(SCRIPT_DIR)
    sc.IconLocation   = f"{icon_path},0"
    sc.Description    = "Yap — Push to talk dictation"
    sc.Save()

    print(f"Shortcut created: {sc_path}")

    # Refresh icon cache
    try:
        import ctypes
        ctypes.windll.shell32.SHChangeNotify(0x8000000, 0, None, None)
    except Exception:
        pass


if __name__ == "__main__":
    print("=== Yap — Creating icon & shortcut ===")
    icon = make_icon()
    create_shortcut(icon)
    print("\nDone! Check your Desktop for the Yap icon.")
    input("Press Enter to exit...")
