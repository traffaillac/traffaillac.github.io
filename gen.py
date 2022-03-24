# TODO :
# _ convert all sizes to em and reduce base size by 90%
# _ for Teaching, replace institutions by their logos

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
	On a personal note I am an avid hiker, cook, cyclist, and guitar player 🤘.
</p>
</div>
</div>'''
header_projects = '''\n\n\n<h1 id=projects style="box-shadow: inset 0 -50px 50px -50px #335c67">Projects</h1>'''
header_publications = '''\n\n\n<h1 id=publications style="box-shadow: inset 0 -50px 50px -50px #e09f3e; margin-top: 100px">Publications</h1>
<div class=references>'''
# FIXME je participe souvent à la rédaction des TDs
header_teaching = '''\n\n\n<h1 id=teaching style="box-shadow: inset 0 -50px 50px -50px #540b0e; margin-top: 100px">Teaching</h1>
<div class=courses>
	<h3><b>Period</b></h3>
	<h3><b>Course</b></h3>
	<h3><b>Level</b></h3>
	<h3><b>Institution</b></h3>
	<h3><b>Hours</b></h3>'''
header_duties = '''\n\n\n<h1 id=duties style="box-shadow: inset 0 -50px 50px -50px #ffd200; margin-top: 100px">Academic duties</h1>
<div class=duties>'''
header_misc = '''\n\n\n<h1 id=misc style="box-shadow: inset 0 -50px 50px -50px #9e2a2b; margin-top: 100px">Signs of life</h1>
<p style="margin: 20px 175px 15px 175px">
	This section contains stuff that doesn't fit anywhere else.
	I do a lot of challenges (with or without programming), to keep myself mentally fit and just have fun from time to time.
	My main platform for contests training is <a href=https://open.kattis.com/countries/FRA>Kattis</a>, where I hold 2<sup>nd</sup> place in France.
	I also share my solutions to training problems on <a href=https://github.com/traffaillac/traf-kattis>GitHub</a>.
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
	pos = randint(0, 330)
	for e in events:
		if e["type"] == 'project':
			h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
			period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
			bg = 'background-color: rgb(51, 92, 103, 0.15); ' if 'major' in e else ''
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<div{Id} class=card style="{bg}margin-left: {10+pos}px; margin-right: {340-pos}px">', file=f)
			print(f'\t<img src=images/{e["image"]}>', file=f)
			print('\t<div class=flexcolstretch>', file=f)
			print(f'\t\t<h3>{h3} ({period})</h3>', file=f)
			print(f'\t\t<h4>{e["text"]}</h4>', file=f)
			print('\t</div>', file=f)
			print('</div>', file=f)
			pos = (pos + randint(60, 270)) % 330
	# section Publications
	print(header_publications, file=f)
	for e in events:
		if e["type"] == 'publication':
			Id = f' id={e["id"]}' if "id" in e else ''
			bg = ' style="background-color: rgb(224, 159, 62, 0.15)"' if 'major' in e else ''
			print(f'\t<h3{Id}{bg}>{e["reference"]}</h3>', file=f)
			print(f'\t<h4{bg}>{e["text"]}</h4>', file=f)
	print('</div>', file=f)
	# section Teaching
	print(header_teaching, file=f)
	for e in events:
		if e["type"] == 'teaching':
			period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'\t<h4 style="text-align: center">{period}</h4>', file=f)
			print('\t<div>', file=f)
			print(f'\t\t<h4{Id}><b>{e["title"]} ({e["role"]})</b></h4>', file=f)
			print(f'\t\t<h4>{e["text"]}</h4>', file=f)
			print('\t</div>', file=f)
			print(f'\t<h4>{e["level"]}</h4>', file=f)
			print(f'\t<h4>{e["institution"]}</h4>', file=f)
			print(f'\t<h4 style="text-align: center">{e["hours"]}</h4>', file=f)
	print('</div>', file=f)
	# section Academic duties
	print(header_duties, file=f)
	for e in events:
		if e["type"] == 'duty':
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<h3{Id}>{e["text"]}</h3>', file=f)
	print('</div>', file=f)
	# section Signs of life
	print(header_misc, file=f)
	year = None
	for e in events:
		if e["type"] == 'misc':
			if e["finish"] != year:
				year = e["finish"]
				print(f'<h2 style="color: #ddd; margin-top: 25px; text-align: center">{year}</h2>', file=f)
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<div{Id} class=sign>', file=f)
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
				Id = f' id={e["id"]}' if "id" in e else ''
				print(f'<div{Id} class=strip>', file=f)
				period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
				if etype == 'project':
					h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
					print('\t<div class=project>project</div>', file=f)
					print(f'\t<img src=images/{e["image"]} width=300>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{h3} ({period})</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'publication':
					print('\t<div class=publication>publication</div>', file=f)
					print(f'\t<h3>{e["reference"]}</h3>', file=f)
					print(f'\t<h4>{e["text"]}</h4>', file=f)
				elif etype == 'teaching':
					print('\t<div class=teaching>teaching</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]} ({period})</h3>', file=f)
					print(f'\t\t<h4><i>{e["role"]}</i> at <i>{e["level"]}</i> level for <i>{e["hours"]}h</i> at <i>{e["institution"]}</i></h4>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'duty':
					print('\t<div class=duty>academic duty</div>', file=f)
					print(f'<h4>{e["text"]}</h4>', file=f)
				elif etype == 'misc':
					print('\t<div class=misc>sign of life</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]}</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				print('</div>', file=f)
	print(footer, file=f)
