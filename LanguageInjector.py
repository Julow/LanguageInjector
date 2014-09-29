import sublime, sublime_plugin, os, plistlib

class LanguageInjectorListener(sublime_plugin.EventListener):

	xml_location = "Packages/julooLanguageInjectorCache/"

	def get_xml_path(self, id):
		return self.xml_location + str(id) +".tmLanguage"

	def get_full_path(self, theme_path):
		return os.path.join(sublime.packages_path(), os.path.normpath(theme_path[9:]))

	def on_close(self, view):
		if view.settings().has("old_syntax"):
			view.set_syntax_file(view.settings().get("old_syntax"))
			view.settings().erase("old_syntax")
		full_path = self.get_full_path(self.get_xml_path(view.id()))
		if os.path.exists(full_path):
			os.remove(full_path)

	def on_load_async(self, view):
		scope = view.scope_name(view.sel()[0].b).split(" ")[0][:6]
		if scope != "source":
			return
		if view.settings().has("old_syntax"):
			syntax_file = view.settings().get("old_syntax")
		else:
			syntax_file = view.settings().get("syntax")
			view.settings().set("old_syntax", syntax_file)
		data = plistlib.readPlistFromBytes(sublime.load_resource(syntax_file).encode("UTF-8"))
		settings = sublime.load_settings("LanguageInjector.sublime-settings")
		patterns = settings.get("patterns")
		for reg in patterns.keys():
			p = {"match": reg}
			if type(patterns[reg]) is str:
				p["name"] = patterns[reg]
			else:
				captures = {}
				for id in patterns[reg].keys():
					captures[id] = {"name": patterns[reg][id]}
				p["captures"] = captures
			data["patterns"].append(p)
		if not os.path.exists(self.get_full_path(self.xml_location)):
			os.mkdir(self.get_full_path(self.xml_location))
		with open(self.get_full_path(self.get_xml_path(view.id())), "wb") as f:
			plistlib.writePlist(data, f)
		view.set_syntax_file(self.get_xml_path(view.id()))
