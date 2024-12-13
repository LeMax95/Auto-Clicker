# modules/report_writer.py
from datetime import datetime

class ReportWriter:
    def __init__(self, detailed_report_path, summary_report_path):
        self.detailed_report_path = detailed_report_path
        self.summary_report_path = summary_report_path
        self.summary_report = {}

    def write_detailed_report(self, target_link, keyword, success, stay_time, rank):
        with open(self.detailed_report_path, 'a') as file:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now}] Link: {target_link}, Keyword: {keyword}, Success: {success}, Rank: {rank}, Stay time: {stay_time:.2f} seconds\n")

    def update_summary_report(self, target_link, keyword):
        key = (target_link, keyword)
        self.summary_report[key] = self.summary_report.get(key, 0) + 1
        with open(self.summary_report_path, 'w') as file:
            file.write("Link, Keyword, Total Clicks\n")
            for (link, kw), count in self.summary_report.items():
                file.write(f"{link}, {kw}, {count}\n")
