def generate_user_data(userid, start_time, end_time, personality_datasets):
    fake = Faker()
    # Define the lambda for the exponential distribution (rate = 2 minutes) "the song is approximately one every two minutes"
    lam = 2
    current_time = start_time
    records = []
    location=fake.country()
    selected_datasets = {}
    selected_identifiers = []
    personality_key = ''

    # Select datasets and their identifiers
    for personality, datasets in personality_datasets.items():
        selected = random.choice(datasets)
        identifier, dataset = selected
        selected_datasets[personality] = dataset
        selected_identifiers.append(identifier)
        personality_key += identifier

    # Determine the listening personality
    listening_personality = listening_personalities.get(personality_key)

    # Combine the selected datasets
    combined_dataset = pd.concat([df for df in selected_datasets.values()])
    combined_dataset.iloc[:, [0, 2, 5, 6, 7]] = combined_dataset.iloc[:, [0, 2, 5, 6, 7]].replace({',': ''}, regex=True).astype(int)
    combined_dataset.iloc[:, [1, 3, 4]] = combined_dataset.iloc[:, [1, 3, 4]].astype(str)

    random_number = random.randint(0, combined_dataset.shape[0] - 1)

    # Generate the entry record
    entry_record = {
        "songPlays": [
            {
                "songId": combined_dataset.iloc[random_number, 0],
                "songName": combined_dataset.iloc[random_number, 1],
                "originalDuration": combined_dataset.iloc[random_number, 6],  # in seconds
                "releaseDate": combined_dataset.iloc[random_number, 5],
                "popularity": combined_dataset.iloc[random_number, 7],
                "artist": combined_dataset.iloc[random_number, 3],
                "artistID": combined_dataset.iloc[random_number, 2],
            }
        ],
        "userInteractions": [
            {
                "userId": userid,
                "interactionTimestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "location": location,
                "interactionType": "play",
                "listeningPersonality": listening_personality,
            }
        ]
    }
    records.append(entry_record)

    # Generate interaction records
    while current_time < end_time:
        # Generate inter-arrival time
        inter_arrival_time = np.random.exponential(scale=lam)
        current_time += datetime.timedelta(minutes=inter_arrival_time)
        random_number = random.randint(0, combined_dataset.shape[0] - 1)

        if current_time >= end_time:
            break

        interaction_record = {
        "songPlays": [
            {
                "songId": combined_dataset.iloc[random_number, 0],
                "songName": combined_dataset.iloc[random_number, 1],
                "originalDuration": combined_dataset.iloc[random_number, 6],  # in seconds
                "releaseDate": combined_dataset.iloc[random_number, 5],
                "popularity": combined_dataset.iloc[random_number, 7],
                "artist": combined_dataset.iloc[random_number, 3],
                "artistID": combined_dataset.iloc[random_number, 2],
            }
        ],
        "userInteractions": [
            {
                "userId": userid,
                "interactionTimestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "location": location,
                "interactionType": np.random.choice(["play", "skip", "like", "add_to_playlist", "end_song"]),
                "listeningPersonality": listening_personality,
            }
        ]
    }
        records.append(interaction_record)
    random_number = random.randint(0, combined_dataset.shape[0] - 1)
    exit_record = {
        "songPlays": [
            {
                "songId": combined_dataset.iloc[random_number, 0],
                "songName": combined_dataset.iloc[random_number, 1],
                "originalDuration": combined_dataset.iloc[random_number, 6],  # in seconds
                "releaseDate": combined_dataset.iloc[random_number, 5],
                "popularity": combined_dataset.iloc[random_number, 7],
                "artist": combined_dataset.iloc[random_number, 3],
                "artistID": combined_dataset.iloc[random_number, 2],
            }
        ],
        "userInteractions": [
            {
                "userId": userid,
                "interactionTimestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "location": location,
                "interactionType": "leave_app",
                "listeningPersonality": listening_personality,
            }
        ]
    }
    records.append(exit_record)
    return records, selected_identifiers
