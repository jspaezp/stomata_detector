#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import pandas as pd

CSV_COLUMN_NAMES = [
    'filename',
    'xmin',
    'ymin',
    'xmax',
    'ymax',
    'class']


def main(csv_dir: str, out_boxes_csv: str,
         out_classes_csv: str, int_coordinates: bool = False):

    dirfiles = os.listdir(csv_dir)
    csv_files = [x for x in dirfiles if x.endswith(".csv")]

    box_dfs = [pd.read_csv(os.path.join(csv_dir, x)) for x in csv_files]
    full_df = pd.concat(box_dfs)

    if int_coordinates:
        for colname in ['xmin', 'xmax', 'ymax', 'ymin']:
            full_df[colname] = full_df[colname].astype('int32')

    full_df.to_csv(out_boxes_csv, index=False, header=False)
    unique_classes = set(full_df['class'])
    unique_classes = [x for x in unique_classes if isinstance(x, str)]

    with open(out_classes_csv, "w+") as f:

        for i, x in enumerate(unique_classes):
            f.write(x+","+str(i)+"\n")


@click.command()
@click.option("--csv_dir", type=str)
@click.option("--out_boxes_csv", type=str)
@click.option("--out_classes_csv", type=str)
@click.option("--int_coordinates", is_flag=True)
def cli(csv_dir, out_boxes_csv, out_classes_csv, int_coordinates):
    main(csv_dir=csv_dir,
         out_boxes_csv=out_boxes_csv,
         out_classes_csv=out_classes_csv,
         int_coordinates=int_coordinates)


if __name__ == '__main__':
    cli()
