import subprocess
import shutil
import os


def run_cdhit(input_fasta, output_fasta, threshold=0.90):
    """
    Runs the CD-HIT algorithm, if CD-HIT is not installed on the user's computer it uses "fallback" data (reference_clusters.fasta from CD-HITs done on Metacentrum's cluster)
    """
    print(f"--- Clustering (Current threshold: {threshold}) ---")

    # Path to "fallback" data
    sample_file = os.path.join("sample_data", "reference_clusters.fasta")

    # Checks that CD-HIT is installed on the computer
    if not shutil.which("cd-hit"):
        print("Warning: CD-HIT was not found.")

        # Attempts to use "fallback" data to allow the program to finish
        if os.path.exists(sample_file):
            print(f"   -> Using the fallback data: {sample_file}")
            shutil.copy(sample_file, output_fasta)
            print(f"   -> Result saved to: {output_fasta}")
            return count_sequences(output_fasta)
        else:
            # If CD-HIT is not installed and no fallback data found, a dummy run is initialized - copies the input to output
            print("   -> Fallback data could not be found, dummy run initialized")
            shutil.copy(input_fasta, output_fasta)
            return count_sequences(output_fasta)

    # CD-HIT algoritm
    cmd = [
        "cd-hit",
        "-i",
        input_fasta,
        "-o",
        output_fasta,
        "-c",
        str(threshold),
        "-n",
        "5",
        "-M",
        "16000",
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"CD-HIT run finished!")
        return count_sequences(output_fasta)
    except subprocess.CalledProcessError as e:
        print(f"Error CD-HIT: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def count_sequences(fasta_file):
    """A function that counts the number of sequences succesfully clustered"""
    try:
        with open(fasta_file, "r") as f:
            return sum(1 for line in f if line.startswith(">"))
    except:
        return 0
