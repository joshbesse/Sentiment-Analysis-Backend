import logging
import os
from .BasicAnalyzerMaker import BasicAnalyzerMaker
from .AdvancedAnalyzerMaker import AdvancedAnalyzerMaker
from .LogisticRegressionAnalyzerMaker import LogisticRegressionAnalyzerMaker
from .RandomForestAnalyzerMaker import RandomForestAnalyzerMaker
from .BERTAnalyzerMaker import BERTAnalyzerMaker
from sentiment_analysis.utils import download_file_from_s3

logger = logging.getLogger(__name__)

class ModelRegistry:
    _models = {}
    LOCAL_MODEL_DIR = "/tmp/models"

    @classmethod
    def get_model(cls, analyzer_type):
        if analyzer_type in cls._models:
            logger.info(f"Using cached model for analyzer type: {analyzer_type}")
            return cls._models[analyzer_type]

        maker = cls._get_maker(analyzer_type)
        if not maker:
            logger.error(f"Invalid analyzer type: {analyzer_type}")
            return None

        # Download models from S3 to disk if necessary
        cls._download_models_if_needed(analyzer_type)

        # Create the analyzer instance (which loads model files from disk)
        analyzer = maker.make_analyzer()
        if analyzer:
            cls._models[analyzer_type] = analyzer
            logger.info(f"Loaded and cached model for analyzer type: {analyzer_type}")
        else:
            logger.error(f"Failed to create analyzer for type: {analyzer_type}")
            
        return analyzer

    @staticmethod
    def _get_maker(analyzer_type):
        if analyzer_type == "basic":
            return BasicAnalyzerMaker()
        elif analyzer_type == "advanced":
            return AdvancedAnalyzerMaker()
        elif analyzer_type == "logistic_regression":
            return LogisticRegressionAnalyzerMaker()
        elif analyzer_type == "random_forest":
            return RandomForestAnalyzerMaker()
        elif analyzer_type == "BERT":
            return BERTAnalyzerMaker()
        else:
            return None

    @classmethod
    def _download_models_if_needed(cls, analyzer_type):
        # Determine S3 keys and local paths based on analyzer type
        if analyzer_type == "logistic_regression":
            vectorizer_s3_key = "log_reg_tfidf_vectorizer.pkl"
            model_s3_key = "log_reg_model.pkl"
            vectorizer_local_path = os.path.join(cls.LOCAL_MODEL_DIR, "log_reg_tfidf_vectorizer.pkl")
            model_local_path = os.path.join(cls.LOCAL_MODEL_DIR, "log_reg_model.pkl")

            # Download vectorizer if not present on disk
            if not os.path.exists(vectorizer_local_path):
                download_file_from_s3(vectorizer_s3_key, vectorizer_local_path)
            
            # Download model if not present on disk
            if not os.path.exists(model_local_path):
                download_file_from_s3(model_s3_key, model_local_path)
