
import RawArchiver.Modules.ModuleBase
import RawArchiver.Modules.WebComics

ACTIVE_MODULES = [
	RawArchiver.Modules.WebComics.WebComicsRawModule
]


for module in ACTIVE_MODULES:
	assert(issubclass(module, RawArchiver.Modules.ModuleBase.RawScraperModuleBase))

