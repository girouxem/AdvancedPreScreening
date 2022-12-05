ColourPalleteMulti <- function(df, group, subgroup){
  # Find how many colour categories to create and the number of colours in each
  categories <- aggregate(as.formula(paste(subgroup, group, sep="~" )), df, function(x) length(unique(x)))
  category.start <- (scales::hue_pal(l = 100)(nrow(categories))) # Set the top of the colour pallete
  category.end  <- (scales::hue_pal(l = 40)(nrow(categories))) # set the bottom
  # Build Colour pallette
  colours <- unlist(lapply(1:nrow(categories),
                           function(i){
                             colorRampPalette(colors = c(category.start[i], category.end[i]))(categories[i,2])}))
  return(colours)
}

# https://stackoverflow.com/questions/49818271/stacked-barplot-with-colour-gradients-for-each-bar?rq=1