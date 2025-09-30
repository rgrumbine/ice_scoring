# ice_scoring
Tools for model evaluation, primarily of sea ice models.

Now includes submodules
* SIDFEx https://github.com/helgegoessling/SIDFEx
* SITools https://github.com/XiaLinUCL/Sea-Ice-Evaluation-Tool
* DIAG_SUITE https://github.com/NeilBarton-NOAA/DIAG_SUITE

as well as the local
* gross_checks   -- check for structural problems (grid seams) or 
                         impossible values ( T < -3)
* NCEP_si_verf   -- NCEP tools for model evaluation

Additional support:
* model_definitions -- translate between models' own names and names used 
                         in verification codes, e.g. nx vs. ni vs. nlon, 
                         and so forth 
* mmablib           -- Library of general support code (Fortran, C, C++, Python)


* exec    -- executables (not on git)
* fix     -- fixed files of use at least in NCEP verification (not on git) 
* *  WCOSS: /u/Robert.Grumbine/rgdev/fix
* *  Ursa: /home/Robert.Grumbine/rgdev/fix
* *  Gaea: /home/Robert.Grumbine/rg/fix


Robert Grumbine
3 March 2025
