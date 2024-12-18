from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


class SentimentModule:
    """
    A service class responsible for analyzing sentiment in text using NLTK's VADER sentiment analyzer.
    """

    def __init__(self, positive_threshold=0.05):
        """
        Initialize the SentimentService.

        Args:
            positive_threshold (float): The compound score threshold above which a sentence
                                      is considered positive. Defaults to 0.05.
        """
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')

        self.sia = SentimentIntensityAnalyzer()
        self.positive_threshold = positive_threshold

    def is_positive(self, text: str) -> bool:
        """
        Determines if the given text has a positive sentiment.

        Args:
            text (str): The text to analyze.

        Returns:
            bool: True if the text has positive sentiment, False otherwise.

        Raises:
            ValueError: If the input text is empty or None.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or None")

        scores = self.sia.polarity_scores(text)
        return scores['compound'] > self.positive_threshold

    def get_sentiment_score(self, text: str) -> float:
        """
        Returns the compound sentiment score for the given text.

        Args:
            text (str): The text to analyze.

        Returns:
            float: The compound sentiment score between -1 (very negative) 
                  and 1 (very positive).

        Raises:
            ValueError: If the input text is empty or None.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or None")

        scores = self.sia.polarity_scores(text)
        return scores['compound']

    def analyze_sentiment(self, text: str) -> dict:
        """
        Provides a detailed sentiment analysis of the given text.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: A dictionary containing sentiment analysis results including:
                - is_positive: boolean indicating if sentiment is positive
                - compound: the compound score (-1 to 1)
                - pos: the positive score (0 to 1)
                - neu: the neutral score (0 to 1)
                - neg: the negative score (0 to 1)

        Raises:
            ValueError: If the input text is empty or None.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or None")

        scores = self.sia.polarity_scores(text)
        return {
            "is_positive": scores['compound'] > self.positive_threshold,
            "compound": scores['compound'],
            "pos": scores['pos'],
            "neu": scores['neu'],
            "neg": scores['neg']
        }

