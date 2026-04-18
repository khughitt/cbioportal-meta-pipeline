"""Download a cBioPortal study tarball and extract into ``data_dir``.

Idempotent: if all declared outputs already exist on disk, the script exits
without re-downloading. This protects against accidental re-download when a
rerun is triggered (e.g., by ``--forceall`` after the Snakefile's
``protected()`` outputs have been manually unprotected). cBioPortal
occasionally returns HTTP 403 on re-requests from the same IP, which would
otherwise leave the raw data wiped.
"""

import sys
import time
import tarfile
import urllib.request
from io import BytesIO
from pathlib import Path

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

if all(Path(out).exists() for out in snek.output):
    sys.exit(0)

url = f"https://cbioportal-datahub.s3.amazonaws.com/{snek.wildcards['id']}.tar.gz"

with urllib.request.urlopen(url) as stream:
    with tarfile.open(name=None, fileobj=BytesIO(stream.read())) as fp:
        fp.extractall(snek.config["data_dir"])

# be nice..
time.sleep(30)
