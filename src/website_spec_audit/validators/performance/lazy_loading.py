from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LazyLoadingValidator(BaseValidator):
    slug = "lazy-loading"
    title = "Lazy loading images, iframes, and video"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/lazy-loading/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        images = list(doc.iter("img"))
        iframes = list(doc.iter("iframe"))

        if not images and not iframes:
            return self.pass_result("No <img> or <iframe> tags found on the page.")

        issues: list[str] = []
        details: list[str] = []
        lazy_img_count = 0
        lazy_iframe_count = 0

        for idx, img in enumerate(images):
            loading = (img.get("loading") or "").lower()
            src = img.get("src", "")

            if idx == 0 and loading == "lazy":
                issues.append(
                    f"First/hero image has loading=\"lazy\" which may hurt LCP: {src}"
                )

            if idx > 0 and loading == "lazy":
                lazy_img_count += 1

        for iframe in iframes:
            loading = (iframe.get("loading") or "").lower()
            if loading == "lazy":
                lazy_iframe_count += 1

        non_first_images = max(0, len(images) - 1)
        imgs_without_lazy = non_first_images - lazy_img_count
        iframes_without_lazy = len(iframes) - lazy_iframe_count

        if imgs_without_lazy > 0:
            details.append(
                f"{imgs_without_lazy} below-the-fold image(s) missing loading=\"lazy\"."
            )
        if iframes_without_lazy > 0:
            details.append(
                f"{iframes_without_lazy} iframe(s) missing loading=\"lazy\"."
            )

        all_details = issues + details

        if issues:
            return self.warn_result(
                "Lazy loading issues detected.",
                details=all_details,
            )

        if details:
            return self.warn_result(
                "Some resources could benefit from lazy loading.",
                details=all_details,
            )

        return self.pass_result(
            "Lazy loading is properly applied to below-the-fold images and iframes."
        )
