heap <- read.csv('./vocabWordCount.csv', head=TRUE, sep=',')
plot(heap$WordCount, heap$Vocab, log='y', type='l', xlab='Words in Collection (wiki-small)', ylab='Words in Vocabulary', main='Vocabulary growth and Heap\'s est. curve (dash)\nwith parameters k = 0.90 and beta = 0.009')

par(new=TRUE)

k <- 90
beta <- 0.009

est <- k * (heap$WordCount^beta)
plot(heap$WordCount, est,  type='l', lty=2, xlab='', ylab='', main='', xaxt='n', yaxt='n')