from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class FaviconsValidator(BaseValidator):
    slug = "favicons"
    title = "Favicons and app icons"
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/favicons/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        icon_links = doc.cssselect('link[rel="icon"], link[rel="shortcut icon"]')
        apple_touch = doc.cssselect('link[rel="apple-touch-icon"]')

        # Check /favicon.ico via HEAD request
        favicon_ico = await context.fetch("/favicon.ico")
        has_favicon_ico = favicon_ico.status_code == 200

        details: list[str] = []
        if has_favicon_ico:
            details.append("/favicon.ico is reachable.")
        else:
            details.append("/favicon.ico returned HTTP {}.".format(favicon_ico.status_code))

        if icon_links:
            details.append(f"Found {len(icon_links)} <link rel=\"icon\"> element(s).")
        else:
            details.append("No <link rel=\"icon\"> found in HTML.")

        if apple_touch:
            details.append(f"Found {len(apple_touch)} <link rel=\"apple-touch-icon\"> element(s).")
        else:
            details.append("No <link rel=\"apple-touch-icon\"> found in HTML.")

        if not has_favicon_ico and not icon_links:
            return self.fail_result("No favicon found.", details=details)

        if not apple_touch:
            return self.warn_result(
                "Favicon found but no apple-touch-icon declared.",
                details=details,
            )

        return self.pass_result("Favicons and app icons found.")
