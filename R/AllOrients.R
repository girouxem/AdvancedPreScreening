# Create the custom `AllOrients' function for primer sequences for all possible orientations created by Benjamin Callahan. See: https://benjjneb.github.io/dada2/ITS_workflow.html      
library("Biostrings")
AllOrients   <- function(primer) {
     require(Biostrings)
     dna     <- Biostrings::DNAString(primer)
     orients <- c(Forward    = dna, 
                  Complement = Biostrings::complement(dna), 
                  Reverse    = Biostrings::reverse(dna), 
                  RevComp    = Biostrings::reverseComplement(dna))
    return(sapply(orients, toString))
}
