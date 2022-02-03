from django_neomodel import DjangoNode
from rest_framework import serializers

from constants import alphabets


def validate_protein_sequence(validated_data: dict, instance: DjangoNode = None) -> dict:
    validated_data = validated_data.copy()

    sequence = validated_data.get('sequence', getattr(instance, 'sequence', ''))
    strand = validated_data.get('strand', getattr(instance, 'strand', None))
    start = validated_data.get('start', getattr(instance, 'start', None))
    stop = validated_data.get('stop', getattr(instance, 'stop', None))

    if sequence:
        sequence = sequence.upper()

        if not all(letter in alphabets.protrein for letter in sequence):
            raise serializers.ValidationError(f"Protein sequence {sequence} contains not allowed characters. "
                                              f"Please submit a protein sequence "
                                              f"with the following chars: {alphabets.protrein}")

        validated_data['sequence'] = sequence

    if strand is not None or start is not None or stop is not None:
        if strand == 'forward' and start > stop:
            raise serializers.ValidationError(f"Start and stop values of {start} - {stop} "
                                              f"do not match the strand value of {strand}")

        if strand == 'reverse' and stop > start:
            raise serializers.ValidationError(f"Start and stop values of {start} - {stop} "
                                              f"do not match the strand value of {strand}")

    return validated_data


def validate_dna_sequence(validated_data: dict, instance: DjangoNode = None) -> dict:
    validated_data = validated_data.copy()

    sequence = validated_data.get('sequence', getattr(instance, 'sequence', ''))
    strand = validated_data.get('strand', getattr(instance, 'strand', None))
    start = validated_data.get('start', getattr(instance, 'start', None))
    stop = validated_data.get('stop', getattr(instance, 'stop', None))
    length = validated_data.get('length', getattr(instance, 'length', None))

    if sequence:
        sequence = sequence.upper()

        if not all(letter in alphabets.dna for letter in sequence):
            raise serializers.ValidationError(f"DNA sequence {sequence} contains not allowed characters. "
                                              f"Please submit a DNA sequence "
                                              f"with the following chars: {alphabets.dna}")

        validated_data['sequence'] = sequence

    if length is None:
        length = len(sequence)

    if len(sequence) != length:
        raise serializers.ValidationError(f"Provided sequence of length {len(sequence)} "
                                          f"does not match length field of {length}")

    if strand is not None or start is not None or stop is not None:

        if strand == 'forward' and start > stop:
            raise serializers.ValidationError(f"Start and stop values of {start} - {stop} "
                                              f"do not match the strand value of {strand}")

        if strand == 'reverse' and stop > start:
            raise serializers.ValidationError(f"Start and stop values of {start} - {stop} "
                                              f"do not match the strand value of {strand}")

        diff = stop - start
        if strand == 'reverse':
            diff = start - stop

        if diff != length:
            raise serializers.ValidationError(f"Start and stop values of {start} - {stop} "
                                              f"do not match the provided sequence of length {len(sequence)}")

    return validated_data
