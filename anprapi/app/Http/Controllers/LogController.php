<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\Log;

class LogController extends Controller
{
    //

    function logs(){
        $v = Log::all();
        return response()->json(count($v));
    }

    function saveLog(Request $request){
        $v = new Log();
        $v->camera_id = $request->input('cameraid');
        $v->highway = $request->input('highwayname');
        $v->spotted_plate = $request->input('spottedplate');
        $v->save();
        return response()->json("success");
    }
}
