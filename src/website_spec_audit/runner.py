import asyncio

import httpx

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import AuditReport, CategoryResult, CheckResult, CheckStatus

CATEGORY_ORDER = [
    "foundations",
    "seo",
    "accessibility",
    "security",
    "well-known",
    "agent-readiness",
    "performance",
    "privacy",
    "resilience",
    "i18n",
]


class AuditRunner:
    def __init__(self, validators: list[BaseValidator], concurrency: int = 10):
        self.validators = validators
        self.concurrency = concurrency

    async def run(self, url: str) -> AuditReport:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
            headers={"User-Agent": "website-spec-audit/0.1.0"},
        ) as client:
            context = AuditContext(url=url, client=client)
            await context.fetch("/")

            semaphore = asyncio.Semaphore(self.concurrency)

            async def run_one(validator: BaseValidator) -> CheckResult:
                async with semaphore:
                    try:
                        return await validator.validate(context)
                    except Exception as exc:
                        return CheckResult(
                            topic=validator.meta,
                            check_status=CheckStatus.SKIP,
                            message=f"error: {exc}",
                        )

            results = await asyncio.gather(*[run_one(v) for v in self.validators])

        by_category: dict[str, list[CheckResult]] = {}
        for result in results:
            by_category.setdefault(result.topic.category, []).append(result)

        category_results = []
        for cat in CATEGORY_ORDER:
            if cat in by_category:
                category_results.append(CategoryResult(category=cat, results=by_category[cat]))

        return AuditReport(url=url, categories=category_results)
