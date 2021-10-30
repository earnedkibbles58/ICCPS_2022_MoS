import os
import subprocess
from subprocess import PIPE




def main():

    STORM_CONV_PATH = '/opt/storm/build/bin/storm-conv'

    MODEL_ROOT_FOLDER = '/data/models'

    AEBS_PROPS_FILE = '/data/models/AEBS/propsAEBS.props'
    WATER_TANK_PROPS_FILE = '/data/models/waterTank/tankPropsSink.props'

    for subdir, dirs, files in os.walk(MODEL_ROOT_FOLDER):
        for file in files:
            if file.endswith('.prism'):
                # print(os.path.join(subdir, file))
                # print(subdir)

                if "/AEBS/" in subdir:
                    print(AEBS_PROPS_FILE)
                    PROPS_FILE = AEBS_PROPS_FILE
                    continue
                elif "/waterTank/" in subdir:
                    print(WATER_TANK_PROPS_FILE)
                    PROPS_FILE = WATER_TANK_PROPS_FILE
                else:
                    raise ValueError('Hardcoded string parsing failed')
                
                JANI_FILE = os.path.join(subdir, file.replace(".prism",".jani"))
                print(JANI_FILE)

                with open(JANI_FILE, 'w') as fp:
                    pass

                # with open(JANI_FILE,'w') as f:
                #     pass
                proc = subprocess.run([STORM_CONV_PATH, '--prism', os.path.join(subdir, file) ,'--prop', PROPS_FILE, '--tojani', JANI_FILE], stdout=PIPE, stderr=PIPE)
                print(proc.stdout)

                f = open(JANI_FILE,"r")
                lines = f.readlines()
                f.close()
                for i,line in enumerate(lines):
                    line = line.replace("\"fun\": \"values\"," , "\"fun\": \"max\",")
                    lines[i] = line
                
                f = open(JANI_FILE,"w")
                new_file_contents = "".join(lines)
                f.write(new_file_contents)
                f.close()

                subprocess.call(['chmod','ugo+w',JANI_FILE])







if __name__ == "__main__":
    main()