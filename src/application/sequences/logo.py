from io import StringIO
from typing import List, Tuple

import logomaker as lm
import pandas as pd

from application.sequences.lasagna import Align


def lasagna_alignment(sequences: List[str]) -> List[str]:
    to_align = {'sequences': [], 'headers': []}
    for i, seq in enumerate(sequences):
        to_align['sequences'].append(seq.upper())
        to_align['headers'].append(f'seq_{i}')

    aligned_sequences = Align(to_align, k=0)
    return aligned_sequences['sequences']


def relative_frequency(*args, **kwargs):
    kwargs['normalize'] = True
    return pd.value_counts(*args, **kwargs)


def make_pwm(sequences: List[str]) -> Tuple[pd.DataFrame, List[str]]:
    aligned_sequences = lasagna_alignment(sequences)
    df = pd.DataFrame([list(seq) for seq in aligned_sequences])
    pwm = df.apply(relative_frequency)
    pwm = pwm.fillna(0)
    pwm = pwm.transpose()
    return pwm, aligned_sequences


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
