import json
import argparse
from datetime import datetime
import html
import re

def parse_gemini_json(json_data):
    # Extract messages from the nested structure
    messages = []
    for item in json_data:
        if isinstance(item, list) and len(item) > 1:
            dt = datetime.fromtimestamp(item[4][0]).strftime("%Y-%m-%d %H:%M")

            messages.append({
                "sender": "human",
                "text": item[2][0][0],
                "dt": dt
            })

            messages.append({
                "sender": "assistant",
                "text": item[3][0][0][1][0],
                "dt": dt
            })

    return messages


def json_to_html(json_data, output_file, conv_title, human_name, model_name):
    title = conv_title
    model = model_name
    formatted_date = json_data[0]["dt"]

    he = lambda x: html.escape(x, quote=True)

    content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{he(title)}</title>\n<style>pre {{white-space: pre-wrap;}} .msg-dt {{ float: right}}</style>\n</head>\n<body>\n<h1>{he(title)}</h1>\n<pre>Date: {he(formatted_date)}</pre>\n<hr>\n"

    for i, message in enumerate(json_data):
        if i > 0:
            content += "<hr/>\n"
        sender = message.get("sender", "").replace("human", human_name).replace("assistant", model)
        text = message.get("text", "")
        msg_date = message.get("dt", "(unknown date)")

        content += f"<pre><div><b>{he(sender)}</b> <span class=\"msg-dt\">{he(msg_date)}</span></div>\n<div>{he(text)}</div>\n"

        # FIXME: how to handle attachement?

        content += "</pre>"

    content += "</body>\n</html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Gemini JSON to HTML")
    parser.add_argument("json_file", help="Path to the Gemini JSON file")
    parser.add_argument("html_file", help="Path to the output HTML file")
    parser.add_argument("-t", "--title", default="Gemini Conversation??", help="Page title")
    parser.add_argument("-p", "--partner", default="<unknown partner name>", help="Partner name")
    parser.add_argument("-m", "--model", default="<unknown model name>", help="Model name")

    args = parser.parse_args()
    conv_title = None

    with open(args.json_file, "r", encoding="utf-8") as f:
        for i in f:
            # try to find the first line that contains json data
            if i[0] == '[':
                x = json.loads(i)
                x = json.loads(x[0][2])[0]
                json_data = x[1]
                title_data = x[2]
                conv_title = title_data[1]
                # ~ exit()
                break

    messages = parse_gemini_json(json_data)
    json_to_html(messages, args.html_file, conv_title or args.title, args.partner, args.model)
    print(f"HTML file generated: {args.html_file}")
