from lxml import etree

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SitemapIndexValidator(BaseValidator):
    slug = "sitemap-index"
    title = "Sitemap index files"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/sitemap-index/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/sitemap.xml")

        if resource.status_code != 200:
            return self.skip_result("No sitemap.xml found; cannot check for sitemap index.")

        try:
            root = etree.fromstring(resource.text.encode())
        except etree.XMLSyntaxError:
            return self.skip_result("sitemap.xml is not valid XML; cannot check for sitemap index.")

        local_name = etree.QName(root.tag).localname

        if local_name == "sitemapindex":
            children = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap")
            count = len(children)
            return self.pass_result(
                f"Sitemap index found with {count} child sitemap(s)."
            )

        return self.skip_result(
            "sitemap.xml uses <urlset> root; sitemap index is not applicable for small sites."
        )
