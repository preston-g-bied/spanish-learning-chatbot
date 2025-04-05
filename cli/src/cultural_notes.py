"""
Spanish Learning Chatbot - Cultural Notes
This module provides cultural context and information about Spanish-speaking countries
"""

import json
import os
import random
from src.utils import load_json_data, save_json_data, clear_screen, create_directory_if_not_exists

class CulturalNotesManager:
    """Manages cultural notes and grammar explanations"""
    
    def __init__(self, notes_file='data/cultural_notes.json', grammar_file='data/grammar_notes.json'):
        """
        Initialize with notes file paths
        
        Args:
            notes_file (str): Path to cultural notes JSON file
            grammar_file (str): Path to grammar notes JSON file
        """
        # Create the data directory if it doesn't exist
        create_directory_if_not_exists('data')
        
        # Default cultural notes data
        self.default_cultural_notes = {
            "countries": [
                {
                    "name": "Spain",
                    "capital": "Madrid",
                    "language": "Spanish (Castilian)",
                    "dialects": ["Castilian", "Andalusian", "Canarian"],
                    "population": "47 million",
                    "notes": [
                        {
                            "title": "Siesta Tradition",
                            "content": "The siesta is a short nap taken in the early afternoon, usually after lunch. Traditionally, this break allowed workers to rest during the hottest part of the day. While less common in big cities today, some businesses in smaller towns still close for a few hours in the afternoon."
                        },
                        {
                            "title": "Regional Languages",
                            "content": "Besides Castilian Spanish, Spain has several co-official regional languages: Catalan, Basque (Euskara), Galician, and Valencian. Each has its own unique history and cultural significance."
                        },
                        {
                            "title": "Tapas Culture",
                            "content": "Tapas are small portions of food often served with drinks. This dining style encourages socializing and trying many different dishes. The word 'tapa' means 'cover' or 'lid' - one theory suggests they originated as small plates of food used to cover drinks to keep flies away."
                        }
                    ],
                    "pronunciation_differences": "Castilian Spanish is known for its distinctive 'th' sound (the 'z' and soft 'c' are pronounced like the 'th' in 'think')."
                },
                {
                    "name": "Mexico",
                    "capital": "Mexico City",
                    "language": "Spanish",
                    "dialects": ["Mexican Spanish"],
                    "population": "126 million",
                    "notes": [
                        {
                            "title": "Día de los Muertos",
                            "content": "The Day of the Dead is a celebration held on November 1-2 where families welcome back the souls of deceased relatives. It includes creating colorful altars (ofrendas) with photos, food, and marigold flowers to guide spirits home."
                        },
                        {
                            "title": "Indigenous Influence",
                            "content": "Mexican Spanish includes many words from indigenous languages, especially Nahuatl. Words like chocolate, tomate, and aguacate (avocado) originated from native languages and were later adopted into global Spanish and English."
                        },
                        {
                            "title": "Regional Cuisine",
                            "content": "Mexican cuisine varies greatly by region and has been recognized by UNESCO as an Intangible Cultural Heritage of Humanity. From Oaxacan mole to Yucatecan cochinita pibil, each area has distinctive dishes and techniques."
                        }
                    ],
                    "pronunciation_differences": "Mexican Spanish tends to be clear and evenly paced, without the 'th' sound used in Spain. The letter 's' is always pronounced as 's' rather than dropped."
                },
                {
                    "name": "Colombia",
                    "capital": "Bogotá",
                    "language": "Spanish",
                    "dialects": ["Colombian Andean", "Coastal/Caribbean", "Paisa"],
                    "population": "50 million",
                    "notes": [
                        {
                            "title": "Coffee Culture",
                            "content": "Colombia is world-famous for its coffee production. The Coffee Growing Axis (Eje Cafetero) is a UNESCO World Heritage site where much of the country's coffee is grown in ideal mountainous conditions."
                        },
                        {
                            "title": "Language Pride",
                            "content": "Colombian Spanish, particularly from Bogotá, is often considered one of the clearest and most 'neutral' forms of Spanish. Many call centers and Spanish dubbing studios employ Colombian speakers for their clarity and pronunciation."
                        },
                        {
                            "title": "Literary Heritage",
                            "content": "Colombia has a rich literary tradition, most famously represented by Gabriel García Márquez, who won the Nobel Prize for Literature in 1982. His novel 'One Hundred Years of Solitude' is considered a masterpiece of magical realism."
                        }
                    ],
                    "pronunciation_differences": "Colombian Spanish is known for its clear pronunciation and melodic intonation. The letter 's' is clearly pronounced rather than aspirated."
                }
            ]
        }
        
        # Default grammar notes data
        self.default_grammar_notes = {
            "topics": [
                {
                    "name": "Gender and Articles",
                    "difficulty": "beginner",
                    "explanation": "In Spanish, all nouns have a gender (masculine or feminine). The definite articles are 'el' (masculine singular), 'la' (feminine singular), 'los' (masculine plural), and 'las' (feminine plural).",
                    "examples": [
                        {"spanish": "el libro", "english": "the book (masculine)"},
                        {"spanish": "la mesa", "english": "the table (feminine)"},
                        {"spanish": "los libros", "english": "the books (masculine plural)"},
                        {"spanish": "las mesas", "english": "the tables (feminine plural)"}
                    ],
                    "tips": [
                        "Most nouns ending in -o are masculine (el libro, el plato).",
                        "Most nouns ending in -a are feminine (la casa, la silla).",
                        "There are exceptions! For example: 'el día' (day) is masculine despite ending in -a.",
                        "Some words use 'el' even when feminine if they start with a stressed 'a' sound: 'el agua' (water) is feminine."
                    ]
                },
                {
                    "name": "Present Tense Conjugation",
                    "difficulty": "beginner",
                    "explanation": "Spanish verbs change their endings depending on who is performing the action. This is called conjugation. In the present tense, regular verbs follow predictable patterns based on whether they end in -ar, -er, or -ir.",
                    "examples": [
                        {"spanish": "Yo hablo español", "english": "I speak Spanish"},
                        {"spanish": "Tú hablas español", "english": "You speak Spanish"},
                        {"spanish": "Él/Ella habla español", "english": "He/She speaks Spanish"},
                        {"spanish": "Nosotros hablamos español", "english": "We speak Spanish"},
                        {"spanish": "Vosotros habláis español", "english": "You all speak Spanish (Spain)"},
                        {"spanish": "Ellos/Ellas hablan español", "english": "They speak Spanish"}
                    ],
                    "tips": [
                        "-AR verbs end with: -o, -as, -a, -amos, -áis, -an",
                        "-ER verbs end with: -o, -es, -e, -emos, -éis, -en",
                        "-IR verbs end with: -o, -es, -e, -imos, -ís, -en",
                        "Many common verbs are irregular and don't follow these patterns (ser, estar, ir, tener)."
                    ]
                },
                {
                    "name": "Ser vs. Estar",
                    "difficulty": "intermediate",
                    "explanation": "Spanish has two verbs for 'to be': ser and estar. Ser is used for permanent characteristics, identity, origin, and time. Estar is used for temporary conditions, locations, and certain feelings or states.",
                    "examples": [
                        {"spanish": "Yo soy estudiante", "english": "I am a student (permanent identity - ser)"},
                        {"spanish": "Yo estoy cansado", "english": "I am tired (temporary condition - estar)"},
                        {"spanish": "La casa es grande", "english": "The house is big (permanent characteristic - ser)"},
                        {"spanish": "La casa está limpia", "english": "The house is clean (state/condition - estar)"}
                    ],
                    "tips": [
                        "Use SER for: Identity, Characteristics, Origin, Time, Relationships, Possession",
                        "Use ESTAR for: Location, Temporary Conditions, Ongoing Actions (with present participle)",
                        "Some adjectives change meaning depending on whether they're used with ser or estar!",
                        "Example: 'Ser aburrido' = to be boring (personality), 'Estar aburrido' = to be bored (feeling)"
                    ]
                }
            ]
        }
        
        # Load cultural notes
        if os.path.exists(notes_file):
            self.cultural_notes = load_json_data(notes_file)
        else:
            self.cultural_notes = self.default_cultural_notes
            save_json_data(self.cultural_notes, notes_file)
        
        # Load grammar notes
        if os.path.exists(grammar_file):
            self.grammar_notes = load_json_data(grammar_file)
        else:
            self.grammar_notes = self.default_grammar_notes
            save_json_data(self.grammar_notes, grammar_file)
        
        self.notes_file = notes_file
        self.grammar_file = grammar_file
    
    def get_countries(self):
        """Get list of all countries"""
        return self.cultural_notes['countries']
    
    def get_grammar_topics(self):
        """Get list of all grammar topics"""
        return self.grammar_notes['topics']
    
    def get_country_by_name(self, name):
        """Get a country by name"""
        for country in self.cultural_notes['countries']:
            if country['name'].lower() == name.lower():
                return country
        return None
    
    def get_grammar_by_name(self, name):
        """Get a grammar topic by name"""
        for topic in self.grammar_notes['topics']:
            if topic['name'].lower() == name.lower():
                return topic
        return None
    
    def get_random_cultural_note(self):
        """Get a random cultural note"""
        if not self.cultural_notes['countries']:
            return None
        
        country = random.choice(self.cultural_notes['countries'])
        if not country['notes']:
            return None
        
        note = random.choice(country['notes'])
        return {
            'country': country['name'],
            'title': note['title'],
            'content': note['content']
        }
    
    def get_random_grammar_tip(self):
        """Get a random grammar tip"""
        if not self.grammar_notes['topics']:
            return None
        
        topic = random.choice(self.grammar_notes['topics'])
        if not topic['tips']:
            return None
        
        tip = random.choice(topic['tips'])
        return {
            'topic': topic['name'],
            'difficulty': topic['difficulty'],
            'tip': tip
        }
    
    def display_country_notes(self, country_name):
        """Display all notes for a specific country"""
        country = self.get_country_by_name(country_name)
        if not country:
            print(f"Country '{country_name}' not found.")
            return
        
        clear_screen()
        print(f"\n🇪🇸  CULTURAL NOTES: {country['name'].upper()}  🇪🇸\n")
        print(f"Capital: {country['capital']}")
        print(f"Official Language: {country['language']}")
        print(f"Dialects: {', '.join(country['dialects'])}")
        print(f"Population: {country['population']}")
        
        if 'pronunciation_differences' in country:
            print(f"\nPronunciation: {country['pronunciation_differences']}")
        
        print("\nCultural Notes:")
        for i, note in enumerate(country['notes'], 1):
            print(f"\n{i}. {note['title']}")
            print(f"   {note['content']}")
        
        input("\nPress Enter to return...")
    
    def display_grammar_topic(self, topic_name):
        """Display a specific grammar topic"""
        topic = self.get_grammar_by_name(topic_name)
        if not topic:
            print(f"Grammar topic '{topic_name}' not found.")
            return
        
        clear_screen()
        print(f"\n🇪🇸  GRAMMAR: {topic['name'].upper()}  🇪🇸\n")
        print(f"Difficulty: {topic['difficulty'].capitalize()}")
        print(f"\nExplanation: {topic['explanation']}")
        
        print("\nExamples:")
        for example in topic['examples']:
            print(f"  • {example['spanish']} - {example['english']}")
        
        print("\nTips:")
        for i, tip in enumerate(topic['tips'], 1):
            print(f"  {i}. {tip}")
        
        input("\nPress Enter to return...")
    
    def browse_cultural_notes(self):
        """Interactive browser for cultural notes"""
        while True:
            clear_screen()
            print("\n🇪🇸  CULTURAL NOTES  🇪🇸\n")
            print("Learn about Spanish-speaking countries and cultures:\n")
            
            print("Countries:")
            for i, country in enumerate(self.cultural_notes['countries'], 1):
                print(f"{i}. {country['name']}")
            
            print(f"\n{len(self.cultural_notes['countries']) + 1}. Return to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == len(self.cultural_notes['countries']) + 1:
                    return
                
                if 1 <= choice <= len(self.cultural_notes['countries']):
                    self.display_country_notes(self.cultural_notes['countries'][choice - 1]['name'])
                else:
                    print("\nInvalid choice. Please try again.")
                    input("\nPress Enter to continue...")
            
            except ValueError:
                print("\nPlease enter a number.")
                input("\nPress Enter to continue...")
    
    def browse_grammar_notes(self):
        """Interactive browser for grammar notes"""
        while True:
            clear_screen()
            print("\n🇪🇸  GRAMMAR NOTES  🇪🇸\n")
            print("Learn about Spanish grammar:\n")
            
            # Group topics by difficulty
            beginner_topics = []
            intermediate_topics = []
            advanced_topics = []
            
            for topic in self.grammar_notes['topics']:
                if topic['difficulty'] == 'beginner':
                    beginner_topics.append(topic)
                elif topic['difficulty'] == 'intermediate':
                    intermediate_topics.append(topic)
                else:
                    advanced_topics.append(topic)
            
            print("Beginner Topics:")
            for i, topic in enumerate(beginner_topics, 1):
                print(f"{i}. {topic['name']}")
            
            print("\nIntermediate Topics:")
            for i, topic in enumerate(intermediate_topics, 1):
                print(f"{len(beginner_topics) + i}. {topic['name']}")
            
            print("\nAdvanced Topics:")
            for i, topic in enumerate(advanced_topics, 1):
                print(f"{len(beginner_topics) + len(intermediate_topics) + i}. {topic['name']}")
            
            total_topics = len(beginner_topics) + len(intermediate_topics) + len(advanced_topics)
            print(f"\n{total_topics + 1}. Return to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == total_topics + 1:
                    return
                
                if 1 <= choice <= total_topics:
                    # Determine which topic was selected
                    if choice <= len(beginner_topics):
                        topic = beginner_topics[choice - 1]
                    elif choice <= len(beginner_topics) + len(intermediate_topics):
                        topic = intermediate_topics[choice - len(beginner_topics) - 1]
                    else:
                        topic = advanced_topics[choice - len(beginner_topics) - len(intermediate_topics) - 1]
                    
                    self.display_grammar_topic(topic['name'])
                else:
                    print("\nInvalid choice. Please try again.")
                    input("\nPress Enter to continue...")
            
            except ValueError:
                print("\nPlease enter a number.")
                input("\nPress Enter to continue...")