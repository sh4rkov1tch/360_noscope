import json
import os
import argparse as ap

import threesixty_ns as tns
from clint.textui import colored, puts

def main():
    parser = ap.ArgumentParser(prog = "360 NoScope", description = "Download helper for original Xbox and Xbox 360 games")

    parser.add_argument('-o', "--output", type=str, default=os.getcwd(), help="The output folder you want to download your game to, defaults to the current dir.")
    parser.add_argument("--force-refresh", type=bool, action=ap.BooleanOptionalAction, help="Force a games.json refresh")
    parser.add_argument("search_string", help="The name of the game you want")
    args = parser.parse_args()

    if os.path.exists("games.json") == False or args.force_refresh == True:
        results: dict = tns.scrape_game_links()
        with open("games.json", 'w') as j:
            json.dump(results, j)
    else:
        puts(colored.green("[*] Using cached list instead"))
        results: dict = json.load(open("games.json", 'r'))

    matched_names: list = []

    for name in results.keys():
        if args.search_string.lower() in name.lower():
            matched_names.append(name)

    if len(matched_names) != 0:
        puts(colored.green(f"[*] Found {len(matched_names)} results: "))
    else:
        puts(colored.red(f"[!] Did not find any results."))
        exit()
    
    puts(colored.green("[?] Please select the game you want to download: "))

    for i, name in enumerate(matched_names):
        print(f"{i + 1}. {name}")
    
    choice: int = int(input("Select the game you want to download: ")) - 1

    tns.dl_file(results[matched_names[choice]], matched_names[choice], args.output)

if __name__ == "__main__":
    main()