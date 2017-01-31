<?php
class movie{

    public $movie_id;
    public $movie_image = "";
    public $movie_name = "";
    public $movie_liked = "FALSE";

    public function __construct($id) {
        $this->movie_id = $id;
        $this->getMovieDetails();
    }

    protected function getMovieDetails(){
        $omdb_url = "http://www.omdbapi.com/?i=".$this->movie_id."&r=json";
        $omdb_str = file_get_contents($omdb_url);
        $movieDetails = json_decode($omdb_str, true);
        $this->movie_name = $movieDetails['Title'];
        
        $movie_image_URL = ("./images/scraped/" . $this->movie_id . ".jpg");

        if (file_exists($movie_image_URL)){
            $this->movie_image = $movie_image_URL;
        }else{
            $this->movie_image = "./img/noimagefound.jpg";
        }
    }

    public function setMovieState(){
        
    }
}

?>