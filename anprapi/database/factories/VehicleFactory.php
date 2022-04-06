<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Vehicle>
 */
class VehicleFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        return [
            'registration_number' => $this->faker->unique()->regexify('[A-Z]{2}[0-9]{3}[A-Z]{2}'),
            'owner' => $this->faker->name(),
            'vehicle_make' => $this->faker->randomElement([
                'Toyota', 'Honda', 'Nissan', 'Mazda', 'Ford', 'Hyundai',
                'Kia', 'Chevrolet', 'Volkswagen', 'Audi', 'BMW', 'Mercedes-Benz', 'Mitsubishi', 'Suzuki', 'Lexus', 'Subaru',
                'Dodge', 'Land Rover', 'Jeep', 'Citroen', 'Infiniti', 'Maserati', 'Porsche', 'Audi', 'Volvo', 'Jaguar', 'Ferrari',
                'Lamborghini', 'Bugatti', 'Rolls-Royce', 'Bentley', 'Aston Martin', 'Tesla', 'Maserati', 'Lamborghini', 'Porsche',
                'Audi', 'Volvo', 'Jaguar', 'Ferrari', 'Lamborghini', 'Bugatti', 'Rolls-Royce', 'Bentley', 'Aston Martin', 'Tesla',
                'Maserati', 'Lamborghini', 'Porsche', 'Audi', 'Volvo', 'Jaguar', 'Ferrari', 'Lamborghini', 'Bugatti', 'Rolls-Royce',
                'Bentley', 'Aston Martin', 'Tesla', 'Maserati', 'Lamborghini', 'Porsche', 'Audi', 'Volvo', 'Jaguar', 'Ferrari',
                'Lamborghini', 'Bugatti', 'Rolls-Royce', 'Bentley', 'Aston Martin', 'Tesla', 'Maserati', 'Lamborghini', 'Porsche',
                'Audi', 'Volvo', 'Jaguar', 'Ferrari', 'Lamborghini', 'Bugatti', 'Rolls-Royce', 'Bentley', 'Aston Martin', 'Tesla',
                'Maserati', 'Lamborghini', 'Porsche', 'Audi', 'Volvo', 'Jaguar', 'Ferrari', 'Lamborghini', 'Bugatti', 'Rolls-Royce',
                'Bentley', 'Aston Martin', 'Tesla', 'Maserati', 'Lamborghini', 'Porsche', 'Audi', 'Volvo'
            ]),
            'year_of_manufacture' => $this->faker->year(),
            'engine_capacity' => $this->faker->randomElement([
                '1.0', '1.2', '1.4', '1.6', '1.8', '2.0', '2.2', '2.4', '2.6', '2.8', '3.0', '3.2',
                '3.4', '3.6', '3.8', '4.0', '4.2', '4.4', '4.6', '4.8', '5.0', '5.2', '5.4', '5.6', '5.8', '6.0', '6.2', '6.4', '6.6', '6.8', '7.0',
                '7.2', '7.4', '7.6', '7.8', '8.0', '8.2', '8.4', '8.6', '8.8', '9.0', '9.2', '9.4', '9.6', '9.8', '10.0', '10.2', '10.4', '10.6', '10.8',
                '11.0', '11.2', '11.4', '11.6', '11.8', '12.0', '12.2', '12.4', '12.6', '12.8', '13.0', '13.2', '13.4', '13.6', '13.8', '14.0', '14.2',
                '14.4', '14.6', '14.8', '15.0', '15.2', '15.4', '15.6', '15.8', '16.0', '16.2', '16.4', '16.6', '16.8', '17.0', '17.2', '17.4', '17.6',
                '17.8', '18.0', '18.2', '18.4', '18.6', '18.8', '19.0', '19.2', '19.4', '19.6', '19.8', '20.0', '20.2', '20.4'
            ]),
            'body_type' => $this->faker->randomElement([
                'Sedan', 'Hatchback', 'SUV', 'Coupe', 'Convertible', 'Crossover', 'Pickup', 'Van',
                'Wagon', 'Truck', 'Bus', 'Motorcycle', 'Tractor', 'Trike', 'Tractor-Trailer', 'Other'
            ]),
            'color' => $this->faker->colorName(),
            'logbook_number' => $this->faker->unique()->regexify('[A-Z]{2}[0-9]{3}[A-Z]{2}'),
            'engine_number' => $this->faker->unique()->regexify('[A-Z]{2}[0-9]{3}[A-Z]{2}'),
            'chassis_number' => $this->faker->unique()->regexify('[A-Z]{2}[0-9]{3}[A-Z]{2}'),
        ];
    }
}
