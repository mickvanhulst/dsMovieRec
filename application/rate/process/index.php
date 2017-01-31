<?php
if(!isset($_SESSION)) { session_start(); }

$userID = $_SESSION["userID"];
$moviesWithRating = [];
$ratings = $_POST;
$currently_rated = [];

include("../../functions/database.php");

foreach($ratings as $key => $value){
    $rating = substr($key, 0, 1);
    $movie = substr($key, 1, 9);
    array_push($moviesWithRating, $movie);
    $movieID = intval($_SESSION[$movie]);
    $query = "INSERT INTO ratings (userId, movieId, rating)  VALUES (". $userID .", ". $movieID .", ". $rating .")";
    insert_data_to_database($query);
}

foreach($_SESSION['currently_rated'] as $ratedImdbID){

    $query = "SELECT points FROM `sampleUserInitial` WHERE `movieId` = " . $_SESSION[$ratedImdbID] . "";
    $result = mysqli_fetch_array(select_data_from_database($query));
    
    if (in_array($ratedImdbID, $moviesWithRating)){
        $newValue = intval($result['points']) + 1;
        
    }else{
        $newValue = intval($result['points']) - 2;
    }

    $updateQuery = "UPDATE sampleUserInitial SET points =" . $newValue . " WHERE `movieId` = " . $_SESSION[$ratedImdbID] . "";
    insert_data_to_database($updateQuery); 

}

?>

<html>
    <head>
        <?php

        include_once("../../elements/head.php"); 
        writeHead("Login");

        ?>
        <link href='../../css/forms.css' rel='stylesheet' type='text/css' media='all'/>
    </head>
    <body>

        <?php
        $query = "SELECT count(rating) as ratingCount FROM `ratings` WHERE `userId` = " . $_SESSION["userID"] . "";
        $result = mysqli_fetch_array(select_data_from_database($query));
        $numberOfRatings = intval($result['ratingCount']);
        
        if ($numberOfRatings < 20){
            $_SESSION['wait'] = TRUE;
            ?> <div id="box" class="warning" style="height:150px">
                <p> Thank you for your input. Click to go to the next step. </p>
                <a href="/">
                <div class="submit">
                    <h2> Next </h2>
                </div>
                </a>
            </div>
        <?php 
        }else{
            #var_dump($_SESSION);
            $sessionVariablesToKeep = ["isLoggedIn", "userID", "username", "firstname", "name"];
    
            unset($_SESSION["ratedMoviesIMDB"]);
            unset($_SESSION["ratedMovies"]);
            unset($_SESSION["currently_rated"]);
            unset($_SESSION["wait"]);

            foreach($_SESSION as $sessionVariable => $sessionVariableValue){
                if (substr($sessionVariable, 0 ,2) == "tt"){
                    unset($_SESSION[$sessionVariable]);
                }
                
            } 

            $_SESSION['wait'] = true
        ?>
        
        <div id="box" class="warning" style="height:150px">
            <p> Thank you for your input. Click to go to the next step. </p>
            <a href="/userBasedRating/">
                <div class="submit">
                    <h2> Next </h2>
                </div>
            </a>
        </div>

        <?php 
        }
            ?>
            
    </body>
</html>