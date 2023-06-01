# MAYDO :
# _ for Teaching, replace institutions by their logos
# _ générer le cv également à partir des données
# _ research assistant for ECL

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
	<span><a href="maikto:thibaukt.raffaikkac@ec-kyon.fr" onmouseover="this.href=this.href.replace(/k/g,'l')" class=nodot style="font: 26px Pacifico; margin-right: .6em; text-decoration: none">email contact</a><a href=https://github.com/traffaillac class=nodot><img class=rotate src=images/github.png width=26></a></span>
	<h2><a href=index.html#{date.today().year}>Timeline</a></h2>
	<h2><a href=sections.html#engineering>Engineering</a></h2>
	<h2><a href=sections.html#publications>Publications</a></h2>
	<h2><a href=sections.html#teaching>Teaching</a></h2>
	<h2><a href=sections.html#academia>Service & Awards</a></h2>
	<h2><a href=sections.html#misc>Signs of life</a></h2>
</div>
</nav>
<div class=flexcolstretch style="margin: 20px 40px 0 40px">
<p>
	I am a postdoctoral researcher at INRAE and CIRAD in Montpellier, member of research units <a href=https://umr-sens.fr/>SENS</a> and <a href=https://umr-selmet.cirad.fr/>SELMET</a> since September 2022.
	In the past I :
</p>
<ul>
	<li>worked as teacher, researcher and engineer at École Centrale de Lyon (September 2019 – September 2022).</li>
	<li>did a PhD in Human-Computer Interaction supervised by <a href=https://loki.lille.inria.fr/~huot/>Stéphane Huot</a> at Inria Lille (November 2015 – December 2019).</li>
	<li>did a short internship at Inria Saclay (March 2015 – August 2015).</li>
	<li>worked as R&D engineer in Paris on optimizing software for embedded TV decoders (December 2012 – June 2014).</li>
	<li>did a double degree in Engineering and Computer Science from Centrale Marseille and KTH Royal Institute of Technology (September 2008 – October 2012).</li>
</ul>
<p>
	My research field is Human-Computer Interaction.
	I currently work on designing graphical interfaces atop agent-based simulations, to explore possible futures in the management of pastoral territories.
	In parallel I work on the interactions between researchers and engineers of UI frameworks, to improve the impact of research on the evolution of frameworks.
	I have been a member of the Sustainable Development and Societal Responsibility committee at Centrale Lyon, and am very much driven by that domain.
	As a teacher I have given courses on User Interfaces and Competitive Programming, and have been assistant in Algorithmics, Software Engineering and Web Development.
	I work hard to explore unconventional paths, most of my spare time going into compulsively crafting code then sharing it with engineering and academic communities.
</p>
<p>
	On a personal note I am a passionate hiker, cook, cyclist, and musician ♫.
