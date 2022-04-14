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

    function delete_from_watchlist($key){
        $v = WatchList::where('registration_number', 'like', "$key")->get();
        // dd(count($v));
        if (count($v) > 0){
        $v->delete();
        return response()->json('success');
        }
        else{
            return response()->json('error');
        }
    }
}
