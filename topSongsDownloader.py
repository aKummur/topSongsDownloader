import urllib2
from difflib import SequenceMatcher as sm
import os

def parse(lang):
	response = urllib2.urlopen('http://www.radiomirchi.com/more/' + lang)
	htmlsrc = response.read()
	
	htmlsrc = htmlsrc.split('<article', 1)[1]
	articles = htmlsrc.split('</article>')

	songs=[]
	for article in articles:
		try:
			songs.append((article.split('<h2>')[1].split('</h2>', 1)[0], article.split('<h3>')[1].split('<br>', 1)[0]))
		except:
			pass

	return songs

def download(link, song, directory):
	try:
		htmlsrc = urllib2.urlopen(link).read()
		downlink = htmlsrc.split('itemprop="name">' + song, 1)[1].split('itemprop="audio" href="', 1)[1].split('">', 1)[0]
		print downlink

		if not os.path.exists(directory):
			os.makedirs(directory)

		f = open(os.path.join(directory, song+'.mp3'), 'w')
		f.write(urllib2.urlopen(downlink).read())
		f.close()

	except Exception,e:
		print str(e)

def downloader(songs, lang):
	for song, album in songs:
		print 'http://music.vidmate.mobi/search-' + song.strip().replace(' ', '%20') + '%20' + album.strip().replace(' ', '%20') + '.html'
		response = urllib2.urlopen('http://music.vidmate.mobi/search-' + song.strip().replace(' ', '%20') + '%20' + album.strip().replace(' ', '%20') + '.html')
		htmlsrc = response.read()

		htmlsrc = htmlsrc.split('id="music-search-song-container">', 1)[1]
		results = htmlsrc.split('music-song-search-item-open')
		for result in results:
			try:
				ps = result.split('<p')
				s = ps[1].split('</p>', 1)[0][1:]
				a = ps[2].split('<a', 1)[1].split('>', 1)[1].split('</a>', 1)[0].split('|')[0].strip()
				link = 'http://music.vidmate.mobi' + ps[2].split('<a', 1)[1].split('>', 1)[0].split('href="')[1].split('">')[0]
				#print a, s
				#print sm(None, song, s).ratio(), sm(None, album, a).ratio()
				if sm(None, song, s).ratio() > 0.8 and sm(None, album, a).ratio() > 0.8:
					print s
					download(link, s, lang)
					break
				else:
					pass
			except:
				pass

#languages list
langs = ['kannada-top-20', 'tamil-top-20', 'telugu-top-20', 'malayalam-top-20', 'mirchi-top-20']

for lang in langs:
	print '---', lang, '---'
	songs = parse(lang)
	for song, album in songs:
		print song, 'FROM', album

	print '===', 'search result'
	downloader(songs, lang)
