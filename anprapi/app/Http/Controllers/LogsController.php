<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Log;

class LogsController extends Controller
{
    function storeData(Request $request){
        $log = $request->registration_number;
        dd($log);
    }
}
