#!/usr/bin/env python3
"""Expand checked-in response archives after verifying their recorded hashes."""
from pathlib import Path
import gzip
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def main():
    manifest=json.loads((ROOT/'results/model-artifacts.json').read_text())
    for row in manifest['archives']:
        archive=ROOT/row['archive']; dest=ROOT/row['uncompressed_path']
        blob=archive.read_bytes()
        if hashlib.sha256(blob).hexdigest()!=row['archive_sha256']:
            raise ValueError('Archive checksum failed: '+str(archive))
        data=gzip.decompress(blob)
        if hashlib.sha256(data).hexdigest()!=row['uncompressed_sha256']:
            raise ValueError('Uncompressed checksum failed: '+str(dest))
        if dest.exists() and dest.read_bytes()!=data:
            raise ValueError('Refusing to replace a different local file: '+str(dest))
        dest.write_bytes(data)
    print('Verified and unpacked',len(manifest['archives']),'archives. No API calls.')


if __name__=='__main__': main()
