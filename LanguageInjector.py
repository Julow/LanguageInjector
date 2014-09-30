import sublime, sublime_plugin, os, plistlib

xml_location = "Packages/julooLanguageInjectorCache/"

def get_xml_path(id):
	return xml_location + str(id) +".tmLanguage"

def get_full_path(p):
	return os.path.join(sublime.packages_path(), os.path.normpath(p[9:]))

class LanguageInjectorListener(sublime_plugin.EventListener):

	def on_close(self, view):
		view.settings().clear_on_change("syntax")
		if view.settings().has("old_syntax"):
			view.set_syntax_file(view.settings().get("old_syntax"))
			view.settings().erase("old_syntax")
		full_path = get_full_path(get_xml_path(view.id()))
		if os.path.exists(full_path):
			os.remove(full_path)

	def on_load_async(self, view):
		view.run_command("language_injector_update")


class LanguageInjectorUpdateCommand(sublime_plugin.TextCommand):

	xml_pos = ""

	def override_syntax(self):
		self.view.settings().clear_on_change("syntax")
		if self.view.settings().has("old_syntax"):
			syntax_file = self.view.settings().get("old_syntax")
		else:
			syntax_file = self.view.settings().get("syntax")
			self.view.settings().set("old_syntax", syntax_file)
		plist = plistlib.readPlistFromBytes(sublime.load_resource(syntax_file).encode("UTF-8"))
		settings = sublime.load_settings("LanguageInjector.sublime-settings")
		patterns = settings.get("patterns")
		for reg in patterns.keys():
			p = {"match": reg}
			valid = True
			if type(patterns[reg]) is str:
				p["name"] = patterns[reg]
			else:
				captures = {}
				for param in patterns[reg].keys():
					if param == "parent":
						valid = False
						for parent in patterns[reg]["parent"]:
							if self.view.match_selector(0, parent):
								valid = True
					elif param == "scope":
						p["name"] = patterns[reg]["scope"]
					elif param.isdigit():
						captures[param] = {"name": patterns[reg][param]}
				if len(captures.keys()) > 0:
					p["captures"] = captures
			if valid:
				plist["patterns"].append(p)
		if not os.path.exists(get_full_path(xml_location)):
			os.mkdir(get_full_path(xml_location))
		self.xml_pos = get_xml_path(self.view.id())
		with open(get_full_path(self.xml_pos), "wb") as f:
			plistlib.writePlist(plist, f)
		self.view.set_syntax_file(self.xml_pos)
		self.view.settings().add_on_change("syntax", self.syntax_change)

	def syntax_change(self):
		if self.view.settings().get("syntax") != self.xml_pos:
			if self.view.settings().has("old_syntax"):
				self.view.settings().erase("old_syntax")
			self.override_syntax()

	def run(self, edit, **args):
		self.override_syntax()
