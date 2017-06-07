import csv
import argparse
from itertools import chain
from pathlib import Path

import numpy as np
from scipy import signal

from util import read_metrics

pieces = [
    (149548966594, 149548968508),
    (149548979485, 149548980446),
    (149548990624, 149548992008),
    (149549001955, 149549003385),
    (149549010527, 149549011624),
    (149549040783, 149549041642),
    (149553054319, 149553055178),
    (149557630619, 149557632044),
    (149557643820, 149557644763),
    (149557654211, 149557655868),
    (149557674346, 149557675390),
    (149560789000, 149560790204),
    (149560866752, 149560868158),
    (149594523281, 149594524633),
    (149594523281, 149594524633),
    (149594551757, 149594553148),
    (149594626381, 149594627599),
    (149594635493, 149594636955),
    (149594643600, 149594645437),
    (149594658705, 149594659976),
    (149594669061, 149594670259),
    (149594688497, 149594689545),
    (149594697573, 149594698437),
    (149594702782, 149594703850),
    (149594807024, 149594808016),
    (149594814978, 149594816205),
    (149595133201, 149595134298),
    (149595142865, 149595143850),
    (149595146100, 149595147037),
    (149595206059, 149595207087),
    (149595221024, 149595222101),
    (149595238747, 149595239715),
    (149595251076, 149595252277),
    (149595273922, 149595275749),
    (149595294895, 149595296981),
    (149595299715, 149595301519),
    (149600813900, 149600815690),
    (149600827479, 149600828604),
    (149600837883, 149600839774),
    (149600849534, 149600850690),
    (149600858650, 149600859567),
    (149609451146, 149609451993),
    (149609462283, 149609464040),
    (149609473178, 149609474415),
    (149618091392, 149618092124),
    (149618096644, 149618098539),
    (149618138006, 149618139683),
    (149618149826, 149618151056),
    (149626760554, 149626762266),
    (149626773935, 149626774900),
    (149626784609, 149626786166),
    (149626796038, 149626797494),
    (149631045846, 149631046834),
    (149631073830, 149631074685),
    (149631131613, 149631133309),
]


def lpf(sig):
    b, a = signal.butter(3, 0.05, 'low')
    return signal.filtfilt(b, a, sig)


def process_piece(root, piece_no, start, end, writer):
    timestamps = [p.stem for p in root.rglob("*.jpg")
                  if int(p.stem) >= start and int(p.stem) <= end]
    metrics = np.array([read_metrics(next(root.rglob("{}.bin".format(ts))))
                        for ts in timestamps])
    reset_metrics = metrics - metrics[0]
    filtered_metrics = np.apply_along_axis(lpf, 0, reset_metrics)
    for i in range(metrics.shape[0]):
        writer.writerow([piece_no, timestamps[i], *metrics[i].tolist(),
                         *reset_metrics[i].tolist(), *filtered_metrics[i].tolist()])


def preprocess(root: Path, output: Path):
    with open(output, "w") as f:
        writer = csv.writer(f)
        for i, (start, end) in enumerate(pieces):
            process_piece(root, i, start, end, writer)


def main():
    parser = argparse.ArgumentParser(description='Preprocess Data.')
    parser.add_argument('--root', dest='root',
                        required=True, help='root path of data')
    parser.add_argument('--output', dest='output', default='processed.csv',
                        required=False, help='output path of processed data')
    args = parser.parse_args()
    root = Path(args.root)
    preprocess(root, args.output)


if __name__ == "__main__":
    main()
