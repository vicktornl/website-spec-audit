from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AnalyticsPrivacyValidator(BaseValidator):
    slug = "analytics-privacy"
    title = "Privacy-respecting analytics"
    category = "privacy"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/privacy/analytics-privacy/"

    TRACKING_INDICATORS = [
        ("google-analytics.com", "Google Analytics"),
        ("googletagmanager.com", "Google Tag Manager"),
        ("gtag/js", "Google gtag.js"),
        ("analytics.google.com", "Google Analytics"),
        ("connect.facebook.net", "Facebook Pixel"),
        ("fbevents.js", "Facebook Pixel"),
        ("hotjar.com", "Hotjar"),
        ("clarity.ms", "Microsoft Clarity"),
        ("mixpanel.com", "Mixpanel"),
        ("segment.com", "Segment"),
        ("amplitude.com", "Amplitude"),
        ("heap-analytics", "Heap Analytics"),
        ("fullstory.com", "FullStory"),
    ]

    PRIVACY_FRIENDLY = [
        ("plausible.io", "Plausible"),
        ("fathom", "Fathom"),
        ("umami", "Umami"),
        ("simpleanalytics.com", "Simple Analytics"),
        ("goatcounter.com", "GoatCounter"),
        ("counter.dev", "Counter.dev"),
        ("pirsch.io", "Pirsch"),
        ("matomo", "Matomo"),
    ]

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        html_lower = resource.text.lower()

        trackers_found: list[str] = []
        privacy_friendly_found: list[str] = []

        for indicator, name in self.TRACKING_INDICATORS:
            if indicator in html_lower:
                trackers_found.append(name)

        for indicator, name in self.PRIVACY_FRIENDLY:
            if indicator in html_lower:
                privacy_friendly_found.append(name)

        details: list[str] = []

        if trackers_found:
            # Deduplicate
            trackers_found = list(dict.fromkeys(trackers_found))
            details.append(
                f"Tracking scripts detected: {', '.join(trackers_found)}."
            )

        if privacy_friendly_found:
            privacy_friendly_found = list(dict.fromkeys(privacy_friendly_found))
            details.append(
                f"Privacy-friendly analytics detected: {', '.join(privacy_friendly_found)}."
            )

        if trackers_found and not privacy_friendly_found:
            return self.warn_result(
                "Invasive tracking scripts detected without privacy-friendly alternatives.",
                details=details,
            )

        if trackers_found and privacy_friendly_found:
            return self.warn_result(
                "Both tracking scripts and privacy-friendly analytics detected.",
                details=details,
            )

        if privacy_friendly_found:
            return self.pass_result(
                f"Privacy-friendly analytics in use: {', '.join(privacy_friendly_found)}.",
            )

        return self.pass_result("No analytics scripts detected.")
