zipf <- read.csv('./sorted-1-2-gram.org.csv', head=TRUE, sep=',')
plot(zipf$Freq, zipf$Rank, log='xy', xlab='Rank', ylab='Freq', main='Zipfs curve for wiki-small corpus')
