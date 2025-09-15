import subprocess
import os

FFMPEG = r"D:\Programming\Tkinter exe\ffmpegDIr\ffmpeg.exe"
mkv_file = r"D:\Programming\Tkinter exe\_ The Man I Know I'm Not _ - Stanley Pines\｜ The Man I Know I'm Not ｜ - Stanley Pines.mkv"
cover_image = r"D:\Programming\Tkinter exe\_ The Man I Know I'm Not _ - Stanley Pines\cover.jpg"

def attach_cover(mkv_file, cover_image):
    base, ext = os.path.splitext(mkv_file)
    output_file = f"{base}.withcover{ext}"

    cmd = [
        FFMPEG,
        "-i", mkv_file,
        "-i", cover_image,
        "-map", "1",  # map all streams from mkv
        "-map", "0",  # map the cover image
        "-c", "copy",  # copy video/audio/subtitles
        "-disposition:v:0", "attached_pic",  # mark second video stream as attached picture
        output_file
    ]

    print("Running command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Created new MKV with cover: {output_file}")

attach_cover(mkv_file, cover_image)
