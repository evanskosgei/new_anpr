<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
<<<<<<< HEAD
=======
use App\Models\Log;
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa

class LogController extends Controller
{
    //
<<<<<<< HEAD
=======
    function logs(){
        $v = Log::all();
        return response()->json(count($v));
    }
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
}
