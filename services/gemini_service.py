# services/gemini_service.py

import google.generativeai as genai
from typing import Optional


class GeminiService:
    """Service class for interacting with Google's Gemini AI model."""

    def __init__(self, api_key: str):
        """Initialize the Gemini service with API key.

        Args:
            api_key (str): The API key for Gemini authentication
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

        # Define the prompt as a class constant
        self.AFFIRMATION_PROMPT = """
        Please provide a single, powerful positive affirmation quote that can inspire 
        and motivate someone. Make it brief, meaningful, and uplifting. 
        Respond with just the affirmation text.
        """.strip()

    def get_affirmation_text(self) -> Optional[str]:
        """Generate a positive affirmation quote using Gemini.

        Returns:
            Optional[str]: The generated affirmation text, or None if an error occurs
        """
        try:
            response = self.model.generate_content(self.AFFIRMATION_PROMPT)
            return response.text.strip()

        except Exception as e:
            print(f"Error generating affirmation: {str(e)}")
            return None

    def __repr__(self) -> str:
        """Return a string representation of the GeminiService."""
        return f"GeminiService(api_key='{self.api_key[:5]}...')"