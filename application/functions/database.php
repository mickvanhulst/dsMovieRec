<?php

//$servername = '81.204.145.155/';
//$DBusername = 'dsMinor';
//$DBpassword = 'dsMinor!123';

function open_connection(){
    $conn = mysqli_connect('localhost','root','root', 'MoviesDS');
    //$conn = mysqli_connect('81.204.145.155','dsMinor','dsMinor!123', 'MoviesDS');
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    return $conn; 
}

function close_connection($conn){
    $conn->close();
}

function select_data_from_database($query){
    //echo $query;
    //echo "open connection";
    $conn = open_connection();
    //echo "get result";
    $result = $conn->query($query);
    //echo "close connection";
    //echo "$result";
    close_connection($conn);

    return $result;
}

function insert_data_to_database($query){
    $conn = open_connection();
    $result = $conn->query($query);
    close_connection($conn);
} 

?>