"""
Synthesis Engine Module.

Manages two LLM providers with robust Try-Except chain for failover logic.
    Primary: Google Gemini (gemini-2.5-flash)
    Secondary: Groq (llama-3.3-70b-versatile)
"""

import os
import time
from typing import Optional, Dict, Any
from enum import Enum


class Provider(Enum):
    """LLM provider enumeration."""

    GOOGLE = "google"
    GROQ = "groq"


class SynthesisEngine:
    """
    Manages LLM providers with automatic failover logic.

    Implements a robust Try-Except chain that switches to the next provider
    if the current one fails due to rate limits or API errors.
    """

    def __init__(self):
        """Initialize the Synthesis Engine with API keys from environment."""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        self.providers_order = [Provider.GOOGLE, Provider.GROQ]
        self.current_provider = Provider.GOOGLE
        self.last_error = None
        self.provider_status = {
            Provider.GOOGLE: "available",
            Provider.GROQ: "available"
        }

    def generate_docstring(
        self,
        function_signature: str,
        code_context: str,
        docstring_style: str = "google"
    ) -> Dict[str, Any]:
        """
        Generate a docstring for a function using the best available provider.

        Uses failover logic to automatically switch providers on failure.

        Args:
            function_signature: The function signature.
            code_context: The function implementation code.
            docstring_style: The docstring style (google, numpy, rest).

        Returns:
            Dictionary with 'docstring', 'provider', and 'success' keys.
        """
        prompt = self._build_prompt(function_signature, code_context, docstring_style)

        for provider in self.providers_order:
            if self.provider_status[provider] == "available":
                try:
                    self.current_provider = provider
                    result = self._call_provider(provider, prompt)

                    if result:
                        return {
                            "docstring": result,
                            "provider": provider.value,
                            "success": True,
                            "error": None
                        }
                except Exception as e:
                    self.last_error = str(e)
                    self._handle_provider_failure(provider, str(e))
                    continue

        # All providers failed
        return {
            "docstring": None,
            "provider": None,
            "success": False,
            "error": f"All providers failed. Last error: {self.last_error}"
        }

    def _call_provider(self, provider: Provider, prompt: str) -> Optional[str]:
        """
        Call the specified LLM provider.

        Args:
            provider: The provider to call.
            prompt: The prompt for docstring generation.

        Returns:
            Generated docstring or None if failed.

        Raises:
            Exception: If the API call fails.
        """
        if provider == Provider.GOOGLE:
            return self._call_google(prompt)
        elif provider == Provider.GROQ:
            return self._call_groq(prompt)

    def _call_google(self, prompt: str) -> Optional[str]:
        """
        Call Google Gemini API.

        Args:
            prompt: The prompt for docstring generation.

        Returns:
            Generated docstring.

        Raises:
            Exception: If the API call fails.
        """
        try:
            import google.generativeai as genai  # type: ignore

            genai.configure(api_key=self.google_api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        except Exception as e:
            raise Exception(f"Google Gemini API error: {str(e)}")


    def _call_groq(self, prompt: str) -> Optional[str]:
        """
        Call Groq API.

        Args:
            prompt: The prompt for docstring generation.

        Returns:
            Generated docstring.

        Raises:
            Exception: If the API call fails.
        """
        try:
            from groq import Groq  # type: ignore

            client = Groq(api_key=self.groq_api_key)
            message = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return message.choices[0].message.content
        except ImportError:
            raise ImportError("groq package not installed")
        except Exception as e:
            # If Groq fails, mark as unavailable
            self.provider_status[Provider.GROQ] = "error"
            raise Exception(f"Groq API error: {str(e)}")

    def _build_prompt(
        self,
        function_signature: str,
        code_context: str,
        docstring_style: str
    ) -> str:
        """
        Build the prompt for docstring generation.

        Args:
            function_signature: The function signature.
            code_context: The function implementation code.
            docstring_style: The docstring style.

        Returns:
            The formatted prompt.
        """
        style_instructions = self._get_style_instructions(docstring_style)

        prompt = f"""Generate a docstring for the following Python function in the exact {docstring_style.upper()} style format.

Function Signature:
{function_signature}

Function Implementation:
{code_context}

{style_instructions}

Strict Requirements:
1. Follow the exact {docstring_style.upper()} style formatting precisely.
2. Include Args, Returns, and Raises sections only if applicable to the function.
3. Do not add any introductory or concluding paragraphs, narratives, or extra text.
4. Use only the structured sections as defined in the style.
5. Return ONLY the docstring content without code fences or explanations.

Generate the docstring:"""

        return prompt

    def _get_style_instructions(self, style: str) -> str:
        """Get style-specific instructions."""
        styles = {
            "google": """Google Style:
- Summary line (imperative mood)
- Blank line
- Extended description (optional)
- Args section with type hints
- Returns section with type
- Raises section if applicable""",
            "numpy": """NumPy Style:
- Summary line (imperative mood)
- Extended description (optional)
- Parameters section
- Returns section
- Raises section if applicable""",
            "rest": """reStructuredText Style:
- Summary line (imperative mood)
- Extended description (optional)
- :param name: description (for each parameter)
- :return: description
- :raises ErrorType: description"""
        }
        return styles.get(style, styles["google"])

    def _handle_provider_failure(self, provider: Provider, error: str) -> None:
        """
        Handle provider failure and update status.

        Args:
            provider: The provider that failed.
            error: The error message.
        """
        # Check if it's a rate limit error
        if "rate" in error.lower() or "quota" in error.lower():
            self.provider_status[provider] = "rate_limited"
            # Optionally implement exponential backoff
        else:
            self.provider_status[provider] = "error"

    def get_provider_status(self) -> Dict[str, str]:
        """
        Get the current status of all providers.

        Returns:
            Dictionary with provider statuses.
        """
        return self.provider_status.copy()

    def reset_provider_status(self) -> None:
        """Reset all providers to available status."""
        for provider in self.provider_status:
            self.provider_status[provider] = "available"
