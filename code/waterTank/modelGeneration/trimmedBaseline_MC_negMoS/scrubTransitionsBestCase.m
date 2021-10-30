function [scrubbedNextwls,scrubbedNextvs] = scrubTransitionsBestCase(nextwls,deltawl)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

scrubbedNextwls = [];

if any(nextwls <= 0)
    scrubbedNextwls = [0];
    return
elseif any(nextwls > 100)
    scrubbedNextwls = [101];
    return
end


for i = 1:size(nextwls,1)
    nextwl = nextwls(i);
    if(isWorse(nextwl,nextwls))
        scrubbedNextwls = [scrubbedNextwls; nextwl];
    end
end
end


function worse = isWorse(nextwl,nextwls)
    for j = 1:size(nextwls,1)
        if(isBetter(nextwl,nextwls(j)))
            worse = 0;
            return
        end
    end
    worse = 1;
end

function better = isBetter(wl1,wl2)
    if(wl1==wl2)
        better = 0;
        return
    end
    
    if(sign(wl1-50) ~= sign(wl2-50))
        better = 0;
        return
    end
    
    if(wl1>50)
        if(wl1>wl2)
            better = 1;
            return
        else
            better = 0;
            return
        end
    else
        if(wl1<wl2)
            better = 1;
            return
        else
            better = 0;
            return
        end
    end

end
