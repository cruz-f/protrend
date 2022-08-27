from io import StringIO
from typing import List

import logomaker as lm
import pandas as pd
from Bio import motifs
from Bio.Seq import Seq


def relative_frequency(*args, **kwargs):
    kwargs['normalize'] = True
    return pd.value_counts(*args, **kwargs)


def make_pwm(aligned_sequences: List[str]) -> pd.DataFrame:
    df = pd.DataFrame([list(seq) for seq in aligned_sequences])
    pwm = df.apply(relative_frequency)
    pwm = pwm.fillna(0)
    pwm = pwm.transpose()
    return pwm


def make_motif(aligned_sequences: list):
    sequences = [Seq(sequence) for sequence in aligned_sequences]
    motif = motifs.create(sequences, alphabet='ATGC-')
    return motif


def make_motif_logo(pwm: pd.DataFrame) -> lm.Logo:
    logo = lm.Logo(pwm, color_scheme='classic')
    logo.ax.set_ylabel("nucleotide frequency", labelpad=-1)
    return logo


def make_motif_img(logo: lm.Logo) -> str:
    img_data = StringIO()
    logo.fig.savefig(img_data, format='svg')
    img_data.seek(0)

    data = img_data.getvalue()
    return data


def make_jaspar(motif):
    # heavily inspired by https://biopython.org/DIST/docs/api/Bio.motifs.jaspar.html#Bio.motifs.jaspar.write,
    # but changed to include the hyphen letter. All credits go to the Biopython team
    letters = "ACGT-"
    lines = [f">{motif.id} {motif.name}\n"]

    for letter in letters:
        terms = [f"{value:6.2f}" for value in motif.counts[letter]]
        line = f"{letter} [{' '.join(terms)}]\n"
        lines.append(line)

    text = "".join(lines)

    return text
