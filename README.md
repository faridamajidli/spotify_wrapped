# Spotify Wrapped Data Simulation
![image](https://github.com/dtroje2/streamanalytics/assets/94994961/4080a74e-edd0-4c96-96d3-45268ab2d4c0)

## Overview

This project is designed to create a comprehensive AVRO schema tailored for the Spotify Wrapped data feed, alongside scripts that generate synthetic data to emulate user streaming experiences. By simulating user interactions with songs—including playing, skipping, liking, and playlist additions—it captures the essence of real-world music streaming behavior. Utilizing different datasets, the project categorizes songs and user interactions into distinct listening personalities, reflecting varied musical preferences and habits. 

## Objective

- **Develop an AVRO schema** for the Spotify Wrapped data feed, defining data structures for song plays, user interactions, and other relevant data points.
- **Categorize personality** by assigning listening personalities to users based on the songs they interact with.
- **Create synthetic data generation scripts** to simulate the streaming experiences of both a single user and multiple, independent users, producing realistic, time-series data reflecting user interaction patterns.

## Deliverables

- **AVRO Schema Design Document**: Outlines the structure and types of data in the Spotify Wrapped feed. (spotify_data.avro)
- **Synthetic Data Generation Scripts**:
  - A script to simulate the streaming experience of a single user, creating a realistic sequence of song plays, pauses, skips, and other interactions. (single_user.py)
  - A script to simulate multiple, independent users, ensuring a variety of streaming behaviors are represented. (multiple_user.py)

## Tools Used

- **fastavro**: Utilized for handling data serialization in AVRO format. 
- **Numpy / Pandas**: For numerical calculations and data frame manipulation, crucial in structuring and analyzing synthetic data. 
- **Faker**: Used for synthetic data generation.

## Installation

To run the scripts, you need to install several Python libraries. You can install them using pip:

```bash
pip install pandas numpy fastavro arrow faker
from fastavro import parse_schema
from fastavro import writer, reader
from google.colab import drive
import pandas as pd
import numpy as np
import uuid
import datetime
import random, os
from faker import Faker
```
## Usage

1. Mount Google Drive to access the datasets:

```bash
from google.colab import drive
drive.mount('/content/drive')
```

2. Load the Datasets from your Google Drive following the directory structure provided in the code.

3. Run the Synthetic Data Generation Scripts to generate data for a specified time range and user interactions.

```bash
start_day = datetime.datetime.now()
end_day = start_day + datetime.timedelta(hours=1)  # Simulate for one hour
all_data, user_personalities = generate_multiple_user_data(start_day, end_day, personality_datasets)
```

## Features
- **Realism and Variety**: Generates data that realistically mimics user behavior patterns in terms of song selections, play times, interaction types, and session durations.
- **Scalability**: Can simulate varying loads, from a single user to multiple users, to test the system’s scalability and robustness.
- **Configurability**: Allows configuration of parameters like the duration of simulation, the time of a session, the frequency of users entering the app, and frequency of interactions.

## Challenges and Solutions:

- **Time Generation**:
The primary challenge involved realistically simulating user behavior within the app. Our approach utilized a Poisson distribution to accurately model the timing of user arrivals, durations spent in the app, and intervals between interactions with songs.

- **User Personality Differentiation**:
We aimed to capture the diversity of user personalities, adopting the Spotify classification system as a foundation. Personalities were linked to specific datasets, restricting interactions to songs within those collections. This method, while effective, may not fully capture the complexity of musical tastes, as users often explore beyond their usual preferences.

- **Behavioral Variety**:
Ensuring a broad spectrum of user actions from entry to exit posed a significant challenge. We confined interactions to predefined actions such as playing, skipping, and liking tracks. This restriction, however, may limit the accuracy of analyses concerning the duration of song engagement by users.

## References
- Inspired by Spotify's concept of "Listening Personality", this project aims to creatively reflect the features in the synthetic feed, influencing the fields and data types. https://engineering.atspotify.com/2023/01/whats-a-listening-personality/ 
- Explores the use of generative AI models for creating complex and varied datasets, including text generation models for realistic user comments or interaction patterns. 
- For a deeper understanding of AVRO data serialization, consult the official AVRO documentation and tutorials.

## Credits
The authors of this project are:

1. Majidli, Farida
2. Troje, Delphine
3. Ploquin, Tomas
4. Pascual, Fernando
5. Conesa, Angel
6. Oliver, Paula

