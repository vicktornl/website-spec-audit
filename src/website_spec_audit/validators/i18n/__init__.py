from website_spec_audit.validators.i18n.avoid_auto_geo_redirects import AvoidAutoGeoRedirectsValidator
from website_spec_audit.validators.i18n.hreflang import HreflangValidator
from website_spec_audit.validators.i18n.idn_support import IdnSupportValidator
from website_spec_audit.validators.i18n.international_url_structure import InternationalUrlStructureValidator
from website_spec_audit.validators.i18n.lang_attribute import LangAttributeValidator
from website_spec_audit.validators.i18n.language_switcher import LanguageSwitcherValidator
from website_spec_audit.validators.i18n.locale_content import LocaleContentValidator
from website_spec_audit.validators.i18n.localised_metadata import LocalisedMetadataValidator
from website_spec_audit.validators.i18n.plural_rules import PluralRulesValidator
from website_spec_audit.validators.i18n.rtl_support import RtlSupportValidator
from website_spec_audit.validators.i18n.sitemap_hreflang import SitemapHreflangValidator
from website_spec_audit.validators.i18n.writing_modes import WritingModesValidator

ALL_VALIDATORS = [
    InternationalUrlStructureValidator(),
    HreflangValidator(),
    LocalisedMetadataValidator(),
    SitemapHreflangValidator(),
    AvoidAutoGeoRedirectsValidator(),
    LangAttributeValidator(),
    LanguageSwitcherValidator(),
    RtlSupportValidator(),
    WritingModesValidator(),
    LocaleContentValidator(),
    PluralRulesValidator(),
    IdnSupportValidator(),
]
