import json

#Changes all objects X and Y coordinates by xRelative, YRelative 
#Credits to https://gist.github.com/CristenPerret/ea3da944c2e976408662b988ee07d9e6

#Edit values here
fileName = 'WhiteEditFV.hideout'
xRelative = 0
yRelative = 0
fvFixed = 64 #64 after Scourge Hideout Decoration (fv: 64) is how you add decorations to the scourge dimension
fileName_output = 'test.hideout' 

#If changing hideout 'tiles/map' you must change the "hideout_name" + "hideout_hash" manually.
#- IE Moving from backstreet to shaped. Open a shaped hideout file. 
#- Copy the name and hash line (line 4+5), then replace those lines in your backstreet file.




#errors="ignore": used to ignore unicode errors that can occur when reading a hideoutfile that was made in a different language
with open(fileName, errors="ignore") as f:
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]


output_file = []
for line in lines:
    if '"x":' in line:
        coord = int(line.split(':')[1].rstrip(','))
        coord += xRelative
        line = '          "x":' + str(coord) + ","
        output_file.append(line +'\n')
    elif '"y":' in line:
        coord = int(line.split(':')[1].rstrip(','))
        coord += yRelative
        line = '          "y":' + str(coord) + ","
        output_file.append(line + '\n') 
    elif '"fv":' in line:
        coord = int(line.split(':')[1].rstrip(','))
        coord = fvFixed
        line = '      "fv":' + str(coord) + ","
        output_file.append(line + '\n')
        pass
    else:
        output_file.append(line + '\n')

with open(fileName_output, 'w+') as f:
    f.writelines(output_file) 