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


    function getVehicle($key){
        $data = Vehicle::where('registration_number', 'like', "$key")->get();
        dd($data);
        if (count($data) > 0) {
            return response()->json($data);
        } else {
            return response()->json('error');
        }
    }

}
