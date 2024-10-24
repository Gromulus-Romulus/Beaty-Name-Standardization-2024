# Goal: Compare 2 names, even if they are different variations of the same name, and 
# return True if they are the same name and false if they are different. 
# @author: Audra

library(stringr)
library(stringdist)
library(readxl)
library(tidyverse)

# Splits the names into their individual parts and removes all punctuation and spaces
tokenize_name <- function(name){
  clean_name <- str_to_lower(str_trim(name))
  
  tokens <- str_split(clean_name, "[\\s.]+", simplify = TRUE)
  tokens <- tokens[!tokens %in% c("and", "or", "is")]
  tokens <- tokens[tokens != '']
  return(as.list(tokens))
}

# Standardizes the tokens to make them easier to compare
standardize_tokens <- function(tokens){
  standardized_tokens <- sort(unique(tokens))
  return(standardized_tokens)
}

# Compares two names using string distance to allow variance between the exact strings
compare_names <- function(name1, name2, threshold = 0.7){
  tokens1 <- tokenize_name(name1)
  tokens2 <- tokenize_name(name2)
  
  stand_tokens1 <- standardize_tokens(tokens1[[1]])
  stand_tokens2 <- standardize_tokens(tokens2[[1]])
  
  #Jaro-Winkler Method (not as widely applicable)
  #distance <- stringdist(stand_tokens1, stand_tokens2, method = 'jw')
  
  #Levenshtein distance
  distance <- adist(stand_tokens1, stand_tokens2, partial = TRUE)
  
  #For JW
  #similarity_score <- 1 - distance
  
  # For Levenshtien
  similarity_score <- 1 - (distance / max(nchar(stand_tokens1), nchar(stand_tokens2)))
  
  if(similarity_score >= threshold){
    return(TRUE)
  } else {
    return(FALSE)
  }
}

# Combining all of the name parts to create one name to compare to the standardized name 
# and creating a new column of whether the given name matches the standardized name. 
# Basically demonstrates that the compare_names function can accurately compare 2 names even with
# variations in the inputs in a lot of the cases given. (Exceptions being misspellings or nicknames.)

Names_to_Standardise <- read_excel("Names/Names to Standardise.xlsx", skip = 1)
Names_to_Standardise <- Names_to_Standardise[, -c(7,8,9)]

standardized_names <- unique(Names_to_Standardise$`Standardized Name`)

Names_to_Standardise <- Names_to_Standardise %>%
  unite(col = "full_name", First.Name...2, Middle.Initial...3, Last.Name...4, na.rm = TRUE, remove = FALSE, sep = " " )

Names_to_Standardise$same_name <- mapply(compare_names, Names_to_Standardise$full_name, Names_to_Standardise$`Standardized Name`)

# Could be a useful function when looking at the entirety of the name data.
# We could potentially create a list of all standardized names and try to us it to match them
# (though that would likely be very long and complex computing so there is probably a simpler way to do it.)



