#Kmeans
#Opmerking: plekken waar  "NOT AUTO" staat, betekent dat hier nog handmatig aanpassingen moet worden gedaan als bijv
#centroids veranderd moeten worden.
#Covariance 

#!!!!!!!!!!!!!!!!! Kmeans centroid bepaling werkt nog niet optimaal (na eerste iteratie)

vectorCentroid1<- NULL
vectorCentroid2 <- NULL

#testdataframe of user ratings; 1 & 0 -> easier to check if algorithm works.
users<-  c(1,2,3,4,5,6,7,8,9,10) 
movie1<- c(3,4.7,0.8,0,1,1,5,3.8,5,4.7)
movie2<-c(1,3.7,1,3.9,3.1,2.1,4,3,5,2.5) 
movie3<- c(2.8,5,3.9,1.2,4.9,2,1.7,2.5,5,3.5) 
movie4<- c(4,1.5,2.9,4.1,0.5,1.6,4.1,2,5,1.9) 
movie5<- c(5,2.7,3.9,4,5,0.4,5,4.7,5,4.1)
movie6 <- c(4,2.3,3.6,4.8,2,4.8,3.1,4.2,5,1)
movie7 <- c(3.1,2.9,4.5,3.7,5,3.9,0,1.6,5,2.6)



test.dataframe <- data.frame(users,movie1,movie2,movie3,movie4,movie5,movie6,movie7) #NOT AUTO

#0. Needed functions
EuclideanDist <- function(x,y){ # x & y are vector that contain the user rows
  range <- 1:(length(x)-1)#user column not included
  
  first<- as.vector(x, mode="numeric")
  second<- as.vector(y, mode= "numeric")
  
  Dist = 0
  
  for (i in range){
    Dist <- (first[range+1] - second[range+1])^2 #first location is user column
  }
  
  Dist = sqrt(sum(Dist))
  
  return(Dist)
}

newCentroid <- function(x){# x is a vector with number that indicate the user ID's. New centroid is calculated
  rangeID <- 1:length(x)
  centroid <- as.numeric(vector(length = length(test.dataframe)))
  
  for ( i in rangeID){
    centroid <- test.dataframe[x[i],] + centroid
  }
  centroid <- centroid / length(x)
  
  return(centroid)
}

#1. pick k random users as representatives (centroids) !!!!!!!!!!!!!!!!!! Fill it by hand, only part thats not automatic
#Number of centroids # NOT AUTO
k<-2

RandomUsers <-sample(nrow(test.dataframe), k, replace = F) #NOT AUTO
centroid1 <- RandomUsers[1]
centroid2 <- RandomUsers[2]

#2. inspect the euclidean distance between datapoints and centroids

#Make a distance matrix NOT AUTO
lengthCol <- nrow(test.dataframe) -k #minus column users, minus datapoints that are centroids
matrixDistance <- matrix(byrow = T, nrow =2, ncol = lengthCol)
rownames(matrixDistance) <- c(centroid1, centroid2 )
Datapoints <- 1:(nrow(test.dataframe))

#deletes centroids from datapoints ## NOT AUTO
Datapoints <- Datapoints[!Datapoints %in% c(centroid1, centroid2)]

colnames(matrixDistance)<- Datapoints

#Calculate and enter distances
rangeRow <- 1:nrow(matrixDistance)
rangeCol <- 1:ncol(matrixDistance)


for (i in rangeRow){
  for (j in rangeCol){
    matrixDistance[i,j] <- EuclideanDist(test.dataframe[as.integer(rownames(matrixDistance)[i]),],
                                         test.dataframe[as.integer(colnames(matrixDistance)[j]),])
  }
}


#3.form clusters; which datapoint is closer to which centroid?

#!!!!!!!!!!!!!!!!!!!!!!Find a way to empty a matrix instead of copying
matrixCluster <- matrix(nrow = nrow(matrixDistance),
                        ncol = ncol(matrixDistance))
rownames(matrixCluster)<- rownames(matrixDistance)
colnames(matrixCluster)<- colnames(matrixDistance)


