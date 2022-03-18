from io import StringIO

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from rest_framework import serializers

from constants import alphabets


def make_fasta_file(identifier: str, name: str, sequence: str, description: str):
    if not sequence:
        sequence = ''

    sequence = sequence.upper()

    if not all(letter in alphabets.protrein for letter in sequence):
        raise serializers.ValidationError(f"Protein sequence {sequence} contains not allowed characters. "
                                          f"Please submit a protein sequence "
                                          f"with the following chars: {alphabets.protrein}")

    seq = Seq(sequence)
    record = SeqRecord(seq=seq,
                       id=identifier,
                       name=name,
                       description=description)

    buffer = StringIO()
    SeqIO.write(record, buffer, "fasta")
    return buffer.getvalue()
