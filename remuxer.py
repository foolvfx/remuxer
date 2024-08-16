import argparse
from argparse import ArgumentParser
import subprocess
import os
from shutil import which

def get_mkvs(folder: str) -> list:
    mkv_files = []
    
    for path, subdirs, files in os.walk(folder):
        for name in files:
            if name.endswith(".mkv"):
                mkv_files.append([path, name])
    
    return mkv_files

def remux_all(remove: bool, input_path: str, output_path: str):
    if not output_path:
        output_path = input_path
    
    remuxed = 0
    
    mkv_files = get_mkvs(input_path)
    
    for path, name in mkv_files:
        i_path = os.path.join(path, name)
        o_path = os.path.join(output_path, name.replace('.mkv', '.mp4'))
        
        if remux_file(i_path, o_path) == 0:
            if remove:
                os.remove(i_path)
            print(f"[{remuxed}] {name} successfully remuxed")
            remuxed += 1
        else:
            print(f"Error remuxing {i_path}")
            
def remux_file(input_file: str, output_path: str):
    command = f"ffmpeg -y -hwaccel cuda -i \"{input_file}\" -map 0 -codec copy \"{output_path}\""

    proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    try:
        outs, errs = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        
    return proc.returncode

def verify_paths(args) -> bool:
    if not args.input:
        parser.print_help()
        return False
    
    if not os.path.isdir(args.input):
        print(f"Input Option {args.input} does not exist or is not a folder.")
        return False
        
    if args.output:
        if not os.path.isdir(args.output):
            print(f"Output Option {args.output} does not exist or is not a folder.")
            return False
    
    return True

def create_parser():
    parser: ArgumentParser = argparse.ArgumentParser(description="Remux *.mkv files to mp4 using ffmpeg")
    parser.add_argument("-i", "--input", metavar="", help="Input folder with .mkv files")
    parser.add_argument("-o", "--output", nargs='?', help="Optional output folder for converted .mp4 files, will default to the same as the input directory")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove .mkv file after conversion")
    return parser

if __name__ in '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if not which("ffmpeg"):
        print("ffmpeg not found, if you have it installed add it to your PATH environment variable")
    else:
        if verify_paths(args):
            remux_all(args.remove, args.input, args.output)