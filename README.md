# LanguageInjector

Allows you to inject native language patterns.

It's more powerful than python regex parsing

Useful for adding `invalid` patterns or highlighting a language that is not supported by sublime text

![Example](https://raw.githubusercontent.com/Julow/LanguageInjector/master/captures/example.png)

_See below for usage_

### Installation

[Using Package Control.](https://sublime.wbond.net/packages/LanguageInjector)

OR manually:

`git clone` this repo in `%Sublime text location%/Packages/LanguageInjector/`

Folder name does not matter but it must be in `Packages/`

### Settings syntax

It's very simple to add patterns

Example:

```js
{
	"patterns": {

		// Simple rule "regexp": "scope"
		"[ \t]+$": "invalid.trailing",

		// Using captures
		"^ +(\t+)|^\t+( +)": {
			// Scope for capture 1
			"1": "invalid.indentation.tab-in-space",
			// Scope for capture 2
			"2": "invalid.indentation.space-in-tab"
			// Order or holes do not matter
		},

		"\\{\\{[^\\}]+\\}\\}": {
			// Only for html
			"parent": ["text.html"],

			// Without using capture
			"scope": "string.regexp.template"
		},

		// Using custom scope
		"[a-fA-F0-9]{4} [a-fA-F0-9]{2,4}": {
			"parent": ["text.plain"],

			"scope": "juloo.hex.group"
		}
	}
}
```

If a regex syntax is not valid, sublime text doesn't load the syntax and color scheme.
(White background and black foreground)

_The scope is a "description" of part of text, used for color schemes_

### License

> The MIT License (MIT)
> 
> Copyright (c) 2014 juloo
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy of
> this software and associated documentation files (the "Software"), to deal in
> the Software without restriction, including without limitation the rights to
> use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
> the Software, and to permit persons to whom the Software is furnished to do so,
> subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
> FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
> COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
> IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
> CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
