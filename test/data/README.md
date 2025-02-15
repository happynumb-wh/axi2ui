
Change .txt to .simple : type in the following command line
find -name "*.txt" | xargs -I '{}' sh -c "cut -d ',' -f3,4 {} | sed 's/, / /g' > {}.simple"
