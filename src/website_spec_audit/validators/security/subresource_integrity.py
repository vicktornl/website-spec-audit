from urllib.parse import urlparse

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SubresourceIntegrityValidator(BaseValidator):
    slug = "subresource-integrity"
    title = "Subresource Integrity (SRI)"
    category = "security"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/security/subresource-integrity/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        site_parsed = urlparse(context.url)
        site_origin = f"{site_parsed.scheme}://{site_parsed.netloc}"

        missing_integrity: list[str] = []

        # Check external <script> tags
        for script in doc.iter("script"):
            src = script.get("src")
            if not src:
                continue
            if self._is_cross_origin(src, site_origin):
                if not script.get("integrity"):
                    missing_integrity.append(f"<script src=\"{src}\">")

        # Check external <link rel="stylesheet"> tags
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "stylesheet" not in rel:
                continue
            href = link.get("href")
            if not href:
                continue
            if self._is_cross_origin(href, site_origin):
                if not link.get("integrity"):
                    missing_integrity.append(f"<link rel=\"stylesheet\" href=\"{href}\">")

        if not missing_integrity:
            return self.pass_result(
                "All cross-origin scripts and stylesheets have integrity attributes."
            )

        return self.warn_result(
            f"{len(missing_integrity)} cross-origin resource(s) missing integrity attribute.",
            details=missing_integrity,
        )

    @staticmethod
    def _is_cross_origin(url: str, site_origin: str) -> bool:
        """Return True if the URL points to a different origin."""
        if url.startswith("//"):
            url = "https:" + url
        parsed = urlparse(url)
        if not parsed.netloc:
            # Relative URL, same origin
            return False
        resource_origin = f"{parsed.scheme}://{parsed.netloc}"
        return resource_origin.lower() != site_origin.lower()
