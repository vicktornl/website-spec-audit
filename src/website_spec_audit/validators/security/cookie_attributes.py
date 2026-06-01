from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CookieAttributesValidator(BaseValidator):
    slug = "cookie-attributes"
    title = "Cookie attributes \u2014 Secure, HttpOnly, SameSite"
    category = "security"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/security/cookie-attributes/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")

        # httpx.Headers stores multiple values; get all Set-Cookie headers
        set_cookie_headers = resource.headers.multi_items()
        cookies = [
            value for name, value in set_cookie_headers if name.lower() == "set-cookie"
        ]

        if not cookies:
            return self.pass_result("No cookies set on the response.")

        issues: list[str] = []

        for cookie_str in cookies:
            parts = [p.strip() for p in cookie_str.split(";")]
            cookie_name = parts[0].split("=", 1)[0].strip() if parts else "unknown"
            attrs_lower = [p.lower() for p in parts[1:]]

            missing: list[str] = []

            if not any(a == "secure" for a in attrs_lower):
                missing.append("Secure")

            if not any(a == "httponly" for a in attrs_lower):
                missing.append("HttpOnly")

            if not any(a.startswith("samesite") for a in attrs_lower):
                missing.append("SameSite")

            if missing:
                issues.append(f"Cookie '{cookie_name}' missing: {', '.join(missing)}.")

        if issues:
            return self.fail_result(
                f"{len(issues)} cookie(s) with missing security attributes.",
                details=issues,
            )

        return self.pass_result("All cookies have Secure, HttpOnly, and SameSite attributes.")
