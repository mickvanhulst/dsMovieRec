<?php
if(!isset($_SESSION)) { session_start(); }
?>

<html>
    <head>
        <?php 
        include_once("../elements/head.php"); 
        writeHead("Login");
        ?>
        
        <link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>
    </head>
    <body>

        <?php
        
        include_once("../functions/database.php");

        $user_exists = TRUE;

        $username = $_POST['username'];
        $query = "SELECT * FROM user WHERE username = '" . $username ."'";
        $users = select_data_from_database($query);

        if ($users->num_rows == 0){
            $user_exists = FALSE;
        }

        $query = "SELECT MAX(userId) AS max from user";
        $last_user_id = select_data_from_database($query);

        $newUserID = 0;

        while ($row = $last_user_id->fetch_row()) {
            $newUserID = $row[0];
        }
        
        $newUserID = $newUserID + 1;
        

        if($user_exists){

            $_SESSION["init_firstname"] = $_POST['firstname'];
            $_SESSION["init_lastname"] = $_POST['lastname'];

            ?>
            <div id="box" class="warning">
                <p> Sorry, this username has already been taken. </p>
                <a href="/register/">
                <div class="submit">
                    <h2> Return </h2>
                </div>
                </a>
            </div>
            <?php
        }else{
            // Create user
            $username = $_POST['username'];
            $password = $_POST['password'];
            $firstname = $_POST['firstname'];
            $lastname = $_POST['lastname'];
            $query = "INSERT INTO user (userId, username, password, firstName, lastName) VALUES ($newUserID, '$username', '$password', '$firstname', '$lastname')";
            insert_data_to_database($query);
            ?>
            <div id="box" class="warning">
                <p> Your account is created! Login to get your recommendations! </p>
                <a href="/login/">
                <div class="submit">
                    <h2> Login </h2>
                </div>
                </a>
            </div>
            <?php
        }

        ?>

    </body>
</html>