import re
import argparse
import subprocess
import os

def parse_text(text):
    # Pretty regex found on stackoverflow (where else)
    regex = "(?P<url>https?://[^\s]+)"
    all_links = re.findall(regex, text)
    yt_links = filter(lambda x: x.startswith("https://www.youtube"), all_links)
    return(list(yt_links))

def parse_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return parse_text(text)

def download_links(links, extract_audio=False):
    with open("tmp.txt", "w") as f: 
        for link in links:
            f.write(link)
            f.write("\n")
    
    commands = ["youtube-dl \"" + link + "\"" for link in links]
    if extract_audio:
        commands = [command + " -x --audio-format mp3 --no-playlist" for command in commands]

    command = f'youtube-dl -a tmp.txt -x --audio-format mp3 --no-playlist -o "%(autonumber)s - %(title)s-%(id)s.%(ext)s"'
    ret = subprocess.call(command, shell=True)

    os.remove("tmp.txt")

def main():
    parser = argparse.ArgumentParser(
        description='Silly youtube parser downloader. \
        Simple python script that parses text file and extracts every link to youtube \
        and downloads videos from those links. Requires youtube-dl'
        )

    parser.add_argument('filename', type=str, help='Path to input file')
    parser.add_argument('--extract-audio', '-x', action='store_true', help='Convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe)')
    
    args = parser.parse_args()

    links = parse_file(args.filename)
    download_links(links, args.extract_audio)

if __name__ == "__main__":
    main()