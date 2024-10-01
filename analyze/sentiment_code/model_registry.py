import os 
import joblib
import logging
from .BasicAnalyzerMaker import BasicAnalyzerMaker
from .AdvancedAnalyzerMaker import AdvancedAnalyzerMaker
from .LogisticRegressionAnalyzerMaker import LogisticRegressionAnalyzerMaker
from .RandomForestAnalyzerMaker import RandomForestAnalyzerMaker
from .BERTAnalyzerMaker import BERTAnalyzerMaker
from sentiment_analysis.utils import download_file_from_s3

logger = logging.getLogger(__name__)

class ModelRegistry:
    _models = {}

    @classmethod
    def get_model(cls, analyzer_type):
        if analyzer_type in cls._models:
            return cls._models[analyzer_type]

        maker = cls._get_maker(analyzer_type)
        if not maker:
            logger.error(f"Invalid analyzer type: {analyzer_type}")
            return None

        analyzer = maker.make_analyzer()
        cls._models[analyzer_type] = analyzer
        logger.info(f"Loaded and cached model for analyzer type: {analyzer_type}")
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
