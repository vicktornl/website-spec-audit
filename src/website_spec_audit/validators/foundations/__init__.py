from website_spec_audit.validators.foundations.canonical_url import CanonicalUrlValidator
from website_spec_audit.validators.foundations.color_scheme import ColorSchemeValidator
from website_spec_audit.validators.foundations.doctype import DoctypeValidator
from website_spec_audit.validators.foundations.favicons import FaviconsValidator
from website_spec_audit.validators.foundations.feed_discovery import FeedDiscoveryValidator
from website_spec_audit.validators.foundations.feed_hygiene import FeedHygieneValidator
from website_spec_audit.validators.foundations.html_lang import HtmlLangValidator
from website_spec_audit.validators.foundations.meta_charset import MetaCharsetValidator
from website_spec_audit.validators.foundations.meta_description import MetaDescriptionValidator
from website_spec_audit.validators.foundations.meta_viewport import MetaViewportValidator
from website_spec_audit.validators.foundations.open_graph import OpenGraphValidator
from website_spec_audit.validators.foundations.popover_api import PopoverApiValidator
from website_spec_audit.validators.foundations.theme_color import ThemeColorValidator
from website_spec_audit.validators.foundations.title import TitleValidator

ALL_VALIDATORS = [
    DoctypeValidator(),
    HtmlLangValidator(),
    MetaCharsetValidator(),
    MetaViewportValidator(),
    TitleValidator(),
    MetaDescriptionValidator(),
    CanonicalUrlValidator(),
    FaviconsValidator(),
    ThemeColorValidator(),
    ColorSchemeValidator(),
    OpenGraphValidator(),
    FeedDiscoveryValidator(),
    FeedHygieneValidator(),
    PopoverApiValidator(),
]
