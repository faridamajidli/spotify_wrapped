# Spotify Wrapped: Milestone 2
## Overview of Milestone 1
Leveraging the Spotify dataset from Kaggle, we generated eight distinct datasets aligned with the 16 listening personalities published on Spotify website. These personalities derive from four dualistic traits:

1. Familiarity (F) vs. Exploration (E): Do listeners prefer repeated tracks from favorite artists, or explore new ones?
2. Loyalty (L) vs. Variety (V): Is there a tendency to replay the same tracks, or a preference for a diverse listening experience?
3. Timelessness (T) vs. Newness (N): Do users focus on the latest tracks, or enjoy a broader historical range?
4. Commonality (C) vs. Uniqueness (U): Do listeners choose popular tracks shared by millions, or seek out lesser-known artists?

Based on these characteristics, we segmented our dataset into eight subsets, each corresponding to one trait (F, E, L, V, T, N, C, U). For instance, the 'F' dataset primarily includes tracks from a single artist, whereas the 'E' dataset features a variety of artists. This segmentation is crucial for analyzing the simulated listening preferences of our users.

Each user was randomly assigned one of the 16 personalities for the simulation. In the first milestone, our AVRO schema featured two array fields for user interactions and song plays. For the second milestone, we streamlined the data structure by eliminating these array fields.

The user data simulation comprised two phases: extracting song-related data from the Spotify dataset and generating synthetic user data using the Faker library. To ensure continuity, we pre-ran the simulation to establish a fixed set of user IDs. We set the simulation period to 48 hours, during which we generated approximately 7000 unique users. This dataset was then processed and ingested by Kafka using pre-defined unique user IDs. The updated code for Milestone 1 is available on this repository.

## Installation
To run the scripts, you need to install several Python libraries. You can install them using pip:

```bash
!pip install fastavro kafka-python
!pip install fastavro
!pip install arrow
!pip install faker
!pip install pycountry-convert
!pip install azure.storage.queue
!pip install pyspark
!pip install azure.eventhub
!pip install findspark
```
## Usage

1. Mount Google Drive to access the datasets:

```bash
from google.colab import drive
drive.mount('/content/drive')
```
In total, there are 9 .csv files that need to be imported to correctly run the code. 8 of these datasets are related to the 16 listening personalities of the users. The remaining 1 file consists around 7,000 unique user IDs. All of the files are included in the "data" folder in this repository branch. 

2. Load the Datasets from your Google Drive following the directory structure provided in the code.
The lines in the .ipynb file that need to be changed accordingly are:
```bash
commonality = pd.read_csv("/content/drive/MyDrive/data/commonality.csv")
exploration = pd.read_csv("/content/drive/MyDrive/data/exploration.csv")
familiarity = pd.read_csv("/content/drive/MyDrive/data/familiarity.csv")
loyalty = pd.read_csv("/content/drive/MyDrive/data/loyalty.csv")
newness = pd.read_csv("/content/drive/MyDrive/data/newness.csv")
timelessness = pd.read_csv("/content/drive/MyDrive/data/timelessness.csv")
uniqueness = pd.read_csv("/content/drive/MyDrive/data/uniqueness.csv")
variety = pd.read_csv("/content/drive/MyDrive/data/variety.csv")
```

```bash
user_personality_df = pd.read_csv("/content/drive/data/user_personality_df.csv")
```

4. Run the notebook to obtain the analyses described in the following sections.

## Configuration

The setup for Milestone 2 involves four key steps: creating the Kafka environment, setting up the data producer, configuring the data consumer, and configuring the Kafka and Spark Python environment.

Step 1. Create the Kafka Environment

First, we establish a Kafka environment, comprising a Kafka broker and the topic "SpotifyWrapped". We configure the topic with six partitions to align with the seven continents, merging Oceania and Antarctica due to lower population density. This partitioning strategy ensures data distribution uniformity, enhancing scalability. Given our single broker setup, we limited the number of partitions.

Step 2. Create the Data Producer

Here, we define an Avro schema for the Spotify Wrapped data, encompassing fields such as userId, songId, and genre, along with enumerations for interactionType and subscriptionType. We load CSV files containing the song personality dataset and user ID information into Pandas DataFrames.

