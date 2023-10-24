# MAYDO :
# _ for Teaching, replace institutions by their logos
# _ générer le cv également à partir des données
# _ Adapter data.json à partir du CV de qualification
# _ nouvelle photo
# _ Refaire le layout avec les tailles de police
# _ illustrer les publications avec des images
# _ seuls les liens # n'ouvrent pas de nouvel onglet
# _ fix the display of projects on narrow screens

from datetime import date
from json import load
from random import randint
from types import SimpleNamespace


intro_teaching = '''
I really enjoy teaching and innovative educational activities.
In 2019 at Centrale Lyon I volunteered to develop the software for an innovative week-long educational event held several times a year, the <a href=https://youtu.be/FeiMQfe_QVU?t=59>WEEX éolienne</a>.
Then in 2020 I developed a website to display individual skills assessments as part of the implementation of the Competency-Based Education at Centrale Lyon.
I have also organized competitive programming trainings since 2015, in Lille, Lyon and Montpellier, and gave advanced courses on the topic.
In 2021 we raised Centrale Lyon to the <a href=https://open.kattis.com/countries/FRA>top rank</a> among the French institutions on the international training platform Kattis, reached the <a href=https://www.codingame.com/contests/escape/fall-challenge-2021>4<sup>th</sup> place</a> at CodinGame Fall Challenge 2021, then got the <a href=https://judge.swerc.eu/public>54<sup>th</sup> and 64<sup>th</sup> places</a> at the major European competition SWERC 2021.
'''
intro_publications = '''
My research in HCI has focused mainly on reducing complexity when programming interactive systems.
In the case of graphical interfaces, this complexity is due to the large number of objects and behaviors to manage, and I have proposed models [<a href=#EICS19>EICS'19</a>, <a href=#EICS17>EICS'17</a>] and principles [<a href=#EICS22>EICS'22</a>] to give more concise mental representations.
In the case of data structures, this complexity is due to the abstraction effort required to navigate between visual representation and code, and I have initiated a tool allowing to work directly on visual graphs [<a href=#EIAH21>EIAH'21</a>].
Finally, in the case of compilers, the complexity is due to the numerous transformations that lead from the source code to the executable file, and I explored the idea of a human-compiler communication to improve its understanding [<a href=#PPIG12>PPIG'12</a>].
'''
header_academia = '''\n\n\n<h1 id=academia style="box-shadow: inset 0 -50px 50px -50px #ffd200; margin-top: 100px">Academic service</h1>
<div class=academic>'''
header_misc = '''\n\n\n<h1 id=misc style="box-shadow: inset 0 -50px 50px -50px #9e2a2b; margin-top: 100px">Signs of life</h1>
<p style="margin: 20px 175px 15px 175px">
	This section contains stuff that doesn't fit anywhere else.
	I believe technical mastery is essential to tackle impossible societal challenges, so I dedicate a good amount of time to organizing local training sessions for contests and challenges.
	These events are a lot of fun and a good way to test the skills of prospective students.
	My main platform for contests training is Kattis, where I hold the <a href=https://open.kattis.com/countries/FRA>2<sup>nd</sup> place in France</a>.
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
	with open('index-header.html', 'r') as h:
		print(h.read(), file=f)
	# section Projets
	print('<titresection id=projects style="box-shadow: inset 0 -50px 50px -50px #335c67">Projects</titresection>', file=f)
	pos = randint(0, 330)
	for e in events:
		if e["type"] == 'project':
			h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
			period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
			bg = 'background-color: rgb(51, 92, 103, 0.15); ' if 'major' in e else ''
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<projet{Id} style="{bg}margin-left: {10+pos}px; margin-right: {340-pos}px">', file=f)
			print(f'\t<img src=images/{e["image"]}>', file=f)
			print('\t<div class=flexcolstretch>', file=f)
			print(f'\t\t<b>{h3} ({period})</b>', file=f)
			print(f'\t\t<div>{e["text"]}</div>', file=f)
			print('\t</div>', file=f)
			print('</projet>', file=f)
			pos = (pos + randint(60, 270)) % 330
	# section Publications
	print('<titresection id=publications style="box-shadow: inset 0 -50px 50px -50px #e09f3e; margin-top: 100px">Publications</titresection><conteneur><p>', file=f)
	print(intro_publications, file=f)
	print("</p><references>", file=f)
	for a, s in (("international","International peer-reviewed conferences"), ("national","National peer-reviewed conferences"), ("abstract","Works in progress, extended abstracts and posters"), ("thesis","Theses and dissertations")):
		print(f"<sousreference>{s}</sousreference>", file=f)
		for e in events:
			if e["type"] == 'publication' and e["audience"] == a:
				Id = f' id={e["id"]}' if "id" in e else ''
				bg = ' style="background-color: rgb(224, 159, 62, 0.15)"' if 'major' in e else ''
				print(f'\t<div class=flexrowcenter{Id}{bg}>{e["reference"]}</div>', file=f)
				print(f'\t<div{bg}>{e["authors"]}. <b>{e["title"]}</b>. <i>{e["proceedings"]}</i>. {e["misc"]}</div>', file=f)
	print('</references></conteneur>', file=f)
	# section Teaching
	print('<titresection id=teaching style="box-shadow: inset 0 -50px 50px -50px #540b0e">Teaching</titresection><conteneur><p>', file=f)
	print(intro_teaching, file=f)
	print("</p><cours><b>Period</b><b>Course</b><b>Level</b><b>Institution</b><b>Hours</b>", file=f)
	for e in events:
		if e["type"] == 'teaching':
			period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'\t<center>{period}</center>', file=f)
			print('\t<div class=flexcolstretch>', file=f)
			print(f'\t\t<b{Id}>{e["title"]} ({e["role"]})</b>', file=f)
			print(f'\t\t<div>{e["text"]}</div>', file=f)
			print('\t</div>', file=f)
			print(f'\t<div>{e["level"]}</div>', file=f)
			print(f'\t<div>{e["institution"]}</div>', file=f)
			print(f'\t<center>{e["hours"]}</center>', file=f)
	print('</cours></conteneur>', file=f)
	# section Academic service
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
	with open('index-header.html', 'r') as h:
		print(h.read(), file=f)
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
					print('\t<div class=engineering>Projects</div>', file=f)
					print(f'\t<img src=images/{e["image"]} width=300>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{h3} ({period})</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'publication':
					print('\t<div class=publication>Publications</div>', file=f)
					print(f'\t<h3>{e["reference"]}</h3>', file=f)
					print(f'\t<h4{bg}>{e["authors"]}. {e["title"]}. <i>{e["proceedings"]}</i>. {e["misc"]}</h4>', file=f)
				elif etype == 'teaching':
					print('\t<div class=teaching>Teaching</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]} ({period})</h3>', file=f)
					print(f'\t\t<h4><i>{e["role"]}</i> at <i>{e["level"]}</i> level for <i>{e["hours"]}h</i> at <i>{e["institution"]}</i></h4>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				elif etype == 'academia':
					print('\t<div class=academia>Academic service</div>', file=f)
					print(f'<h4>{e["text"]}</h4>', file=f)
				elif etype == 'misc':
					print('\t<div class=misc>Signs of life</div>', file=f)
					print('\t<div class=flexcolstretch style="justify-content: center">', file=f)
					print(f'\t\t<h3>{e["title"]}</h3>', file=f)
					print(f'\t\t<h4>{e["text"]}</h4>', file=f)
					print('\t</div>', file=f)
				print('</div>', file=f)
	print(footer, file=f)
