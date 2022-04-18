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

    function allLogs(){
        return response()->json(Log::all());
    }

    function saveLog(Request $request){
        $v = new Log();
        $v->camera_id = $request->input('cameraid');
        $v->highway = $request->input('highwayname');
        $v->spotted_plate = $request->input('spottedplate');
        $v->save();
        return response()->json("success");
    }

    function logfilter(Request $request){
        $fro = $request->input('from');
        $to = $request->input('to');  
        $plate = $request->input('plate');

        if(empty($plate)){
            $logs = Log::whereBetween('created_at', [$fro, $to])->get();
            return response()->json($logs);
        }
        else{
            $logs = Log::where('spotted_plate', $plate)
                ->whereBetween('created_at', [$fro, $to])->get();
            return response()->json($logs);
        }
    }
}
