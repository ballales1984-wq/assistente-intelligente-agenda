#!/usr/bin/env python3
"""
🔗 SMART LINKS - Intelligent Link Detection & Generation
Riconosce quando l'utente chiede ricerche e genera link intelligenti.

Author: Assistente AI
Date: 5 Nov 2025
"""

import logging
import re

from app.integrations.web_search import WebSearchService

logger = logging.getLogger(__name__)


class SmartLinksManager:
    """
    Gestisce il riconoscimento e la generazione di smart links.
    """

    def __init__(self):
        self.web_search = WebSearchService()

        # Pattern per riconoscere richieste di ricerca
        self.search_patterns = [
            # Italiano
            r"cerca\s+(.+)",
            r"ricerca\s+(.+)",
            r"trova\s+(?:informazioni\s+su\s+)?(.+)",
            r"google\s+(.+)",
            r"guarda\s+su\s+internet\s+(.+)",
            r"dammi\s+informazioni\s+su\s+(.+)",
            r"cosa\s+sai\s+di\s+(.+)",
            # English
            r"search\s+(?:for\s+)?(.+)",
            r"look\s+up\s+(.+)",
            r"find\s+(?:information\s+(?:on|about)\s+)?(.+)",
            r"google\s+(.+)",
            r"tell\s+me\s+about\s+(.+)",
            r"what\s+(?:do\s+you\s+know\s+about|is)\s+(.+)",
            # Español
            r"busca\s+(.+)",
            r"buscar\s+(.+)",
            r"encuentra\s+(.+)",
            r"información\s+sobre\s+(.+)",
        ]

        # Pattern per notizie
        self.news_patterns = [
            r"notizie\s+(?:su\s+)?(.+)",
            r"news\s+(?:about\s+)?(.+)",
            r"ultim[ie]\s+notizie\s+(?:su\s+)?(.+)",
            r"latest\s+news\s+(?:about\s+)?(.+)",
            r"cosa\s+(?:è\s+successo|succede)\s+(?:con|a)\s+(.+)",
        ]

    def detect_search_intent(self, text: str):
        """
        Rileva se l'utente vuole fare una ricerca.

        Args:
            text: Testo dell'utente

        Returns:
            dict: {
                'is_search': bool,
                'is_news': bool,
                'query': str o None,
                'confidence': float (0-1)
            }
        """
        text_lower = text.lower().strip()

        # Check news patterns first (more specific)
        for pattern in self.news_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                return {
                    "is_search": True,
                    "is_news": True,
                    "query": query,
                    "confidence": 0.95,
                }

        # Check general search patterns
        for pattern in self.search_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                return {
                    "is_search": True,
                    "is_news": False,
                    "query": query,
                    "confidence": 0.9,
                }

        # No search intent detected
        return {"is_search": False, "is_news": False, "query": None, "confidence": 0.0}

    def generate_search_response(
        self, query: str, is_news: bool = False, max_results: int = 5
    ):
        """
        Genera una risposta con risultati di ricerca.

        Args:
            query: Query di ricerca
            is_news: Se True, cerca notizie invece di risultati generali
            max_results: Numero massimo di risultati

        Returns:
            dict: {
                'success': bool,
                'response': str (messaggio per l'utente),
                'results': list (risultati della ricerca),
                'query': str
            }
        """
        try:
            logger.info(
                f"🔗 Generating smart link response for: '{query}' (news: {is_news})"
            )

            # Esegui ricerca
            if is_news:
                results = self.web_search.search_news(query, max_results=max_results)
                search_type = "notizie"
            else:
                results = self.web_search.search(query, max_results=max_results)
                search_type = "risultati"

            if not results:
                return {
                    "success": False,
                    "response": f"❌ Non ho trovato {search_type} per '{query}'. Riprova con termini diversi.",
                    "results": [],
                    "query": query,
                }

            # Costruisci risposta
            response = (
                f"🔍 Ho trovato {len(results)} {search_type} per **'{query}'**:\n\n"
            )

            for idx, result in enumerate(results, 1):
                title = result["title"]
                url = result["href"]
                body = result["body"][:150]  # Limita snippet

                if is_news and "source" in result:
                    source = result["source"]
                    response += f"{idx}. **{title}**\n"
                    response += f"   📰 {source}\n"
                    response += f"   🔗 {url}\n"
                    response += f"   {body}...\n\n"
                else:
                    response += f"{idx}. **{title}**\n"
                    response += f"   🔗 {url}\n"
                    response += f"   {body}...\n\n"

            response += "💡 **Clicca sui link per aprire nel browser!**"

            return {
                "success": True,
                "response": response,
                "results": results,
                "query": query,
            }

        except Exception as e:
            logger.error(f"❌ Error generating search response: {e}")
            return {
                "success": False,
                "response": f"❌ Errore durante la ricerca: {str(e)}",
                "results": [],
                "query": query,
            }

    def process_message(self, text: str):
        """
        Processa un messaggio e genera smart links se necessario.

        Args:
            text: Messaggio dell'utente

        Returns:
            dict: {
                'has_smart_links': bool,
                'response': str o None,
                'results': list o None
            }
        """
        # Detect search intent
        intent = self.detect_search_intent(text)

        if not intent["is_search"]:
            return {"has_smart_links": False, "response": None, "results": None}

        # Generate search response
        search_response = self.generate_search_response(
            query=intent["query"], is_news=intent["is_news"], max_results=5
        )

        if search_response["success"]:
            logger.info(
                f"✅ Smart links generated: {len(search_response['results'])} results"
            )
            return {
                "has_smart_links": True,
                "response": search_response["response"],
                "results": search_response["results"],
            }
        else:
            return {
                "has_smart_links": True,
                "response": search_response["response"],
                "results": [],
            }


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("🔗 TESTING SMART LINKS MANAGER")
    print("=" * 70)

    sm = SmartLinksManager()

    # Test messages
    test_messages = [
        "cerca python tutorial",
        "dimmi di machine learning",
        "notizie su intelligenza artificiale",
        "search for python programming",
        "latest news about AI",
        "crea appuntamento per domani",  # Non è una ricerca
    ]

    for idx, msg in enumerate(test_messages, 1):
        print(f"\n{idx}. MESSAGE: '{msg}'")
        print("-" * 70)

        # Detect intent
        intent = sm.detect_search_intent(msg)
        print(f"Intent: {intent}")

        # Process if search
        if intent["is_search"]:
            result = sm.process_message(msg)
            print(f"\nResponse:\n{result['response'][:300]}...")
            print(
                f"\nResults count: {len(result['results']) if result['results'] else 0}"
            )

    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 70)
