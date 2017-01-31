<?php
if(!isset($_SESSION)) { session_start(); }

if(!isset($_SESSION['loadRecommendations'])){

    echo "<html>";
        echo "<head>";
            include("../elements/head.php"); writeHead("Give your movie preferences");
            echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
            echo "<meta http-equiv='refresh' content='5'>";
        echo "</head>";
            ?>
            <div class="wait">
                <div class="loader"></div>
                <div class="loader_text">
                    <h3> Please wait... </h3>
                </div>
            </div>
            <?php
        echo "</body>";

        $_SESSION['loadRecommendations'] = 0;
    echo "</html>";

}elseif($_SESSION['loadRecommendations'] == 0){
    echo "<html>";
        echo "<head>";
            include("../elements/head.php"); writeHead("Give your movie preferences");
            echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
            echo "<meta http-equiv='refresh' content='5'>";
        echo "</head>";
        echo "<body>";
            ?>
            <div class="wait">
                <div class="loader"></div>
                <div class="loader_text">
                    <h3> Please wait... </h3>
                </div>
            </div>
            <?php
        echo "</body>";
        $command = ("/usr/local/bin/python3.5 ../python/combine_scores_models.py " . $_SESSION['userID']);
        exec($command, $output, $ret_code);
        
        $command = ("/usr/local/bin/python3.5 ../python/gen_based_genre_user_input.py " . $_SESSION['userID'] . " 21");
        exec($command, $output, $ret_code);
        $remove = array("[", "]");
        $output = str_replace($remove, "", $output);
        $movies = explode(", ", $output[0]);

        $_SESSION['genBasedMovies'] = $movies;

        $_SESSION['loadRecommendations'] = 1;
    echo "</html>";
}elseif($_SESSION['loadRecommendations'] == 1){
    
    echo "<html>";
        echo "<head>";
            include("../elements/head.php"); writeHead("Recommendations");
            echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
            echo "<link href='../css/slider.css' rel='stylesheet' type='text/css' media='all'/>";
        echo "</head>";
        echo "<body>";

        ?>
        <style>
        .main-slides {
            width: 150px;
            height: 225px !important;
        }

        .movieTitle{
            width: 150px;
            margin-top: -225px;
        }

        .column{
            width: 50%;
            float: left;
        }

        </style>
        <?php

            echo "<div class='column'>";


                echo "<div id='title'>";
                echo "<h1 style='text-align: center; margin: 15px; font-size: 30px; color: #e0b54e; margin-top: 20px;'> User Based Recommendations </h1>";
                echo "</div>";

                include("../functions/database.php");
                $query = "SELECT DISTINCT UR.movieId, M.title, M.imdbId FROM userRecommendations AS UR INNER JOIN movies AS M ON UR.movieId = M.movieId WHERE UR.userId =" . $_SESSION['userID'];
                $result = mysqli_fetch_all(select_data_from_database($query));

                $index = 0;
                $maxRecommendations = 21;

                foreach ($result as $key => $value){
                    
                    if ($index < $maxRecommendations){
                        $movieID = $value[0];
                    $title = $value[1];
                    $imdbId = $value[2];

                    $filename = "../images/scraped/". $imdbId .".jpg";

                    echo "<fieldset id='" . $movieID . "'>" . PHP_EOL;;
                    echo "<div id='step" .$index. "' class='main-slides'>" . PHP_EOL;

                    if (file_exists($filename)) {
                        echo "<img src='../../images/scraped/". $imdbId .".jpg' alt='' width='100%'/>" . PHP_EOL;
                    } else {
                        echo "<div style='height: 225px;'>" . PHP_EOL;
                        echo "<img src='../../images/notavailable.png' alt='' width='100%' style='margin-top: 80px;'/>" . PHP_EOL;
                        echo "</div>" . PHP_EOL;
                    }

                    echo "<div class='movieTitle'>" . PHP_EOL;
                    echo "<h3>". $title . "</h3>" . PHP_EOL;
                    echo "</div>" . PHP_EOL;


                    echo "</div>" . PHP_EOL;
                    echo "</fieldset>" . PHP_EOL;
                    $index += 1;

                    }
                    
                }
            
            echo "</div>";

            echo "<div class='column'>";

                echo "<div id='title'>";
                echo "<h1 style='text-align: center; margin: 15px; font-size: 30px; color: #e0b54e; margin-top: 20px;'> Genre Based Recommendations </h1>";
                echo "</div>";

                $movie_string = "";
                foreach ($_SESSION['genBasedMovies'] as $value){
                    $movie_string = $movie_string  . " '" . $value . "', ";
                }

                $movie_string = substr($movie_string, 0, -2);
                $movie_string = "(" . $movie_string . ")";
                $query = "SELECT DISTINCT movieId, imdbId, title FROM movies WHERE movieId IN" . $movie_string;

                $result = mysqli_fetch_all(select_data_from_database($query));

                foreach ($result as $key => $value){
                    $movieID = $value[0];
                    $imdbId = $value[1];
                    $title = $value[2];

                    $filename = "../images/scraped/". $imdbId .".jpg";

                    echo "<fieldset id='" . $movieID . "'>" . PHP_EOL;;
                    echo "<div id='step" .$index. "' class='main-slides'>" . PHP_EOL;

                    if (file_exists($filename)) {
                        echo "<img src='../../images/scraped/". $imdbId .".jpg' alt='' width='100%'/>" . PHP_EOL;
                    } else {
                        echo "<div style='height: 225px;'>" . PHP_EOL;
                        echo "<img src='../../images/notavailable.png' alt='' width='100%' style='margin-top: 80px;'/>" . PHP_EOL;
                        echo "</div>" . PHP_EOL;
                    }

                    echo "<div class='movieTitle'>" . PHP_EOL;
                    echo "<h3>". $title . "</h3>" . PHP_EOL;
                    echo "</div>" . PHP_EOL;


                    echo "</div>" . PHP_EOL;
                    echo "</fieldset>" . PHP_EOL;
                    
                }
            echo "</div>";
            echo "<div style='height: 30px; width: 100%; position:relative;display: inline-block;'></div>";

        echo "</body>";

    echo "</html>";
}




?>