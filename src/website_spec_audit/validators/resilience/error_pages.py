from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ErrorPagesValidator(BaseValidator):
    slug = "error-pages"
    title = "Custom error pages (404, 500)"
    category = "resilience"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/resilience/error-pages/"

    NOT_FOUND_PATH = "/this-path-does-not-exist-spec-audit"
    MIN_BODY_LENGTH = 200

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch(self.NOT_FOUND_PATH)
        details: list[str] = []

        if resource.status_code != 404:
            details.append(
                f"Expected 404 status but got {resource.status_code}."
            )
            return self.fail_result(
                "Non-existent path did not return 404 status.",
                details=details,
            )

        body_length = len(resource.text.strip())

        if body_length == 0:
            return self.fail_result(
                "404 page returned an empty response body.",
                details=["A custom error page should provide helpful content."],
            )

        if body_length < self.MIN_BODY_LENGTH:
            return self.warn_result(
                f"404 page has a very short response body ({body_length} characters).",
                details=[
                    "The error page may be a default server error rather than a custom page.",
                ],
            )

        # Check for common default server error indicators
        default_indicators = [
            "nginx",
            "apache",
            "iis",
            "not found</title>",
            "404 not found</h1>",
        ]
        text_lower = resource.text.lower()
        for indicator in default_indicators:
            if f"<title>{indicator}" in text_lower or f"<center>{indicator}" in text_lower:
                details.append(
                    f"Page appears to be a default server error page (contains '{indicator}')."
                )
                return self.warn_result(
                    "404 page may be a default server error page.",
                    details=details,
                )

        return self.pass_result(
            "Custom 404 error page detected with meaningful content."
        )
