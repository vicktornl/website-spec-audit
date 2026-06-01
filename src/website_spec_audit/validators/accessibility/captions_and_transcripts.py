from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class CaptionsAndTranscriptsValidator(BaseValidator):
    slug = "captions-and-transcripts"
    title = "Captions and transcripts"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/captions-and-transcripts/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        videos = doc.cssselect("video")
        audios = doc.cssselect("audio")

        if not videos and not audios:
            return self.pass_result("No <video> or <audio> elements found.")

        details: list[str] = []
        missing_tracks = 0

        for video in videos:
            tracks = video.cssselect("track")
            if not tracks:
                src = video.get("src", "(inline)")
                details.append(f'<video src="{src}"> has no <track> elements.')
                missing_tracks += 1
            else:
                details.append(
                    f"<video> has {len(tracks)} <track> element(s)."
                )

        for audio in audios:
            tracks = audio.cssselect("track")
            if not tracks:
                src = audio.get("src", "(inline)")
                details.append(f'<audio src="{src}"> has no <track> elements.')
                missing_tracks += 1
            else:
                details.append(
                    f"<audio> has {len(tracks)} <track> element(s)."
                )

        if missing_tracks:
            return self.warn_result(
                f"{missing_tracks} media element(s) missing <track> elements.",
                details=details,
            )

        return self.pass_result(
            "All media elements have <track> elements.",
        )
