from invoke import task, Collection
from invoke.context import Context

import os
import pathlib
import shutil
import urllib.request as request


PAGES_BASE_URL = "https://pages.musicpresence.app"

ROOT_DIR = "releases"
CHECKSUM_FILENAME = "sha256sum.txt"
SIGNATURE_FILENAME = f"{CHECKSUM_FILENAME}.sig"
PUBLIC_KEY = "keys/ed25519_musicpresence_release.pub.pem"

PUBLIC_DIR = "docs"
BUILD_DIR = "build"


def make_directories(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def get_release_file(version, file):
    url = f"{PAGES_BASE_URL}/{ROOT_DIR}/{version}/{file}"
    result = f"{BUILD_DIR}/{version}/{file}"
    request.urlretrieve(url, result)
    return result


def line_ending(file):
    with open(file, newline=None) as f:
        f.readline()
        if f.newlines == "\r\n":
            return "CRLF"
        if f.newlines == "\r":
            return "CR"
        if f.newlines == "\n":
            return "LF"
        return None


def verify_command(checksum_path, signature_path):
    join = lambda *args: " ".join(args)
    return join(
        "openssl",
        "pkeyutl",
        "-verify",
        "-pubin",
        "-inkey",
        PUBLIC_KEY,
        "-rawin",
        "-in",
        checksum_path,
        "-sigfile",
        signature_path,
    )


@task
def prepare(c: Context):
    make_directories(BUILD_DIR)


@task
def clean(c: Context):
    shutil.rmtree(BUILD_DIR, ignore_errors=True)


@task(pre=[prepare], post=[clean])
def verify(c: Context):
    for version in os.listdir(f"{PUBLIC_DIR}/{ROOT_DIR}"):
        make_directories(f"{BUILD_DIR}/{version}")
        checksum = get_release_file(version, CHECKSUM_FILENAME)
        signature = get_release_file(version, SIGNATURE_FILENAME)
        le = line_ending(checksum)
        print(f"verifying {version}/{CHECKSUM_FILENAME} ({le})...")
        c.run(verify_command(checksum, signature))


namespace = Collection(clean, verify)
