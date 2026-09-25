import cairosvg, glob, sys
fs = sys.argv[1:] or sorted(glob.glob("figs/fig*.svg"))
for f in fs:
    cairosvg.svg2png(url=f, write_to=f[:-4]+".png", scale=2, background_color="white")
print("ok", len(fs))
