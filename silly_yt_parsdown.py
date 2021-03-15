import re
import argparse
import subprocess

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
    commands = ["youtube-dl \"" + link + "\"" for link in links]
    if extract_audio:
        commands = [command + " -x --audio-format mp3" for command in commands]
    print("Running: ")
    for command in commands:
        print("\t" + command)

    for i, command in enumerate(commands):
        print(f'{i+1} / {len(commands)}')
        ret = subprocess.call(command, shell=True)

def main():
    parser = argparse.ArgumentParser(
        description='Silly youtube parser downloader. \
        Simple python script that parses text file and extracts every link to youtube \
        and downloads videos from those links. Requires youtube-dl'
        )

    parser.add_argument('filename', type=str, help='Path to input file')
    parser.add_argument('--extract-audio', '-x', action='store_true', help='Convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe)')
    
    args = parser.parse_args()
    print(args)

    links = parse_file(args.filename)
    download_links(links, args.extract_audio)

if __name__ == "__main__":
    main()