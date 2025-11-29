## Reference Data (CD-HIT Analysis)
Since running CD-HIT requires Linux/Cluster environment, this repository includes pre-computed results generated on the Metacentrum cluster.

**Redundancy Analysis Results:**
* Original dataset: 672 sequences
* 95% similarity cutoff: 609 clusters
* **90% similarity cutoff: 607 clusters (Selected for final dataset)**
* 80% similarity cutoff: 598 clusters
...
* 40% similarity cutoff: 460 clusters

The included fallback file `sample_data/reference_clusters.fasta` corresponds to the **90% cutoff** dataset.

## Configuration
By default, the pipeline is configured to run in a **fast demonstration mode**, scraping only the first 5 families (GH1-5, GT1-5) to verify functionality without long waiting times.

* **Demo Run:** Scrapes ~10 families (takes < 1 minute).
* **Full Production Run:** Scrapes all families (GH1-195, GT1-120). The included reference data (`sample_data/reference_clusters.fasta`) was generated using this full dataset 

To execute a full run, verify the range settings in `main.py`.