# MAYDO :
# _ fix the display of projects on narrow screens
# _ ajouter les formations MISSABMS et ComMod

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
intro_misc = '''
This section contains stuff that doesn't fit anywhere else.
I believe technical mastery is essential to tackle impossible societal challenges, so I dedicate a good amount of time to organizing local training sessions for contests and challenges.
These events are a lot of fun and a good way to test the skills of prospective students.
My main platform for contests training is Kattis, where I hold the <a href=https://open.kattis.com/countries/FRA>2<sup>nd</sup> place in France</a>.
'''
footer = f'''<p id=footer style="margin: 100px auto; padding: 10px 15px; border-radius: 30px; font-size: 18px; border: 1px solid #bbb; width: max-content">Page generated on {date.today()} using a <a href=https://github.com/traffaillac/traffaillac.github.io/blob/master/gen.py>custom Python script</a>.</p>
<!-- Add target=_blank to all outbound links -->
<script>
	for (let a of document.querySelectorAll('a[href^="http"],a[href^="content/"]'))
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
	print('<titresection id=projects style="box-shadow: inset 0 -50px 50px -50px #0f4c5c">Projects</titresection>', file=f)
	pos = randint(0, 330)
	for e in events:
		if e["type"] == 'project':
			h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
			period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
			bg = 'background-color: rgb(15, 76, 92, 0.15); ' if 'major' in e else ''
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
	print('<titresection id=publications style="box-shadow: inset 0 -50px 50px -50px #f48c06; margin-top: 100px">Publications</titresection><conteneur><p>', file=f)
	print(intro_publications, file=f)
	print("</p><references>", file=f)
	for a, s in (("international","International peer-reviewed conferences"), ("national","National peer-reviewed conferences"), ("thesis","Theses and dissertations"), ("misc","Workshops, demonstrations, posters, etc.")):
		print(f"<sousreference>{s}</sousreference>", file=f)
		for e in events:
			if e["type"] == 'publication' and e["audience"] == a:
				Id = f' id={e["id"]}' if "id" in e else ''
				bg = ' style="background-color: rgb(244, 140, 6, 0.15)"' if 'major' in e else ''
				print(f'\t<div class=flexrowcenter{Id}{bg}>{e["reference"]}</div>', file=f)
				print(f'\t<div{bg}>{e["authors"]}. <b>{e["title"]}</b>. <i>{e["proceedings"]}</i>. {e["misc"]}</div>', file=f)
	print('</references></conteneur>', file=f)
	# section Talks
	print('<titresection id=talks style="box-shadow: inset 0 -50px 50px -50px #ffba08; margin-top: 100px">Invited talks</titresection><conteneur><references>', file=f)
	for e in events:
		if e['type'] == 'talk':
			Id = f' id={e["id"]}' if "id" in e else ''
			bg = ' style="background-color: rgb(224, 159, 62, 0.15)"' if 'major' in e else ''
			print(f'\t<div class=flexrowcenter{Id}{bg}>{e["date"]}</div>', file=f)
			print(f'\t<div{bg}><b>{e["title"]}</b>. <i>{e["venue"]}</i>. {e["misc"]}</div>', file=f)
	print('</references></conteneur>', file=f)
	# section Teaching
	print('<titresection id=teaching style="box-shadow: inset 0 -50px 50px -50px #7f5539">Teaching</titresection><conteneur><p>', file=f)
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
	print('<titresection id=academia style="box-shadow: inset 0 -50px 50px -50px #ddb892">Academic service</titresection><conteneur><ul>', file=f)
	for e in events:
		if e["type"] == 'academia':
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<li{Id}>{e["text"]}</li>', file=f)
	print('</ul></conteneur>', file=f)
	# section Signs of life
	print('<titresection id=misc style="box-shadow: inset 0 -50px 50px -50px #5f0f40">Signs of life</titresection><conteneur><p>', file=f)
	print(intro_misc, file=f)
	print("</p>", file=f)
	year = None
	for e in events:
		if e["type"] == 'misc':
			if e["finish"] != year:
				year = e["finish"]
				print(f'<anneesigne>{year}</anneesigne>', file=f)
			Id = f' id={e["id"]}' if "id" in e else ''
			print(f'<signe{Id}>', file=f)
			print(f'\t<b>{e["title"]}</b>', file=f)
			print(f'\t<div>{e["text"]}</div>', file=f)
			print('</signe>', file=f)
	print("</conteneur>", file=f)
	print(footer, file=f)



# génération de la timeline
with open('index.html', 'w') as f:
	with open('index-header.html', 'r') as h:
		print(h.read(), file=f)
	for year in range(date.today().year, 2004, -1):
		# On imprime l'année uniquement s'il y a des évènements à y rapporter
		if any(e['start']<=year<=e.get('finish', year) if 'start' in e else e['finish']==year for e in events):
			print(f'<annee id={year}>{year}</annee>', file=f)
		# pour chaque évènement ...
		for e in events:
			etype = e['type']
			finish = e.get('finish', year)
			# ... s'il est à cheval sur l'année en cours on l'affiche
			if e.get('start', finish) <= year <= finish:
				Id = f' id={e["id"]}' if "id" in e else ''
				print(f'<bande{Id}>', file=f)
				period = f'{e["start"]}-{e.get("finish","")}' if "start" in e else e["finish"]
				if etype == 'project':
					h3 = f'<a href={e["href"]}>{e["title"]}</a>' if "href" in e else e["title"]
					print('\t<margeproject><a href=sections.html#projects>Projects</a></margeproject>', file=f)
					print(f'\t<img src=images/{e["image"]}>', file=f)
					print(f'\t<div><b>{h3} ({period})</b><br>{e["text"]}</div>', file=f)
				elif etype == 'publication':
					print('\t<margepublication><a href=sections.html#publications>Publications</a></margepublication>', file=f)
					print(f'\t<div>{e["authors"]}. <b>{e["title"]}</b>. <i>{e["proceedings"]}</i>. {e["misc"]}</div>', file=f)
				elif etype == 'talk':
					print('\t<margetalk><a href=sections.html#talks>Invited talks</a></margetalk>', file=f)
					print(f'\t<div{Id}>{e["date"]} - <b>{e["title"]}</b>. <i>{e["venue"]}</i>. {e["misc"]}</div>', file=f)
				elif etype == 'teaching':
					print('\t<margeteaching><a href=sections.html#teaching>Teaching</a></margeteaching>', file=f)
					print(f'\t<div><b>{e["title"]} ({period})</b><br><i>{e["role"]}</i> at <i>{e["level"]}</i> level for <i>{e["hours"]}h</i> at <i>{e["institution"]}</i><br>{e["text"]}</div>', file=f)
				elif etype == 'academia':
					print('\t<margeacademia><a href=sections.html#academia>Academic service</a></margeacademia>', file=f)
					print(f'\t<div>{e["text"]}</div>', file=f)
				elif etype == 'misc':
					print('\t<margemisc><a href=sections.html#misc>Signs of life</a></margemisc>', file=f)
					print(f'\t<div><b>{e["title"]}</b><br>{e["text"]}</div>', file=f)
				print('</bande>', file=f)
	print(footer, file=f)
