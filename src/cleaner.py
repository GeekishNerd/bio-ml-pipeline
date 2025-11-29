import pandas as pd
import os


def process_data(gh_file, gt_file, output_file):
    """
    Loads raw data files (from scraper.py), filters for ligand-containing entries,
    removes invalid IDs, and saves a unique list of UniProt IDs.

    Args:
        gh_file (str): Path to GH raw data.
        gt_file (str): Path to GT raw data.
        output_file (str): Path to save the clean ID list.
    """
    print(f"--- merging and cleaning data ---")

    try:
        # 1. Check if files exist
        if not os.path.exists(gh_file) or not os.path.exists(gt_file):
            print("Error: Input files not found. Skipping cleaning step.")
            return None

        # 2. Load data in CSV files
        df_gh = pd.read_csv(gh_file, sep="\t")
        df_gt = pd.read_csv(gt_file, sep="\t")

        # 3. Filter for Ligands (remove entries with 'none')
        df_gh_filtered = df_gh.loc[df_gh["Ligands"] != "none"].copy()
        df_gt_filtered = df_gt.loc[df_gt["Ligands"] != "none"].copy()

        # 4. Combine datasets (merges the data for GH and GT enzyme families)
        df_combined = pd.concat([df_gh_filtered, df_gt_filtered])

        # 5. Clean IDs (remove 'noID', 'unk' and NaNs)
        junk_values = ["noID", "unk"]
        valid_data = df_combined.loc[~df_combined["UniProt_ID"].isin(junk_values)]
        valid_data = valid_data.dropna(subset=["UniProt_ID"])

        # 6. Get unique IDs
        unique_ids = valid_data["UniProt_ID"].unique()

        print(f"Found {len(unique_ids)} unique sequences with ligands.")

        # 7. Save to file
        with open(output_file, "w") as f:
            for uid in unique_ids:
                f.write(f"{uid}\n")

        return output_file

    except Exception as e:
        print(f"Error during data processing: {e}")
        return None
