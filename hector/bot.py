import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone

from .client import APIClient
from .models import DiffCoverageReport, CovReport


logging.basicConfig(level=logging.DEBUG)


class CoverageBot:
    def __init__(self, cov: CovReport, diff_cov: DiffCoverageReport):
        self.diff_cov = diff_cov
        self.cov = cov
        self.client = APIClient()

    def get_comment(self):
        return self._format_comment()

    def _format_comment(self):
        comment = ""

        overall_coverage = self.cov.overall_coverage

        diff_coverage = self.diff_cov.diff_coverage
        lines_covered = self.diff_cov.lines_covered
        lines_missed = self.diff_cov.lines_missed

        # add title
        emoji = self._title_emoji()
        comment += f"## 📈 Diff Coverage {diff_coverage:.2f}% {emoji} \n\n"
        # add subtitle
        comment += f"##### Overall Coverage {overall_coverage:.2f}% | Covered Lines {lines_covered} | Missing {lines_missed} \n\n"

        # add file stats
        comment += "📂 Impacted Files \n\n"
        file_stats = self._format_file_stats()
        comment += file_stats

        # add footer
        commit_link = self._format_commit_link()
        timestamp = self.timestamp()
        comment += f"###### 📝 Reported on commit {commit_link} | {timestamp})"
        return comment

    def _title_emoji(self):
        if (
            os.environ.get("BITBUCKET_EXIT_CODE")
            and int(os.environ.get("BITBUCKET_EXIT_CODE")) != 0
        ):
            return "❗️"
        return "✅"

    def _format_file_stats(self):
        src_stats = self.diff_cov.src_stats
        file_stats = ["sh"]
        for file, stat in src_stats.items():
            if stat["percent_covered"] < 100:
                file_stat = f"❗️ {stat['percent_covered']:5.2f}% | {file} {self.__convert_to_ranges(stat['violation_lines'])}"
                logging.info(file_stat)
                file_stats.append(file_stat)
        file_stats_len = len(file_stats)
        if file_stats_len > 10:
            file_stats = file_stats[:10]
        file_stats.append("")
        step_link = f"https://bitbucket.org/{os.environ.get('BITBUCKET_WORKSPACE')}/{os.environ.get('BITBUCKET_REPO_SLUG')}/pipelines/results/{os.environ.get('BITBUCKET_PIPELINE_UUID')}/steps/{os.environ.get('BITBUCKET_STEP_UUID')}"
        if file_stats_len > 10:
            file_stats.append(
                f"> _{file_stats_len - 10}_ more files [Full Coverage Report]({step_link}) \n\n"
            )
        else:
            file_stats.append(f"> Check [Full Coverage Report]({step_link}) \n\n")
        return "\n".join(file_stats)

    def _format_commit_link(self):
        commit_link = f"https://bitbucket.org/{os.environ.get('BITBUCKET_WORKSPACE')}/{os.environ.get('BITBUCKET_REPO_SLUG')}/commits/{os.environ.get('BITBUCKET_COMMIT')}"
        commit_link = f"[{commit_link}]({commit_link})"
        commit_link += "{: data-inline-card='' }"
        return commit_link

    def timestamp(self):
        return datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
            "%I:%M %p %Z, %A, %d %B %Y"
        )

    def post_comment(self, comment: str):
        repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")
        pr_id = os.environ.get("BITBUCKET_PR_ID")
        url = f"https://api.bitbucket.org/2.0/repositories/{os.environ.get('BITBUCKET_WORKSPACE')}/{repo_slug}/pullrequests/{pr_id}/comments"
        logging.debug(url)
        headers = {
            "Authorization": f"Bearer {os.environ.get('TEST_COVERAGE_TOKEN')}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = json.dumps({"content": {"raw": comment}})
        resp = self.client.post(url, headers=headers, data=payload)
        logging.debug(resp.status_code)
        logging.debug(resp.json())

    @staticmethod
    def __convert_to_ranges(lst: list):
        if not lst:
            return ""
        ranges = []
        start = end = lst[0]
        for num in lst[1:]:
            if num == end + 1:
                end = num
            else:
                ranges.append(f"{start}-{end}" if start != end else str(start))
                start = end = num
        ranges.append(f"{start}-{end}" if start != end else str(start))
        return ", ".join(ranges)


if __name__ == "__main__":
    with open("diff-coverage.json", encoding="utf-8") as f:
        diff_cov = DiffCoverageReport(**json.load(f))

    with open("coverage.json", encoding="utf-8") as f:
        cov = CovReport(**json.load(f))

    bot = CoverageBot(cov=cov, diff_cov=diff_cov)

    bot_comment = bot.get_comment()
    logging.info(bot_comment)
    bot.post_comment(comment=bot_comment)
