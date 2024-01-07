#!/bin/bash

DATA_FOLDER=truncated_data/

python3 cli.py resetall
python3 cli.py newtitles --filename $DATA_FOLDER/truncated_title.basics.tsv
python3 cli.py newakas --filename $DATA_FOLDER/truncated_title.akas.tsv
python3 cli.py newnames --filename $DATA_FOLDER/truncated_name.basics.tsv
python3 cli.py newcrew --filename $DATA_FOLDER/truncated_title.crew.tsv
python3 cli.py newepisode --filename $DATA_FOLDER/truncated_title.episode.tsv
python3 cli.py newprincipals --filename $DATA_FOLDER/truncated_title.principals.tsv
python3 cli.py newratings --filename $DATA_FOLDER/truncated_title.ratings.tsv

