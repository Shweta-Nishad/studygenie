import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "Machine learning is hard",
    "Python programming basics",
    "Neural networks and deep learning",
    "Web development using Flask"
]

labels = ["ML", "Programming", "ML", "Web"]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

with open("backend/model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Model saved successfully")
