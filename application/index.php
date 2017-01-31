<?php
if(!isset($_SESSION)) { session_start(); }
# User is not logged in.
if(!isset($_SESSION['userID'])){
    
    # Show start screen.
    include_once("elements/startScreen.php");

# User is logged in.
}else{

    # Check if user rated any movies.
    include_once("functions/database.php");
    $query = "SELECT COUNT(userId) as ratingCount FROM ratings WHERE userId = '" . $_SESSION['userID'] ."'";
    $userRating = mysqli_fetch_array(select_data_from_database($query));
    $userRatingCount = intval($userRatingCount['ratingCount']);

    # User has rated movies. The application will give some recommendations.
    if ($userRatingCount > 20){
        echo "<html>";
                echo "<head>";

                echo "</head>";
                echo "<body>";
                    echo "Hier komen de aanbevelingen";
                echo "</body>";   
            echo "</html>";

    # User has not rated enough movies.
    }else{

        $wait = false;
        $run = true;

        # First loop. The user has to wait.
        if(!isset($_SESSION['wait'])){
            
            $_SESSION['wait'] = FALSE;
            $wait = true; 
            $run = false;

        # Check for minimum of 50 movies in sample data table.
        }else{
            include_once("functions/database.php");
            $query = "SELECT count(movieId) AS movie_count FROM sampleUserInitial WHERE points > 0";
            $result = select_data_from_database($query);
            $rows_in_db = mysqli_fetch_assoc($result)['movie_count'];

            if ($rows_in_db < 200){
                $wait = true;
            }

        }

        # User has to wait.
        if($wait){
            echo "<html>";
                echo "<head>";
                    include("elements/head.php"); 
                    writeHead("Give your movie preferences");
                    echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
                    if($rows_in_db < 200){
                        if($run){
                            echo "<meta http-equiv='refresh' content='12'>";
                        }else{
                            echo "<meta http-equiv='refresh' content='3'>";
                        }
                    }
                echo "</head>";
                echo "<body>";
                    if($run){
                        shell_exec("/usr/local/bin/python3.5 ./python/genMovUserSpec.py");
                    }
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

        # User can start rating movies.
        }else{
            echo "<html>";
                echo "<head>";
                    include("elements/head.php"); 
                    writeHead("Give your movie preferences");
                    echo "<link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
                echo "</head>";
                echo "<body>";
                    ?>
                    <div id="box" class="warning message" style='height: 150px !important;'>
                        <p> Please rate the following movies for us.</p>
                        <a href="/rate/">
                        <div class="submit">
                            <h2> Rate! </h2>
                        </div>
                        </a>
                    </div>
                    <?php
                echo "</body>";
            echo "</html>";

        }


    }
}

?>

