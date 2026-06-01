from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MetaCharsetValidator(BaseValidator):
    slug = "meta-charset"
    title = "<meta charset>"
    category = "foundations"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/foundations/meta-charset/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        first_1024 = resource.text[:1024].lower()

        has_charset_meta = 'charset="utf-8"' in first_1024 or "charset=utf-8" in first_1024
        has_http_equiv = (
            'http-equiv="content-type"' in first_1024
            and "charset=utf-8" in first_1024
        )

        if has_charset_meta or has_http_equiv:
            return self.pass_result(
                "UTF-8 charset declaration found within the first 1024 bytes."
            )

        doc = await context.fetch_html("/")
        meta_charset = doc.cssselect('meta[charset]')
        meta_http_equiv = doc.cssselect('meta[http-equiv="Content-Type"]')

        if meta_charset or meta_http_equiv:
            return self.warn_result(
                "Charset declaration found but not within the first 1024 bytes of the document."
            )

        return self.fail_result("No <meta charset> declaration found.")
