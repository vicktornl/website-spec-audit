from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class RtlSupportValidator(BaseValidator):
    slug = "rtl-support"
    title = "RTL and bidirectional text"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/rtl-support/"

    RTL_LANGUAGES = {
        "ar", "he", "fa", "ur", "ps", "sd", "yi", "arc", "dv", "ku",
        "ckb", "syr", "ug",
    }

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        html_elements = doc.xpath("//html")
        if not html_elements:
            return self.skip_result("No <html> element found.")

        html_el = html_elements[0]
        lang = (html_el.get("lang") or "").strip().lower()

        if not lang:
            return self.skip_result("No lang attribute on <html> element.")

        # Extract primary language subtag
        primary_lang = lang.split("-")[0]

        if primary_lang not in self.RTL_LANGUAGES:
            return self.skip_result(
                f"Page language '{lang}' is not an RTL language."
            )

        # Check for dir attribute
        dir_attr = (html_el.get("dir") or "").strip().lower()

        if dir_attr == "rtl":
            return self.pass_result(
                f"RTL language '{lang}' detected with dir=\"rtl\" attribute.",
            )

        if dir_attr == "auto":
            return self.pass_result(
                f"RTL language '{lang}' detected with dir=\"auto\" attribute.",
            )

        if dir_attr:
            return self.fail_result(
                f"RTL language '{lang}' detected but dir=\"{dir_attr}\" is set instead of \"rtl\".",
            )

        return self.fail_result(
            f"RTL language '{lang}' detected but no dir attribute is set on <html>.",
            details=["Add dir=\"rtl\" to the <html> element for proper RTL rendering."],
        )
