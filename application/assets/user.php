<?php
class user{

    public $user_id;
    public $user_name = "";
    public $user_username = "";

    public function __construct($username) {
        $this->user_username = $username;
        $this->getUserDetails();
    }

    protected function getMovieDetails(){
       
    }

    public function setMovieState(){
        
    }
}

?>