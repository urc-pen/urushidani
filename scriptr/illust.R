X <- as.matrix(read.csv("mutationplot_cycle1.csv", header=TRUE,row.names=1))

tmp <- colnames(X)
tmp2 <- rownames(X)

tmp <- names(rev(sort(apply(X,1,var))))[1:1000]
X<-X[tmp,]
rcol <- c()
dr <- c()

for (i in 1:length(tmp)) {
  a <- substring(tmp[i], 1, 1)
  if (a == "D"){
    dr <- append(dr, tmp[i])
  }
}

for (i in 1:length(tmp)) {
  a <- substring(tmp[i], 1, 1)
  if (a == "D"){
    rcol[tmp[i]] <- "blue"
  }
  if (a == "N"){
    rcol[tmp[i]] <- "LightGrey"
  }
}

heatmap(X,col=c("LightGrey", "red"), hclustfun = function(X) { hclust(X, method = "ward.D") }, scale = c("none"), RowSideColors=rcol)
