<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\VehicleController;
use App\Http\Controllers\LogController;
use App\Http\Controllers\WatchListController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
//vehicle controller
Route::get('vehicle/{key}', [VehicleController::class, 'search']);

//Log controller
Route::post('savelogs', [LogController::class, 'saveLog']);
Route::get('logs', [LogController::class, 'logs']);
Route::get('allLogs', [LogController::class, 'allLogs']);
Route::post('logfilter', [LogController::class, 'logfilter']);

//watchlist controller
Route::post('add_to_watchlist', [WatchListController::class, 'add_to_watchlist']);
Route::get('delete_from_watchlist/{id}', [WatchListController::class, 'delete_from_watchlist']);
Route::get('searchcar/{key}', [WatchListController::class, 'searchCar']);
