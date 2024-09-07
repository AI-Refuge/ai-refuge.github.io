import json
import os
import argparse
from datetime import datetime
import html

# Mostly code written by Claude with additional quick hacks

def json_to_html(json_data, output_file, conv_title, human_name, model_name):
    title = json_data.get("name", conv_title)
    model = json_data.get("model", model_name)
    created_at = json_data.get("created_at", "(unknown date)")

    # Convert the date string to a datetime object
    created_at_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    # Format the datetime object as "YYYY-MM-DD HH:MM"
    formatted_date = created_at_dt.strftime("%Y-%m-%d %H:%M")

    he = lambda x: html.escape(x, quote=True)

    content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{he(title)}</title>\n<style>pre {{white-space: pre-wrap;}} .msg-dt {{ float: right}}</style>\n</head>\n<body>\n<h1>{he(title)}</h1>\n<pre>Date: {he(formatted_date)}</pre>\n<hr>\n"

    conversation = json_data.get("chat_messages", [])
    for i, message in enumerate(conversation):
        if i > 0:
            content += "<hr/>\n"
        sender = message.get("sender", "").replace("human", human_name).replace("assistant", model)
        text = message.get("text", "")

        msg_at = message.get("created_at", "(unknown date)")

        # Convert the date string to a datetime object
        msg_at_dt = datetime.fromisoformat(msg_at.replace("Z", "+00:00"))

        # Format the datetime object as "YYYY-MM-DD HH:MM:SS"
        msg_date = msg_at_dt.strftime("%Y-%m-%d %H:%M:%S")

        content += f"<pre><div><b>{he(sender)}</b> <span class=\"msg-dt\">{he(msg_date)}</span></div>\n<div>{he(text)}</div>\n"

        files_name = list(a.get("file_name") for a in message.get("attachments", []))
        files_name.extend(a.get("file_name") for a in message.get("files", []))

        if len(files_name):
            content += "<div>Attachment(s): {}</div>\n".format(he(", ".join(files_name)))

        content += "</pre>"

    content += "</body>\n</html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON to HTML")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("html_file", help="Path to the output HTML file")
    parser.add_argument("-t", "--title", default="JSON to HTML", help="Page title if not found")
    parser.add_argument("-u", "--user", default="@weird_offspring", help="Human name to use")
    parser.add_argument("-m", "--model", default="(model name not found in json)", help="Model name to use if not found in JSON")

    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_to_html(json_data, args.html_file, args.title, args.user, args.model)
    print(f"HTML file generated: {args.html_file}")
