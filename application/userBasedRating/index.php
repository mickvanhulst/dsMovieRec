<?php
if(!isset($_SESSION)) { session_start(); }
    
    if (!isset($_SESSION['userBasedMovies'])){
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
            $_SESSION['userBasedMovies'] = 0;

    }elseif($_SESSION['userBasedMovies'] == 0){
        echo "<html>";
            echo "<head>";
                include("../elements/head.php"); writeHead("Give your movie preferences");
                echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
                echo "<meta http-equiv='refresh' content='2'>";
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
        echo "</html>";

        $_SESSION['userBasedMovies'] = 1;
        $command = ("/usr/local/bin/python3.5 ../python/gen_based_genre_user_input.py " . $_SESSION['userID'] . " 20");
        exec($command, $output, $ret_code);
        $remove = array("[", "]");
        $output = str_replace($remove, "", $output);
        $movies = explode(", ", $output[0]);

        $_SESSION['userBasedMovies'] = $movies;


    }else{
         echo "<html>";
            echo "<head>";
                include("../elements/head.php"); writeHead("Give your movie preferences");
                echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
            echo "</head>";
                ?> <div id="box" class="warning" style="height:150px">
                <p> Please rate the following movies for us. </p>
                    <a href="/userBasedRating/rate">
                    <div class="submit">
                        <h2> Next </h2>
                    </div>
                    </a>
                </div>
                <?php 
            echo "</body>";
        echo "</html>";
    }


?>