"""Stage a cBioPortal study into ``data_dir`` and write a per-out_dir marker.

The single declared snakemake output is a *marker file* under ``out_dir``,
NOT the raw tarball contents. This decouples the per-run snakemake metadata
from the shared ``data_dir`` tree so a fresh ``out_dir`` cannot trigger a
re-download — and, critically, cannot let snakemake's pre-rule cleanup
remove existing raw files when it decides to re-run this rule. (The previous
design wrote ``protected()`` outputs to ``data_dir/{id}/data_*.txt``;
``protected()`` only guards against ``--forceall``, not against the normal
rerun-cleanup that wipes outputs before the rule body runs. cBioPortal
returns HTTP 403 on re-requests, so a single accidental rerun in a fresh
``out_dir`` could permanently destroy the raw data.)

Behavior:
  - If the canonical raw files already exist in ``data_dir/{id}/``,
    just touch the marker and exit.
  - Otherwise, download the tarball from cBioPortal datahub and extract.

Required raw files (per study):
  - data_mutations.txt
  - data_clinical_sample.txt
  - data_clinical_patient.txt
  - data_gene_panel_matrix.txt   (only for studies in panel_bearing_studies)
"""

import tarfile
import time
import urllib.request
from io import BytesIO
from pathlib import Path

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

study_id = snek.wildcards["id"]
data_dir = Path(snek.config["data_dir"])
study_dir = data_dir / study_id
marker = Path(snek.output[0])

REQUIRED = ["data_mutations.txt", "data_clinical_sample.txt", "data_clinical_patient.txt"]
if study_id in (snek.config.get("panel_bearing_studies") or []):
    REQUIRED.append("data_gene_panel_matrix.txt")


def _all_present() -> bool:
    return all((study_dir / name).exists() for name in REQUIRED)


def _touch_marker() -> None:
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{study_id}\n")


if _all_present():
    print(f"download_study ({study_id}): raw data already present in {study_dir} — staging marker only")
    _touch_marker()
    raise SystemExit(0)

print(f"download_study ({study_id}): missing required raw files {REQUIRED} in {study_dir} — downloading from cBioPortal")
url = f"https://cbioportal-datahub.s3.amazonaws.com/{study_id}.tar.gz"
with urllib.request.urlopen(url) as stream:
    with tarfile.open(name=None, fileobj=BytesIO(stream.read())) as fp:
        fp.extractall(data_dir)

if not _all_present():
    raise RuntimeError(
        f"download_study ({study_id}): tarball extracted but required files still missing: "
        f"{[name for name in REQUIRED if not (study_dir / name).exists()]}"
    )

_touch_marker()
# be nice..
time.sleep(30)
