#!/usr/bin/env python3
"""
🌐 WEB SEARCH INTEGRATION - DuckDuckGo
Permette ricerca web direttamente dalla chat senza API keys!

Author: Assistente AI
Date: 5 Nov 2025
"""

import logging

from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


class WebSearchService:
    """
    Servizio di ricerca web usando DuckDuckGo.
    Zero API keys, gratis, illimitato!
    """

    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 5, region: str = "wt-wt"):
        """
        Esegue una ricerca web e ritorna i top risultati.

        Args:
            query: Termine di ricerca (es. "machine learning")
            max_results: Numero massimo di risultati (default: 5)
            region: Regione (default: 'wt-wt' = worldwide)
                    'it-it' = Italia, 'us-en' = USA, etc.

        Returns:
            list: Lista di dict con:
                - title: Titolo risultato
                - href: URL
                - body: Snippet descrittivo

        Example:
            >>> ws = WebSearchService()
            >>> results = ws.search("python tutorial", max_results=3)
            >>> for r in results:
            >>>     print(f"{r['title']}: {r['href']}")
        """
        # Check cache first (24h cache per query comuni)
        cache_key = f"search:{query.lower().replace(' ', '_')}"
        cached_results = cache.get(cache_key)

        if cached_results:
            logger.info(f"✅ Cache HIT: {cache_key}")
            return cached_results

        logger.info(f"❌ Cache MISS: {cache_key}")

        try:
            logger.info(f"🔍 DuckDuckGo search: '{query}' (max: {max_results})")

            # Esegui ricerca
            results = []
            search_gen = self.ddgs.text(
                keywords=query,
                region=region,
                safesearch="moderate",
                max_results=max_results,
            )

            for idx, result in enumerate(search_gen, 1):
                if idx > max_results:
                    break

                results.append(
                    {
                        "title": result.get("title", "No Title"),
                        "href": result.get("href", ""),
                        "body": result.get("body", "No description")[
                            :200
                        ],  # Limita a 200 char
                    }
                )

            logger.info(f"✅ Found {len(results)} results")

            # Salva in cache (24 ore)
            if results:
                cache.set(cache_key, results, timeout=86400)
                logger.info(f"💾 Cache SET: {cache_key} (TTL: 24h)")

            return results

        except Exception as e:
            logger.error(f"❌ DuckDuckGo search error: {e}")
            return []

    def search_news(self, query: str, max_results: int = 5):
        """
        Cerca notizie recenti.

        Args:
            query: Termine di ricerca
            max_results: Numero massimo di risultati

        Returns:
            list: Lista di notizie recenti
        """
        # Check cache first (1 ora per news - aggiornamento frequente)
        cache_key = f"news:{query.lower().replace(' ', '_')}"
        cached_results = cache.get(cache_key)

        if cached_results:
            logger.info(f"✅ Cache HIT: {cache_key}")
            return cached_results

        logger.info(f"❌ Cache MISS: {cache_key}")

        try:
            logger.info(f"📰 DuckDuckGo news: '{query}' (max: {max_results})")

            results = []
            news_gen = self.ddgs.news(keywords=query, max_results=max_results)

            for idx, item in enumerate(news_gen, 1):
                if idx > max_results:
                    break

                results.append(
                    {
                        "title": item.get("title", "No Title"),
                        "href": item.get("url", ""),
                        "body": item.get("body", "No description")[:200],
                        "date": item.get("date", "Unknown"),
                        "source": item.get("source", "Unknown"),
                    }
                )

            logger.info(f"✅ Found {len(results)} news")

            # Salva in cache (1 ora - news cambiano spesso)
            if results:
                cache.set(cache_key, results, timeout=3600)
                logger.info(f"💾 Cache SET: {cache_key} (TTL: 1h)")

            return results

        except Exception as e:
            logger.error(f"❌ DuckDuckGo news error: {e}")
            return []

    def instant_answer(self, query: str):
        """
        Cerca una risposta istantanea (es. definizioni, calcoli).

        Args:
            query: Query (es. "what is python", "2+2")

        Returns:
            dict: Risposta istantanea o None

        Note: Feature temporarily disabled in duckduckgo-search 8.x API
        """
        # TODO: Reimplement when API supports instant answers again
        logger.info(f"⚡ DuckDuckGo instant: '{query}' (feature disabled)")
        return None


# ========================================
# HELPER FUNCTION per facile import
# ========================================


def quick_search(query: str, max_results: int = 5):
    """
    Funzione helper per ricerca veloce.

    Usage:
        from app.integrations.web_search import quick_search
        results = quick_search("python tutorial", max_results=3)
    """
    ws = WebSearchService()
    return ws.search(query, max_results)


def quick_news(query: str, max_results: int = 5):
    """
    Funzione helper per news veloci.

    Usage:
        from app.integrations.web_search import quick_news
        news = quick_news("tech news", max_results=3)
    """
    ws = WebSearchService()
    return ws.search_news(query, max_results)


# ========================================
# TESTING (run questo file direttamente)
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("🔍 TESTING WEB SEARCH SERVICE")
    print("=" * 70)

    ws = WebSearchService()

    # Test 1: Ricerca normale
    print("\n1. TEST: Normal Search")
    results = ws.search("python programming", max_results=3)
    for idx, r in enumerate(results, 1):
        print(f"\n{idx}. {r['title']}")
        print(f"   URL: {r['href']}")
        print(f"   {r['body'][:100]}...")

    # Test 2: News
    print("\n2. TEST: News Search")
    news = ws.search_news("artificial intelligence", max_results=2)
    for idx, n in enumerate(news, 1):
        print(f"\n{idx}. {n['title']}")
        print(f"   Source: {n['source']} - {n['date']}")
        print(f"   URL: {n['href']}")

    # Test 3: Instant Answer
    print("\n3. TEST: Instant Answer")
    answer = ws.instant_answer("what is python")
    if answer:
        print(f"\n{answer['text'][:200]}...")
        print(f"URL: {answer['url']}")
    else:
        print("No instant answer found")

    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 70)
