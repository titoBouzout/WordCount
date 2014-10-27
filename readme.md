**This is a [Sublime Text 3+](http://www.sublimetext.com/) Package. Please install via an updated version of  [Package Control 2+](https://sublime.wbond.net/installation) as instructed below. *DO NOT* install manually.**

## Installation

1. If you don't have it already, follow the instructions on [https://sublime.wbond.net/installation](https://sublime.wbond.net/installation) to install Package Control 2+.
2. In Sublime Text, press <kbd>Ctrl+Shift+P</kbd> (Win, Linux) or <kbd>⌘⇧p</kbd> (OS X) to open the command palette.
3. Choose `Package Control: Install Package`.
4. Select **WordCount** when avaliable.

## Description

Provides a real-time Word Count and character count in the status-bar for Sublime Text. See: http://www.sublimetext.com/

Count words and/or characters on document or in selections. By default, whitespace is not included in the character count.

The minimal word length is 1 and does not count digits.

An estimated reading time is now appended to the end of the word count.

## Preferences

 - `enable_live_count` : true

 		Allows to control if the live word counter is enabled. Otherwise will be enabled for selections only.

 - `enable_readtime` : false

 		Allows you to control if the estimated reading time is enabled.
 		Reading time is only displayed when there is a time > 1s.

 - `readtime_wpm` : 200

 		Sets the WPM to calculate the Estimated Reading Time for the file.

 - `whitelist_syntaxes` : []

		An array of syntax names that WordCount should run on.
		Example: ["Plain text", "Markdown"]
		If the array is empty, like it is by default, WordCount will run on any syntax.

 - `blacklist_syntaxes` : []

		An array of syntax names that WordCount should not run on.
		Example: ["Plain text", "Markdown"]
		If the array is empty, like it is by default, WordCount will run on any syntax.

 - `char_ignore_whitespace` : true

		Whether to skip whitespace for the character count.

 - `enable_line_word_count` : false

		Display the count of words found on current line.

 - `enable_line_char_count` : false

		Display the count of characters found on current line.

 - `enable_count_lines` : false

 		Display the number of lines in file

 - `enable_count_chars` : false

		Display the number of characters in file

 - `enable_count_pages` : true

		Display the number of pages in file

 - `word_regexp` : ""

		Word Regular expression. Defaults empty, an internal regular expression is used. If the portion of text matches this RegExp then the word is counted.

 - `word_split` : ""

		Split portions of text to test later as words with a Regular expression. Defaults to String.split() with no arguments, means that content will trim() and empty values (all whitespaces) are not used. In case of containing some value different than empty, the return of "re.findall" will be used.

 - `split`: {}

		Remove regex patterns by syntax. Use lowercase for the syntax names.

		Example to ignore all tags, including comments, from HTML:

		```
		"strip": {
			"html": [
				"<[^>]*>"
			]
		}
		```

## Inspiration

 - The main loop inspired by sublimelint https://github.com/lunixbochs/sublimelint
 - The count inspired by the original WordCount plugin http://code.google.com/p/sublime-text-community-packages/source/browse/#svn%2Ftrunk%2FWordCount committed by mindfiresoftware

## Contributors

 - Liam Cain
 - Lee Grey
 - Hawken Rives
 - Yaw Anokwa
 - James Brooks
 - Antony Male
 - Alex Galonsky
 - RikkiMongoose
 - ChrisJefferson
 - Harry Ng. (From [Word Count Tool](http://wordcounttools.com/))
