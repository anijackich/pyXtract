from sys import exit
from os import PathLike, SEEK_SET
from os.path import getsize
from argparse import ArgumentParser

PYINST20_COOKIE_SIZE = 24  # For pyinstaller 2.0
PYINST21_COOKIE_SIZE = 24 + 64  # For pyinstaller 2.1+

SEARCH_CHUNK_SIZE = 8192
MAGIC_BYTES = b'MEI\014\013\012\013\016'


class PyInstallerArchive:
    def __init__(self, path: str | PathLike[str], magic: bytes = None):
        self.exe_path = path
        self.magic = magic

        self._open()

    def _open(self):
        try:
            self.exe = open(self.exe_path, 'rb')
            self.exe_size = getsize(self.exe_path)
        except Exception as E:
            print(f'[!] Could not open {self.exe_path}: {str(E)}')
            exit()

    def _close(self):
        self.exe.close()

    def _verify_archive(self):
        print(f'[*] Verifying {self.exe_path}...')

        end = self.exe_size
        cookie_at = -1

        if end < len(self.magic):
            print(f'[!] {self.exe_path} is too short or truncated')
            return False

        while True:
            start = max(0, end - SEARCH_CHUNK_SIZE)
            chunk_size = end - start

            if chunk_size < len(self.magic):
                break

            self.exe.seek(start, SEEK_SET)
            offset = self.exe.read(chunk_size).rfind(self.magic)

            if offset != -1:
                cookie_at = start + offset
                break

            end = start + len(self.magic) - 1

            if start == 0:
                break

    def extract(self):
        pass


def main():
    argp = ArgumentParser(
        description='PyXtract | PyInstaller extractor'
    )

    argp.add_argument('filename')
    argp.add_argument('-m', help='Magic number which identifies PyInstaller', type=str)

    argp.parse_args()


if __name__ == '__main__':
    main()
