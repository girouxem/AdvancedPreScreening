r <- getOption("repos")
r["CRAN"] <- "http://cran.us.r-project.org"
options(repos = r)

if (!requireNamespace("BiocManager"))
  install.packages("BiocManager")
BiocManager::install()

library("BiocManager")
.cran_packages <- c("cowplot", "data.table", "ggplot2", "knitr", "reticulate", "rprojroot")
.bioc_packages <- c("ape", "BarcodingR", "BiocStyle", "biomartr", "Biostrings", "dada2",  
                    "GenomicFeatures","phyloseq", "ShortRead")
.inst <- .cran_packages %in% installed.packages()
if(any(!.inst)) {
  install.packages(.cran_packages[!.inst])
}
.inst <- .bioc_packages %in% installed.packages()
if(any(!.inst)) {
  BiocManager::install(.bioc_packages[!.inst], ask = FALSE)
  #BiocManager::install(.bioc_packages[!.inst], ask = FALSE, lib = "/cloud/lib/x86_64-pc-linux-gnu-library/4.2")
}

sapply(c(.cran_packages, .bioc_packages), require, character.only = TRUE)