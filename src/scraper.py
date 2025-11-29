import requests
import time
import os


def scrape_cazy(family_type, start, end, output_file):
    """
    Scrapes structure data for a range of CAZy families (GH or GT)
    and saves it to a TSV file.

    Args:
        family_type (str): 'GH' or 'GT'.
        start (int): Start family number.
        end (int): End family number.
        output_file (str): Path to the output TSV file.
    """
    # Create header if file does not exist
    if not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Family\tEC_Number\tPDB_ID\tUniProt_ID\tLigands\tResolution\n")

    print(f"--- Starting scrape for {family_type} families {start} to {end} ---")

    for family_num in range(start, end + 1):
        family_name = f"{family_type}{family_num}"
        url = f"https://www.cazy.org/{family_name}_structure.html"

        print(f"Processing: {family_name}...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            ifile = response.text.splitlines()

            # Lists to store parsed data
            ecs, pdbs, ligs, ress, unips = [], [], [], [], []

            # --- Parse EC numbers ---
            for i in range(len(ifile)):
                if ifile[i][2:45] == '<tr valign="top" onmouseover="this.bgColor=':
                    ecline = ifile[i + 2]
                    sline = str.split(ecline, 'target="_link">')
                    oneecs = []
                    if len(sline) > 1:
                        for j in range(len(sline) - 1):
                            oneecs.append(str.split(sline[j + 1], "<")[0])
                    ecs.append(oneecs if oneecs else ["unk"])

            # --- Parse PDB data ---
            for i in range(len(ifile)):
                if ifile[i][5:36] == "<table width='100%' border='0'>":
                    pdbline, ligline, resline = [], [], []

                # PDB ID
                if ifile[i][2:39] == '<td id="separateur2"   width="125px">':
                    pdbline.append(str.split(str.split(ifile[i], ">")[2], "<")[0])

                # Ligands
                if (
                    ifile[i][5:27] == '<td id="separateur2" >'
                    or ifile[i][5:10] == "<td >"
                ):
                    if (
                        '<td id="separateur2" ></td>' in ifile[i]
                        or "<td ></td>" in ifile[i]
                    ):
                        ligline.append("none")
                    else:
                        sline = str.split(ifile[i], ">")
                        full = ""
                        for j in range(len(sline) - 3):
                            full = full + sline[j + 1][:-3]
                        ligline.append(full if full else "none")

                # Resolution
                if (
                    ifile[i][5:40] == '<td id="separateur2"  width="145px"'
                    or ifile[i][5:23] == '<td  width="145px"'
                ):
                    sline = str.split(ifile[i], ">")
                    resline.append(str.split(sline[1], "<")[0])

                # End of entry
                if ifile[i][5:18] == "</table></td>":
                    pdbs.append(pdbline)
                    ligs.append(ligline)
                    ress.append(resline)

                # UniProt ID
                if (
                    ifile[i][3:64]
                    == '<td id="separateur2"><a href="http://www.uniprot.org/uniprot/'
                ):
                    unips.append(str.split(str.split(ifile[i], ">")[2], "<")[0])

                # Handle missing UniProt
                if ifile[i][3:35] == '<td id="separateur2">&nbsp;</td>':
                    if (
                        (i + 1 < len(ifile))
                        and ifile[i + 1][3:64]
                        != '<td id="separateur2"><a href="http://www.uniprot.org/uniprot/'
                        and ifile[i + 1][3:35] != '<td id="separateur2">&nbsp;</td>'
                    ):
                        unips.append("noID")

            # Write to file
            with open(output_file, "a", encoding="utf-8") as f:
                for i in range(len(ecs)):
                    for j in range(len(pdbs[i])):
                        if j < len(ligs[i]) and j < len(ress[i]) and i < len(unips):
                            oline = f"{family_name}\t{ecs[i][0]}\t{pdbs[i][j]}\t{unips[i]}\t{ligs[i][j]}\t{ress[i][j]}\n"
                            f.write(oline)

        except Exception:
            # Skip families that don't exist or have errors
            pass

        time.sleep(0.2)  # A pause between requests to avoid server-side block
