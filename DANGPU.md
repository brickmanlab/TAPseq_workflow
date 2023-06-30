# Running pipeline

## 1. Preparation

```bash
srun -N 1 --ntasks-per-node=30 --pty bash
module load miniconda/latest
source activate snakemake
```

Go to your project folder and copy the [Tapseq_workflow pipeline](https://github.com/brickmanlab/TAPseq_workflow).

```bash
cd Brickman/projects/<PROJECT_ID>
git clone https://github.com/brickmanlab/TAPseq_workflow.git
```

## 2. Merging FASTQ files

If your `FASTQ` files are coming from multiple lanes,
you will have to merge them all into one read.

This means if you have files like this

```text
AGTAAACC_L0001_R1_001.fastq.gz
AGTAAACC_L0001_R2_001.fastq.gz
AGTAAACC_L0002_R1_001.fastq.gz
AGTAAACC_L0002_R2_001.fastq.gz
AGTAAACC_L0003_R1_001.fastq.gz
AGTAAACC_L0004_R2_001.fastq.gz
```

You will have to merge them like this below:

```bash
cat AGTAAACC/*R1_001.fastq.gz > AGTAAACC_R1.fastq.gz
cat AGTAAACC/*R2_001.fastq.gz > AGTAAACC_R2.fastq.gz
```

## 3. Update the configuration

Next step is to update the `config.yml` file. Here is a short
example what should be changed. Keep the second part of the configuration
unchanged. There is no need to customize it.

```yml
# sample id: /path/to/fastq/directory
samples:
  AACCGTAA: /projects/dan1/data/Brickman/projects/schuh-et-al-2024/data/assays/TAP_20230628/raw/fastq/
  ACGTCCCT: /projects/dan1/data/Brickman/projects/schuh-et-al-2024/data/assays/TAP_20230628/raw/fastq/

# estimated number of cells per sample, for which dge data should be extracted.
cell_numbers:
  AACCGTAA: 8000
  ACGTCCCT: 8000


# alignment reference for each  sample
align_ref:
  AACCGTAA: data/alignment_references/mm10_tapseq_ref
  ACGTCCCT: data/alignment_references/mm10_tapseq_ref

# 10x cell barcode whitelist file for each sample
10x_cbc_whitelist:
  AACCGTAA: "meta_data/10x_cell_barcode_whitelists/3M-february-2018.txt"
  ACGTCCCT: "meta_data/10x_cell_barcode_whitelists/3M-february-2018.txt"

# number of minimum molecules per CROP-seq vector to define a cell perturbed for a given vector
perturbation_status:
  min_txs:
    AACCGTAA: 8
    ACGTCCCT: 8
```

If you want to update the reference version change this part of the config.

```yaml
# step 1: create alignment reference ---------------------------------------------------------------
download_genome_annot:
  mm10:
    fasta_url: http://ftp.ensembl.org/pub/release-98/fasta/mus_musculus/dna/Mus_musculus.GRCm38.dna.primary_assembly.fa.gz
    gtf_url: http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M23/gencode.vM23.primary_assembly.annotation.gtf.gz
```

## 4. Create `cropseq_vectors`

Next, update the file in `meta_data/cropseq_vectors/CROPseq_vector_guides.xlsx`.
Run python script which will convert it to a correct format.

```bash
cd meta_data/cropseq_vectors
python ../../scripts/make_cropseq_fasta.py
```

## 5. Create target file

Last step is to create target file. You do so, by running `scripts/create_tapseq_annot.R`.

## 6. Run run run

Now you can run the pipeline with the commands below.

```bash
# generate references
snakemake --use-conda --jobs 30 alignment_references

# align reads
snakemake --use-conda --jobs 30 align_reads

# DGE
snakemake --use-conda --jobs 30 dge
```
