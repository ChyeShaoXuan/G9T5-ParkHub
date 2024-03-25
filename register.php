<?php
header('Access-Control-Allow-Origin: http://127.0.0.1:8001'); // This allows all origins
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE'); // Adapts to allowed request methods
header('Access-Control-Allow-Headers: Content-Type, Authorization'); // Required for CORS preflight

require 'db.php';  // Make sure this points to your database connection script

header("Content-Type: application/json"); // Specify the content type

$input = json_decode(file_get_contents('php://input'), true); // Decode the JSON object

if (isset($input['email']) && isset($input['password']) && isset($input['phoneNo']) && isset($input['name'])) {
    // Sanitize and validate your input as needed

    $email = $input['email'];
    $name = $input['name'];
    $password = $input['password'];  // Remember to hash this password before storing
    $phoneNo = $input['phoneNo'];  // Assuming you want to store this too

    $hashed_password = password_hash($password, PASSWORD_DEFAULT);  // Hash the password

    $sql = "INSERT INTO users (name, password, email, phoneNo) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssss", $name, $hashed_password, $email, $phoneNo);

    if ($stmt->execute()) {
        http_response_code(200);
        echo json_encode(array("message" => "Registration successful"));
    } else {
        http_response_code(500);
        echo json_encode(array("message" => "Error while registering the user"));
    }
} else {
    http_response_code(400); // Bad request
    echo json_encode(array("message" => "Incomplete request"));
}
?>
