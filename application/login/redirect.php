<html>
    <head>
        <?php 
        if(!isset($_SESSION)) { session_start(); }
        include_once("../elements/head.php"); 
        writeHead("Login");

        ?>
        
        
        <link href='../css/forms.css' rel='stylesheet' type='text/css' media='all'/>
    </head>
    <body>

        <?php

        include_once("../functions/database.php");
        
        $query = "SELECT * FROM user WHERE username = '" . $_POST["username"] ."'";
        $users = select_data_from_database($query);

        $userID = "";
        $userPass = "";
        $userFirstName = "";
        $userLastName = "";

        if ($users->num_rows != 0){
            while ($row = $users->fetch_row()) {
                $userID = $row[0];
                $userPass = $row[2];
                $userFirstName = $row[3];
                $userLastName = $row[4];
            }
        }

        if ($userPass == $_POST["password"]){
            $_SESSION['isLoggedIn'] = TRUE;
            $_SESSION['userID'] = $userID;
            $_SESSION['username'] = $_POST["username"];
            $_SESSION['firstname'] = $userFirstName;
            $_SESSION['name'] = $userLastName;
        }

        if($_SESSION['isLoggedIn'] == TRUE){

           ?> <div id="box" class="warning" style="height:200px">
                <p> Your credentials are correct! Click here to go to the Homepage. </p>
                <a href="/">
                <div class="submit">
                    <h2> Homepage </h2>
                </div>
                </a>
            </div>
        <?php 
        }else{ 
        ?> 
            
            <div id="box" class="warning" style="height:150px">
                <p> There's something wrong with your credentials. Try again! </p>
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