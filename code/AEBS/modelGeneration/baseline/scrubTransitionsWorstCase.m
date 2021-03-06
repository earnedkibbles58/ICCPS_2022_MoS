function [scrubbedNextds,scrubbedNextvs] = scrubTransitionsWorstCase(nextds,nextvs,deltad,deltav)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

scrubbedNextds = [];
scrubbedNextvs = [];

scrubbedNextdids = [];
scrubbedNextvids = [];

nextdids = [];
nextvids = [];

for i = 1:length(nextds)
    nextd = nextds(i);
    nextv = nextvs(i);
    nextdid = floor(nextd/deltad)+1;
    nextvid = ceil(nextv/deltav)+1;
    
    nextdids = [nextdids; nextdid];
    nextvids = [nextvids; nextvid];
end

%% sort nextdids and vids by MoS
[nextvids,I] = sort(nextvids,'descend');
nextdids = nextdids(I);
nextds = nextds(I);
nextvs = nextvs(I);

[nextdids,I] = sort(nextdids);
nextvids = nextvids(I);
nextds = nextds(I);
nextvs = nextvs(I);            
            

%%

for i = 1:length(nextdids)
    nextd = nextds(i);
    nextv = nextvs(i);
    nextdid = nextdids(i);
    nextvid = nextvids(i);
    if(isWorse(nextdid,nextvid,nextdids,nextvids))
        alreadyHasPoint = 0;
        for j = 1:length(scrubbedNextdids)
            if(nextdid==scrubbedNextdids(j) && nextvid==scrubbedNextvids(j))
                alreadyHasPoint = 1;
                break
            end
        end
        if(~alreadyHasPoint)
            scrubbedNextds = [scrubbedNextds; nextd];
            scrubbedNextvs = [scrubbedNextvs; nextv];
            
            scrubbedNextdids = [scrubbedNextdids; nextdid];
            scrubbedNextvids = [scrubbedNextvids; nextvid];
        end
    end
end
end


function worse = isWorse(nextd,nextv,nextds,nextvs)
    for j = 1:length(nextds)
        if(isBetter(nextd,nextv,nextds(j),nextvs(j)))
            worse = 0;
            return
        end
    end
    worse = 1;
end

function better = isBetter(d1,v1,d2,v2)
    if(abs(d1-d2)<0.0001)
        d2=d1;
    end
    if(abs(v1-v2)<0.00001)
        v1=v2;
    end
    if (d1>d2 && v1 < v2)
        better = 1;
    elseif (d1>d2 && v1 <= v2)
        better = 1;
    elseif (d1>=d2 && v1 < v2)
        better = 1;
    else
        better = 0;
    end
end