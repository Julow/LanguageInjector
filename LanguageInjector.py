import sublime, sublime_plugin, os, plistlib, random

global_id = 0

xml_location = "Packages/julooLanguageInjectorCache/"

def get_new_id():
	global global_id
	global_id = global_id + 1
	return str(global_id) + "".join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(7))

def get_xml_path(id):
	return xml_location + id +".tmLanguage"

def get_full_path(p):
	return os.path.join(sublime.packages_path(), os.path.normpath(p[9:]))

class LanguageInjectorListener(sublime_plugin.EventListener):

	def on_close(self, view):
		view.run_command("language_injector_update", {"action": "destroy"})

	def on_load_async(self, view):
		view.run_command("language_injector_update", {"action": "update"})


class LanguageInjectorUpdateCommand(sublime_plugin.TextCommand):

	xml_id = "0"
	xml_pos = ""
	last_syntax = ""

	def override_syntax(self):
		if self.view.settings().has("old_syntax"):
			syntax_file = self.view.settings().get("old_syntax")
		else:
			syntax_file = self.view.settings().get("syntax")
			self.view.settings().set("old_syntax", syntax_file)
		plist = plistlib.readPlistFromBytes(sublime.load_resource(syntax_file).encode("UTF-8"))
		plist["name"] = plist["name"] + " Injected"
		plist["fileTypes"] = []
		settings = sublime.load_settings("LanguageInjector.sublime-settings")
		patterns = settings.get("patterns", {})
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
		self.xml_pos = get_xml_path(self.xml_id)
		self.last_syntax = self.xml_pos
		with open(get_full_path(self.xml_pos), "wb") as f:
			plistlib.writePlist(plist, f)
		self.view.set_syntax_file(self.xml_pos)
		self.view.settings().add_on_change("language_injector_syntax_listener", self.syntax_change)

	def syntax_change(self):
		syntax = self.view.settings().get("syntax")
		if syntax != self.last_syntax and syntax != self.view.settings().get("old_syntax"):
			self.last_syntax = syntax
			self.view.settings().set("old_syntax", syntax)
			self.view.run_command("language_injector_update", {"action": "update"})

	def run(self, edit, **args):
		self.view.settings().clear_on_change("language_injector_syntax_listener")
		if self.xml_pos != "" and os.path.exists(get_full_path(self.xml_pos)):
			os.remove(get_full_path(self.xml_pos))
		if args["action"] == "update":
			self.xml_id = get_new_id()
			self.override_syntax()
		elif args["action"] == "destroy":
			if self.view.settings().has("old_syntax"):
				self.view.set_syntax_file(self.view.settings().get("old_syntax"))
				self.view.settings().erase("old_syntax")
