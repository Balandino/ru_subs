import glob
import os

from vtt_to_srt.vtt_to_srt import ConvertFile

for file in glob.glob("vtt_storage\\*.vtt"):
    convert_file = ConvertFile(file, "utf-8")
    convert_file.convert()

    os.remove(file)

