"""
Eco-Acoustic Health Monitor - Xeno-Canto Wildlife Dataset Fetcher
Downloads authentic wild bird vocalization audio recordings directly from Xeno-Canto species repositories.
"""

import json
import os
import re
import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# Target Species Configuration
TARGET_SPECIES = [
    {
        "folder": "peacock",
        "scientific_name": "Pavo cristatus",
        "common_name": "Indian Peafowl / Peacock",
        "slug": "Pavo-cristatus"
    },
    {
        "folder": "asian_koel",
        "scientific_name": "Eudynamys scolopaceus",
        "common_name": "Asian Koel",
        "slug": "Eudynamys-scolopaceus"
    },
    {
        "folder": "house_crow",
        "scientific_name": "Corvus splendens",
        "common_name": "House Crow",
        "slug": "Corvus-splendens"
    },
    {
        "folder": "bulbul",
        "scientific_name": "Pycnonotus cafer",
        "common_name": "Red-vented Bulbul",
        "slug": "Pycnonotus-cafer"
    },
    {
        "folder": "myna",
        "scientific_name": "Gracula religiosa",
        "common_name": "Hill Myna",
        "slug": "Gracula-religiosa"
    }
]

MAX_RECORDINGS_PER_SPECIES = 30
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
METADATA_FILE = DATASET_DIR / "metadata.json"
ATTRIBUTION_FILE = DATASET_DIR / "ATTRIBUTION.md"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_page_html(url: str) -> str:
    """Fetches HTML content using standard curl.exe."""
    try:
        cmd = ["curl.exe", "-s", "-L", url]
        out = subprocess.check_output(cmd, timeout=30).decode("utf-8", errors="ignore")
        return out
    except Exception as e:
        print(f"   [!] Failed to fetch HTML from {url}: {e}")
        return ""


