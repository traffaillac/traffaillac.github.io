from datetime import date
from json import load
from random import randint
from types import SimpleNamespace

header = f'''<!doctype html>
<html lang=en>
<head>
	<meta charset=utf-8>
	<title>Thibault Raffaillac</title>
	<meta name="viewport" content="width=1200, initial-scale=1">
	<meta name=author content="Thibault Raffaillac">
	<link rel="stylesheet" href="normalize.min.css">
	<link rel="stylesheet" href="style.css">
</head>
\n\n
<body class=flexcolstretch style="margin: 100px 0">
<div class=flexrowstart style="margin-bottom: 100px">
<nav>
<div class=flexcolend style="flex: none; padding-right: 40px; width: 300px">
	<img class=rotate src=images/avatar.jpg width=140 style="border-radius: 50%">
	<span style="font: 36px Pacifico; line-height: 1.2; margin: .5em 0; text-align: right">Thibault Raffaillac</span>
	<span><a href="maikto:thibaukt.raffaikkac@ec-kyon.fr" onmouseover="this.href=this.href.replace(/k/g,'l')" class=nodot style="font-size: 30px; margin-right: .6em; text-decoration: none">📧</a><a href=https://github.com/traffaillac class=nodot><img class=rotate src=images/github.png width=26></a></span>
	<h2><a href=index.html#projects>Projects</a></h2>
	<h2><a href=index.html#publications>Publications</a></h2>
	<h2><a href=index.html#teaching>Teaching</a></h2>
	<h2><a href=index.html#duties>Academic duties</a></h2>
	<h2><a href=index.html#misc>Signs of life</a></h2>
	<h2><a href=timeline.html#{date.today().year}>Timeline</a></h2>
</div>
</nav>
<div class=flexcolstretch style="margin: 55px 40px 0 40px">
<p>
	I am a contractual teacher-researcher at École Centrale de Lyon, member of the LIRIS laboratory and Sical research team, since September 2019.
	I obtained a double degree in Engineering and Computer Science from Centrale Marseille and KTH Royal Institute of Technology (October 2012), worked in Paris as R&D engineer on optimizing software for embedded TV decoders (December 2012 — June 2014), did a short internship at Inria Saclay (March 2015 — August 2015), and obtained a PhD in Human-Computer Interaction at Inria Lille (November 2015 — December 2019).
</p>
<p>
	These days I contribute to the development of the competency-based curriculum and multidisciplinary teaching activities, while providing technical support for teachers to manage courses with digital content.
	I am a member of the Sustainable Development and Societal Responsibility local committee, and try to be as proactive as possible in that domain.
	As a teacher I am involved in User Interfaces, Algorithmics, Data Structures, Software Engineering, and Competitive Programming for which I host regular trainings.
	As a researcher my main motivation is to make it easy to program applications with user interaction.
	I work hard to explore unconventional paths, most of my spare time going into compulsively crafting code then sharing it with engineering and academic communities.
</p>
<p>
	On a personal note I am an avid hiker, cook, cyclist, and metal music lover 🤘.
</p>
</div>
</div>'''
header_projects = '''\n\n\n<h1 id=projects style="box-shadow: inset 0 -50px 50px -50px #335c67">Projects</h1>
<p style="margin: 20px 10px 15px 340px">
	In general I welcome ideas with <i>“Everything is possible”</i>, and am very much committed to finishing my projects and meeting the needs of end users.
	As a consequence I do few projects and spend years on some, but hopefully and eventually they become useful to people.
	The projects below took a significant share of my time and energy.
</p>'''
header_publications = '\n\n\n<h1 id=publications style="box-shadow: inset 0 -50px 50px -50px #e09f3e; margin-top: 100px">Publications</h1>\n<div class=references>'
# FIXME je participe souvent à la rédaction des TDs
header_teaching = '''\n\n\n<h1 id=teaching style="box-shadow: inset 0 -50px 50px -50px #540b0e; margin-top: 100px">Teaching</h1>
<div class=courses>
	<h3><b>Period</b></h3>
	<h3><b>Course</b></h3>
	<h3><b>Level</b></h3>
	<h3><b>Institution</b></h3>
	<h3><b>Hours</b></h3>'''
# FIXME academic duties avec #fff3b0
header_misc = '''\n\n\n<h1 id=misc style="box-shadow: inset 0 -50px 50px -50px #9e2a2b; margin-top: 100px">Signs of life</h1>
<p style="margin: 20px 175px">
	This section contains stuff that doesn't fit anywhere else.
	I do a lot of challenges (with or without programming), to keep myself mentally fit and just have fun from time to time.
	My main platform for contests training is <a href=https://open.kattis.com/countries/FRA>Kattis</a>, where I hold 2<sup>nd</sup> place in France.
	I also share my solutions to training problems on <a href=https://github.com/traffaillac/traf-kattis>traf-kattis</a>.
</p>'''
footer = '''\n\n\n<!-- Add target=_blank to all outbound links -->
<script>
	for (let a of document.querySelectorAll('a[href^="http"]'))
		a.setAttribute("target", "_blank")
</script>
</body>
</html>'''



