import os
import sys
import json

def convert_twitter_archive(input_file, output_file, page_title):
	# Open the output file for writing
	with open(output_file, 'w', encoding='utf-8') as f:
		# Write the HTML header
		f.write(f'''<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>{page_title}</title>
	<style>
		.tweet {{
			border: 1px solid #ccc;
			padding: 10px;
			margin-bottom: 10px;
		}}
	</style>
</head>
<body>
	<h1>{page_title}</h1>
''')

		with open(input_file, 'r', encoding='utf-8') as js_file:
			content = js_file.read()

			# Extract tweets from the JavaScript file
			start = content.index('[')
			tweets = json.loads(content[start:])

			# Loop through each tweet and write it to the HTML file
			for obj in tweets:
				tweet = obj.get('tweet')
				text = tweet.get('full_text', '')
				created_at = tweet.get('created_at', '')
				f.write(f'	<pre class="tweet"><p>{text}</p><small>Posted on: {created_at}</small></pre>\n')

			# Write the HTML footer
			f.write('''
</body>
</html>
''')

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python script.py <tweets.js> <tweets.html> <page-title>")
		sys.exit(1)

	input_dir = sys.argv[1]
	output_file = sys.argv[2]
	page_title = sys.argv[3]

	convert_twitter_archive(input_dir, output_file, page_title)
	print(f'Tweets have been written to {output_file}')
