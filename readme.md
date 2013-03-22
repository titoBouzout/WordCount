## Description

Provides a real-time Word Count in the status-bar for Sublime Text 2. See: http://www.sublimetext.com/

Count words on document or in selections.

The minimal word length is 1 and does not count digits.

An estimated reading time is now appended to the end of the word count.

## Installation

Install this repository automatically via "Package Control" http://wbond.net/sublime_packages/package_control

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

 - `enable_line_word_count` : false

		Display the count of words found on current line.

 - `enable_line_char_count` : false

		Display the count of words found on current line.

## Inspiration

 - The main loop inspired by sublimelint https://github.com/lunixbochs/sublimelint
 - The count inspired by the original WordCount plugin http://code.google.com/p/sublime-text-community-packages/source/browse/#svn%2Ftrunk%2FWordCount committed by mindfiresoftware

## Contributors

 - Hawken Rives
 - Yaw Anokwa
 - James Brooks
 - Antony Male
 - Alex Galonsky
 - RikkiMongoose
