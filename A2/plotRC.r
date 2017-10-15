zipf <- read.csv('./sorted-1-2-gram.csv', head=TRUE, sep=',')
plot(zipf$Rank, sort(zipf$C), xlab='Rank', pch='.', ylab='C', main=' Rank and C')