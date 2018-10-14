
import RawArchiver.ModuleBase
import RawArchiver.Modules

ACTIVE_MODULES = []

for module in RawArchiver.Modules.plugins:
	for comp_name in dir(module):
		component = getattr(module, comp_name)
		try:
			if issubclass(component, RawArchiver.ModuleBase.RawScraperModuleBase):
				if not component in ACTIVE_MODULES:
					ACTIVE_MODULES.append(component)
		except TypeError:
			pass



def dump_active_modules():

	print("Enumerating active modules in raw scraper.")

	for module in ACTIVE_MODULES:
		print("	-> ", module)


if __name__ == '__main__':
	dump_active_modules()

