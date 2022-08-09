from io import StringIO
from typing import List, Tuple

import logomaker as lm
import pandas as pd

from application.sequences.lasagna import Align


def relative_frequency(*args, **kwargs):
    kwargs['normalize'] = True
    return pd.value_counts(*args, **kwargs)


def make_pwm(aligned_sequences: List[str]) -> pd.DataFrame:
    df = pd.DataFrame([list(seq) for seq in aligned_sequences])
    pwm = df.apply(relative_frequency)
    pwm = pwm.fillna(0)
    pwm = pwm.transpose()
    return pwm


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
