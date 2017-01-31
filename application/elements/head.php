<?php

function writeHead($pageTitle){
    
    // Write page title.
    echo "<title>Recommendations | ". $pageTitle ."</title>";
    
    // Get CSS.
    echo "<link href='/css/style.css' rel='stylesheet' type='text/css' media='all'/>";

    // Get fonts
    echo "<link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>";

    // Get Javascript
    echo "<script src='/js/jquery.min.js'></script>";
    //echo "<script src='/js/slider.js'></script>";

    // Set Meta Data
    echo "<meta name='viewport' content='width=device-width, initial-scale=1'>";
    echo "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>";

    // Aditional Scripts
    echo "<script type='application/x-javascript'> addEventListener('load', function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>";


}

?>