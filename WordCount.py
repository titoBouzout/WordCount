import sublime, sublime_plugin, re
import time
import threading
from os.path import basename

s = sublime.load_settings('WordCount.sublime-settings')

class Pref:
	def load(self):
		Pref.view                   = False
		Pref.modified               = False
		Pref.elapsed_time           = 0.4
		Pref.running                = False
		Pref.wrdRx                  = re.compile("\w{1,}", re.U)
		Pref.wrdRx                  = Pref.wrdRx.match
		Pref.enable_live_count      = s.get('enable_live_count', True)
		Pref.enable_readtime        = s.get('enable_readtime', False)
		Pref.enable_line_word_count = s.get('enable_line_word_count', False)
		Pref.enable_line_char_count = s.get('enable_line_char_count', False)
		Pref.enable_count_lines     = s.get('enable_count_lines', False)
		Pref.enable_count_chars     = s.get('enable_count_chars', False)
		Pref.readtime_wpm           = s.get('readtime_wpm', 200)
		# sometimes s.get() is returning None instead of the default?
		Pref.whitelist              = [x.lower() for x in s.get('whitelist_syntaxes', []) or []]
		Pref.blacklist              = [x.lower() for x in s.get('blacklist_syntaxes', []) or []]
		# Pref.whitelist              = map(lambda x: x.lower(), s.get('whitelist_syntaxes', []))

Pref = Pref()
Pref.load();
s.add_on_change('reload', lambda:Pref.load())

class WordCount(sublime_plugin.EventListener):

	def should_run_with_syntax(self, view):
		syntax = view.settings().get('syntax')
		syntax = basename(syntax).replace('.tmLanguage', '').lower() if syntax != None else "plain text"
		if len(Pref.blacklist) > 0:
			for white in Pref.blacklist:
				if white == syntax:
					view.erase_status('WordCount');
					return False
		if len(Pref.whitelist) > 0:
			for white in Pref.whitelist:
				if white == syntax:
					return True
			view.erase_status('WordCount');
			return False
		return True

	def on_activated(self, view):
		self.asap(view)

	def on_post_save(self, view):
		self.asap(view)

	def on_selection_modified(self, view):
		Pref.modified = True

	def on_close(self, view):
		Pref.view = False
		Pref.modified = True

	def asap(self, view):
		Pref.view = view
		Pref.modified = True
		Pref.elapsed_time = 0.4
		sublime.set_timeout(lambda:WordCount().run(True), 0)

	def guess_view(self):
		if sublime.active_window() and sublime.active_window().active_view():
			Pref.view = sublime.active_window().active_view()

	def run(self, asap = False):
		if Pref.modified and (Pref.running == False or asap):
			if Pref.view != False and not Pref.view.settings().get('is_widget'):
				if self.should_run_with_syntax(Pref.view):
					Pref.modified = False
					view = Pref.view
					if view.size() > 10485760:
						pass
					else:
						sel = view.sel()
						if len(sel) == 1 and sel[0].empty():
							if Pref.enable_live_count:
								WordCountThread(view, [view.substr(sublime.Region(0, view.size()))], view.substr(view.line(view.sel()[0].b)), False).start()
							else:
								view.erase_status('WordCount')
						else:
							WordCountThread(view, [view.substr(sublime.Region(s.begin(), s.end())) for s in sel], view.substr(view.line(view.sel()[0].b)), True).start()
			else:
				self.guess_view()

	def display(self, view, on_selection, word_count, char_count, word_count_line, char_count_line):
		m = int(word_count / Pref.readtime_wpm)
		s = int(word_count % Pref.readtime_wpm / (Pref.readtime_wpm / 60))

		# word count on line
		if Pref.enable_line_char_count and char_count_line > 1:
			chars_count_line = ", %d chars in line" % (char_count_line)
		else:
			chars_count_line = ""

		# char count on line
		if Pref.enable_line_word_count and word_count_line > 1:
			word_count_line = ", %d Words in line" % (word_count_line)
		else:
			word_count_line = ""

		# line count
		if Pref.enable_count_lines:
			line_count = ", %d Lines" % (view.rowcol(view.size())[0] + 1)
		else:
			line_count = ""

		# char count
		if Pref.enable_count_chars and char_count > 0 and not on_selection:
			char_count = ", "+self.makePlural('Char', char_count)
		else:
			char_count = ""

		# Estimated Reading Time
		if Pref.enable_readtime and s >= 1:
			read_time = " ~%dm, %ds reading time" % (m, s)
		else:
			read_time = ""

		view.set_status('WordCount', "%s%s%s%s%s%s" % (
		                self.makePlural('Word', word_count),
		                char_count,
		                word_count_line,
		                chars_count_line,
		                line_count,
		                read_time))

	def makePlural(self, word, count):
		return "%s %s%s" % (count, word, ("s" if count != 1 else ""))

class WordCountThread(threading.Thread):

	def __init__(self, view, content, content_line, on_selection):
		threading.Thread.__init__(self)
		self.view = view
		self.content = content
		self.content_line = content_line
		self.on_selection = on_selection

		self.char_count = 0
		self.word_count_line = 0
		self.chars_in_line = 0

	def run(self):
		#print 'running:'+str(time.time())
		Pref.running         = True

		self.word_count      = sum([self.count(region) for region in self.content])

		if Pref.enable_count_chars and not self.on_selection:
			self.char_count      = sum([len(region) for region in self.content])

		if Pref.enable_line_word_count:
			self.word_count_line = self.count(self.content_line)

		if Pref.enable_line_char_count:
			self.chars_in_line = len(self.content_line.strip());

		sublime.set_timeout(lambda:self.on_done(), 0)

	def on_done(self):
		try:
			WordCount().display(self.view, self.on_selection, self.word_count, self.char_count, self.word_count_line, self.chars_in_line)
		except:
			pass
		Pref.running = False

	def count(self, content):

		#begin = time.time()

		#=====1
		# wrdRx = Pref.wrdRx
		# """counts by counting all the start-of-word characters"""
		# # regex to find word characters
		# matchingWrd = False
		# words = 0
		# space_symbols = [' ', '\r', '\n']
		# for ch in content:
		# # 	# test if this char is a word char
		# 	isWrd = ch not in space_symbols
		# 	if isWrd and not matchingWrd:
		# 		words = words + 1
		# 		matchingWrd = True
		# 	if not isWrd:
		# 		matchingWrd = False

		#=====2
		wrdRx = Pref.wrdRx
		words = len([x for x in content.replace('\n', ' ').split(' ') if False == x.isdigit() and wrdRx(x)])

		#Pref.elapsed_time = end = time.time() - begin;
		#print 'Benchmark: '+str(end)

		return words

def word_count_loop():
	word_count = WordCount().run
	while True:
		# sleep time is adaptive, if takes more than 0.4 to calculate the word count
		# sleep_time becomes elapsed_time*3
		if Pref.running == False:
			sublime.set_timeout(lambda:word_count(), 0)
		time.sleep((Pref.elapsed_time*3 if Pref.elapsed_time > 0.4 else 0.4))

if not 'running_word_count_loop' in globals():
	running_word_count_loop = True
	t = threading.Thread(target=word_count_loop)
	t.start()