To generate records, we employ two functions: "generate_user_data" and "generate_multiple_user_data". The former simulates user interactions with Spotify over time, mimicking real-life behavior through techniques such as setting exponential distribution rates for song plays and selecting geographic context and subscription types. The latter function manages the system-wide behavior and user interactions by defining arrival rates and session durations. Each generated record is sent to the Kafka topic, and the partition is determined based on the continent field.

Step 3. Create the Data Consumer

In this step, we set up the Kafka consumer with the group id "Python AVRO Consumer" to listen to the "SpotifyWrapped" topic. The consumer connects to the Kafka server running on localhost, with auto_offset_reset set to 'earliest' to ensure no message loss on restart. It continuously listens for messages, printing the deserialized message value upon receipt.

Step 4. Configuration for the Kafka and Spark Python Environment

For the Kafka and Spark environment, default settings are utilized. However, we modified the SparkSession parameter to set "check correctness" to false to address errors related to global watermarking in stateful operators. While this setting temporarily resolves the issue, in real-world scenarios, we aim to rectify errors without disabling this parameter, ensuring proper watermark handling.

## Technical Overview of the 3 Analyses
Our project utilizes three distinct analytical approaches to harness stream data for Spotify’s diverse stakeholders, namely Spotify itself, its users, and artists. These analyses are structured to cater to different needs and provide actionable insights through technical methodologies tailored for specific outcomes.

For internal Spotify use, we have implemented two main analyses. The first involves using LSTM (Long Short-Term Memory) models for predictive analytics. We deploy one model to forecast weekly user engagement and another to predict daily session counts. Initially attempting to utilize Spark for this machine learning task, we transitioned to using a Pandas DataFrame when Spark proved inadequate. In constructing our models, we aggregate data over specified time windows, normalize it to enhance model training efficiency, and split it into training and test datasets. The LSTM models, designed with layers configured to capture temporal dependencies effectively, provide forecasts that inform Spotify’s resource allocation and user engagement strategies.

The second internal analysis targets the identification of anomalous user behaviors, such as potential fraud or unusually high activity among free-tier users. By tracking session data and user interactions over time, we can pinpoint outliers and direct these findings to an Azure queue for further examination, potentially flagging fraudulent activities or areas for marketing focus.

For Spotify users, reminiscent of the personalized Spotify Wrapped experience, our analysis delves into music consumption patterns across continents and individual user behaviors. We analyze streaming data to identify top 3 songs, artists, genres, and users by continent, creating dynamic in-memory tables that update with new stream data. Additionally, we explore individual listening preferences, setting up streaming queries that reflect each user’s listening personality and favorite 5 artists, songs, and genres, thereby enhancing user engagement through tailored content.

Lastly, for Spotify artists, our approach bifurcates into real-time analytics and strategic dashboarding. Initially, we utilize Spark to perform real-time analysis of streaming data to ascertain the most played songs and geographical listening patterns for pre-defined artists like "The Beatles." This analysis helps artists understand their popularity and reach. Subsequently, we channel this data into an Azure event hub, integrating it with PowerBI to furnish a dashboard that artists can access to monitor their performance metrics. Although currently all artists can view each other's data, future enhancements will restrict data access to relevant stakeholders only, ensuring privacy and personalized insights. In addition, we output the complete data in Azure Blob using Azure Stream Analytics.

Through these methods, we aim to empower Spotify and its stakeholders with deep, actionable insights derived from streaming data, utilizing advanced analytics and real-time data processing to drive strategic decisions and enhance user engagement.

## Rationale Behind the Analyses and Key Insights
We have structured our analysis to enhance Spotify's internal operations and user engagement. Our two internal analyses involve predictive modeling to assist the marketing and technology departments. The first model predicts weekly user growth, aiding the marketing team in timing their campaigns to coincide with peak user activity, thus optimizing advertisement targeting and resource allocation. The second model forecasts daily session loads, allowing the technology team to anticipate and manage server stress, ensuring platform stability.

