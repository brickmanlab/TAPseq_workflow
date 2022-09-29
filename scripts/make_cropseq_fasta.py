#!/usr/bin/env python
import pandas as pd

ROW_LENGTH: int = 80

df = pd.read_excel("CROPseq_vector_guides_file_final.xlsx", header=None)


with open("cropseq_vectors.fasta", "w") as output:
    for _, row in df.iterrows():
        comment = f">{row[0]}"
        seq = "\n".join(
            [row[2][i : i + ROW_LENGTH] for i in range(0, len(row[2]), ROW_LENGTH)]
        )
        output.write(f"{comment}\n")
        output.write(f"{seq}\n")
