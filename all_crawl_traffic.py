import pathlib
import os

def main():
    files = [f for f in pathlib.Path().glob("files/*")]
    for filename in files:
        parse_filename = str(filename).replace('files/','')
        os.system(f'python3 /home/seungmin/phish/traffic_crawl.py {parse_filename}')

main()

        