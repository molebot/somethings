-module(water).
-compile(export_all).

wall(L)->get_level(-1,1,1,L).

get_level(Sum,Old,Pos,List) when Old>0 ->
	This = level(Pos,0,0,0,List),
	get_level(Sum+Old,This,Pos+1,List);
get_level(Sum,_Old,_Pos,_List)->Sum.

level(_Pos,Sum,_,_,[])->Sum;
level(Pos,Sum,Cur,Mod,[H|T])->
    case Pos>H of
        true ->
            case Mod of
                1 ->    level(Pos,Sum,Cur+1,Mod,T);		% water
                0 ->    level(Pos,Sum,Cur,Mod,T)		% air
            end;
        _->
            case Mod of
                1 ->    level(Pos,Sum+Cur,0,1,T);		% touch right wall
                0 ->    level(Pos,Sum,0,1,T)			% touch left wall
            end
    end.
