original_data = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/Spotify-2000.csv")
commonality = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/commonality.csv")
exploration = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/exploration.csv")
familiarity = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/familiarity.csv")
loyalty = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/loyalty.csv")
newness = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/newness.csv")
timelessness = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/timelessness.csv")
uniqueness = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/uniqueness.csv")
variety = pd.read_csv("/content/drive/MyDrive/Stream Spotify Project/new personality datasets/variety.csv")

personality_datasets = {
    'fe': [('F', familiarity), ('E', exploration)],
    'tn': [('T', timelessness), ('N', newness)],
    'lv': [('L', loyalty), ('V', variety)],
    'cu': [('C', commonality), ('U', uniqueness)]
}

listening_personalities = {
    'ENVC': 'The Early Adopter',
    'ENLU': 'The Nomad',
    'FNVU': 'The Specialist',
    'FNLC': 'The Enthusiast',
    'FTLC': 'The Connoisseur',
    'FTVU': 'The Deep Diver',
    'FNVC': 'The Fanclubber', 
    'ETLC': 'The Top Charter',
    'FTLU': 'The Replayer',   
    'FTVC': 'The Jukeboxer', 
    'ENLC': 'The Voyager',
    'FNLU': 'The Devotee',
    'ETLU': 'The Maverick',   
    'ETVU': 'The Time Traveler',
    'ETVC': 'The Musicologist',
    'ENVU': 'The Adventurer',
}
