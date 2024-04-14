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

## Methodology

### Datasets needed for the simulation
Using the Spotify dataset found on Kaggle, we created eight different datasets. This was done according to the 16 personalities identified by Spotify on their website. These 16 personalities are made of four pairs of characteristics. These four categories are the following:
1. FAMILIARITY (F) vs. EXPLORATION (E): Do you mostly listen to your favorite artists over and over (Familiarity), or do you sample a lot of new artists (Exploration)?
2. LOYALTY (L) vs. VARIETY (V): Do you find yourself going back to the same tracks and playing them on repeat (Loyalty) or do you like to spin through a lot of music before repeating (Variety)?
3. TIMELESSNESS (T) vs. NEWNESS (N): Do you listen to brand new music right when it comes out (Newness), or do you wander the vast catalog of all the music ever made (Timelessness)? 
4. COMMONALITY (C) vs. UNIQUENESS (U): Do you listen to mostly popular artists along with millions of fellow fans (Commonality) or do you look deeper for someone less well known (Uniqueness)?


According to these descriptions, we split our dataset. Every letter (F, E, L, V, T, N, C, U) had its respective dataset. For example, in the first category, the F dataset has songs from mainly 1 artist, while the E dataset contains songs from various artists. Overall, creating eight datasets seemed to be essential when analyzing the listening personality of our users in the simulation.  


Once these datasets were created, each user was randomly assigned to adopt one of these 16 listening personalities.

### Simulation

The data simulation for the users consisted of two parts. The first part was to access the song-related columns from the Spotify dataset. The second part was to generate fake data for user-related columns using Faker(). 


To be able to observe the same users across time, we prerun the simulation to get a fix set of users id.  We set the simulation time to 48 hours and generated in total around 7,000 unique users. Later this generated dataset was fed to Kafka for pre-set unique userIDs. The complete updated code for Milestone 1 is to be found on the GitHub. 

In this step, an Avro schema for the Spotify Wrapped data is defined with various fields such as userId, songId, genre, etc., including enumerations for interactionType and subscriptionType. The above-mentioned CSV files containing the song personality dataset and user ID information are loaded into Pandas DataFrames. 


To generate records we used two functions: generate_user_data and generate_multiple_user_data, with the latest having start time and end time as input and calling the former function until the end time is reached. The function generate_user_data ensures that the user and the user interaction data for Spotify between a start and an end time are as similar to real life as possible, this is achieved through several techniques. 


First, it sets the rate for the exponential distribution, which is used to model the time between song plays as we assumed that a song plays approximately every two minutes. We chose this value because in general, a song is 3 minutes.  Per session the user has the same location, continent, user personality, and subscription type. Location and continent are determined using helper functions that get a valid country and its continent. These locations are used to provide geographic context to the data. The subscription type (e.g., Free, Premium, Family) is randomly selected from the provided options and will be used later in the analysis. To ensure that the songs played are consistent with the personality of our users, we take use random personality_datasets, and one dataset is randomly selected for each personality trait group. These selections are combined into a combined_dataset DataFrame, which represents the song information that matches the user's personality. The events are appended to a record that is saved in the machine. There are several challenges that arised with this code and that contradict real life behavior, we will talk about it in the chapter “Challenges encounters”.
The function generate_multiple_user_data is in charge of ensuring that the system as a whole and the behavior between users simulate real life. It achieved this through the following mechanisms. Firstly, the simulation configuration defines the rate of arrival of the new user and the rate defining session duration. The rate parameter for the exponential distribution governing the arrival of new users, set to imply 0.05 every minute new users every minute or 1 every two minutes. This rate is not attempting to be the one of Spotify but we lowered it to enable a reasonable performance, we believe this rate will mirror the rate of smaller companies with lower users.  The  rate parameter for the exponential distribution that determines the length of each user's session, set to an average session duration of 30 minutes with a minimum at 5 minutes to ensure that there is a session opening. We set this parameter as based on our personal observation, the duration of a session average this time. The user ID for this session is taken from a dataset as we this enables us to model the same users over a period of time. Each generated record is then sent to the Kafka topic specified by topic_name. The continent field from the record is used to determine the partition to which the message should be sent, based on the partitions dictionary.



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

