# Spotify Wrapped: Milestone 2
## Overview of Milestone 1
Leveraging the Spotify dataset from Kaggle, we generated eight distinct datasets aligned with the 16 listening personalities published on Spotify website. These personalities derive from four dualistic traits:

1. Familiarity (F) vs. Exploration (E): Do listeners prefer repeated tracks from favorite artists, or explore new ones?
2. Loyalty (L) vs. Variety (V): Is there a tendency to replay the same tracks, or a preference for a diverse listening experience?
3. Timelessness (T) vs. Newness (N): Do users focus on the latest tracks, or enjoy a broader historical range?
4. Commonality (C) vs. Uniqueness (U): Do listeners choose popular tracks shared by millions, or seek out lesser-known artists?

Based on these characteristics, we segmented our dataset into eight subsets, each corresponding to one trait (F, E, L, V, T, N, C, U). For instance, the 'F' dataset primarily includes tracks from a single artist, whereas the 'E' dataset features a variety of artists. This segmentation is crucial for analyzing the simulated listening preferences of our users.

Each user was randomly assigned one of the 16 personalities for the simulation. In the first milestone, our AVRO schema featured two array fields for user interactions and song plays. For the second milestone, we streamlined the data structure by eliminating these array fields.

The user data simulation comprised two phases: extracting song-related data from the Spotify dataset and generating synthetic user data using the Faker library. To ensure continuity, we pre-ran the simulation to establish a fixed set of user IDs. We set the simulation period to 72 hours, during which we generated approximately 20,000 unique users. This dataset was then processed and ingested by Kafka using pre-defined unique user IDs. The updated code for Milestone 1 is available on this repository.

## Configuration

The setup for Milestone 2 involves four key steps: creating the Kafka environment, setting up the data producer, configuring the data consumer, and configuring the Kafka and Spark Python environment.

Step 1. Create the Kafka Environment

First, we establish a Kafka environment, comprising a Kafka broker and the topic "SpotifyWrapped". We configure the topic with seven partitions to align with the seven continents, merging Oceania and Antarctica due to lower population density. This partitioning strategy ensures data distribution uniformity, enhancing scalability. Given our single broker setup, we limited the number of partitions.

Step 2. Create the Data Producer

Here, we define an Avro schema for the Spotify Wrapped data, encompassing fields such as userId, songId, and genre, along with enumerations for interactionType and subscriptionType. We load CSV files containing the song personality dataset and user ID information into Pandas DataFrames.

To generate records, we employ two functions: "generate_user_data" and "generate_multiple_user_data". The former simulates user interactions with Spotify over time, mimicking real-life behavior through techniques such as setting exponential distribution rates for song plays and selecting geographic context and subscription types. The latter function manages the system-wide behavior and user interactions by defining arrival rates and session durations. Each generated record is sent to the Kafka topic, and the partition is determined based on the continent field.

Step 3. Create the Data Consumer

In this step, we set up the Kafka consumer with the group id "Python AVRO Consumer" to listen to the "SpotifyWrapped" topic. The consumer connects to the Kafka server running on localhost, with auto_offset_reset set to 'earliest' to ensure no message loss on restart. It continuously listens for messages, printing the deserialized message value upon receipt.

Step 4. Configuration for the Kafka and Spark Python Environment

For the Kafka and Spark environment, default settings are utilized. However, we modified the SparkSession parameter to set "check correctness" to false to address errors related to global watermarking in stateful operators. While this setting temporarily resolves the issue, in real-world scenarios, we aim to rectify errors without disabling this parameter, ensuring proper watermark handling.

## Technical Overview of the 3 Analyses
Our project utilizes three distinct analytical approaches to harness stream data for Spotify’s diverse stakeholders, namely Spotify itself, its users, and artists. These analyses are structured to cater to different needs and provide actionable insights through technical methodologies tailored for specific outcomes.

For internal Spotify use, we've implemented two main analyses. The first involves using LSTM (Long Short-Term Memory) models for predictive analytics. We deploy one model to forecast weekly user engagement and another to predict daily session counts. Initially attempting to utilize Spark for this machine learning task, we transitioned to using a Pandas DataFrame when Spark proved inadequate. In constructing our models, we aggregate data over specified time windows, normalize it to enhance model training efficiency, and split it into training and test datasets. The LSTM models, designed with layers configured to capture temporal dependencies effectively, provide forecasts that inform Spotify’s resource allocation and user engagement strategies.

The second internal analysis targets the identification of anomalous user behaviors, such as potential fraud or unusually high activity among free-tier users. By tracking session data and user interactions over time, we can pinpoint outliers and direct these findings to an Azure queue for further examination, potentially flagging fraudulent activities or areas for marketing focus.

For Spotify users, reminiscent of the personalized Spotify Wrapped experience, our analysis delves into music consumption patterns across continents and individual user behaviors. We analyze streaming data to identify popular songs, artists, and genres by continent, creating dynamic in-memory tables that update with new stream data. Additionally, we explore individual listening preferences, setting up streaming queries that reflect each user’s favorite artists, songs, and genres, thereby enhancing user engagement through tailored content.

Lastly, for Spotify artists, our approach bifurcates into real-time analytics and strategic dashboarding. Initially, we utilize Spark to perform real-time analysis of streaming data to ascertain the most played songs for artists like "The Beatles" and geographical listening patterns for artists like "Coldplay." This analysis helps artists understand their popularity and reach. Subsequently, we channel this data into an Azure event hub, integrating it with PowerBI to furnish a dashboard that artists can access to monitor their performance metrics. Although currently all artists can view each other's data, future enhancements will restrict data access to relevant stakeholders only, ensuring privacy and personalized insights.

Through these methods, we aim to empower Spotify and its stakeholders with deep, actionable insights derived from streaming data, utilizing advanced analytics and real-time data processing to drive strategic decisions and enhance user engagement.
