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

        $firstname = "firstname";
        $lastname = "lastname";

        if(isset($_SESSION['init_firstname'])){
            $firstname = $_SESSION["init_firstname"];
        }
        if(isset($_SESSION['init_lastname'])){
            $lastname = $_SESSION["init_lastname"];
        }

        ?>

        <div id="box" class="register" style='height: 350px;'>
            <form action="complete_registration.php" method="post">
                <?php 
                
                if(!($firstname == "firstname")){
                    echo "<input type='text' name='firstname' value='". $firstname ."'>";
                }else{
                    echo "<input type='text' name='firstname' placeholder='Firstname'>";
                }

                if(!($lastname == "lastname")){
                    echo "<input type='text' name='lastname' value='". $lastname ."'>";
                }else{
                    echo "<input type='text' name='lastname' placeholder='Lastname'>";
                }
                
                ?>

                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <input class="submit" type="submit" value="Submit" id="submit"> 
            </form>
            
        </div>
    </body>
</html>
