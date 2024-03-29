<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\WatchList;

class WatchListController extends Controller
{
    //
    function add_to_watchlist(Request $request){
        $v = new WatchList();
        $v->registration_number = $request->input('reg_plate');
        $v->owner = $request->input('owner');
        $v->vehicle_make = $request->input('vehicle_make');
        $v->year_of_manufacture = $request->input('model_year');
        $v->engine_capacity = $request->input('engine_capacity');
        $v->body_type = $request->input('body_type');
        $v->color = $request->input('color');
        $v->logbook_number = $request->input('logbook_number');
        $v->engine_number = $request->input('engine_number');
        $v->chassis_number = $request->input('chasis_number');
        $v->save();
        return response()->json('success');
    }

    function delete_from_watchlist($id){
        $v = WatchList::where('registration_number', $id)->get();
        // dd(count($v));
        if (count($v) > 0){
            WatchList::where('registration_number', $id)->delete();
            return response()->json('success');
        }
        else{
            return response()->json('error');
        }
    }

    function searchCar($key){
        $v = WatchList::where('registration_number', 'like', "$key")->get();
        if (count($v) > 0) {
            return response()->json($v);
        } else {
            return response()->json('error');
        }
    }

    function watchlist(){
        $data = WatchList::select("registration_number", "owner", "vehicle_make", "year_of_manufacture", "engine_capacity", "body_type", "color", "logbook_number", "engine_number", "chassis_number")->get();
        if (count($data) > 0) {
            return $data;
        } else {
            return "error";
        }
    }
}
