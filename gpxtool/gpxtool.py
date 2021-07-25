import sys
import gpxtool_subcommands as SC

if len(sys.argv) < 3:
	print("Usage: gpxtool <subcommand> <gpx file>\n")
	sys.exit(1)

subcommand = sys.argv[1]
gpx_file = sys.argv[2]

exit_code = 1
if subcommand == "distance":
	exit_code = SC.distance(gpx_file)

sys.exit(exit_code)
