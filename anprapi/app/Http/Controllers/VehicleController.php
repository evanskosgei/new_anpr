<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Vehicle;

class VehicleController extends Controller
{
    //
    function search($key){
        $v = Vehicle::where('registration_number', 'like', "$key")->get();
        if (count($v) > 0) {
            return response()->json($v);
        } else {
            return response()->json('error');
        }
    }

<<<<<<< HEAD
    function getVehicle($key){
        $data = Vehicle::where('registration_number', 'like', "$key")->get();
        dd($data);
        if (count($data) > 0) {
            return response()->json($data);
        } else {
            return response()->json('error');
        }
    }
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
}
