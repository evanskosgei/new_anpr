<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
use App\Models\Log;
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
use App\Models\Log;
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
use App\Models\Log;
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa

class LogController extends Controller
{
    //
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
    function logs(){
        $v = Log::all();
        return response()->json(count($v));
    }
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
}
