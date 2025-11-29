import os
import sys
import argparse

# Add the current directory to the Python path to ensure the 'src' module is found
# This prevents "ModuleNotFoundError" when running the script from different locations
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import scraper, cleaner, sequence_downloader, clustering

# Configuration
DATA_DIR = "data"
GH_FILE = os.path.join(DATA_DIR, "gh_data.tsv")
GT_FILE = os.path.join(DATA_DIR, "gt_data.tsv")
CLEAN_IDS_FILE = os.path.join(DATA_DIR, "clean_uniprot_ids.txt")
FASTA_FILE = os.path.join(DATA_DIR, "all_sequences.fasta")
FINAL_DATASET = os.path.join(DATA_DIR, "dataset_final_90.fasta")


def main():
    # Setup Argument Parser
    # Allows the user to run 'python main.py --full' for the complete dataset
    # FULL RUN is computationally expensive!
    parser = argparse.ArgumentParser(description="Bio-ML Dataset Pipeline")

    parser.add_argument(
        "--full",
        action="store_true",
        help="Run the full analysis on all families. WARNING: This is resource-intensive and recommended for cluster/HPC environments.",
    )
    args = parser.parse_args()

    # 2. Determine scraping range based on arguments
    if args.full:
        gh_end, gt_end = 195, 120
        print("Full run initialized (This may take a while)")
    else:
        gh_end, gt_end = 5, 5
        print("Demo run initialized (Scraping only first 5 families)")
        print("    (Use 'python main.py --full' to scrape everything)")

    # Ensure the data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    print("ML DATASET PREPARATION PIPELINE")

    # 3. STEP 1: SCRAPING
    # Scrapes data from CAZy database based on the determined range
    scraper.scrape_cazy("GH", 1, gh_end, GH_FILE)
    scraper.scrape_cazy("GT", 1, gt_end, GT_FILE)

    # 4. STEP 2: CLEANING & FILTERING
    # Filters for ligand-containing entries and merges datasets
    cleaner.process_data(GH_FILE, GT_FILE, CLEAN_IDS_FILE)

    # 5. STEP 3: DOWNLOADING SEQUENCES
    # Fetches FASTA sequences from UniProt API if the ID list exists
    if os.path.exists(CLEAN_IDS_FILE):
        sequence_downloader.fetch_sequences(CLEAN_IDS_FILE, FASTA_FILE)

    # 6. STEP 4: CLUSTERING (CD-HIT)
    # Removes redundant sequences. Uses fallback data if CD-HIT is not installed (Windows).
    if os.path.exists(FASTA_FILE):
        # For a full production run, we typically use 0.90 threshold
        clustering.run_cdhit(FASTA_FILE, FINAL_DATASET, threshold=0.90)

    print("\nPIPELINE FINISHED")


if __name__ == "__main__":
    main()
