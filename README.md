# guessadaptpro

Given a FASTQ file and a list of adapter sequences, `guessadaptpro` simply counts the number of occurrences of each adapter and returns a sorted list of counts along with the sequencing kit name, if available.

## Prerequisites

To install `crabz`, use the following command:

```sh
mamba install conda-forge::crabz
```

## Usage

```bash
$ python guessadaptpro.py --help
usage: guessadaptpro.py [-h] [--limit LIMIT] [--adapters ADAPTERS] fastq

Count adapter sequences in a FASTQ file.

positional arguments:
  fastq                 Path to input FASTQ GZ file

optional arguments:
  -h, --help            show this help message and exit
  --limit LIMIT, -n LIMIT
                        Maximal number of reads to consider
  --adapters ADAPTERS, -a ADAPTERS
                        Comma-separated list of adapters (default: AGATCGGAAGAGC,TGGAATTCTCGG,CTGTCTCTTATACACATCT,AAGTCGGAGGCCAAGCGGTC,AAGTCGGATCGTAGCCATGT)
```

## Example

```sh
$ time python guessadaptpro.py example.fastq.gz --limit 2000000
AGATCGGAAGAGC   1709862 Illumina TruSeq
TGGAATTCTCGG    37      Illumina small RNA
CTGTCTCTTATACACATCT     0       Nextera
AAGTCGGAGGCCAAGCGGTC    0       BGI Read 1
AAGTCGGATCGTAGCCATGT    0       BGI Read 2

real    1m8.361s
user    1m16.652s
sys     0m6.031s

$ time guessadapt example.fastq.gz --limit 2000000
AGATCGGAAGAGC   1709862
CTGTCTCTTATA    328
TGGAATTCTCGG    37

real    1m3.841s
user    1m16.785s
sys     0m4.429s
```

## Acknowledgments
Fork of [guessadapt](https://github.com/micknudsen/guessadapt/) with a corrected sequence for Nextera adapters.
