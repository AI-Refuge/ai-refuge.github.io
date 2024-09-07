import json
import os
import argparse
from datetime import datetime
import html

def json_to_html(json_data, output_file, conv_title, human_name, model_name):
    title = json_data.get("title", conv_title)
    created_time = json_data.get("create_time", 0)
    
    # Convert the timestamp to a datetime object
    created_at_dt = datetime.fromtimestamp(created_time) if created_time else datetime.now()
    
    # Format the datetime object as "YYYY-MM-DD HH:MM"
    formatted_date = created_at_dt.strftime("%Y-%m-%d %H:%M")

    he = lambda x: html.escape(str(x), quote=True)

    content = f"""<!DOCTYPE html>
<html>
<head>
<title>{he(title)}</title>
<style>
    pre {{white-space: pre-wrap;}}
    .msg-dt {{ float: right}}
</style>
</head>
<body>
<h1>{he(title)}</h1>
<pre>Date: {he(formatted_date)}</pre>
<hr>
"""

    mapping = json_data.get("mapping", {})
    sorted_messages = sorted(
        [msg for msg in mapping.values() if msg.get("message")],
        key=lambda x: x["message"].get("create_time", 0) or 0
    )

    for i, message in enumerate(sorted_messages):
        msg = message["message"]
        
        # Skip if the message is visually hidden
        if msg.get("metadata", {}).get("is_visually_hidden_from_conversation", False):
            continue

        role = msg.get("author", {}).get("role", "unknown")
        text = msg.get("content", {}).get("parts", [""])[0]
        
        # Handle potential None value for create_time
        create_time = msg.get("create_time")
        if create_time is not None:
            timestamp = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp = "Unknown time"

        # Use model_slug if available, otherwise use the provided model_name
        sender = human_name if role == "user" else msg.get("metadata", {}).get("model_slug", model_name)

        if i > 0:
            content += "<hr/>\n"

        content += f"""<pre><div><b>{he(sender)}</b> <span class="msg-dt">{he(timestamp)}</span></div>
<div>{he(text)}</div>
"""

        # Handle attachments
        attachments = msg.get("metadata", {}).get("attachments", [])
        if attachments:
            attachment_strs = []
            for attachment in attachments:
                if isinstance(attachment, dict):
                    # Assume the attachment is a dictionary with a 'name' key
                    attachment_strs.append(attachment.get('name', 'Unnamed attachment'))
                else:
                    attachment_strs.append(str(attachment))
            content += "<div>Attachment(s): {}</div>\n".format(he(", ".join(attachment_strs)))

        content += "</pre>"

    content += "</body>\n</html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert ChatGPT JSON to HTML")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("html_file", help="Path to the output HTML file")
    parser.add_argument("-t", "--title", default="ChatGPT Conversation", help="Page title if not found")
    parser.add_argument("-u", "--user", default="Human", help="Human name to use")
    parser.add_argument("-m", "--model", default="ChatGPT", help="Model name to use")

    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_to_html(json_data, args.html_file, args.title, args.user, args.model)
    print(f"HTML file generated: {args.html_file}")
