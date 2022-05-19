local is_saber_tracked = false
--TODO: make this clean up the file

concommand.Add( "gm_sabertracking", function( ply, cmd, arg )
	running = true
	start_tracking(ply)
 end )

function lastline(path)

    local f = file.Open(path, "r", "DATA")
	
	-- all angles will have 3 char max (for now)
	-- e.g. -90 vs 090
	-- so this is a good approximation of EOF
	local ang = f:ReadLine(f:Seek(f:Size()-3))
	--print(ang)

	--print( f:Tell() )

    f:Close()
	
	return tonumber(ang)
end

function get_angle(filename)
	local angle = lastline(filename)
	if angle == nil then
		return 90
	end
	return tonumber(angle)
end

function start_tracking(ply)
	print("\nPlayer: " .. ply:AccountID())

	local prevangle = get_angle("test/tracking.txt")

	print("\nPreviously read angle: " .. tostring(prevangle))

	print("\nHand angles: " .. tostring(ply:GetManipulateBoneAngles(11)))
	
	angle = get_angle("test/tracking.txt")
	ply:ManipulateBoneAngles(11, Angle(0, 0, angle-90))
	
	print("\nNewly read angle: " .. angle)
	
	prevangle = angle
	
	print()
	print("Angles after update: ")
	print(ply:GetManipulateBoneAngles(11))
end
