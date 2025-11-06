"""Configuration file for Wizard Search."""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'files')
STOPWORDS_FILE = os.path.join(FILES_DIR, 'qualityFiles', 'stopWords.txt')

# Search Engine Settings
DEFAULT_EMBEDDING_METHOD = 'tfidf'  # Options: 'tfidf', 'bert'
TOP_K_RESULTS = 10

# Wikipedia Settings
DEFAULT_WIKIPEDIA_PAGES = [
    # Science & Technology
    'Artificial_intelligence', 'Computer_science', 'Mathematics', 'Physics',
    'Chemistry', 'Biology', 'Astronomy', 'Quantum_mechanics', 'Genetics',
    'Evolution', 'Climate_change', 'Renewable_energy', 'Internet', 'Blockchain',
    'Machine_learning', 'Robotics', 'Nanotechnology', 'Biotechnology',

    # History & Culture
    'World_War_II', 'Ancient_Egypt', 'Roman_Empire', 'Renaissance',
    'Industrial_Revolution', 'Cold_War', 'Ancient_Greece', 'Middle_Ages',
    'French_Revolution', 'American_Revolution', 'Mesopotamia', 'Maya_civilization',

    # Geography
    'Earth', 'United_States', 'China', 'India', 'Europe', 'Africa',
    'Asia', 'South_America', 'Australia', 'Antarctica', 'Pacific_Ocean',
    'Amazon_rainforest', 'Sahara', 'Himalayas', 'Great_Barrier_Reef',

    # Philosophy & Religion
    'Philosophy', 'Religion', 'Christianity', 'Islam', 'Buddhism',
    'Hinduism', 'Judaism', 'Ethics', 'Logic', 'Metaphysics', 'Epistemology',

    # Arts & Literature
    'Art', 'Music', 'Literature', 'Painting', 'Sculpture', 'Architecture',
    'Poetry', 'Novel', 'Drama', 'Film', 'Photography', 'Dance', 'Opera',
    'William_Shakespeare', 'Leonardo_da_Vinci', 'Ludwig_van_Beethoven',

    # Sports & Entertainment
    'Association_football', 'Basketball', 'Cricket', 'Tennis', 'Olympics',
    'Chess', 'Video_game', 'Cinema', 'Television', 'Theatre',

    # Nature & Animals
    'Animal', 'Plant', 'Mammal', 'Bird', 'Fish', 'Insect', 'Reptile',
    'Dinosaur', 'Ocean', 'Forest', 'Desert', 'Mountain', 'River', 'Lake',
    'Ecosystem', 'Biodiversity', 'Ecology', 'Conservation_biology',

    # Human Body & Health
    'Human_body', 'Brain', 'Heart', 'Medicine', 'Disease', 'Virus',
    'Bacteria', 'Immune_system', 'Nutrition', 'Exercise', 'Mental_health',
    'Cancer', 'DNA', 'Cell_(biology)', 'Protein',

    # Social Sciences
    'Economics', 'Psychology', 'Sociology', 'Anthropology', 'Political_science',
    'Law', 'Education', 'Linguistics', 'Democracy', 'Capitalism', 'Socialism',

    # Language & Communication
    'Language', 'English_language', 'Spanish_language', 'Chinese_language',
    'Arabic', 'French_language', 'German_language', 'Japanese_language',
    'Writing_system', 'Alphabet', 'Grammar',

    # Food & Cuisine
    'Food', 'Cooking', 'Italian_cuisine', 'Chinese_cuisine', 'French_cuisine',
    'Mexican_cuisine', 'Indian_cuisine', 'Japanese_cuisine', 'Bread',
    'Pizza', 'Chocolate', 'Coffee', 'Tea', 'Wine', 'Beer',

    # Everyday Topics
    'Sun', 'Moon', 'Star', 'Planet', 'Water', 'Fire', 'Weather', 'Cloud',
    'Rain', 'Snow', 'Wind', 'Rainbow', 'Thunder', 'Lightning',
    'Hot_dog', 'Television', 'Norway', 'Love', 'Friendship', 'Family',
    'Time', 'Space', 'Energy', 'Matter', 'Light', 'Color', 'Sound'
]

# Flask Settings
DEBUG = True
SECRET_KEY = 'dev-secret-key-change-in-production'