For fraud detection and marketing optimization, we employ two distinct analyses. We identify "heavy free users"—those who engage frequently but have no sobscuption - who are a targeted group for marketing premium services, potentially increasing conversion rates and revenue. Additionally, we track anomalous user behaviors indicative of potential fraud, enabling timely interventions that safeguard revenue and maintain platform integrity. Both analyses use weekly data aggregation to strike a balance between timely responsiveness and comprehensive engagement assessment.

On the consumer front, our analysis tailors Spotify's user experience by personalizing playlists and recommendations based on individual music tastes and listening habits. This personalization not only improves user satisfaction and engagement but also boosts the likelihood of free users upgrading to premium, enhancing ad targeting and ultimately, increasing ad revenue. By closely monitoring music trends and user preferences, Spotify can stay ahead of market shifts and maintain high user retention through continuously relevant content.

For artists, our approach provides real-time data on how their music performs across different regions, informing their promotional strategies and content release plans. With tools like PowerBI, artists gain access to detailed performance metrics, allowing them to make informed decisions that enhance their careers and revenue potential. In addition, we output the complete data in Azure Blob using Azure Stream Analytics to for long-term retention. 

These analytics support Spotify's broader strategy of building a robust ecosystem that benefits both users and artists, driving the company's overall growth and market dominance.

## Challenges
Throughout our project, we faced three main challenges: 
1. Simulating realistic user behavior
2. Balancing realism with performance
3. Adopting a test-and-learn approach under technical constraints

Our first challenge involved creating a realistic simulation of user behavior, which proved difficult due to the complexity of maintaining consistent user attributes like location, personality, and subscription type over time. In real-world applications, user demographics and subscription statuses often shift as the platform gains or loses popularity. Our simulation struggled to accurately model these dynamics, including setting a realistic monthly user growth rate. Additionally, our data did not include event timestamps aligned with regional time zones, a feature typical in live environments. To improve future simulations, we plan to integrate reference data from Azure Blob Storage for more dynamic user ID generation and regional time settings.

The second challenge was managing the trade-off between a realistic simulation and system performance. Running a year-long simulation required us to reduce the rate of user arrivals to manage data processing times effectively, impacting the realism of our model.

Our third major challenge was the need to adapt our development processes to the limitations of our hardware and software. Initial attempts to use joins in Spark were unsuccessful due to the absence of watermarks, which are crucial for handling late data in streaming applications. We plan to incorporate watermarks in future implementations to enhance functionality. Additionally, we initially used Azure queues to analyze continent-specific data, which was not ideal as queues are typically used for anomalies rather than regular data processing. This method also resulted in slow processing times due to the volume of streaming data. We subsequently shifted to direct queries using Spark SQL and plan to further refine our approach by utilizing Azure Event Hubs and Stream Analytics for better integration and performance. We also aim to replace our method of converting data to Pandas DataFrames with a more seamless integration of Azure Machine Learning for analytics.

Lastly, we encountered difficulties in creating a user-friendly interface for specific user and artist analytics. These challenges hindered our ability to provide a smooth data retrieval platform for both Spotify users and artists. Future versions of the project will focus on developing a more robust interface to facilitate efficient access to tailored analytics, enhancing the overall user and artist experience.

## Reflection and Discussion Summary
Throughout this project, we learned how to use streaming data as well as overcome challenges that streaming data poses. We implemented an architecture to create and process streaming data and learned about the possible analyses of the given data. We were successful in creating analyses that gave meaningful insights and would make business sense. However, we could also reflect on the resource constraints, which were time, computational resources, and the absence of real data, and find methods to overcome them.

For a real-life implementation with real data, we would add triggers and watermarks to handle late data, different customer groups for each analysis, and additional brokers to have replication for each partition and ensure data safety. The triggers will be based on the window size that we created as it would also reflect how often we need this analysis for the departments and for the users. A watermark will drop late values to ensure that values outside of the window are not included in the weekly or daily report.

## Credits
The authors of this project are:

Majidli, Farida
Troje, Delphine
Ploquin, Tomas
Pascual, Fernando
Conesa, Angel
Oliver, Paula
