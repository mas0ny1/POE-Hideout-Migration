
#Edit values here
fileName = 'teststart.hideout'
fvFixed = 64 #64 after Scourge Hideout Decoration (fv: 64) is how you add decorations to the scourge dimension
fileName_output = 'testFV.hideout' 
scourgeBool = False
#If changing hideout 'tiles/map' you must change the "hideout_name" + "hideout_hash" manually.
#- IE Moving from backstreet to shaped. Open a shaped hideout file. 
#- Copy the name and hash line (line 4+5), then replace those lines in your backstreet file.


#How to use this
#Move Scourge Hideout Decoration in the list of doodads in front of the other decorations (that make the image)
#Run code
#All decorations after Scourge Hideout Decoration will have an fv value of 64 (hence moved to the Scourge dimension)
#It seems like scourge hideout dont have a varying fv value (so only a value of 64)
#I am unsure of what fv actually is but it seems like it might determine the visibility of a decoration? or something like that
#Honestly im pretty stumped. I think the next step is to have the code sort the decorations by fv value 
#then adding them to the scourge dimension by fv order (lowest to highest)? dunno tbh

#errors="ignore": used to ignore unicode errors that can occur when reading a hideoutfile that was made in a different language
with open(fileName, errors="ignore") as f:
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]


output_file = []
for line in lines:
    if "Scourge Hideout Decoration" in line:
        scourgeBool = True
    if '"fv":' in line and scourgeBool == True:
        coord = int(line.split(':')[1].rstrip(','))
        coord = fvFixed
        line = '      "fv":' + str(coord)
        output_file.append(line + '\n')
        pass
    else:
        output_file.append(line + '\n')

with open(fileName_output, 'w+') as f:
    f.writelines(output_file) 