import sys
import gpxtool_subcommands as SC

try:
	if len(sys.argv) < 3:
		raise Exception("Usage: gpxtool <subcommand> <gpx file>\n")

	subcommand = sys.argv[1]
	gpx_file = sys.argv[2]

	if subcommand == "distance":
		SC.distance(gpx_file)
	elif subcommand == "top":
		SC.top(gpx_file)
	else:
		raise Exception("Unrecognised subcommand \"{subcommand}\"")

except Exception as e:
	print(e.args[0])
	sys.exit(1)
