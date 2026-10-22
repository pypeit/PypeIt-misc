#!/usr/bin/env python
"""
Plot the growth of PypeIt (physical lines of code and documentation) over
time from the CSV written by count_lines.py, with the GenAI-attributed
portion shown as a stacked band inside each category.

Layers (bottom to top):
    Code, human     pypeit_src + pypeit_tests + doc_py, minus the AI lines
    Code, GenAI     the AI-attributed lines in those categories
    Docs, human     doc_hand + doc_gen (.rst), minus the AI lines
    Docs, GenAI     the AI-attributed lines in the docs

Usage:
    python plot_lines.py [--csv line_counts.csv] [--out lines_of_code]
"""
import argparse
import csv
from datetime import date

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CODE = ['pypeit_src', 'pypeit_tests', 'doc_py']
DOCS = ['doc_hand', 'doc_gen']
FIRST_AI = date(2026, 3, 16)

# Hues follow the entity (code vs docs); shade + hatch mark GenAI vs human.
BLUE, ORANGE = '#2a78d6', '#eb6834'
SURFACE, INK, INK2, GRID = '#ffffff', '#0b0b0b', '#52514e', '#e4e3df'


def tint(hex_color, frac=0.35):
    """Mix a hex color toward white; frac=1 is the full color."""
    rgb = np.array(matplotlib.colors.to_rgb(hex_color))
    return tuple(1 - frac * (1 - rgb))


def load(path):
    rows = []
    with open(path, newline='') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    rows.sort(key=lambda r: r['date'])
    d = np.array([date.fromisoformat(r['date']) for r in rows])
    tot = lambda keys, suf='': np.array(
        [sum(int(r[k + suf]) for k in keys) for r in rows])
    code, code_ai = tot(CODE), tot(CODE, '_ai')
    docs, docs_ai = tot(DOCS), tot(DOCS, '_ai')
    tags = [(date.fromisoformat(r['date']), r['label']) for r in rows
            if r['label'] and r['label'] != 'tip']
    return d, code, code_ai, docs, docs_ai, tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default='line_counts.csv')
    ap.add_argument('--out', default='lines_of_code')
    args = ap.parse_args()

    d, code, code_ai, docs, docs_ai, tags = load(args.csv)
    layers = [
        ('Code, human', code - code_ai, tint(BLUE), None),
        ('Code, GenAI', code_ai, BLUE, '////'),
        ('Docs, human', docs - docs_ai, tint(ORANGE), None),
        ('Docs, GenAI', docs_ai, ORANGE, '////'),
    ]

    plt.rcParams.update({
        'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
        'xtick.color': INK2, 'ytick.color': INK2, 'hatch.linewidth': 0.6,
    })
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    base = np.zeros_like(code, dtype=float)
    tops = []
    for name, y, color, hatch in layers:
        ax.fill_between(d, base, base + y, step=None, facecolor=color,
                        edgecolor=SURFACE if hatch is None else color,
                        linewidth=0.8, hatch=hatch, label=name, zorder=2)
        tops.append((base + y).copy())
        base = base + y

    # thin white separators between fills (the 2px surface gap)
    for t in tops[:-1]:
        ax.plot(d, t, color=SURFACE, linewidth=1.2, zorder=3)

    # release tags: x.y.0 only, as recessive ticks along the top
    major = [(td, lab) for td, lab in tags
             if lab.count('.') == 2 and lab.endswith('.0')
             and not lab.startswith('v')]
    # label only tags at least ~150 days apart so labels never collide
    shown, last = [], None
    for td, lab in sorted(major):
        if last is None or (td - last).days >= 150:
            shown.append((td, lab))
            last = td
    ymax = base.max() * 1.12
    for td, lab in shown:
        ax.axvline(td, color=GRID, linewidth=0.6, zorder=1)
        ax.text(td, ymax * 0.985, lab, rotation=90, ha='right', va='top',
                fontsize=6.5, color=INK2, zorder=4)

    # first GenAI-coauthored commit
    ax.axvline(FIRST_AI, color=INK, linewidth=0.8, linestyle=(0, (3, 3)),
               zorder=4)
    ax.annotate('first Claude\nco-authored commit\n2026-03-16',
                xy=(FIRST_AI, base[-1] * 0.55), xytext=(-8, 0),
                textcoords='offset points', ha='right', va='center',
                fontsize=7.5, color=INK)

    # direct labels at the right edge for every layer
    x_end = d[-1]
    prev = 0.0
    for (name, y, color, hatch), top in zip(layers, tops):
        mid = 0.5 * (prev + top[-1])
        ax.annotate(f'{name}  {int(y[-1]):,}', xy=(x_end, mid),
                    xytext=(6, 0), textcoords='offset points',
                    va='center', ha='left', fontsize=8, color=INK)
        prev = top[-1]

    total, ai = int(base[-1]), int(code_ai[-1] + docs_ai[-1])
    ax.set_title(
        f'PypeIt: {total:,} lines on develop as of {d[-1]:%Y-%m-%d}; '
        f'{ai:,} ({100 * ai / total:.1f}%) attributed to GenAI',
        fontsize=11, color=INK, loc='left', pad=12)
    ax.set_ylabel('Physical lines (code + docs)')
    ax.set_xlim(d[0], d[-1])
    ax.set_ylim(0, ymax)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v / 1000:.0f}k'))
    ax.grid(axis='y', color=GRID, linewidth=0.6, zorder=0)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), frameon=False,
              fontsize=8.5, ncol=4)
    fig.subplots_adjust(left=0.08, right=0.80, top=0.88, bottom=0.14)

    for ext in ('png', 'pdf'):
        fig.savefig(f'{args.out}.{ext}', facecolor=SURFACE)
        print(f'wrote {args.out}.{ext}')


if __name__ == '__main__':
    main()
