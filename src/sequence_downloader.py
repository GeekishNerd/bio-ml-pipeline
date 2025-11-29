import requests
import time


def fetch_sequences(id_file, output_fasta, chunk_size=200):
    """
    Reads a list of IDs and downloads their FASTA sequences from UniProt API.

    Args:
        id_file (str): Path to the file containing IDs.
        output_fasta (str): Path to save the FASTA sequences.
        chunk_size (int): Number of IDs to query at once.
    """
    print(f"Downloading sequences from UniProt")

    try:
        # Read IDs
        with open(id_file, "r") as f:
            unique_ids = [line.strip() for line in f if line.strip()]

        total_ids = len(unique_ids)

        with open(output_fasta, "w") as out_f:
            # Process in chunks, this avoids server-side request errors (Error 414)
            for i in range(0, total_ids, chunk_size):
                chunk = unique_ids[i : i + chunk_size]
                print(f"Downloading batch {i} - {min(i+chunk_size, total_ids)}...")

                # Prepare API request
                ids_str = ",".join(chunk)
                url = "https://rest.uniprot.org/uniprotkb/accessions"
                params = {"accessions": ids_str, "format": "fasta"}

                response = requests.get(url, params=params)

                if response.ok:
                    out_f.write(response.text)
                else:
                    print(
                        f"Warning: Batch failed with status code {response.status_code}"
                    )
                # Rate limiting - avoids overloading the server with requests
                time.sleep(0.5)

        print(f"Sequences saved to: {output_fasta}")
        return output_fasta

    except Exception as e:
        print(f"Error during download: {e}")
        return None
