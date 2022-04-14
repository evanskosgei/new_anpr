<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\VehicleController;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
use App\Http\Controllers\LogsController;
=======
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
use App\Http\Controllers\LogController;

>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
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

Route::get('vehicle/{key}', [VehicleController::class, 'search']);
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

Route::post('logs', [LogsController::class, 'storeData']);
=======
Route::get('logs', [LogController::class, 'logs']);
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
Route::get('logs', [LogController::class, 'logs']);
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
=======
Route::get('logs', [LogController::class, 'logs']);
>>>>>>> 7f8e3d4e753450cd53bfc0a8f69cf7945769a2fa
