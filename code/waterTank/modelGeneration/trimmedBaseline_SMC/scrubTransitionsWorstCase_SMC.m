function [scrubbedNextwls] = scrubTransitionsWorstCase_SMC(nextwls,deltawl)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

scrubbedNextwls = [];



for i = 1:size(nextwls,1)
    nextwl = nextwls(i);
    if isWorseThanAll(nextwl,nextwls)
        scrubbedNextwls = [nextwl];
        return
    end

end



for i = 1:size(nextwls,1)
    nextwl = nextwls(i);
    scrubbedNextwls = [scrubbedNextwls; nextwl];
end
end



function worseThanAll = isWorseThanAll(nextwl,nextwls)
    worseThanAll = 1;
    for j = 1:length(nextwls)
        if(sign(nextwl-50) ~= sign(nextwls(j)-50))
            worseThanAll = 0;
            return
        end
        
        if nextwl<50 && nextwl>nextwls(j)
            worseThanAll = 0;
            return
        end
        
        if nextwl>50 && nextwl<nextwls(j)
            worseThanAll = 0;
            return
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
        if(wl1<wl2)
            better = 1;
            return
        else
            better = 0;
            return
        end
    else
        if(wl1>wl2)
            better = 1;
            return
        else
            better = 0;
            return
        end
    end

end
