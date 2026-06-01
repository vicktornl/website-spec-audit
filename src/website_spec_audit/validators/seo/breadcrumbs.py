import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class BreadcrumbsValidator(BaseValidator):
    slug = "breadcrumbs"
    title = "Breadcrumbs"
    category = "seo"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/seo/breadcrumbs/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        # Check JSON-LD for BreadcrumbList
        scripts = doc.cssselect('script[type="application/ld+json"]')
        for script in scripts:
            text = script.text_content().strip()
            if not text:
                continue
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                continue

            items = data if isinstance(data, list) else [data]
            for item in items:
                if isinstance(item, dict) and item.get("@type") == "BreadcrumbList":
                    return self.pass_result("BreadcrumbList found in JSON-LD structured data.")

        # Check for breadcrumb navigation in HTML
        # aria-label="breadcrumb" or aria-label="Breadcrumb"
        nav_elements = doc.cssselect("nav")
        for nav in nav_elements:
            aria_label = (nav.get("aria-label") or "").lower()
            if "breadcrumb" in aria_label:
                return self.pass_result(
                    'Breadcrumb navigation found via <nav aria-label="breadcrumb">.'
                )

        # Check for ol/ul with breadcrumb-related attributes or classes
        for el in doc.cssselect('[itemtype="https://schema.org/BreadcrumbList"]'):
            return self.pass_result("Breadcrumb found via Microdata (schema.org/BreadcrumbList).")

        return self.fail_result("No breadcrumb navigation or BreadcrumbList structured data found.")
