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

        <div id="box" class="login">
           
            <form action="/login/redirect.php" method="post">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
            
                <p> <a href="mailto:yoeriv@nbruchem.nl"> Forgot Password? </a> </p>
                <input class="submit" type="submit" value="Submit" id="submit"> 
         
            </form>
        </div>

    </body>
</html>
