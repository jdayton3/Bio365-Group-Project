import json
import os, shutil


def get_sidebar(sections):
    links = []
    for section in sections:
        links.append('<a href="/Bio365-Group-Project/html/{1}.html">{0}</a>'.format(section[0], section[1]))
    return '''
    <div id="sidebar">
        {}
    </div>
    '''.format('\n'.join(links))


def get_content(content_list):
    html = []
    for content in content_list:
        if isinstance(content, unicode):
            html.append('<p>{}</p>'.format(content))
        else:
            if 'video' in content:
                html.append('''
                <div class="video">
                    <iframe width = "560" height = "315" src = "{}" frameborder = "0" allowfullscreen ></iframe >
                </div>'''.format(content["video"]))
            elif 'picture' in content:
                html.append('''<div class="picture">
                    <img src="../pics/{}">
                </div>'''.format(content["picture"]))
    return '\n'.join(html)


def get_footer(prev_page, next_page):
    if prev_page is not None:
        prev_page += 1
    if next_page:
        next_page += 1

    def get_button_html(id, text, page_num):
        if page_num:
            return '''
                <button id="{0}" onclick="location.href='/Bio365-Group-Project/html/{2}.html'">{1}</button>
            '''.format(id, text, page_num)
        else:
            return ''

    prev = get_button_html('prev', 'Prev', prev_page)
    next = get_button_html('next', 'Next', next_page)

    return '''
    <footer>
        {prev}
        {next}
    </footer>
    '''.format(prev=prev, next=next)


def generate_html(sections, page, prev, next):
    sidebar_html = get_sidebar(sections)
    footer_html = get_footer(prev, next)
    content_html = get_content(page["content"])
    title = page["title"]
    return '''
<html>
	<head>
		<title>Bioinformatics</title>
		<link rel="stylesheet" href="../site.css">
	</head>
	<body>
		{sidebar}
		<div id="main">
			<div id="content">
				<h1>{title}</h1>
				{content}
			</div>
			{footer}
		</div>
	</body>
</html>
'''.format(sidebar=sidebar_html, title=title, content=content_html, footer = footer_html)


def delete_prev_html():
    folder = os.getcwd() + '/html'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def save_html_file(html, num):
    file = open('html/{}.html'.format(num), 'w')
    file.write(html)
    file.close()


delete_prev_html()


# open pages.json file
with open('pages.json') as file:
    dict = json.load(file)
    pages = dict["pages"]
    sections = []
    section_set = set()
    for i, page in enumerate(pages):
        if page["section"] not in section_set:
            section_set.add(page["section"])
            sections.append((page["section"], i + 1))

    for i, page in enumerate(pages):
        prev = i - 1 if i != 0 else None
        next = i + 1 if i != len(pages) - 1 else None
        html = generate_html(sections, page, prev, next)
        save_html_file(html, i + 1)