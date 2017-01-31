<?php
if(!isset($_SESSION)) { session_start(); }

include("../../../functions/database.php");
$userID = $_SESSION['userID'];

foreach($_POST as $key => $value){

    $rating = substr($key, 0, 1);
    $movieID = substr($key, 1);
    $query = "INSERT INTO ratings (userId, movieId, rating)  VALUES (". $userID .", ". $movieID .", ". $rating .")";
    insert_data_to_database($query); 
}

echo "<html>";
    echo "<head>";
        include("../../../elements/head.php"); writeHead("Give your movie preferences");
        echo "<link href='../../../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
    echo "</head>";
    echo "<body>";
        ?> <div id="box" class="warning" style="height:150px">
                <p> Thanks for your input! </p>
                <a href="/recommendations/">
                <div class="submit">
                    <h2> Get Recommendations! </h2>
                </div>
                </a>
            </div>
            <?php 
    echo "</body>";
echo "</html>";

?>

