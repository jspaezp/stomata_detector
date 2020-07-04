#!/usr/bin/env python
# -*- coding: utf-8 -*-

# modified from:
# https://gist.github.com/rotemtam/88d9a4efae243fc77ed4a0f9917c8f6c

import os
import glob
import click

import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path: str) -> pd.DataFrame:
    xml_list = []
    for xml_file in glob.glob(path):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = int(bbx.find('xmin').text)
            ymin = int(bbx.find('ymin').text)
            xmax = int(bbx.find('xmax').text)
            ymax = int(bbx.find('ymax').text)
            label = member.find('name').text

            # The columns are organized as the csv required by keras-retinanet
            # https://github.com/fizyr/keras-retinanet#csv-datasets
            # path/to/image.jpg,x1,y1,x2,y2,class_name

            value = (root.find('filename').text,
                     # int(root.find('size')[0].text),
                     # int(root.find('size')[1].text),
                     xmin, ymin,
                     xmax, ymax,
                     label)
            xml_list.append(value)
    column_name = ['filename',
                   # 'width',
                   # 'height',
                   'xmin',
                   'ymin',
                   'xmax',
                   'ymax',
                   'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xml_to_csv_file(infile: str, outfile: str):
    xml_df = xml_to_csv(infile)
    print(xml_df)
    xml_df.to_csv(outfile, index=None)


@click.group(help='Converts a pascal xml to csv')
def cli():
    pass


@cli.command()
@click.option('--dir', type=str,
              help='Name of source directory,' +
              ' will convert all xml files in it')
@click.option('--out_dir', type=str,  help='Name of the destination directory')
def directory(dir, out_dir):
    files_convert = [x for x in os.listdir(dir) if x.endswith("xml")]
    for xml_file in files_convert:
        base = os.path.basename(xml_file)
        filename = os.path.splitext(base)[0]

        out_filename = filename + ".csv"
        out_path = os.path.join(out_dir, out_filename)
        xml_to_csv_file(os.path.join(dir, xml_file), out_path)


@cli.command()
@click.option('--file', type=str,  help='File to be converted to csv')
@click.option('--out', type=str,  help='Name of the destination file')
def xml(file, out):
    xml_to_csv_file(file, out)


if __name__ == '__main__':
    cli()
