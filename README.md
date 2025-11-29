

# Bio-ML Dataset Preparation Pipeline

**Automated ETL pipeline for scraping, cleaning, and clustering biological sequence data to prepare high-quality datasets for Machine Learning.**

This project addresses a common challenge in bioinformatics: aggregating fragmented structural data from web databases (CAZy) and sequence repositories (UniProt) into a single, non-redundant dataset suitable for training Graph Neural Networks (GNNs).

-----

## Key Features

  * **Robust Web Scraping:** Automated extraction of structural data (PDB IDs, Ligands, EC numbers) from the CAZy database with error handling for missing pages.
  * **Data Cleaning & Filtering:** Uses `pandas` to merge disjoint datasets, filter for enzyme-substrate complexes, and remove invalid entries.
  * **API Integration:** Batch-processing downloader for UniProt REST API with rate limiting to prevent server timeouts.
  * **Cross-Platform Architecture:** Features a smart wrapper for the Linux-native `cd-hit` tool. The pipeline detects the operating system and adjusts behavior automatically (see Technical Highlights).

-----

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/TVOJE_JMENO/bio-ml-pipeline.git
    cd bio-ml-pipeline
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

-----

## Usage

The pipeline is controlled via the `main.py` entry point.

### 1\. Fast Demo Mode (Default)

Runs the pipeline on a small subset of families (GH1-5, GT1-5) to demonstrate functionality without long wait times.

```bash
python main.py
```

### 2\. Full Production Run

Scrapes and processes the entire database (hundreds of families). **Warning:** This is resource-intensive and takes time.

```bash
python main.py --full
```

-----

## Technical Highlights

### "Graceful Degradation" for CD-HIT

This project utilizes **CD-HIT**, a standard bioinformatic tool for removing redundant sequences, which is native to Linux/HPC environments.

To ensure this Python project runs successfully on **Windows machines** (where CD-HIT is typically missing), I implemented a fallback mechanism in `src/cluster.py`:

1.  The script checks for the tool using `shutil.which("cd-hit")`.
2.  **If found (Linux/WSL):** It executes the actual clustering algorithm using `subprocess`.
3.  **If missing (Windows):** It logs a warning and switches to **"Demo Mode"**, using pre-computed reference data stored in `sample_data/` to simulate the step.

This ensures the pipeline **never crashes** due to missing system-level dependencies.

### Project Structure

```text
bio_ml_pipeline/
├── data/          # Output directory for generated files
├── sample_data/   # Reference files for Windows fallback mode
├── src/           # Modular source code
│   ├── scraper.py     # CAZy web scraper
│   ├── cleaner.py     # Pandas data processor
│   ├── downloader.py  # UniProt API client
│   └── cluster.py     # CD-HIT wrapper
├── main.py        # CLI entry point
└── requirements.txt
```

-----

## Results (Reference)

Redundancy analysis performed on the full dataset using the Metacentrum HPC cluster:

  * **Original dataset:** 672 sequences
  * **95% similarity cutoff:** 609 clusters
  * **90% similarity cutoff:** 607 clusters **(Selected for ML training)**
  * **40% similarity cutoff:** 460 clusters

-----

## License

This project is licensed under the MIT License.
