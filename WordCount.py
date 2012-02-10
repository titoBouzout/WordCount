import sublime, sublime_plugin, re
import time
import threading, thread
import functools

s = sublime.load_settings('WordCount.sublime-settings')
s.add_on_change('enable_live_count', lambda:Object().reload_prefs())
s.add_on_change('enable_readtime', lambda:Object().reload_prefs())

class Object:
	view              = False
	modified          = False
	wrdRx             = re.compile("\w{1,}", re.U)
	wrdRx				      = wrdRx.match
	elapsed_time      = 0.4
	running           = False
	enable_live_count = s.get('enable_live_count', True)
	enable_readtime   = s.get('enable_readtime', True)

	def reload_prefs(self):
		Object.enable_live_count = s.get('enable_live_count', True)
		Object.enable_readtime = s.get('enable_readtime', True)

class WordCount(sublime_plugin.EventListener):

	def on_activated(self, view):
		self.asap(view)
	
	def on_post_save(self, view):
		self.asap(view)

	def on_selection_modified(self, view):
		Object.modified = True

	def on_close(self, view):
		Object.view = False
		Object.modified = True

	def asap(self, view):
		Object.view = view
		Object.modified = True
		Object.elapsed_time = 0.4
		sublime.set_timeout(lambda:WordCount().run(True), 0)

	def guess_view(self):
		if sublime.active_window() and sublime.active_window().active_view():
			Object.view = sublime.active_window().active_view()

	def run(self, asap = False):
		if Object.modified and (Object.running == False or asap):
			if Object.view != False:
				Object.modified = False
				view = Object.view
				if view.size() > 10485760:
					pass
				else:
					sel = view.sel()
					if len(sel) == 1 and sel[0].empty():
						if Object.enable_live_count:
							WordCountThread(view, [view.substr(sublime.Region(0, view.size()))], False).start()
						else:
							view.erase_status('WordCount')
					else:
						WordCountThread(view, [view.substr(sublime.Region(s.begin(), s.end())) for s in sel], True).start()
			else:
				self.guess_view()

	def display(self, view, word_count, on_selection):
		m = int(word_count / 200)
		s = int(word_count % 200 / (200 / 60))

		# Estimated Reading Time
		if Object.enable_readtime and s >= 1:
			readTime = " , ~ %dm, %ds reading time" % (m, s)
		else:
			readTime = ""

		if word_count == 0:
			view.set_status('No words')
		elif on_selection:
			if word_count == 1:
				view.set_status('WordCount', "1 Word selected")
			else:
				view.set_status('WordCount', "%s Words selected%s" % (word_count, readTime))
		else:
			if word_count == 1:
				view.set_status('WordCount', "1 Word")
			else:
				view.set_status('WordCount', "%s Words%s" % (word_count, readTime))

class WordCountThread(threading.Thread):

	def __init__(self, view, content, on_selection):
		threading.Thread.__init__(self)
		self.view = view
		self.content = content
		self.on_selection = on_selection

	def run(self):
		#print 'running:'+str(time.time())
		Object.running = True
		self.word_count = sum([self.count(region) for region in self.content])
		sublime.set_timeout(functools.partial(self.on_done), 0)

	def on_done(self):
		try:
			WordCount().display(self.view, self.word_count, self.on_selection)
		except:
			pass
		Object.running = False

	def count(self, content):

		begin = time.time()

		#=====1
		# wrdRx = Object.wrdRx
		# """counts by counting all the start-of-word characters"""
		# # regex to find word characters
		# matchingWrd = False
		# words = 0;
		# for ch in content:
		# 	# test if this char is a word char
		# 	isWrd = wrdRx(ch) != None
		# 	#print ch
		# 	if isWrd and not matchingWrd:
		# 		# we're moving into a word from not-a-word
		# 		words = words + 1
		# 		matchingWrd = True
		# 	if not isWrd:
		# 		# go back to not matching words
		# 		matchingWrd = False

		#=====2
		wrdRx = Object.wrdRx
		words = len([x for x in content.replace('\n', ' ').split(' ') if False == x.isdigit() and wrdRx(x)])

		Object.elapsed_time = end = time.time() - begin;
		#print 'Benchmark: '+str(end)

		return words

def word_count_loop():
	word_count = WordCount().run
	while True:
		# sleep time is adaptive, if takes more than 0.4 to calculate the word count
		# sleep_time becomes elapsed_time*3
		if Object.running == False:
			sublime.set_timeout(functools.partial(word_count), 0)
		time.sleep((Object.elapsed_time*3 if Object.elapsed_time > 0.4 else 0.4))

if not 'running_word_count_loop' in globals():
	running_word_count_loop = True
	thread.start_new_thread(word_count_loop, ())