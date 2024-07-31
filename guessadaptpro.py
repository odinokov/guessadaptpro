"""
This script is a fork of https://github.com/micknudsen/guessadapt/ with a corrected sequence for Nextera adapters.

Given a FASTQ file and a list of adapter sequences, guessadaptpro simply counts the number of occurrences of each adapter and returns a sorted list of counts along with the sequencing kit name, if available.
"""

import argparse
import subprocess
from typing import Iterator, Dict, List


def count_adapters_in_fastq(stream: Iterator[str], adapters: List[str], limit: int = None) -> Dict[str, int]:
    """
    Parse a FASTQ file stream and count occurrences of specified adapter sequences on-the-fly.
    """
    counts = {adapter: 0 for adapter in adapters}
    count = 0

    while True:
        try:
            next(stream)  # Skip the identifier line
            sequence = next(stream).strip()  # Get the sequence line, stripped of whitespace
            for adapter in adapters:
                if adapter in sequence:
                    counts[adapter] += 1
                    break  # Found an adapter, no need to check further for this sequence
            next(stream)  # Skip the plus line
            next(stream)  # Skip the quality score line
            count += 1
            if limit and count >= limit:
                break
        except StopIteration:
            break

    return counts


def main():
    """
    Main function to parse command-line arguments, read the FASTQ file, count adapters,
    and print the results.
    """
    parser = argparse.ArgumentParser(description='Count adapter sequences in a FASTQ file.')

    # Default adapter sequences and their names
    adapter_names = {
        'AGATCGGAAGAGC': 'Illumina TruSeq',
        'TGGAATTCTCGG': 'Illumina small RNA',
        'CTGTCTCTTATACACATCT': 'Nextera',
        'AAGTCGGAGGCCAAGCGGTC': 'BGI Read 1',
        'AAGTCGGATCGTAGCCATGT': 'BGI Read 2'
    }
    default_adapters = ','.join(adapter_names.keys())

    parser.add_argument('fastq', help='Path to input FASTQ file')
    parser.add_argument('--limit', '-n', type=int, required=False, help='Maximal number of reads to consider')
    parser.add_argument('--adapters', '-a', required=False, default=default_adapters, help='Comma-separated list of adapters (default: %(default)s)')
    
    args = parser.parse_args()

    # Use crabz to decompress the file and pipe the output to the script
    crabz_command = ['crabz', '-dQp1', args.fastq]
    adapter_list = args.adapters.split(',')
    
    try:
        with subprocess.Popen(crabz_command, stdout=subprocess.PIPE, text=True) as proc:
            # Count the adapter sequences in the FASTQ file stream
            adapter_counts = count_adapters_in_fastq(proc.stdout, adapters=adapter_list, limit=args.limit)
                
    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Sort the counts from largest to smallest
    sorted_counts = sorted(adapter_counts.items(), key=lambda x: x[1], reverse=True)

    # Print the counts of each adapter sequence found
    for adapter, count in sorted_counts:
        print(adapter, count, adapter_names.get(adapter, ''))
                
if __name__ == '__main__':
    main()