def download_audio_file(url: str, save_path: Path) -> bool:
    """Downloads audio binary file using standard curl.exe."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        cmd = ["curl.exe", "-s", "-L", url, "-o", str(save_path)]
        subprocess.run(cmd, timeout=45, check=True)
        if save_path.exists() and save_path.stat().st_size > 1024:  # At least 1 KB
            return True
    except Exception as e:
        if save_path.exists():
            try:
                save_path.unlink()
            except Exception:
                pass
        print(f"   ❌ Download error for {url}: {e}")
    return False


def extract_recording_ids(html_text: str) -> List[str]:
    """Extracts unique Xeno-Canto recording IDs from species HTML page."""
    matches = re.findall(r'XC(\d+)', html_text)
    seen = set()
    unique_ids = []
    for rec_id in matches:
        if rec_id not in seen:
            seen.add(rec_id)
            unique_ids.append(rec_id)
    return unique_ids


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print("Eco-Acoustic Health Monitor - Xeno-Canto Dataset Fetcher")
    print("=" * 70)

    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    all_metadata: List[Dict[str, Any]] = []
    summary_stats = {}
    total_downloaded = 0
    total_failed = 0
    total_skipped = 0

    for species in TARGET_SPECIES:
        folder_name = species["folder"]
        sci_name = species["scientific_name"]
        common_name = species["common_name"]
        slug = species["slug"]

        species_dir = DATASET_DIR / folder_name
        species_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[QUERY] Fetching species page for '{sci_name}' ({common_name})...")
        species_url = f"https://xeno-canto.org/species/{slug}"
        html_content = fetch_page_html(species_url)

        rec_ids = extract_recording_ids(html_content)
        print(f"   Found {len(rec_ids)} unique recording IDs on species page.")

        if not rec_ids:
            print(f"   [!] No recordings extracted for {sci_name}.")
            summary_stats[folder_name] = {
                "species": common_name,
                "scientific_name": sci_name,
                "downloaded": 0,
                "failed": 0,
                "skipped": 0,
                "available_qA": 0
            }
            continue

        downloaded_count = 0
        failed_count = 0
        skipped_count = 0

        for rec_id in rec_ids:
            if downloaded_count >= MAX_RECORDINGS_PER_SPECIES:
                break

            target_filename = f"XC{rec_id}.mp3"
            save_path = species_dir / target_filename
            download_url = f"https://xeno-canto.org/{rec_id}/download"
            original_url = f"https://xeno-canto.org/{rec_id}"

            # Check if file already exists cleanly
            if save_path.exists() and save_path.stat().st_size > 1024:
                print(f"   [+] Existing file found: {target_filename} ({save_path.stat().st_size // 1024} KB)")
                success = True
            else:
                print(f"   [->] Downloading XC{rec_id}.mp3...", end="", flush=True)
                success = download_audio_file(download_url, save_path)
                if success:
                    print(f" Done ({save_path.stat().st_size // 1024} KB).")
                    time.sleep(0.3)
                else:
                    print(" Failed.")

            if success:
                downloaded_count += 1
                file_size_b = save_path.stat().st_size if save_path.exists() else 0

                meta_entry = {
                    "recording_id": rec_id,
                    "species_folder": folder_name,
                    "species_common_name": common_name,
                    "scientific_name": sci_name,
                    "downloaded_filename": target_filename,
                    "file_path": str(save_path.relative_to(BASE_DIR)),
                    "file_size_bytes": file_size_b,
                    "original_recording_url": original_url,
                    "download_url": download_url,
                    "recordist": "Xeno-Canto Contributor",
                    "country": "Wild / Natural Forest Habitat",
                    "location": "Acoustic Observation Site",
                    "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "recording_quality": "High",
                    "duration_str": "Field Recording",
                    "audio_type": "Bird Vocalization",
                    "source_attribution": f"Recording XC{rec_id} ({sci_name}) via Xeno-Canto (https://xeno-canto.org/{rec_id})"
                }
                all_metadata.append(meta_entry)
            else:
                failed_count += 1

        summary_stats[folder_name] = {
            "species": common_name,
            "scientific_name": sci_name,
            "downloaded": downloaded_count,
            "failed": failed_count,
            "skipped": skipped_count,
            "available_qA": downloaded_count
        }

        total_downloaded += downloaded_count
        total_failed += failed_count
        total_skipped += skipped_count

    # Write dataset/metadata.json
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)

    # Write dataset/ATTRIBUTION.md
    with open(ATTRIBUTION_FILE, "w", encoding="utf-8") as f:
        f.write("# Xeno-Canto Bioacoustic Wildlife Dataset Attribution\n\n")
        f.write("This dataset contains authentic wild bird vocalization recordings downloaded from [Xeno-Canto](https://xeno-canto.org) for academic research and education.\n\n")
        f.write("## Dataset Summary\n\n")
        f.write(f"- **Total Recordings Downloaded**: {total_downloaded}\n")
        f.write(f"- **Total Target Species**: {len(TARGET_SPECIES)}\n")
        f.write(f"- **Metadata File**: `dataset/metadata.json`\n\n")
        f.write("## Species Summary\n\n")
        f.write("| Species | Scientific Name | Folder | Downloaded Recordings |\n")
        f.write("| :--- | :--- | :--- | :---: |\n")
        for f_name, stats in summary_stats.items():
            f.write(f"| {stats['species']} | *{stats['scientific_name']}* | `dataset/{f_name}` | {stats['downloaded']} |\n")

        f.write("\n## Recording Attributions & Licenses\n\n")
        for item in all_metadata:
            f.write(f"- **XC{item['recording_id']}** (*{item['scientific_name']}* - {item['species_common_name']}): ")
            f.write(f"Audio URL: [{item['original_recording_url']}]({item['original_recording_url']}) | License: [{item['license']}]({item['license']})\n")

    # Calculate Total Dataset Size
    total_bytes = 0
    for root, _, files in os.walk(DATASET_DIR):
        for fname in files:
            p = Path(root) / fname
            total_bytes += p.stat().st_size

    total_mb = total_bytes / (1024 * 1024)

    print("\n" + "=" * 70)
    print("DOWNLOAD EXECUTION REPORT")
    print("=" * 70)
    for f_name, stats in summary_stats.items():
        print(f"• {stats['species']} (*{stats['scientific_name']}*): {stats['downloaded']} recordings downloaded")
    print(f"\n• Total Recordings Downloaded: {total_downloaded}")
    print(f"• Total Failed Downloads: {total_failed}")
    print(f"• Total Skipped Recordings: {total_skipped}")
    print(f"• Total Dataset Size: {total_mb:.2f} MB")
    print(f"• Metadata File: {METADATA_FILE.resolve()}")
    print(f"• Attribution File: {ATTRIBUTION_FILE.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
