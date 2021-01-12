Plan for ACA project
====================

- Focus on one use-case 
    - one class classification 
    - RBF kernel 

- Prune not necessary code from libsvm (?) 

- Dataset test cases, which take more advantages from parallelization?
    - Columns >> rows
    - Rows >> columns
    - Columns ~= Rows 

Profiling
---------

- Use gprof (some other tool?) to analize:
    - call graph
        - find some graphic to visualize it 
    - most time consuming functions

- Insert hook for time measuring
    - around time consuming functions
    - inside most TC part of these functions

- Call graph: at which level the parallelization is applicable?

- Dependencies analisys 

- Figure out which are parallelizable 

Hypothesis
----------

- Given a parallelizable candidate:
    - Estimate improvement based on threads # and cache size 
    - Is it worth it?



 


