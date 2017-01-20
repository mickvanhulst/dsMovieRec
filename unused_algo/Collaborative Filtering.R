#collab filtering user-based

#testdataframe
users<-  c(1,2,3,4,5,6) 
movie1<- c(1,0,0,1,1,1) 
movie2<-c(0,1,1,0,0,0) 
movie3<- c(0,0,1,1,0,1) 
movie4<- c(4,0,1,1,0,1) 
movie5<- c(0,0,1,1,1,0)
test.dataframe <- data.frame(users,movie1,movie2,movie3,movie4, movie5)

#functie om gelijkenis te bereken (cosine similarity)
getCosine <- function(x,y){
  this.cosine<-sum(x*y)/(sqrt(sum(x*x)) * sqrt(sum(y*y)))
  return(this.cosine)
}

#een dataframe maken waarbij de movies tegenoverelkaar staan; tot nu toe leeg
  #verwijder colom users
  test.dataframe.USx<- (test.dataframe[,!(names(test.dataframe) %in% c("users"))])

test.dataframe.similarity<- matrix(NA, nrow=ncol(test.dataframe.USx),
                                   ncol = ncol(test.dataframe.USx),
                                   dimnames = list(colnames(test.dataframe.USx),
                                   colnames(test.dataframe.USx)))

#lege plekken in test.dataframe.similarity worden gevuld door cosine functie;
# van matrix naar dataframe om sneldheid te behouden
for(i in 1:ncol(test.dataframe.USx)){
  for (j in 1:ncol(test.dataframe.USx)){
    test.dataframe.similarity[i,j]<- getCosine(as.matrix(test.dataframe.USx[i]),
                                               as.matrix(test.dataframe.USx[j]))
  }
}

#terug naar dataframe
test.dataframe.similarity<- as.data.frame(test.dataframe.similarity)

#maak het functie waar je een score kan bepalen die afhankelijk is van verleden en
#gelijkenis in artikelen

getScore <- function(history,similarities){
  x<- sum(history*similarities)/sum(similarities)
  return(x)
}


#maak een placeholder matrix waar je uiteindelijk de voorstellen gaat weergeven
#users tov movies
holder <- matrix(NA, nrow = nrow(test.dataframe), ncol = ncol(test.dataframe)-1,
                 dimnames = list((test.dataframe$users), colnames(test.dataframe[-1])))

#loop door de gebruikers
for(i in 1:nrow(holder)){
  #loop door films
  for (j in 1:ncol(holder))
  {
    #onthoud de user en movie naam
    user<- rownames(holder)[i]
    product<- colnames(holder)[j]
    
    #voorkomen om film aan te raden die al geratet is(dit geval wordt opgeslagen als empty)
    if(as.integer(test.dataframe[test.dataframe$users==user,product]) ==1){
      holder[i,j]<-""
    } else{
      #top tien in similarity
      topN<- ((head(n=11,(test.dataframe.similarity[order(test.dataframe.similarity[,product]
                                                          ,decreasing = TRUE),][product]))))
      topN.names <- as.character(rownames(topN))
      topN.similarities <- as.numeric(topN[,1])
      
      #eerste film droppen; altijd hetzelfde
      topN.similarities<- topN.similarities[-1]
      topN.names<-topN.names[-1]
      
      #!!!!!!!!!!!!! purchase history?
      topN.purchases <-test.dataframe[,c("users",topN.names)]
      topN.Userpurchases <- topN.purchases[topN.purchases$user==user,]
      topN.Userpurchases <- as.numeric(topN.Userpurchases[!(names(topN.Userpurchases)
                                                            %in% c("users"))])
      
      #bereken de score tussen product en user
      holder[i,j] <-getScore(similarities = topN.similarities,
                             history = topN.Userpurchases)
    }
  }
}

test.dataframe.scores <-holder
test.dataframe.scores

#recommends mooier maken
test.dataframe.scores.Fini <- matrix(NA, nrow=nrow(test.dataframe.scores), ncol=3,
                                     dimnames= list(rownames(test.dataframe.scores)))
for (i in 1:nrow(test.dataframe.scores)){
  test.dataframe.scores.Fini[i,]<-names(head(n=3,
                                             (test.dataframe.scores[,order(test.dataframe.scores[i,],
                                                                           decreasing = TRUE)])[i,]))
}

test.dataframe.scores.Fini
