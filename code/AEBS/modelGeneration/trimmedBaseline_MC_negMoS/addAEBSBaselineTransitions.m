function [lattice] = addAEBSBaselineTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,rounding)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
format long
latticeSize = size(lattice);

safetyThreshInd = ceil((safetyThresh-0.00000001)/deltad);
for i=1:latticeSize(1)
    for j=1:latticeSize(2)
        tempCell = lattice(i,j);
        d = tempCell.d;
        v = tempCell.v;
        if(tempCell.did==7 && tempCell.vid==13)
            aegre=3;
        end
        newMapKey = N;
        clear newMapValue
        for K=0:1:N

            if d == 6 && v==0.4 && K==1
                dafqe=3;
            end
            [nextds,nextvs] = computeAEBSBaselineTransition(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell);

%             nextds
%             nextvs
            if(rounding==1)
                [nextds,nextvs] = scrubTransitionsBestCase(nextds,nextvs,deltad,deltav,safetyThresh);
            end
            latticeTransitions = [];
%             nextds
%             nextvs
            if(length(nextvs)>1)
                a = 1;
            end
            
            %% remove extra vid=1
            nextdstemp = [];
            nextvstemp = [];
            for iter = 1:length(nextds)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                nextdid = floor(nextd/deltad)+1;
                nextvid = ceil(nextv/deltav)+1;

                
                if tempCell.vid < nextvid
                    nextvid=tempCell.vid;
                end
                if K == 0 && tempCell.vid ~= nextvid
                    nextvid=tempCell.vid;
                end

                if isempty(nextdstemp) && iter == length(nextds)
                    nextdstemp = [nextdstemp nextd];
                    nextvstemp = [nextvstemp nextv];
                elseif nextvid~=1 || nextdid<=safetyThreshInd
                    nextdstemp = [nextdstemp nextd];
                    nextvstemp = [nextvstemp nextv];
                end
            end
            
            
            nextds = nextdstemp;
            nextvs = nextvstemp;
            
            nextdids = [];
            nextvids = [];
            for iter = 1:length(nextds)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                nextdid = floor(nextd/deltad)+1;
                nextvid = ceil(nextv/deltav)+1;

                if tempCell.vid < nextvid
                    nextvid=tempCell.vid;
                end
                if K == 0 && tempCell.vid ~= nextvid
                    nextvid=tempCell.vid;
                end
                
                nextdids = [nextdids nextdid];
                nextvids = [nextvids nextvid];
            end

            
            
            %% Sort vs in descending order and ds in ascending order
            [nextvids,I] = sort(nextvids,'descend');
            nextdids = nextdids(I);
            nextds = nextds(I);
            nextvs = nextvs(I);
            
            [nextdids,I] = sort(nextdids);
            nextvids = nextvids(I);
            nextds = nextds(I);
            nextvs = nextvs(I);            
            
            
            for iter = 1:length(nextds)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                nextdid = floor(nextd/deltad)+1;
                nextvid = ceil(nextv/deltav)+1;

                if tempCell.vid < nextvid
                    nextvid=tempCell.vid;
                end
                if K == 0 && tempCell.vid ~= nextvid
                    nextvid=tempCell.vid;
                end
                
                
                % ignore redundant transitions
                if(isempty(latticeTransitions))
                    latticeTransitions = [latticeTransitions; nextdid nextvid];
                else
                    alreadyHasTransition = 0;
                    % ignore loop transitions
                    if nextdid == i && nextvid == j
                        alreadyHasTransition = 1;
                    else
                        for k=1:size(latticeTransitions,1)
                            tempLatticeTransition = latticeTransitions(k,:);
                            if tempLatticeTransition(1)==nextdid && tempLatticeTransition(2)==nextvid
                                alreadyHasTransition=1;
                                break
                            end
                        end
                    end
                    if alreadyHasTransition==0
                        latticeTransitions = [latticeTransitions; nextdid nextvid];
                    end
                end
            end
            newMapValue{K+1}=latticeTransitions;
        end
        tempCell.nextPoints(newMapKey)=newMapValue;
        lattice(i,j)=tempCell;
    end
end
end

