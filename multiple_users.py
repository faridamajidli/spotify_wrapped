def generate_multiple_user_data(start_day, end_day, personality_datasets):
    # Define the lambda for the exponential distribution for user arrivals (rate = 1/5 minutes)
    lam_arrival =  1/5 # 5 every minutes
    current_time = start_day
    all_user_records = []
    lam_service_duration= 20 #1 every 20 minutes
    user_personalities = {}

    while current_time < end_day:
        # Generate inter-arrival time for users
        inter_arrival_time_user = np.random.exponential(scale=lam_arrival)
        user_start_time = current_time + datetime.timedelta(minutes=inter_arrival_time_user)
        current_time= user_start_time

        # Check if the user_start_time is within the simulation period
        if user_start_time >= end_day:
            break

        # Simulate each user's session length, e.g., between 30 and 120 minutes
        session_length = datetime.timedelta(minutes=np.random.exponential(scale=lam_service_duration)) #1 every 20 minutes
        user_end_time = user_start_time + session_length

        # Ensure the session does not exceed the end of the simulation period
        if user_end_time > end_day:
            user_end_time = end_day

        # Generate a random user_id
        user_id = str(uuid.uuid4())

        # Generate user data for this user
        user_data, identifiers = generate_user_data(user_id, user_start_time, user_end_time, personality_datasets)
        all_user_records.extend(user_data)
        user_personalities[user_id] = identifiers

        # Update the current time to the end of the last user's session

    return all_user_records, user_personalities

start_day = datetime.datetime.now()
end_day = start_day + datetime.timedelta(hours=1)  # Simulate for two hour
all_data, user_personalities = generate_multiple_user_data(start_day, end_day, personality_datasets)

for record in all_data:
    print(record)

for user_id, personalities in user_personalities.items():
    print(f"User {user_id} selected datasets: {personalities}")