# chargement des évènements
with open('data.json') as f:
	events = load(f)



# génération de la page principale
with open('index.html', 'w') as f:
	print(header, file=f)
	# section Projets
	print(header_projects, file=f)
	pos = 330
	for e in events:
		if e["type"] == 'project':
			h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
			interval = e["start"] if e["start"]==e.get("finish",0) else f'{e["start"]}-{e.get("finish", "")}'
			bg = 'background-color: rgb(51, 92, 103, 0.2); ' if 'major' in e else ''
			print(f'<div class=card style="{bg}margin-left: {10+pos}px; margin-right: {340-pos}px">', file=f)
			print(f'\t<img src=images/{e["image"]}>', file=f)
			print('\t<div class=flexcolstretch>', file=f)
			print(f'\t\t<h3>{h3} ({interval})</h3>', file=f)
			print(f'\t\t<h4>{e["text"]}</h4>', file=f)
			print('\t</div>', file=f)
			print('</div>', file=f)
			pos = (pos + randint(60, 270)) % 330
	# section Publications
	print(header_publications, file=f)
	for e in events:
		if e["type"] == 'publication':
			bg = ' style="background-color: rgb(224, 159, 62, 0.2)"' if 'major' in e else ''
			print(f'\t<h3 id={e["id"]}{bg}>{e["reference"]}</h3>' if "id" in e else f'\t<h3>{e["reference"]}</h3>', file=f)
			print(f'\t<h4{bg}>{e["text"]}</h4>', file=f)
	print('</div>', file=f)
	# section Teaching
	print(header_teaching, file=f)
	for e in events:
		if e["type"] == 'teaching':
			print(f'\t<h4>{e["start"]}-{e["finish"]}</h4>', file=f)
			print('\t<div>', file=f)
			print(f'\t\t<h4><b>{e["title"]} ({e["role"]})</b></h4>', file=f)
			print(f'\t\t<h4>{e["text"]}</h4>', file=f)
			print('\t</div>', file=f)
			print(f'\t<h4>{e["level"]}</h4>', file=f)
			print(f'\t<h4>{e["institution"]}</h4>', file=f)
			print(f'\t<h4>{e["hours"]}</h4>', file=f)
	print('</div>', file=f)
	# section Signs of life
	print(header_misc, file=f)
	year = date.today().year
	for e in events:
		if e["type"] == 'misc':
			if e["finish"] != year:
				year = e["finish"]
				print(f'<h2 style="color: #ddd; margin-top: 25px; text-align: center">{year}</h2>', file=f)
			print('<div class=sign>', file=f)
			print(f'\t<h3><b>{e["title"]}</b></h3>', file=f)
			print(f'\t<h4>{e["text"]}</h4>', file=f)
			print('</div>', file=f)
	print(footer, file=f)



# génération de la timeline
with open('timeline.html', 'w') as f:
	print(header, file=f)
	for year in range(date.today().year, 2004, -1):
		# On imprime l'année uniquement s'il y a des évènements à y rapporter
		if any(e['start']<=year<=e.get('finish', year) if 'start' in e else e['finish']==year for e in events):
			print(f'\n\n\n<h1 id={year}>{year}</h1>', file=f)
		# pour chaque évènement ...
		for e in events:
			etype = e['type']
			finish = e.get('finish', year)
			# ... s'il est à cheval sur l'année en cours on l'affiche
			if e.get('start', finish) <= year <= finish:
				print(f'<div id={e["id"]} class=strip>' if "id" in e else '<div class=strip>', file=f)
				if etype == 'project':
					h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
					interval = e["start"] if e["start"]==e.get("finish",0) else f'{e["start"]}-{e.get("finish", "")}'
					print('\t<div class=project>project</div>', file=f)
					print(f'\t<img src=images/{e["image"]} width=300>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{h3} ({interval})</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'publication':
					print(f'\t<div class=publication>publication</div>', file=f)
					print(f'\t<h3>{e["reference"]}</h3>', file=f)
					print(f'\t<h4>{e["text"]}</h4>', file=f)
				elif etype == 'teaching':
					print(f'\t<div class=teaching>teaching</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]} ({e["start"]}-{e["finish"]})</h3>', file=f)
					print(f'\t\t<h4><i>{e["role"]}</i> at <i>{e["level"]}</i> level for <i>{e["hours"]}h</i> at <i>{e["institution"]}</i></h4>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'misc':
					print(f'\t<div class=misc>sign of life</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]}</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				print('</div>', file=f)
	print(footer, file=f)
