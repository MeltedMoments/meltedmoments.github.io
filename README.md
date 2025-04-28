# Melted Moments Portfolio

This portfolio is (currently) a gathering place for small research projects in the general area of data annotation for machine learning. I will be concentrating on learning how to write annotation guidelines for Humans-In-The-Loop. 

## Proposed projects

### IMDB Sentiment Analysis

A very small project to perform a simple sentiment analysis on IMDB movie reviews.

 with one of two labels: positive or negative. 

### Image classification

Take a known body of images (small sample < 100 ), and classify eg cat vs dog.

### Amsterdam Canal House Facades classification

A more ambitious exercise: find a set of images of Amsterdam canal houses. Train an AI to recognise the [different types of facades (*gevels*)](https://www.grachtenvanamsterdam.nl/soortengevels.htm).

Classification

- https://www.joostdevree.nl/bouwkunde2/jpgg/gevel_8_klassiek_www_cultureel_erfgoed_nl.jpg
- https://image.parool.nl/216430784/width/2480/amsterdamse-gevels-van-kop-tot-kont-in-vier-boekjes-he-een

Where to find images?

[TU Delft "AmsterTime: A Visual Place Recognition Benchmark Dataset for Severe Domain Shift"](https://data.4tu.nl/articles/dataset/AmsterTime_A_Visual_Place_Recognition_Benchmark_Dataset_for_Severe_Domain_Shift/19580806
). A set of new and old images. The "old" images are probably more useful as they are in black&white (but watch bias). 

Use Label Studio to attach an ML tool? 

## Label Studio gotchas
- Try and get the labelling UI interface correct from the beginning. Changing things like the field names, or region labels will mess up any annotations already made. 

How to avoid manually redoing the annotations? Plan of attack?

- Export annotated data as JSON and/or CSV
- manually or via python change the data as required
- make a NEW project
- import the labelstudio.md (don't forget to make the changes first)
- then import the edited annotedata

