from typing import List


class Colors:
    _red = '255, 99, 132'
    _orange = '255, 159, 64'
    _yellow = '255, 205, 86'
    _green = '75, 192, 192'
    _blue = '54, 162, 235'
    _purple = '153, 102, 255'
    _grey = '201, 203, 207'

    _all_colors = {'red': _red,
                   'orange': _orange,
                   'yellow': _yellow,
                   'green': _green,
                   'blue': _blue,
                   'purple': _purple,
                   'grey': _grey}

    @classmethod
    def get_color(cls, key: str, muted: bool = False) -> str:
        color = cls._all_colors[key]
        if muted:
            return f'rgba({color}, 0.5)'
        return f'rgba({color}, 1)'

    @classmethod
    def get_palette(cls, size: int, muted: bool = False) -> List[str]:
        if size > len(cls._all_colors):
            raise ValueError('Not enough colors')

        size = size - 1

        if muted:
            colors = []
            for i, color in enumerate(cls._all_colors.values()):
                color = f'rgba({color}, 0.5)'
                colors.append(color)

                if i >= size:
                    break

        else:
            colors = []
            for i, color in enumerate(cls._all_colors.values()):
                color = f'rgba({color}, 1)'
                colors.append(color)

                if i >= size:
                    break

        return colors
