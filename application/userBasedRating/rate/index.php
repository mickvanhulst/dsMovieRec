<?php
if(!isset($_SESSION)) { session_start(); }

echo "<html>";
    echo "<head>";
        include("../../elements/head.php"); writeHead("Give your movie preferences");
        echo "<link href='../../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
        echo "<link href='../../css/slider.css' rel='stylesheet' type='text/css' media='all'/>";
    echo "</head>";
    echo "<body>";

?>

        <form action="/userBasedRating/rate/process/" method="post">

        <?php
        include("../../functions/database.php");
        
        $index = 1;
        foreach ($_SESSION['userBasedMovies'] as $key => $movieID){ 
            
            $query = "SELECT imdbId, title FROM `movies` WHERE `movieId` = " . $movieID . "";
            $result = mysqli_fetch_array(select_data_from_database($query));
            $imdbId = $result['imdbId'];
            $title = $result['title'];

            $filename = "../../images/scraped/". $imdbId .".jpg";

            echo "<fieldset id='" . $movieID . "'>";
            echo "<div id='step" .$index. "' class='main-slides'>" . PHP_EOL;

            if (file_exists($filename)) {
                echo "<img src='../../images/scraped/". $imdbId .".jpg' alt='' width='100%'/>" . PHP_EOL;
            } else {
                echo "<div style='height: 300px;'>" . PHP_EOL;
                    echo "<img src='../../images/notavailable.png' alt='' width='100%' style='margin-top: 80px;'/>" . PHP_EOL;
                echo "</div>" . PHP_EOL;
               
            }

            echo "<div class='movieTitle'>" . PHP_EOL;
            echo "<h3>". $title . "</h3>";
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

<?php

echo "<body>";
echo "</html>";

?>