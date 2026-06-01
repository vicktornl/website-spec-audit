from lxml import etree

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class XmlSitemapsValidator(BaseValidator):
    slug = "xml-sitemaps"
    title = "XML sitemaps"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/xml-sitemaps/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/sitemap.xml")

        if resource.status_code != 200:
            return self.fail_result(
                f"/sitemap.xml returned HTTP {resource.status_code}.",
            )

        try:
            root = etree.fromstring(resource.text.encode())
        except etree.XMLSyntaxError as exc:
            return self.fail_result(
                "sitemap.xml is not valid XML.",
                details=[str(exc)],
            )

        local_name = etree.QName(root.tag).localname
        if local_name not in ("urlset", "sitemapindex"):
            return self.fail_result(
                f"Unexpected root element <{local_name}>; expected <urlset> or <sitemapindex>.",
            )

        return self.pass_result(
            f"Valid XML sitemap found with root element <{local_name}>."
        )
