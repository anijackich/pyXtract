from sys import exit
from os import PathLike
from os.path import getsize
from argparse import ArgumentParser

PYINST20_COOKIE_SIZE = 24  # For pyinstaller 2.0
PYINST21_COOKIE_SIZE = 24 + 64  # For pyinstaller 2.1+


class PyInstallerArchive:
    def __init__(self, path: str | PathLike[str], magic: bytes = None):
        self.exe_path = path

        self._open()

    def _open(self):
        try:
            self.exe = open(self.exe_path, 'rb')
            self.exe_size = getsize(self.exe_path)
        except Exception as E:
            print(f'[!] Error: Could not open {self.exe_path}: {str(E)}')
            exit()

    def _close(self):
        self.exe.close()

    def _verify_archive(self):
        pass

    def extract(self):
        pass


def main():
    argp = ArgumentParser(
        description='PyXtract | PyInstaller extractor',
        epilog='sus'
    )

    argp.add_argument('filename')
    argp.add_argument('-m', help='Magic number which identifies PyInstaller', type=str)

    argp.parse_args()


if __name__ == '__main__':
    main()
