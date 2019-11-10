from django.conf import settings

from . import config

from elasticsearch_dsl import token_filter, analyzer


def _get_locale_specific_analyzer(locale):
    """Get analyzer for locales specified in config otherwise return None
    This function will return an analyzer if
    the locale is configured to use specific analyzer.
    Otherwise, it will return None
    """
    locale_analyzer = config.ES_LOCALE_ANALYZERS.get(locale)
    if locale_analyzer:
        if not settings.ES_USE_PLUGINS and locale_analyzer in settings.ES_PLUGIN_ANALYZERS:
            return None

        return analyzer(locale, type=locale_analyzer)

    snowball_language = config.ES_SNOWBALL_LOCALES.get(locale)
    if snowball_language:
        # The locale is configured to use snowball filter
        token_name = 'snowball_{}'.format(locale.lower())
        snowball_filter = token_filter(token_name, type='snowball', language=snowball_language)

        # Use language specific snowball filter with standard analyzer.
        # The standard analyzer is basically a analyzer with standard tokenizer
        # and standard, lowercase and stop filter
        locale_analyzer = analyzer(locale, tokenizer='standard',
                                   filter=["standard", "lowercase", "stop", snowball_filter])
        return locale_analyzer


def es_analyzer_for_locale(locale):
    """Pick an appropriate analyzer for a given locale.
    If no analyzer is defined for `locale` or the locale analyzer uses a plugin
    but using plugin is turned off from settings, return ES analyzer named "standard".
    """

    local_specific_analyzer = _get_locale_specific_analyzer(locale=locale)
    if local_specific_analyzer:
        return local_specific_analyzer
    else:
        # No specific analyzer found for the locale
        # So use the standard analyzer as default
        return analyzer('default', type='standard')
