"""pptxgenjs 以 SVG 內容當 PNG 備援圖；換成真正的點陣 PNG（舊版 Office 用）"""
import zipfile, sys, glob, shutil
src = sys.argv[1]; tmp = src + ".tmp"
svgs = {open(f, "rb").read(): f[:-4] + ".png" for f in glob.glob("figs/*.svg")}
n = 0
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename.startswith("ppt/media/") and it.filename.endswith(".png") and data in svgs:
            data = open(svgs[data], "rb").read(); n += 1
        zo.writestr(it, data)
shutil.move(tmp, src); print("replaced", n)
