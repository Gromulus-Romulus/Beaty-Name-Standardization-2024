## Audra Cornick - 19 Oct 2024
## Splitting names

# GOAL: Split up names into proper Specify format (first, middle initial, last).
## Errors: Can't recognize last names that have 2 names so it converts the first last name
## into a middle name.
## It also can't recognize organizations and splits them.

library(dplyr)
library(readxl)

agents_df <- read_excel("Agents_10_6_24.xlsx") #Renamed the Agents Download Dataset

# Splits names and leave properly formatted name alone, can't distinguish initials
validate_and_correct_names <- function(first, middle, last) {
  # checks if there is no first name and if the last name has more than one string in it (i.e other names)
  if ((is.na(first) || trimws(first) == "") && length(unlist(strsplit(last, " "))) > 1) {
    full_name <- unlist(strsplit(last, " "))
    #checks if there is only a first and last name or middle name as well
    if (length(full_name) == 2) {
      return(c(First = full_name[1], Middle = NA, Last = full_name[2]))  # First, Middle (NA), Last
    } else if (length(full_name) >= 3) {
      return(c(First = full_name[1], Middle = paste(full_name[2:(length(full_name) - 1)], collapse = " "), Last = full_name[length(full_name)]))  # First, Middle, Last
    }
  }
  
  if (is.na(last) || trimws(last) == "") {
    return(c(First = first, Middle = middle, Last = NA))  # If last name is empty
  }
  
  if (is.na(middle) || trimws(middle) == "") {
    return(c(First = first, Middle = NA, Last = last))  # If middle name is empty
  }
  
  return(c(First = first, Middle = middle, Last = last))  # Return as is
}

# creates a matrix using the function to split all the names then adds it as new columns to our data frame
name_parts <- t(mapply(validate_and_correct_names, agents_df$`First Name`, agents_df$`Middle Initial`, agents_df$`Last Name`))
agents_df <- cbind(agents_df, as.data.frame(name_parts, stringAsFactors = FALSE))

# splits the initials that weren't distinguished in the previous function
split_initials <- function(first, middle) {
  # Return original values if middle is not NA
  if (!is.na(middle)) {
    return(c(First_split = first, Middle_split = middle))
  }
  
  # Check if 'first' is not NA and contains initials
  if (!is.na(first) && grepl("\\.", first)) {
    # Split the first string into parts by the dot
    parts <- unlist(strsplit(first, "\\."))
    
    # Check if there is only one initial (two parts) and middle is NA
    if (length(parts) == 1) {
      return(c(First_split = first, Middle_split = middle))  # Return original values
    }
    
    # Check if there are multiple initials (more than 2 parts)
    if (length(parts) > 1) {
      first <- trimws(parts[1])  # First initial
      middle <- trimws(paste(parts[-1], collapse = " "))  # Middle initials
      first <- paste0(first, ".")
      middle <- paste0(middle, ".")
    }
  }
  
  return(c(First_split = first, Middle_split = middle))
}

# creates a matrix of all of the names after having initals split and then converts adds it to our dataset
split_names <- t(mapply(split_initials, agents_df$First, agents_df$Middle))
agents_df <- cbind(agents_df, as.data.frame(split_names, stringAsFactors = FALSE))

# creates a new dataset containing only the agent guid and the validated and split first, middle, and last names.
final_split_names <- agents_df %>%
   select(`Agent - GUID`, First_split, Middle_split, Last) %>%
   rename(First = First_split, Middle = Middle_split)

