from django.core.cache import cache

from config.settings import CASHE_ENABLED


def get_blog_from_cashe(obj):
    """Если есть в кеше -> берем оттуда, если нет -> кладем в кеш"""
    if not CASHE_ENABLED:
        print(obj)
        return obj
    key = "blog_list"
    objects = cache.get(key)
    if objects is not None:
        return objects
    objects = obj
    cache.set(key, objects)
    return objects