</p>
</div>
</div>'''
header_engineering = '''\n\n\n<h1 id=engineering style="box-shadow: inset 0 -50px 50px -50px #335c67">Engineering</h1>'''
header_publications = '''\n\n\n<h1 id=publications style="box-shadow: inset 0 -50px 50px -50px #e09f3e; margin-top: 100px">Publications</h1>
<p style="margin: 30px 175px 30px 175px">
	My research focuses mainly on reducing complexity when programming interactive systems.
	In the case of graphical interfaces, this complexity is due to the large number of objects and behaviors to manage, and I have proposed models [<a href=#EICS19>EICS'19</a>, <a href=#EICS17>EICS'17</a>] and principles [<a href=#EICS22>EICS'22</a>] to give more concise mental representations.
	In the case of data structures, this complexity is due to the abstraction effort required to navigate between visual representation and code, and I have initiated a tool allowing to work directly on visual graphs [<a href=#EIAH21>EIAH'21</a>].
	Finally, in the case of compilers, the complexity is due to the numerous transformations that lead from the source code to the executable file, and I explored the idea of a human-compiler communication to improve its understanding [<a href=#PPIG12>PPIG'12</a>].
</p>
<div class=references>'''
# FIXME je participe souvent à la rédaction des TDs
header_teaching = '''\n\n\n<h1 id=teaching style="box-shadow: inset 0 -50px 50px -50px #540b0e; margin-top: 100px">Teaching</h1>
<p style="margin: 30px 175px 30px 175px">
	I really enjoy teaching and supervision activities.
	Aside from courses, I have provided assistance to pedagogical innovation, co-organizing 5 editions of an interdisciplinary weekly challenge, and developing a Web site supporting the competency-based evaluations at Centrale Lyon.
	I have also been hosting Competitive Programming trainings since 2015, first in University of Lille then at Centrale Lyon, for which I have given and refined advanced courses on the topic.
	In 2021 we raised Centrale Lyon to the top rank among the French institutions on <a href=https://open.kattis.com/countries/FRA>Kattis</a>, reached the 4<sup>th</sup> place during the <a href=https://www.codingame.com/contests/escape/fall-challenge-2021>CodinGame Fall Challenge</a>, then got 54<sup>th</sup> and 64<sup>th</sup> places at the major European competition <a href=https://judge.swerc.eu/public>SWERC</a>.
</p>
<div class=courses>
	<h3><b>Period</b></h3>
	<h3><b>Course</b></h3>
	<h3><b>Level</b></h3>
	<h3><b>Institution</b></h3>
	<h3><b>Hours</b></h3>'''
header_academia = '''\n\n\n<h1 id=academia style="box-shadow: inset 0 -50px 50px -50px #ffd200; margin-top: 100px">Service & Awards</h1>
<div class=academic>'''
header_misc = '''\n\n\n<h1 id=misc style="box-shadow: inset 0 -50px 50px -50px #9e2a2b; margin-top: 100px">Signs of life</h1>
<p style="margin: 20px 175px 15px 175px">
	This section contains stuff that doesn't fit anywhere else (mostly challenges).
	I believe technical mastery is essential to tackle impossible societal challenges, so I dedicate about 5% of my time to organizing local training sessions for contests and challenges.
	These events are a lot of fun and a good way to test the skills of prospective students.
	My main platform for contests training is Kattis, where I hold <a href=https://open.kattis.com/countries/FRA>4<sup>th</sup> place in France</a>.
</p>'''
footer = f'''\n\n\n<p id=footer>Page generated on {date.today()} using a <a href=https://github.com/traffaillac/traffaillac.github.io/blob/master/gen.py>custom Python script</a>.</p>
<!-- Add target=_blank to all outbound links -->
<script>
	for (let a of document.querySelectorAll('a[href^="http"]'))
		a.setAttribute("target", "_blank")
</script>
</body>
</html>'''



# chargement des évènements
with open('data.json') as f:
	events = load(f)



# génération de la page classée par sections
with open('sections.html', 'w') as f:
	print(header, file=f)
	# section Projets
	print(header_engineering, file=f)
	pos = randint(0, 330)
	for e in events:
		if e["type"] == 'engineering':
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
			print(f'\t<h4{bg}>{e["authors"]}. <b>{e["title"]}</b>. <i>{e["proceedings"]}</i>. {e["misc"]}</h4>', file=f)
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
	# section Service & Awards
	print(header_academia, file=f)
	for e in events:
		if e["type"] == 'academia':
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
with open('index.html', 'w') as f:
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
				if etype == 'engineering':
					h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
					print('\t<div class=engineering>engineering</div>', file=f)
					print(f'\t<img src=images/{e["image"]} width=300>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{h3} ({period})</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'publication':
					print('\t<div class=publication>publication</div>', file=f)
					print(f'\t<h3>{e["reference"]}</h3>', file=f)
					print(f'\t<h4{bg}>{e["authors"]}. <b>{e["title"]}</b>. <i>{e["proceedings"]}</i>. {e["misc"]}</h4>', file=f)
				elif etype == 'teaching':
					print('\t<div class=teaching>teaching</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]} ({period})</h3>', file=f)
					print(f'\t\t<h4><i>{e["role"]}</i> at <i>{e["level"]}</i> level for <i>{e["hours"]}h</i> at <i>{e["institution"]}</i></h4>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'academia':
					print('\t<div class=academia>academic</div>', file=f)
					print(f'<h4>{e["text"]}</h4>', file=f)
				elif etype == 'misc':
					print('\t<div class=misc>sign of life</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]}</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				print('</div>', file=f)
	print(footer, file=f)
