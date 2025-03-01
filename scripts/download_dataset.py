"""
download_dataset.py
"""
import tarfile 
import urllib.request
from io import BytesIO

snek = snakemake

url = f"https://cbioportal-datahub.s3.amazonaws.com/{snek.wildcards['id']}.tar.gz"

with urllib.request.urlopen(url) as stream:
    with tarfile.open(name=None, fileobj=BytesIO(stream.read())) as fp:
        fp.extractall(snek.config['data_dir'])
