#!/bin/bash

echo "Downloading the datasets"
wget http://archive.ics.uci.edu/ml/machine-learning-databases/00346/EPMDataset%20.zip
mv 'EPMDataset .zip' EPMDataset.zip
wget http://archive.ics.uci.edu/ml/machine-learning-databases/00349/OULAD.zip

unzip EPMDataset.zip -d EPMDataset
mv ./EPMDataset/EPM\ Dataset\ 2/* ./EPMDataset/
rmdir EPMDataset/EPM\ Dataset\ 2/
unzip OULAD.zip -d OULAD

