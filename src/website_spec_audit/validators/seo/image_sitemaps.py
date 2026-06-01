from lxml import etree

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ImageSitemapsValidator(BaseValidator):
    slug = "image-sitemaps"
    title = "Image and video sitemap extensions"
    category = "seo"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/seo/image-sitemaps/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/sitemap.xml")

        if resource.status_code != 200:
            return self.skip_result("No sitemap.xml found; cannot check for image/video extensions.")

        try:
            root = etree.fromstring(resource.text.encode())
        except etree.XMLSyntaxError:
            return self.skip_result("sitemap.xml is not valid XML.")

        nsmap = root.nsmap
        all_ns = set(nsmap.values())

        # Also collect namespaces from child elements
        for elem in root.iter():
            all_ns.update(elem.nsmap.values())

        has_image = any("image" in ns for ns in all_ns)
        has_video = any("video" in ns for ns in all_ns)

        if has_image and has_video:
            return self.pass_result("Sitemap contains both image and video namespace extensions.")
        if has_image:
            return self.pass_result("Sitemap contains image namespace extension.")
        if has_video:
            return self.pass_result("Sitemap contains video namespace extension.")

        return self.warn_result(
            "Sitemap found but does not contain image or video namespace extensions."
        )
