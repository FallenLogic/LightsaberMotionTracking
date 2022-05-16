local is_saber_tracked = false
-- vs = ValveBiped skeleton
-- This motion tracking won't work with anything else
local vs_wrist =  62




concommand.Add( "gm_sabertracking", function( ply, cmd, arg )

	if ( is_saber_tracked ) then
		end_tracking()
		return
	end
	
	running = true
	start_tracking(ply)
	
end )

function start_tracking(ply)
	local handler = io.popen("python3 saber_pose_processor.py")
	
	while running do
		local wrist_matrix = ply:getBoneMatrix(62)
		-- idk if it's pitch, yaw, or roll yet
		init_matrix:setAngles( Angle(0, handler:read("*a"), 0))
	end
	
	handler:close()
	
end

function end_tracking()
	running = false
end