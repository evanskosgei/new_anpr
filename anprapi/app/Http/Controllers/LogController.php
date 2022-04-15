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
}
