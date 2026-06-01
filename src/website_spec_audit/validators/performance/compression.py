from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CompressionValidator(BaseValidator):
    slug = "compression"
    title = "Compression (gzip, brotli, zstd)"
    category = "performance"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/performance/compression/"

    SUPPORTED_ENCODINGS = {"br", "gzip", "zstd"}

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        content_encoding = resource.headers.get("content-encoding", "").lower().strip()

        details: list[str] = []

        # Check what the client advertised
        # Note: httpx sends Accept-Encoding by default
        if content_encoding:
            details.append(f"Content-Encoding: {content_encoding}")

        encodings = {e.strip() for e in content_encoding.split(",") if e.strip()}
        matched = encodings & self.SUPPORTED_ENCODINGS

        if not content_encoding:
            return self.fail_result(
                "No Content-Encoding header found. "
                "The response does not appear to be compressed.",
                details=details,
            )

        if not matched:
            return self.fail_result(
                f"Content-Encoding is '{content_encoding}' which is not a recognized compression algorithm.",
                details=details,
            )

        if "br" in matched:
            return self.pass_result(
                f"Response is compressed with Brotli (Content-Encoding: {content_encoding})."
            )

        if "zstd" in matched:
            return self.pass_result(
                f"Response is compressed with Zstandard (Content-Encoding: {content_encoding})."
            )

        return self.pass_result(
            f"Response is compressed (Content-Encoding: {content_encoding})."
        )
