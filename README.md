# POE Hideout Migration Tool
Tool designed to help with moving hideout designs from a hideout type to another. Only tested on POE1 but should work for POE2 assuming they have the same hideout data structure.
POE2 Hideouts don't have any art yet, so this is mostly useful for POE1 hideouts.

Example Hideouts Folder just contains the hideouts that I use (includes a bunch of Hideout MTX and stuff so just port your own using the tool). 

See guide on how to use this tool below:
https://youtu.be/sNVE8de2Dmc

Credits to https://gist.github.com/CristenPerret/ea3da944c2e976408662b988ee07d9e6 for base code

Credits to	chuxfivefive for hideouts:
1. https://hideoutshowcase.com/hideout/show/4956/title/VSHOJO%20-%20Kson

To compile the tool yourself use the following command:
pyinstaller --name="POE Hideout Migration Tool" --windowed --onefile hideout_migration_gui.py
