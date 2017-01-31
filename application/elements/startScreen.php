<html>
    <head>
        <?php
        include_once("elements/head.php");
        writeHead("Welcome");
        echo "<link href='css/startScreen.css' rel='stylesheet' type='text/css' media='all'/>";
        ?>
    </head>
    <body>
        <div id="start_screen">
            <div class="title">
                <h1> Recommendations. </h1>
            </div>
            <div class="sub_title"> 
                <h2> What do you like? </h2>
            </div>
            <div id="loginWindow">
                <a href="./login">
                    <div class="login">
                        <h1> Login </h1>
                    </div> 
                </a>
                <a href="./register">
                    <div class="register">
                        <h1> Register </h1>
                    </div>
                </a>
            </div>
        </div>
    </body>  
</html>
