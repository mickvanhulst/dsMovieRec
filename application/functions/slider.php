<?php
include("../functions/database.php");

$result = select_data_from_database("SELECT DISTINCT(M.imdbId), M.movieId, M.title FROM movies as M INNER JOIN sampleUserInitial as S ON M.movieId = S.movieId WHERE `points` > 0 AND M.movieId NOT IN (SELECT movieId FROM `ratings` WHERE userId = " . $_SESSION["userID"] . ")");
$movies = [];
$movieNames = [];
$movieIDs = [];
$movieIMDBIDs = [];
$alreadyRated = [];

if (isset($_SESSION['ratedMoviesIMDB'])){
    $alreadyRated = $_SESSION['ratedMoviesIMDB'];
}else{
    $_SESSION['ratedMoviesIMDB'] = [];
}

$_SESSION['currently_rated'] = [];

if ($result->num_rows > 0) {
    $maxValue = 20;
    $indexValue = 0;

    while($row = $result->fetch_assoc()) {
        if(in_array($row["imdbId"], $alreadyRated)){
        }else{
            array_push($movies, $row["imdbId"]);
            $movieNames[$row["imdbId"]] = $row["title"];
            $_SESSION[$row["imdbId"]] = $row['movieId'];
            array_push($movieIDs, $row['movieId']);
            array_push($_SESSION['ratedMoviesIMDB'], $row['imdbId']);
            array_push($_SESSION['currently_rated'], $row['imdbId']);
            $indexValue = $indexValue + 1;
        }
        
        if ($indexValue == $maxValue){
            break;
        }
    }
} else {
    echo "0 results";
}

$_SESSION['ratedMovies'] = $movieIDs;



?>
<link href='/css/slider.css' rel='stylesheet' type='text/css' media='all'/>

        <form action="/rate/process/" method="post">

        <?php
        $index = 1;
        foreach ($movies as $movieID){ 

            $filename = "../images/scraped/". $movieID .".jpg";

            echo "<fieldset id='" . $movieID . "'>";
            echo "<div id='step" .$index. "' class='main-slides'>" . PHP_EOL;

            if (file_exists($filename)) {
                echo "<img src='../images/scraped/". $movieID .".jpg' alt='' width='100%'/>" . PHP_EOL;
            } else {
                echo "<div style='height: 300px;'>" . PHP_EOL;
                    echo "<img src='../images/notavailable.png' alt='' width='100%' style='margin-top: 80px;'/>" . PHP_EOL;
                echo "</div>" . PHP_EOL;
               
            }

            echo "<div class='movieTitle'>" . PHP_EOL;
            echo "<h3>". $movieNames[$movieID] . "</h3>";
            echo "</div>" . PHP_EOL;
            echo "<div class='ratingInput'>" . PHP_EOL;
            echo "<div class='stars'>" . PHP_EOL;

                echo "<input class='stare star-5' id='star-5-". $index ."' type='radio' name='5". $movieID ."'/>" . PHP_EOL;
                echo "<label class='stare st". $index ."  star-5' for='star-5-". $index ."'></label>" . PHP_EOL;
                echo "<input class='stare star-4' id='star-4-". $index ."' type='radio' name='4". $movieID ."'/>" . PHP_EOL;
                echo "<label class='stare st". $index ." stare star-4' for='star-4-". $index ."'></label>" . PHP_EOL;
                echo "<input class='stare star-3' id='star-3-". $index ."' type='radio' name='3". $movieID ."'/>" . PHP_EOL;
                echo "<label class='stare st". $index ." stare star-3' for='star-3-". $index ."'></label>" . PHP_EOL;
                echo "<input class='stare star-2' id='star-2-". $index ."' type='radio' name='2". $movieID ."'/>" . PHP_EOL;
                echo "<label class='stare st". $index ." stare star-2' for='star-2-". $index ."'></label>" . PHP_EOL;
                echo "<input class='stare star-1' id='star-1-". $index ."' type='radio' name='1". $movieID ."'/>" . PHP_EOL;
                echo "<label class='stare st". $index ." stare star-1' for='star-1-". $index ."'></label>" . PHP_EOL;

            echo "</div>" . PHP_EOL;
            echo "</div>" . PHP_EOL;
            echo "</div>" . PHP_EOL;
            echo "</fieldset>";

            $index = $index + 1;

        }
        ?>

        <input class="submit" type="submit" value="Rate!" id="submit"> 
        
        </form>
