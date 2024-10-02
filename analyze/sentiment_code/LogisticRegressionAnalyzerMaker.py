from .LogisticRegressionAnalyzer import LogisticRegressionAnalyzer
from sklearn.externals import joblib
import os 

class LogisticRegressionAnalyzerMaker:
    def make_analyzer(self):
        model_dir = "/tmp/models"  # Local directory where models are stored
        vectorizer_path = os.path.join(model_dir, "log_reg_tfidf_vectorizer.pkl")
        model_path = os.path.join(model_dir, "log_reg_model.pkl")
        
        # Load vectorizer and model from disk
        vectorizer = joblib.load(vectorizer_path)
        model = joblib.load(model_path)
        
        return LogisticRegressionAnalyzer(vectorizer, model)
