from website_spec_audit.validators.seo.breadcrumbs import BreadcrumbsValidator
from website_spec_audit.validators.seo.heading_hierarchy import HeadingHierarchyValidator
from website_spec_audit.validators.seo.image_sitemaps import ImageSitemapsValidator
from website_spec_audit.validators.seo.indexnow import IndexNowValidator
from website_spec_audit.validators.seo.internal_linking import InternalLinkingValidator
from website_spec_audit.validators.seo.meta_robots import MetaRobotsValidator
from website_spec_audit.validators.seo.redirects import RedirectsValidator
from website_spec_audit.validators.seo.robots_txt import RobotsTxtValidator
from website_spec_audit.validators.seo.sitemap_index import SitemapIndexValidator
from website_spec_audit.validators.seo.soft_404 import Soft404Validator
from website_spec_audit.validators.seo.structured_data import StructuredDataValidator
from website_spec_audit.validators.seo.url_structure import UrlStructureValidator
from website_spec_audit.validators.seo.xml_sitemaps import XmlSitemapsValidator

ALL_VALIDATORS = [
    BreadcrumbsValidator(),
    HeadingHierarchyValidator(),
    ImageSitemapsValidator(),
    IndexNowValidator(),
    InternalLinkingValidator(),
    MetaRobotsValidator(),
    RedirectsValidator(),
    RobotsTxtValidator(),
    SitemapIndexValidator(),
    Soft404Validator(),
    StructuredDataValidator(),
    UrlStructureValidator(),
    XmlSitemapsValidator(),
]
