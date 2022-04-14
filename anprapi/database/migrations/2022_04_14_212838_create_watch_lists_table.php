<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('watch_lists', function (Blueprint $table) {
            $table->id();
            $table->string('registration_number')->unique();
            $table->string('owner')->nullable();
            $table->string('vehicle_make')->nullable();
            $table->string('year_of_manufacture')->nullable();
            $table->string('engine_capacity')->nullable();
            $table->string('body_type')->nullable();
            $table->string('color')->nullable();
            $table->string('logbook_number')->nullable();
            $table->string('engine_number')->nullable();
            $table->string('chassis_number')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('watch_lists');
    }
};
