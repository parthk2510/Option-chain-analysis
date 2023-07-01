<?php
require 'vendor/autoload.php';

use InfluxDB\Client;
use InfluxDB\Driver\Guzzle;

$client = new Client('localhost', 8086);
$database = $client->selectDB('your_database_name');

$measurement = 'your_measurement_name';
$query = 'SELECT * FROM your_measurement_name';
$result = $database->query($query);
$points = $result->getPoints();

foreach ($points as $point) {
    // Access point data and fields
    // Example: $field1 = $point['field1'];
}
?>
