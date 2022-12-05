#Create the custom `PrimerHits' function for checking our sequences for all orientations of primer sequences 
# as generated above using the AllOrients function. This function generates a table of counts of the number 
# of reads in which the primer is found. This function was created by Benjamin Callahan for the 
# ITS-specific workflow. See: https://benjjneb.github.io/dada2/ITS_workflow.html
library("ShortRead")
PrimerHits <- function(primer, fn) {
    nhits  <- Biostrings::vcountPattern(primer, ShortRead::sread(readFastq(fn)),
                                        fixed = FALSE)
    return(sum(nhits > 0))
}
