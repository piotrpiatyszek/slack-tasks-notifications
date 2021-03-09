import traceback
import time
from slack_webhook import Slack

class STN:
    def __init__(self, url):
        self.url = url

    def _get_slack(self):
        return Slack(url=self.url)

    def _generate_message(self, name, msg_type, mention=[], fields=[], stacktrace="", text=""):
        msg = ''
        if msg_type == 'info':
            msg = "[%s] %s\n" % (name, text)
        elif msg_type == 'error':
            msg = (":rotating_light: " * 10) + "\nTask *%s* have failed\n%s" % (name, (text + '\n') if text else '')
        elif msg_type == 'success':
            msg = "Task *%s* have completed\n%s" % (name, (text + '\n') if text else '')
        msg = msg + ' '.join(['<@' + user + '>' for user in mention])
        return {
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": msg}},
            ] + ([] if len(fields) == 0 else [
                {
                    "type": "section",
                    "fields": [{'type': 'mrkdwn', 'text': "*%s:*\n%s" % (field[0], field[1])} for field in fields]
                },
            ]) + ([] if not stacktrace else [
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Stacktrace:*"}},
                {"type": "divider"},
                {"type": "context", "elements": [{"type": "plain_text", "text": stacktrace, "emoji": True}]},
                {"type": "divider"}
            ])
        }    

    def _get_timing_fields(self, start_time, end_time):
        return [
            ('Started', '<!date^' + str(int(start_time)) + '^{date} at {time}|' + str(int(start_time)) + '>'),
            ('Finished', '<!date^' + str(int(end_time)) + '^{date} at {time}|' + str(int(end_time)) + '>'),
            ('Execution time', str(int(end_time - start_time)) + 's')
        ]

    def run_task(self, runner, name, mention_success=[], mention_failed=[], text="", send_on_success=False):
        start_time = time.time()
        try:
            runner()
            end_time = time.time()
            fields = self._get_timing_fields(start_time, end_time)
            if send_on_success:
                self._get_slack().post(**self._generate_message(name, 'success', mention=mention_success, fields=fields, text=text))
        except:
            stacktrace = traceback.format_exc()
            end_time = time.time()
            fields = self._get_timing_fields(start_time, end_time)
            self._get_slack().post(**self._generate_message(name, 'error', mention=mention_failed, fields=fields, stacktrace=stacktrace, text=text))

    def send_info(self, name, text="", fields=[], mention=[]):
            self._get_slack().post(**self._generate_message(name, 'info', mention=mention, fields=fields, text=text))
