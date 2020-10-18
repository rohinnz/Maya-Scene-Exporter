"""
Dev tools for
1. Generating Qt .py files from .ui files
2. Unloading Python modules so Maya does not need to be restarted
"""
import os
import sys
import subprocess
import logging


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def prepare_scripts(scripts_dir=None, relative_path=None, rebuild_qt_classes=True):
	"""
	Clears scripts cache and generates qt classes under the base path.
	If base path not set, the Maya app scripts dir will be used.
	On Windows this is C:/Users/<user>/Documents/maya/scripts

	:param scripts_dir: path where project scripts are. Defaults to the Maya app scripts dir.
	:param relative_path: relative path to add to the scripts dir
	:param rebuild_qt_classes: Boolean for whether qt classes should be generated from ui files.
	"""
	if not scripts_dir:
		scripts_dir = os.path.join(os.environ['MAYA_APP_DIR'], 'scripts')

	if relative_path:
		scripts_dir = os.path.join(scripts_dir, relative_path)

	LOG.info('Clearing scripts cache in {}'.format(scripts_dir))
	clearPathSymbols([scripts_dir])

	if rebuild_qt_classes:
		generate_qt_ui([scripts_dir])


def generate_qt_ui(paths):
	"""
	Generate python classes from .ui files using the pyside2-uic tool.

	Advantages of using generated code over .ui files:
	1. Easier customisation. E.g. Custom widgets
	2. Faster loading

	:param paths: directories to search recursively for .ui files
	"""
	maya_path = os.path.join(os.environ['MAYA_LOCATION'], 'bin').replace('\\', '/')
	mayapy_path = os.path.join(maya_path, 'mayapy.exe').replace('\\', '/')
	pysid2uic_path = os.path.join(maya_path, 'pyside2-uic').replace('\\', '/')
	CREATE_NO_WINDOW = 0x08000000

	for path in paths:
		for root, dirs, files in os.walk(path):
			for filename in files:
				name, ext = os.path.splitext(filename)
				if ext == '.ui':
					ui_filepath = os.path.join(root, filename).replace('\\', '/')
					gen_filepath = os.path.join(root, name + '.py').replace('\\', '/')

					LOG.info('Generating python class from ui file {}'.format(ui_filepath))
					cmds = [mayapy_path, pysid2uic_path, '-o', gen_filepath, ui_filepath]
					subprocess.call(cmds, creationflags=CREATE_NO_WINDOW)


# clearPathSymbols() by Tyler Fox. Username tfox_TD. copied from
# http://discourse.techart.online/t/maya-scripts-folders/11907/7
def clearPathSymbols(paths, keepers=None):
	"""
	Removes path symbols from the environment.

	This means I can unload my tools from the current process and re-import them
	rather than dealing with the always finicky reload()

	I use directory paths rather than module names because it gives me more control
	over what is unloaded

	Make sure to close any UI's you're clearing before using this function

	Parameters
	----------
	paths : list
		List of directory paths that will have their modules removed
	keepers : list, optional
		List of module names that will not be removed
	"""
	keepers = keepers or []
	paths = [os.path.normcase(os.path.normpath(p)) for p in paths]

	for key, value in sys.modules.items():
		protected = False

		# Used by multiprocessing library, don't remove this.
		if key == '__parents_main__':
			protected = True

		# Protect submodules of protected packages
		if key in keepers:
			protected = True

		ckey = key
		while not protected and '.' in ckey:
			ckey = ckey.rsplit('.', 1)[0]
			if ckey in keepers:
				protected = True

		if protected:
			continue

		try:
			packPath = value.__file__
		except AttributeError:
			continue

		packPath = os.path.normcase(os.path.normpath(packPath))

		isEnvPackage = any(packPath.startswith(p) for p in paths)
		if isEnvPackage:
			sys.modules.pop(key)