#If a datapoint belongs to a cluster, its value is 1
for (i in rangeCol){
 for (j in rangeRow){
   if (j+1 <= length(rangeRow)){
    if (matrixDistance[j,i] > matrixDistance[j+1,i]){ #search which distance is the shortest 
      min <- j+1 
    } else {
      min <- j
    }
     
   }    
 }
  
  for ( l in rangeRow){ #fill in to which cluster the datapoint belongs to
    if (l == min){
      matrixCluster[l,i] <- 1
    } else {
      matrixCluster[l,i] <- 0
    }
    
  }
}


#new centroids: mean of of the datapoints
VectCentr1 <- as.integer(rownames(matrixCluster)[1])
for  (j in rangeCol){
  if (matrixCluster[1,j]==1){
    VectCentr1 <- c(VectCentr1, as.integer(colnames(matrixCluster)[j]))
  }
}

VectCentr2 <- as.integer(rownames(matrixCluster)[2])
for  (j in rangeCol){
  if (matrixCluster[2,j]==1){
    VectCentr2 <- c(VectCentr2, as.integer(colnames(matrixCluster)[j]))
  }
}

#NOT AUTO
newCentroid1 <- newCentroid(VectCentr1)
newCentroid2 <- newCentroid(VectCentr2)

#4. Make iterations -> choose in the cluster a new represenative!
  #need new function for the iterated centroids #!!!!!!!!!!!! Not auto
Iterations <- 0

while (Iterations < 5){ #Insert how many iterations
  #New centroids user ID's aren't going to be needed (non existent) #Not automatic!!!!!!!!!!!!!!!
  centroidData.f <- data.frame(rbind(newCentroid1, newCentroid2))
  
  #Make a new matrix with a new format   #!!!!!!NOT AUTOMATIC
  NewmatrixDistance <- matrix(nrow = k, ncol = nrow(test.dataframe) )
  rownames(NewmatrixDistance)<- c("centroid1", "centroid2") 
  colnames(NewmatrixDistance)<- 1:nrow(test.dataframe)
  
  #Calculate and enter distances
  rangeRow <- 1:nrow(NewmatrixDistance)
  rangeCol <- 1:ncol(NewmatrixDistance)
  
  
  for (i in rangeRow){
    for (j in rangeCol){
      NewmatrixDistance[i,j] <- EuclideanDist(centroidData.f[i, ],
                                           test.dataframe[as.integer(colnames(NewmatrixDistance)[j]),])
    }
  }
  
  #form clusters; which datapoint is closer to which centroid?
  
  #!!!!!!!!!!!!!!!!!!!!!!Find a way to empty a matrix instead of copying
  NewmatrixCluster <- matrix(nrow = nrow(NewmatrixDistance),
                          ncol = ncol(NewmatrixDistance))
  rownames(NewmatrixCluster)<- rownames(NewmatrixDistance)
  colnames(NewmatrixCluster)<- colnames(NewmatrixDistance)
  
  
  #If a datapoint belongs to a cluster, its value is 1 (make it AUTO!! == COMPLETE)
  for (i in rangeCol){
    for (j in rangeRow){
      if (j+1 <= length(rangeRow)){
        if (NewmatrixDistance[j,i] > NewmatrixDistance[j+1,i]){ #search which distance is the shortest 
          min <- j+1 
        } else {
          min <- j
        }
        
      }    
    }
    
    for ( l in rangeRow){ #fill in to which cluster the datapoint belongs to
      if (l == min){
        NewmatrixCluster[l,i] <- 1
      } else {
        NewmatrixCluster[l,i] <- 0
      }
      
    }
  }
  
  #new centroids: mean of of the datapoints
  VectCentr1 <- NULL
  VectCentr2 <- NULL
  
  for  (j in rangeCol){
    if (NewmatrixCluster[1,j]==1){
      VectCentr1 <- c(VectCentr1, as.integer(colnames(NewmatrixCluster)[j]))
    }
  }
  
  for  (j in rangeCol){
    if (NewmatrixCluster[2,j]==1){
      VectCentr2 <- c(VectCentr2, as.integer(colnames(NewmatrixCluster)[j]))
    }
  }
  
  newCentroid1 <- newCentroid(VectCentr1)
  newCentroid2 <- newCentroid(VectCentr2)
    
    vectorCentroid1 <- rbind(vectorCentroid1, newCentroid1)
    vectorCentroid2 <- rbind(vectorCentroid2, newCentroid2)

    Iterations = Iterations + 1
    }

NewmatrixCluster

