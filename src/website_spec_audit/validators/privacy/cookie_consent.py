from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CookieConsentValidator(BaseValidator):
    slug = "cookie-consent"
    title = "Cookie consent"
    category = "privacy"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/privacy/cookie-consent/"

    CONSENT_SCRIPTS = [
        "cookiebot",
        "onetrust",
        "cookieconsent",
        "cookie-consent",
        "cookieyes",
        "termly",
        "iubenda",
        "quantcast",
        "trustarc",
        "cookiefirst",
        "complianz",
        "cookie-script",
        "cookieinformation",
    ]

    # Cookies commonly considered essential / functional (not tracking)
    ESSENTIAL_COOKIE_PREFIXES = [
        "__cfduid",
        "__cf_bm",
        "csrftoken",
        "csrf",
        "session",
        "sid",
        "xsrf",
    ]

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        doc = await context.fetch_html("/")

        details: list[str] = []

        # Check for cookies set on first request
        set_cookie_headers = resource.headers.multi_items()
        cookies = [
            value
            for name, value in set_cookie_headers
            if name.lower() == "set-cookie"
        ]

        non_essential_cookies: list[str] = []
        for cookie_str in cookies:
            cookie_name = cookie_str.split("=", 1)[0].strip().lower()
            is_essential = any(
                cookie_name.startswith(prefix)
                for prefix in self.ESSENTIAL_COOKIE_PREFIXES
            )
            if not is_essential:
                non_essential_cookies.append(cookie_name)

        if non_essential_cookies:
            details.append(
                f"Potentially non-essential cookies set before consent: "
                f"{', '.join(non_essential_cookies)}."
            )

        # Check for consent banner scripts in HTML
        consent_found = False
        html_lower = resource.text.lower()

        for script_id in self.CONSENT_SCRIPTS:
            if script_id in html_lower:
                consent_found = True
                details.append(f"Consent mechanism detected: '{script_id}'.")
                break

        if not consent_found:
            # Also check script src attributes
            for script in doc.iter("script"):
                src = (script.get("src") or "").lower()
                for script_id in self.CONSENT_SCRIPTS:
                    if script_id in src:
                        consent_found = True
                        details.append(
                            f"Consent script detected in src: '{script_id}'."
                        )
                        break
                if consent_found:
                    break

        if not consent_found and non_essential_cookies:
            return self.fail_result(
                "No cookie consent mechanism detected, but cookies are set.",
                details=details,
            )

        if not consent_found and not cookies:
            return self.pass_result("No cookies set and no consent banner needed.")

        if consent_found and non_essential_cookies:
            return self.warn_result(
                "Consent mechanism found, but cookies are set before interaction.",
                details=details,
            )

        if consent_found:
            return self.pass_result("Cookie consent mechanism detected.")

        return self.warn_result(
            "Cookies are set but no consent banner was detected (heuristic check).",
            details=details,
        )
