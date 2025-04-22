import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

class MedicalChatbot:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

        # Combine all symptom columns into one column
        symptom_cols = [col for col in self.data.columns if col.startswith("Symptom")]
        self.data["symptoms"] = self.data[symptom_cols].astype(str).apply(
            lambda row: ", ".join([s for s in row if s.lower() != "nan"]), axis=1
        )

        # Normalize symptoms
        self.data["symptoms"] = self.data["symptoms"].apply(self.normalize)

        # Store all unique symptoms for fuzzy matching
        self.all_symptoms = sorted(set(
            sym.strip() for row in self.data["symptoms"] for sym in row.split(",")
        ))

        # Vectorize
        self.vectorizer = TfidfVectorizer()
        self.symptom_vectors = self.vectorizer.fit_transform(self.data["symptoms"])

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

    def normalize(self, text):
        text = text.lower()
        text = text.replace("_", " ")  # Convert snake_case to space-separated
        text = re.sub(r"[^\w\s,]", "", text)  # Remove punctuation
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace
        return text.strip()

    def correct_symptoms(self, extracted_list):
        corrected = []
        for sym in extracted_list:
            best_match, score = process.extractOne(sym, self.all_symptoms)
            if score > 80:
                corrected.append(best_match)
        return ", ".join(corrected)

    def extract_symptoms(self, message):
        doc = self.nlp(message.lower())
        chunks = [chunk.text for chunk in doc.noun_chunks]
        ents = [ent.text for ent in doc.ents]
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
        combined = set(chunks + ents + keywords)
        normalized = [self.normalize(sym) for sym in combined]
        return self.correct_symptoms(normalized)

    def get_response(self, user_input):
        extracted = self.extract_symptoms(user_input)
        if not extracted:
            return {
                "matched_symptom": None,
                "disease": "Could not understand your symptoms",
                "treatment": "Please consult a doctor."
            }

        user_vec = self.vectorizer.transform([self.normalize(extracted)])
        similarity = cosine_similarity(user_vec, self.symptom_vectors)
        idx = similarity.argmax()
        score = similarity[0][idx]

        if score < 0.1:
            return {
                "matched_symptom": None,
                "disease": "No match found",
                "treatment": "Please consult a doctor."
            }

        match = self.data.iloc[idx]
        return {
            "matched_symptom": match["symptoms"],
            "disease": match["Disease"],
            "treatment": match["Treatment"]
        }
