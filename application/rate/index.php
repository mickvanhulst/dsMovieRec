<?php
if(!isset($_SESSION)) { session_start(); }
echo "<html>";
    echo "<head>";
        include("../elements/head.php"); writeHead("Give your movie preferences");
        echo "<link href='../../css/forms.css' rel='stylesheet' type='text/css' media='all'/>";
    echo "</head>";
    echo "<body>";
        include("../elements/page_elements.php");
        echo "<div class='full'>";
            include_once("../elements/side_menu.php");
            echo "<div class='main'>";
                //echo "<div class='video-content'>";
                    echo "<div class='right-content'>";
                    
                        if(isset($_SESSION['userID'])){                                    
                            include_once("../functions/slider.php");
                        }else{
                            print("niet ingelogd");
                        }
                    echo "</div>";
                    
                echo "</div>";
                //include_once("elements/footer.php");

            //echo "</div>";
            echo "<div class='clearfix'></div>";
        echo "</div>";
    echo "</body>";   
echo "</html>";
?>