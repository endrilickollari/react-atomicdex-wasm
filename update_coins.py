import os
import sys
import shutil
import urllib.request

# Color codes for logs
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
END = "\033[0m"


class CoinsManager:
    def __init__(self, url):
        self.url = url
        self.commit = url.split("/")[-1]
        self.coins_file = f"coins_{self.commit}"
        self.coins_versions_dir = "coins_versions"
        self.public_dir = "../public"

    def run(self):
        if not os.path.isdir(self.coins_versions_dir):
            os.mkdir(self.coins_versions_dir)
            print(YELLOW + "Created coins_versions directory." + END)

        os.chdir(self.coins_versions_dir)
        print(YELLOW + f"Moved to {os.getcwd()} directory." + END)

        if not os.path.isfile(self.coins_file):
            if os.path.isfile("coins"):
                os.rename("coins", self.coins_file)
                print(GREEN + f"Renamed coins file to {self.coins_file}." + END)
            elif os.path.isfile(f"../{self.coins_file}"):
                os.rename(f"../{self.coins_file}", self.coins_file)
                print(GREEN + f"Renamed coins file to {self.coins_file}." + END)
            else:
                print(YELLOW + f"Coins file not found, downloading from {self.url}..." + END)
                try:
                    urllib.request.urlretrieve(self.url, self.coins_file)
                except urllib.error.HTTPError as e:
                    print(RED + f"Error downloading coins file: {e}" + END)
                    sys.exit(1)

        try:
            shutil.copy(self.coins_file, f"{self.public_dir}/coins")
            print(GREEN + f"Coins file for commit {self.commit} has been copied to the public directory." + END)
        except FileNotFoundError as e:
            print(RED + f"Error copying coins file: {e}" + END)
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{YELLOW}Usage: python script.py [URL]{END}")
        sys.exit(1)

    CoinsManager(sys.argv[1]).run()
