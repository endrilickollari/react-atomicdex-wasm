import os
import sys
import shutil
import urllib.request
import zipfile


class Colors:
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"


class WasmVersionUpdater:
    def __init__(self, url):
        self.url = url
        self.filename = os.path.basename(self.url)
        self.temp_dir = "temp"

    def run(self):
        if len(sys.argv) < 2:
            print(f"{Colors.YELLOW}Usage: python script.py [URL]{Colors.RESET}")
            sys.exit(1)

        if not os.path.isdir("wasm_versions"):
            print(f"{Colors.YELLOW}Creating directory: wasm_versions{Colors.RESET}")
            os.mkdir("wasm_versions")
        os.chdir("wasm_versions")

        self.download_file()
        self.update_files()
        print(f"{Colors.GREEN}Done.{Colors.RESET}")

    def download_file(self):
        if not os.path.isfile(self.filename):
            print(f"{Colors.GREEN}Downloading file: {self.filename}{Colors.RESET}")
            urllib.request.urlretrieve(self.url, self.filename)

    def update_files(self):
        self.delete_file_if_exists("../public/mm2_bg.wasm")
        self.delete_dir_if_exists("../src/js/snippets")
        self.delete_dir_if_exists(self.temp_dir)

        print(f"{Colors.GREEN}Creating temp directory{Colors.RESET}")
        os.mkdir(self.temp_dir)

        print(f"{Colors.GREEN}Extracting files from zip{Colors.RESET}")
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(self.temp_dir)

        shutil.move(os.path.join(self.temp_dir, "mm2lib_bg.wasm"), "../public/mm2_bg.wasm")
        shutil.move(os.path.join(self.temp_dir, "mm2lib.js"), "../src/js/mm2.js")
        shutil.copytree(os.path.join(self.temp_dir, "snippets"), "../src/js/snippets")

        self.delete_dir_if_exists(self.temp_dir)

    @staticmethod
    def delete_file_if_exists(file_path):
        if os.path.exists(file_path):
            print(f"{Colors.RED}Deleting existing {file_path} file{Colors.RESET}")
            os.remove(file_path)

    @staticmethod
    def delete_dir_if_exists(dir_path):
        if os.path.exists(dir_path):
            print(f"{Colors.RED}Deleting existing {dir_path} dir{Colors.RESET}")
            shutil.rmtree(dir_path)


if __name__ == "__main__":
    updater = WasmVersionUpdater(sys.argv[1])
    updater.run()
