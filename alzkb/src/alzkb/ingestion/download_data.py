import os
import requests
import gzip
import shutil
import zipfile
from pathlib import Path

# Paths
DATA_DIR = Path("alzkb/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Sources
# Using the stable FTP link found via 'latest' directory listing
GWAS_URL = "ftp://ftp.ebi.ac.uk/pub/databases/gwas/releases/latest/gwas-catalog-associations_ontology-annotated-full.zip"
GWAS_ZIP = DATA_DIR / "gwas_associations.zip"
GWAS_TSV_TARGET = DATA_DIR / "associations.tsv"

CLINVAR_URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
CLINVAR_FILE = DATA_DIR / "variant_summary.txt.gz"

def download_file_http(url, target_path):
    print(f"Downloading {url} to {target_path}...")
    if target_path.exists():
        print(f"File {target_path} already exists. Skipping.")
        return

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(target_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"[✓] Downloaded {target_path}")
    except Exception as e:
        print(f"[X] Failed to download {url}: {e}")
        if target_path.exists():
            target_path.unlink()

def download_file_ftp(url, target_path):
    # Requests doesn't support FTP. Use valid curl command.
    print(f"Downloading {url} to {target_path} using curl...")
    if target_path.exists():
        print(f"File {target_path} already exists. Skipping.")
        return

    ret = os.system(f"curl -o {target_path} {url}")
    if ret == 0:
         print(f"[✓] Downloaded {target_path}")
    else:
         print(f"[X] Failed to download {url}")

def extract_zip(zip_path, target_dir):
    print(f"Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Assume single file or find the tsv
            for member in zip_ref.namelist():
                if member.endswith('.tsv'):
                    source = zip_ref.open(member)
                    target = open(target_dir / member, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
                    print(f"[✓] Extracted {member}")
                    # Rename to standard name
                    (target_dir / member).rename(GWAS_TSV_TARGET)
                    print(f"[✓] Renamed to {GWAS_TSV_TARGET}")
                    break
    except Exception as e:
        print(f"[X] Failed to extract {zip_path}: {e}")

def main():
    print("=== Phase VI: Data Download ===")
    
    # 1. GWAS Catalog (FTP)
    download_file_ftp(GWAS_URL, GWAS_ZIP)
    if GWAS_ZIP.exists():
        extract_zip(GWAS_ZIP, DATA_DIR)
        # Cleanup zip
        GWAS_ZIP.unlink()
    
    # 2. ClinVar (HTTP/HTTPS)
    download_file_http(CLINVAR_URL, CLINVAR_FILE)
    
    print("\n[INFO] Data download complete. Paths:")
    print(f"1. {GWAS_TSV_TARGET}")
    print(f"2. {CLINVAR_FILE}")

if __name__ == "__main__":
    main()
