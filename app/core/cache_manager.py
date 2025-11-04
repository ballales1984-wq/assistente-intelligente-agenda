#!/usr/bin/env python3
"""
🔴 CACHE MANAGER - Redis Caching Utilities
Gestisce cache intelligente per performance ottimali.

Author: Assistente AI
Date: 5 Nov 2025
"""

import logging
from functools import wraps
from app import cache

logger = logging.getLogger(__name__)


class CacheManager:
    """Gestisce operazioni di cache con Redis"""

    # Timeout per diversi tipi di dati (in secondi)
    TIMEOUTS = {
        "predictions": 3600,  # 1 ora - previsioni AI
        "stats": 300,  # 5 minuti - statistiche
        "search": 86400,  # 24 ore - ricerche web
        "user_session": 2592000,  # 30 giorni - sessioni utente
        "feed": 60,  # 1 minuto - community feed
        "quick": 30,  # 30 secondi - dati frequenti
    }

    @staticmethod
    def get_user_cache_key(user_id, prefix):
        """Genera chiave cache per utente specifico"""
        return f"{prefix}:user_{user_id}"

    @staticmethod
    def get_search_cache_key(query):
        """Genera chiave cache per ricerca"""
        # Normalizza query per cache efficace
        normalized = query.lower().strip().replace(" ", "_")
        return f"search:{normalized}"

    @staticmethod
    def invalidate_user_cache(user_id, prefixes=None):
        """
        Invalida cache per un utente specifico.

        Args:
            user_id: ID utente
            prefixes: Lista di prefissi da invalidare (es. ['stats', 'predictions'])
                     Se None, invalida tutti
        """
        if prefixes is None:
            prefixes = ["stats", "predictions", "feed"]

        for prefix in prefixes:
            key = CacheManager.get_user_cache_key(user_id, prefix)
            cache.delete(key)
            logger.info(f"🗑️ Cache invalidated: {key}")

    @staticmethod
    def cache_prediction(timeout=None):
        """
        Decorator per cachare previsioni AI.

        Usage:
            @cache_prediction(timeout=3600)
            def get_weekly_predictions(user_id):
                # expensive calculation
                return predictions
        """
        if timeout is None:
            timeout = CacheManager.TIMEOUTS["predictions"]

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Estrai user_id dal primo argomento o kwargs
                user_id = args[0] if args else kwargs.get("user_id")

                if user_id:
                    cache_key = CacheManager.get_user_cache_key(user_id, "predictions")
                    cached = cache.get(cache_key)

                    if cached:
                        logger.info(f"✅ Cache HIT: {cache_key}")
                        return cached

                    logger.info(f"❌ Cache MISS: {cache_key}")

                # Calcola risultato
                result = f(*args, **kwargs)

                # Salva in cache
                if user_id and result:
                    cache_key = CacheManager.get_user_cache_key(user_id, "predictions")
                    cache.set(cache_key, result, timeout=timeout)
                    logger.info(f"💾 Cache SET: {cache_key} (TTL: {timeout}s)")

                return result

            return decorated_function

        return decorator

    @staticmethod
    def cache_stats(timeout=None):
        """
        Decorator per cachare statistiche.

        Usage:
            @cache_stats(timeout=300)
            def get_user_stats(user_id):
                return stats
        """
        if timeout is None:
            timeout = CacheManager.TIMEOUTS["stats"]

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_id = args[0] if args else kwargs.get("user_id")

                if user_id:
                    cache_key = CacheManager.get_user_cache_key(user_id, "stats")
                    cached = cache.get(cache_key)

                    if cached:
                        logger.info(f"✅ Cache HIT: {cache_key}")
                        return cached

                    logger.info(f"❌ Cache MISS: {cache_key}")

                result = f(*args, **kwargs)

                if user_id and result:
                    cache_key = CacheManager.get_user_cache_key(user_id, "stats")
                    cache.set(cache_key, result, timeout=timeout)
                    logger.info(f"💾 Cache SET: {cache_key} (TTL: {timeout}s)")

                return result

            return decorated_function

        return decorator

    @staticmethod
    def cache_search(timeout=None):
        """
        Decorator per cachare ricerche web.

        Usage:
            @cache_search(timeout=86400)
            def search_web(query):
                return duckduckgo_results
        """
        if timeout is None:
            timeout = CacheManager.TIMEOUTS["search"]

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                query = args[0] if args else kwargs.get("query")

                if query:
                    cache_key = CacheManager.get_search_cache_key(query)
                    cached = cache.get(cache_key)

                    if cached:
                        logger.info(f"✅ Cache HIT: {cache_key}")
                        return cached

                    logger.info(f"❌ Cache MISS: {cache_key}")

                result = f(*args, **kwargs)

                if query and result:
                    cache_key = CacheManager.get_search_cache_key(query)
                    cache.set(cache_key, result, timeout=timeout)
                    logger.info(f"💾 Cache SET: {cache_key} (TTL: {timeout}s)")

                return result

            return decorated_function

        return decorator


# ========================================
# HELPER FUNCTIONS
# ========================================


def clear_all_cache():
    """Cancella tutta la cache (admin only!)"""
    cache.clear()
    logger.warning("🗑️ ALL CACHE CLEARED!")


def get_cache_stats():
    """Ottieni statistiche cache"""
    try:
        # Funziona solo con Redis backend
        info = {
            "backend": "Redis" if os.getenv("REDIS_URL") else "SimpleCache",
            "redis_url": bool(os.getenv("REDIS_URL")),
        }
        return info
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {"backend": "Unknown", "error": str(e)}


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("🔴 TESTING CACHE MANAGER")
    print("=" * 70)

    # Test cache decorator
    @CacheManager.cache_stats(timeout=60)
    def expensive_calculation(user_id):
        print(f"💰 Expensive calculation for user {user_id}...")
        import time

        time.sleep(0.5)  # Simula calcolo pesante
        return {"result": user_id * 100}

    # Prima chiamata (MISS)
    print("\n1. First call (should be MISS):")
    result1 = expensive_calculation(123)
    print(f"Result: {result1}")

    # Seconda chiamata (HIT)
    print("\n2. Second call (should be HIT - instant):")
    result2 = expensive_calculation(123)
    print(f"Result: {result2}")

    # Invalidate
    print("\n3. Invalidate cache:")
    CacheManager.invalidate_user_cache(123, ["stats"])

    # Terza chiamata (MISS again)
    print("\n4. Third call (should be MISS again):")
    result3 = expensive_calculation(123)
    print(f"Result: {result3}")

    print("\n" + "=" * 70)
    print("✅ CACHE MANAGER TESTS COMPLETED!")
    print("=" * 70)
