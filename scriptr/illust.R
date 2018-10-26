X <- as.matrix(read.csv("mutationplot.csv", header=TRUE,row.names=1))

tmp <- colnames(X)
tmp2 <- rownames(X)

tmp <- names(rev(sort(apply(X,1,var))))[1:2000]
X<-X[tmp,]
dr <- c()
nu <- c()
for (i in 1:length(tmp)) {
  a <- substring(tmp[i], 1, 1)
  if (a == "D"){
    dr <- c(dr, tmp[i])
  }
  if (a == "N"){
    nu <- c(nu, tmp[i])
  }
}
rcol <- c()
rcol[nu] <- "LightGrey"
rcol[dr] <- "blue"
length(rcol)
custumcol <- colorRampPalette(c("LightGrey", "red"))
heatmap(X,col=c("LightGrey", "red"), hclustfun = function(X) { hclust(X, method = "ward.D") }, scale = c("none"), RowSideColors=rcol)

