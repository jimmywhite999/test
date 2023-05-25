<?php
// Database connection settings
$host = "database-1.ctm6lvyb8jys.ca-central-1.rds.amazonaws.com"; // MySQL host
$username = "admin"; // MySQL username
$password = "Fuckyou1.z$$$october311993"; // MySQL password
$database = "your_database"; // MySQL database name

// Establish the database connection
$connection = mysqli_connect($host, $username, $password, $database);

// Check if the connection was successful
if (!$connection) {
    die("Database connection failed: " . mysqli_connect_error());
}

// Retrieve the submitted form data
$username = $_POST['username'];
$password = $_POST['password'];

// Perform user validation and license check
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password' AND licence_expiry_date >= CURDATE()";
$result = mysqli_query($connection, $query);

if (mysqli_num_rows($result) > 0) {
    header("Location: dashboard.html");
    exit();
} else {
    header("Location: index.html");
    exit();
}
?>
